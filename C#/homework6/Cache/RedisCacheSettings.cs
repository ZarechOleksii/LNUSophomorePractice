using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace EventApi.Cache
{
    public class RedisCacheSettings
    {
        public bool Enabled { get; set; }
        public string ConnectionString { get; set; }
    }
}
