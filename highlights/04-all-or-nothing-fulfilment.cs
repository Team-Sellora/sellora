// Excerpt from src/Sellora.InventoryService.Application/Stock/FulfilmentResolver.cs
// Repository: Team-Sellora/sellora-inventory (dev branch). Shared for illustration only.

// Input validation omitted. The decision itself: try the agency first, then the whole order from the company.

var agencyOwnerId = await _ownerLookup.FindAgencyOwnerAsync(
    request.AgencyId,
    cancellationToken);

if (agencyOwnerId is null)
{
    return Reject(
        ReservationOutcome.InventoryOwnerNotFound,
        "The agency inventory owner was not found.");
}

var orderReference = request.OrderReference.Trim();

var agencyResult = await _reservationService.ReserveAsync(
    new ReserveStockRequest(
        orderReference,
        agencyOwnerId.Value,
        lines),
    cancellationToken);

// Only a stock shortage permits fallback to company stock.
if (agencyResult.Outcome != ReservationOutcome.InsufficientStock)
{
    return Finish(agencyResult);
}

_decisionLogger.LogDecision(
    orderReference,
    request.AgencyId,
    agencyOwnerId.Value,
    "CompanyFallback",
    "Agency stock cannot fulfil the entire order; trying the complete " +
    "basket against company stock."
);

var companyOwnerId = await _ownerLookup.FindCompanyOwnerAsync(
    cancellationToken);

if (companyOwnerId is null)
{
    return Reject(
        ReservationOutcome.InventoryOwnerNotFound,
        "The company inventory owner was not found.");
}

// Reserve the same complete basket against the company.
var companyResult = await _reservationService.ReserveAsync(
    new ReserveStockRequest(
        orderReference,
        companyOwnerId.Value,
        lines),
    cancellationToken);

if (companyResult.Outcome == ReservationOutcome.InsufficientStock)
{
    return Reject(
        ReservationOutcome.InsufficientStock,
        "Neither the agency nor the company can fulfil the entire " +
        "order. Reported shortages are for company stock.",
        companyResult.Shortages);
}


return Finish(companyResult);
