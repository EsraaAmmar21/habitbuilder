using HabitBuilder.Application.Interfaces;
using HabitBuilder.Domain.Entities;
using HabitBuilder.Infrastructure.Data;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace HabitBuilder.Infrastructure.Services
{
    public class HabitService : IHabitService
    {

        private readonly HabitDbContext _context;

        public HabitService(HabitDbContext context)
        {
            _context = context;
        }

        public async Task<Habit?> GetHabitByIdAsync(Guid habitId)
{
    return await _context.Habits.FirstOrDefaultAsync(h => h.Id == habitId);
}



        public async Task<List<Habit>> GetAllHabitsAsync()
        {
            return await _context.Habits.ToListAsync();
        }

        public async Task<Habit> CreateHabitAsync(Habit habit)
        {
            _context.Habits.Add(habit);
            await _context.SaveChangesAsync();
            return habit;
        }

        public async Task<Habit> UpdateHabitAsync(Habit habit)
        {
            _context.Habits.Update(habit);
            await _context.SaveChangesAsync();
            return habit;
        }

        public async Task<bool> DeleteHabitAsync(Guid habitId)
        {
            var habit = await _context.Habits.FindAsync(habitId);
            if (habit == null)
                return false;

            _context.Habits.Remove(habit);
            await _context.SaveChangesAsync();
            return true;
        }

        public List<Habit> GetHabits()
{
    // Fetching habits from the database
    return _context.Habits.ToList(); // This will get all habits from the database
}

    }
}
