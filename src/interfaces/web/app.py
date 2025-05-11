from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import sqlite3  # Add this import
from src.infrastructure.database import init_db, get_db

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Change this in production

@app.before_first_request
def setup():
    init_db()

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        with get_db() as conn:
            try:
                conn.execute(
                    'INSERT INTO users (username, email, password_hash, created_at) VALUES (?, ?, ?, ?)',
                    (username, email, generate_password_hash(password), datetime.now())
                )
                conn.commit()
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                flash('Username or email already exists!', 'danger')
                
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        with get_db() as conn:
            user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
            
            if user and check_password_hash(user['password_hash'], password):
                session['user_id'] = user['id']
                flash('Welcome back!', 'success')
                return redirect(url_for('dashboard'))
            flash('Invalid username or password', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    with get_db() as conn:
        habits = conn.execute(
            'SELECT * FROM habits WHERE user_id = ? ORDER BY created_at DESC',
            (session['user_id'],)
        ).fetchall()
        
        challenges = conn.execute('''
            SELECT c.* FROM challenges c
            JOIN challenge_participants cp ON c.id = cp.challenge_id
            WHERE cp.user_id = ? AND c.end_date >= date('now')
        ''', (session['user_id'],)).fetchall()
        
    return render_template('dashboard.html', habits=habits, challenges=challenges)

@app.route('/habits', methods=['GET'])
def habits():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    with get_db() as conn:
        habits = conn.execute(
            'SELECT * FROM habits WHERE user_id = ? ORDER BY created_at DESC',
            (session['user_id'],)
        ).fetchall()
        
    return render_template('habits.html', habits=habits)

@app.route('/habits/create', methods=['POST'])
def create_habit():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    name = request.form['name']
    description = request.form['description']
    frequency = request.form['frequency']
    reminder_time = request.form.get('reminder_time')
    
    with get_db() as conn:
        conn.execute('''
            INSERT INTO habits (user_id, name, description, frequency, created_at, reminder_time)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (session['user_id'], name, description, frequency, datetime.now(), reminder_time))
        conn.commit()
        
    flash('Habit created successfully!', 'success')
    return redirect(url_for('habits'))

@app.route('/habits/<int:habit_id>/complete', methods=['POST'])
def complete_habit(habit_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    with get_db() as conn:
        habit = conn.execute(
            'SELECT * FROM habits WHERE id = ? AND user_id = ?',
            (habit_id, session['user_id'])
        ).fetchone()
        
        if habit:
            conn.execute('''
                UPDATE habits 
                SET streak = streak + 1, last_completed = ?
                WHERE id = ?
            ''', (datetime.now(), habit_id))
            conn.commit()
            flash('Habit completed! Keep up the good work!', 'success')
        
    return redirect(url_for('habits'))

@app.route('/habits/<int:habit_id>/delete', methods=['POST'])
def delete_habit(habit_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    with get_db() as conn:
        conn.execute('DELETE FROM habits WHERE id = ? AND user_id = ?', 
                    (habit_id, session['user_id']))
        conn.commit()
        flash('Habit deleted successfully!', 'success')
    return redirect(url_for('habits'))

@app.route('/challenges')
def challenges():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    with get_db() as conn:
        challenges = conn.execute('''
            SELECT c.*, COUNT(cp.user_id) as participant_count 
            FROM challenges c
            LEFT JOIN challenge_participants cp ON c.id = cp.challenge_id
            WHERE c.end_date >= date('now')
            GROUP BY c.id
            ORDER BY c.start_date DESC
        ''').fetchall()
        
        user_challenges = conn.execute('''
            SELECT challenge_id FROM challenge_participants
            WHERE user_id = ?
        ''', (session['user_id'],)).fetchall()
        user_challenges = [c['challenge_id'] for c in user_challenges]
        
    return render_template('challenges.html', challenges=challenges, user_challenges=user_challenges)

@app.route('/challenges/create', methods=['POST'])
def create_challenge():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    name = request.form['name']
    description = request.form['description']
    start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')
    end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d')
    
    with get_db() as conn:
        cursor = conn.execute('''
            INSERT INTO challenges (name, description, creator_id, start_date, end_date)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, description, session['user_id'], start_date, end_date))
        challenge_id = cursor.lastrowid
        
        # Automatically join the creator to the challenge
        conn.execute('''
            INSERT INTO challenge_participants (challenge_id, user_id, joined_at)
            VALUES (?, ?, ?)
        ''', (challenge_id, session['user_id'], datetime.now()))
        conn.commit()
        
    flash('Challenge created successfully!', 'success')
    return redirect(url_for('challenges'))

@app.route('/challenges/<int:challenge_id>/join', methods=['POST'])
def join_challenge(challenge_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    with get_db() as conn:
        try:
            conn.execute('''
                INSERT INTO challenge_participants (challenge_id, user_id, joined_at)
                VALUES (?, ?, ?)
            ''', (challenge_id, session['user_id'], datetime.now()))
            conn.commit()
            flash('You have joined the challenge!', 'success')
        except sqlite3.IntegrityError:
            flash('You are already participating in this challenge!', 'warning')
            
    return redirect(url_for('challenges'))

if __name__ == '__main__':
    app.run(debug=True)