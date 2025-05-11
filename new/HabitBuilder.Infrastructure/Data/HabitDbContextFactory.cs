using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Design;
using Microsoft.Extensions.Configuration;
using System.IO;

namespace HabitBuilder.Infrastructure.Data
{
    public class HabitDbContextFactory : IDesignTimeDbContextFactory<HabitDbContext>
    {
        public HabitDbContext CreateDbContext(string[] args)
        {
            // Set up the configuration
            var configuration = new ConfigurationBuilder()
                .SetBasePath(Directory.GetCurrentDirectory()) // Make sure it's loading from the right directory
                .AddJsonFile("appsettings.json") // Make sure the appsettings file is included in the project
                .Build();

            // Get the connection string from the configuration
            var connectionString = configuration.GetConnectionString("HabitDbContext");

            // Set up the DbContext options
            var optionsBuilder = new DbContextOptionsBuilder<HabitDbContext>();
            optionsBuilder.UseSqlite(connectionString);

            return new HabitDbContext(optionsBuilder.Options);
        }
    }
}





