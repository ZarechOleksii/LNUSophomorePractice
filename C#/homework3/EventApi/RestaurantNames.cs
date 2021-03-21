using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using NpgsqlTypes;

namespace EventApi
{
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