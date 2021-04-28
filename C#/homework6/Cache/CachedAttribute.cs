using EventApi.Services;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Filters;
using Microsoft.Extensions.DependencyInjection;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace EventApi.Cache
{
    [AttributeUsage(AttributeTargets.Class | AttributeTargets.Method)]
    public class CachedAttribute: Attribute, IAsyncActionFilter
    {
        private readonly int _timeToLiveSeconds;

        public CachedAttribute(int time)
        {
            _timeToLiveSeconds = time;
        }
        public async Task OnActionExecutionAsync(ActionExecutingContext context, ActionExecutionDelegate next)
        {
            var cacheSettins = context.HttpContext.RequestServices.GetRequiredService<RedisCacheSettings>();
            if (!cacheSettins.Enabled)
            {
                await next();
                return;
            }
               
            var cacheService = context.HttpContext.RequestServices.GetRequiredService<IResponseCacheService>();

            var cacheKey = GenerateCacheKeyFromRequest(context.HttpContext.Request);
            var cachedResponse = await cacheService.GetCachedResponseAsync(cacheKey);

            if (!string.IsNullOrEmpty(cachedResponse))
            {
                Console.WriteLine("Using cache");
                var contentResult = new ContentResult
                {
                    Content = cachedResponse,
                    ContentType = "application/json",
                    StatusCode = 200
                };
                context.Result = contentResult;
                return;
            }

            var executedContext = await next();

            if (executedContext.Result is OkObjectResult ok)
            {
                Console.WriteLine("Using database");
                await cacheService.CacheResponseAsync(cacheKey, ok.Value, TimeSpan.FromSeconds(_timeToLiveSeconds));
            }
        }
        private static string GenerateCacheKeyFromRequest(HttpRequest request)
        {
            var KeyBuilder = new StringBuilder();
            KeyBuilder.Append($"{request.Path}");
            foreach (var (key, value) in request.Query.OrderBy(x=> x.Key))
            {
                KeyBuilder.Append($"|{key}-{value}");
            }
            return KeyBuilder.ToString();
        }
    }
}
