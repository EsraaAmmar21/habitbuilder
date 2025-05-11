using HabitBuilder.Domain.Entities;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace HabitBuilder.Application.Interfaces
{
    public interface IHabitService
    {
        Task<List<Habit>> GetAllHabitsAsync();  // Async method for getting all habits
        Task<Habit?> GetHabitByIdAsync(Guid habitId);  // Async method for getting habit by ID
        Task<Habit> CreateHabitAsync(Habit habit);  // Async method for creating a habit
        Task<Habit> UpdateHabitAsync(Habit habit);  // Async method for updating a habit
        Task<bool> DeleteHabitAsync(Guid habitId);  // Async method for deleting a habit
        List<Habit> GetHabits();  // Synchronous method for getting all habits
    }
}


