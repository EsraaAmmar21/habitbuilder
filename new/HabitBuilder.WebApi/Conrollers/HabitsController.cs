using HabitBuilder.Application.Interfaces;
using HabitBuilder.Domain.Entities;
using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace HabitBuilder.WebApi.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class HabitsController : ControllerBase
    {
        private readonly IHabitService _habitService;

        public HabitsController(IHabitService habitService)
        {
            _habitService = habitService;
        }

        // GET: api/Habits
        [HttpGet]
        public async Task<ActionResult<List<Habit>>> GetHabits()
        {
            var habits = await _habitService.GetAllHabitsAsync();  // Use the async method
            return Ok(habits);
        }

        // POST: api/Habits
        [HttpPost]
        public async Task<ActionResult<Habit>> AddHabit(Habit habit)
        {
            var createdHabit = await _habitService.CreateHabitAsync(habit);  // Use the async method
            return CreatedAtAction(nameof(GetHabits), new { id = createdHabit.Id }, createdHabit);
        }

        // DELETE: api/Habits/{id}
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteHabit(Guid id)
        {
            var success = await _habitService.DeleteHabitAsync(id);  // Use the async method
            if (!success)
                return NotFound();
            return NoContent();
        }
    }
}


