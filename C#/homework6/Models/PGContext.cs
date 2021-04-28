using Microsoft.EntityFrameworkCore;
using Npgsql;
using System;


namespace EventApi
{
    public class PGContext : DbContext
    {
        public PGContext() { }
        public PGContext(DbContextOptions<PGContext> options) : base(options) { }
        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            optionsBuilder.UseNpgsql(Environment.GetEnvironmentVariable("ConString"));
            NpgsqlConnection.GlobalTypeMapper.MapEnum<RestaurantNames>("RestaurantNames");
            NpgsqlConnection.GlobalTypeMapper.MapEnum<Roles>("Roles");
            NpgsqlConnection.GlobalTypeMapper.MapComposite<Event>("Events");
            NpgsqlConnection.GlobalTypeMapper.MapComposite<Order>("Orders");
            NpgsqlConnection.GlobalTypeMapper.MapComposite<Person>("Person");
        }

        public DbSet<Event> Events { get; set; }
        public DbSet<Person> Person { get; set; }
        public DbSet<Order> Orders { get; set; }
    }
}
