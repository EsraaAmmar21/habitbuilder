using Microsoft.EntityFrameworkCore;
using HabitBuilder.Domain.Entities;

namespace HabitBuilder.Infrastructure.Data
{
    public class HabitDbContext : DbContext
    {
        public HabitDbContext(DbContextOptions<HabitDbContext> options) : base(options)
        {
        }

        public DbSet<Habit> Habits { get; set; }
        public DbSet<User> Users { get; set; }
        // Add other DbSet properties for your entities
    }
}

