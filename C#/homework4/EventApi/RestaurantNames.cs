using NpgsqlTypes;

namespace EventApi
{
    /// <summary>
    /// Restaurant name where event is
    /// </summary>
    /// <example>0</example>
    public enum RestaurantNames
    {
        [PgName("Delice")]
        Delice,
        [PgName("EuroHotel")]
        EuroHotel,
        [PgName("Morio")]
        Morio
    }
}