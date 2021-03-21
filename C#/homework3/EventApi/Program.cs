using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace EventApi
{
    public class Program
    {
        public static void Main(string[] args)
        {
            string filePath = System.IO.Directory.GetCurrentDirectory() + "\\access.env";
            string[] text = System.IO.File.ReadAllLines(filePath);
            foreach (string x in text)
            {
                var parts = x.Split('=', StringSplitOptions.RemoveEmptyEntries);
                Environment.SetEnvironmentVariable(parts[0], parts[1]);
                
            }
            string conString = "";
            string[] conStr = { "Host", "Username", "Password", "Database" };
            foreach (string x in conStr)
                conString += x + " = " + Environment.GetEnvironmentVariable(x) + ";";
            Environment.SetEnvironmentVariable("ConString", conString);
            CreateHostBuilder(args).Build().Run();
        }

        public static IHostBuilder CreateHostBuilder(string[] args) =>
            Host.CreateDefaultBuilder(args)
                .ConfigureWebHostDefaults(webBuilder =>
                {
                    webBuilder.UseStartup<Startup>();
                });
    }
}
