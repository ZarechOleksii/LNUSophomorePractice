using NpgsqlTypes;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace EventApi
{
    public enum Roles
    {
        [PgName("User")]
        User,
        [PgName("Admin")]
        Admin
    }
}
