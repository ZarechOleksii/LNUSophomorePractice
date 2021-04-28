using Microsoft.Extensions.Caching.Distributed;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace EventApi.Services
{
    public class ResponseCacheService : IResponseCacheService
    {
        private readonly IDistributedCache distributedCache;
        public ResponseCacheService(IDistributedCache distributed)
        {
            distributedCache = distributed;
        }
        public async Task CacheResponseAsync(string cacheKey, object response, TimeSpan time)
        {
            if (response == null)
            {
                return;
            }
            var serialize = JsonConvert.SerializeObject(response);
            await distributedCache.SetStringAsync(cacheKey, serialize, new DistributedCacheEntryOptions { AbsoluteExpirationRelativeToNow = time });
        }
        public async Task<string> GetCachedResponseAsync(string cacheKey)
        {
            var cachedResponse = await distributedCache.GetStringAsync(cacheKey);
            if (string.IsNullOrEmpty(cachedResponse))
                return null;
            else
                return cachedResponse;
        }
    }
}
