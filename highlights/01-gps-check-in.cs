// Excerpt from src/Sellora.OrderService.Domain/Orders/GeoDistance.cs
// Repository: Team-Sellora/sellora-order (dev branch). Shared for illustration only.

namespace Sellora.OrderService.Domain.Orders;

/// <summary>
/// Great-circle distance with the Haversine formula. Accurate to well under
/// a metre at the 300 m scale this is used for; PostGIS is not needed.
/// </summary>
public static class GeoDistance
{
    /// <summary>IUGG mean Earth radius in metres.</summary>
    public const double EarthRadiusMeters = 6_371_008.8;

    /// <summary>
    /// Distance in metres, rounded to the nearest centimetre. Rounding makes
    /// the radius comparison deterministic: a point constructed exactly
    /// 300 m away measures 300.00, not 300.0000000001.
    /// </summary>
    public static double Meters(GeoPoint from, GeoPoint to)
    {
        var phi1 = ToRadians(from.Latitude);
        var phi2 = ToRadians(to.Latitude);
        var deltaPhi = ToRadians(to.Latitude - from.Latitude);
        var deltaLambda = ToRadians(to.Longitude - from.Longitude);

        var a = Math.Sin(deltaPhi / 2) * Math.Sin(deltaPhi / 2) +
                Math.Cos(phi1) * Math.Cos(phi2) *
                Math.Sin(deltaLambda / 2) * Math.Sin(deltaLambda / 2);

        var c = 2 * Math.Atan2(Math.Sqrt(a), Math.Sqrt(1 - a));

        return Math.Round(EarthRadiusMeters * c, 2, MidpointRounding.AwayFromZero);
    }

    private static double ToRadians(double degrees) => degrees * Math.PI / 180;
}


// ---- src/Sellora.OrderService.Domain/Orders/CheckInPolicy.cs ----

/// <summary>
/// Tunable limits for the GPS gate, read from configuration so the radius
/// can change without a redeploy.
/// </summary>
/// <param name="RadiusMeters">Accepted when the distance is ≤ this (the exact radius is inside).</param>
/// <param name="Validity">How long an accepted check-in permits payment.</param>
/// <param name="MaxClockSkew">How far in the future a device timestamp may be.</param>
/// <param name="MaxCaptureAge">How old a GPS fix may be, so an old fix cannot be replayed.</param>
public sealed record CheckInPolicy(
    double RadiusMeters,
    TimeSpan Validity,
    TimeSpan MaxClockSkew,
    TimeSpan MaxCaptureAge)
{
    public static CheckInPolicy Default { get; } = new(
        300,
        TimeSpan.FromMinutes(10),
        TimeSpan.FromMinutes(2),
        TimeSpan.FromMinutes(5));
}

