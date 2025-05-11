using HabitBuilder.Application.Interfaces;
using HabitBuilder.Infrastructure.Services;
using HabitBuilder.Infrastructure.Data;
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

// Adding DbContext with connection string from appsettings.json
builder.Services.AddControllers();
builder.Services.AddScoped<IHabitService, HabitService>();

// This will read the connection string from appsettings.json
builder.Services.AddDbContext<HabitDbContext>(options =>
    options.UseSqlite(builder.Configuration.GetConnectionString("HabitDbContext"))); // Use connection string from config

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

// Middleware
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseRouting();
app.UseAuthorization();

app.MapControllers();
app.Run();

