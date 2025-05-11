namespace HabitBuilder.Domain;
namespace HabitBuilder.Domain.Entities;

public class Habit
{
    public int Id { get; set; }
    public string Name { get; set; } = "";
    public string Description { get; set; } = "";
}
