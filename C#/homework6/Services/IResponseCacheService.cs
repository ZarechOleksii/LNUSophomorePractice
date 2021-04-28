using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace EventApi.Services
{
    interface IResponseCacheService
    {
        Task CacheResponseAsync(string cacheKey, object response, TimeSpan time);
        Task<string> GetCachedResponseAsync(string cacheKey);
    }
}
