// Excerpt from src/Sellora.OrderService.Infrastructure/Outbox/OutboxRelayService.cs
// Repository: Team-Sellora/sellora-order (dev branch). Shared for illustration only.
// Shows how a committed event is picked and leased so that events of one order are
// always published in the order they were written, even with several relay instances.

/// <summary>
/// Publishes committed outbox rows to Kafka. The lease-and-publish logic is
/// sellora-organization's, unchanged. One addition: a row is only picked
/// when no earlier event for the same order (same message key) is still
/// unpublished. Without it, a failed OrderConfirmed could be overtaken by
/// its PaymentRecorded — or a second relay instance could publish them out
/// of order. With it, per-order ordering holds across retries and instances.
/// </summary>
public sealed class OutboxRelayService(
    IServiceScopeFactory scopeFactory,
    IEventPublisher publisher,
    IOptions<OutboxRelayOptions> options,
    ILogger<OutboxRelayService> logger) : BackgroundService
{
    private readonly OutboxRelayOptions _options = options.Value;

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            try
            {
                await ProcessPendingMessagesAsync(stoppingToken);
            }
            catch (Exception exception) when (exception is not OperationCanceledException)
            {
                logger.LogError(exception, "Outbox relay polling failed.");
            }

            await Task.Delay(TimeSpan.FromSeconds(_options.PollingIntervalSeconds), stoppingToken);
        }
    }

    /// <returns>How many events were published.</returns>
    public async Task<int> ProcessPendingMessagesAsync(CancellationToken cancellationToken = default)
    {
        var total = 0;

        for (var round = 0; round < _options.MaxRoundsPerPoll; round++)
        {
            var published = await RelayRoundAsync(cancellationToken);
            total += published;

            if (published == 0)
            {
                break;
            }
        }

        return total;
    }

    private async Task<int> RelayRoundAsync(CancellationToken cancellationToken)
    {
        var now = DateTimeOffset.UtcNow;
        var leaseId = Guid.NewGuid();
        var leaseExpiresAt = now.AddSeconds(_options.LeaseSeconds);

        await using var scope = scopeFactory.CreateAsyncScope();
        var db = scope.ServiceProvider.GetRequiredService<OrderDbContext>();

        // Ignore tenant filters: this system process relays every tenant.
        var outbox = db.OutboxMessages.IgnoreQueryFilters();

        var candidateIds = await outbox
            .Where(message =>
                message.PublishedAt == null &&
                message.NextAttemptAt <= now &&
                (message.LeaseExpiresAt == null || message.LeaseExpiresAt < now) &&
                !outbox.Any(earlier =>
                    earlier.MessageKey == message.MessageKey &&
                    earlier.PublishedAt == null &&
                    earlier.Sequence < message.Sequence))
            .OrderBy(message => message.Sequence)
            .Select(message => message.OutboxId)
            .Take(_options.BatchSize)
            .ToListAsync(cancellationToken);

        foreach (var outboxId in candidateIds)
        {
            // Conditional update means only one relay instance can lease a row.
            await outbox
                .Where(message =>
                    message.OutboxId == outboxId &&
                    message.PublishedAt == null &&
                    (message.LeaseExpiresAt == null || message.LeaseExpiresAt < now))
                .ExecuteUpdateAsync(
                    setters => setters
                        .SetProperty(message => message.LeaseId, leaseId)
                        .SetProperty(message => message.LeaseExpiresAt, leaseExpiresAt),
                    cancellationToken);
        }

        // ... publish each leased message in sequence, then mark it published
        //     or record the error and schedule a retry.
    }
}
