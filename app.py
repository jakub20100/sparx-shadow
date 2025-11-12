from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from dotenv import load_dotenv
from flask_socketio import SocketIO, emit
import threading
import time
import json
import os
from datetime import datetime
from utils.sparx_automation import SparxAutomation
from utils.math_solver import MathSolver
from utils.ocr_parser import OCRParser

# Load environment variables from a .env file if present.
# This allows sensitive configuration (like the Flask secret key) to live outside of
# version control. See setup.py for generating a .env file automatically.
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", os.getenv("SECRET_KEY", "change-me"))
socketio = SocketIO(app, cors_allowed_origins="*")

# Global instances
automation = None
math_solver = MathSolver()
ocr_parser = OCRParser()

class ProgressTracker:
    def __init__(self):
        self.questions_solved = 0
        self.total_questions = 0
        self.accuracy = 0
        self.current_question = ""
        self.status = "Ready"
        self.start_time = None
        self.solutions = []
    
    def reset(self):
        self.__init__()

progress_tracker = ProgressTracker()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('index'))
    return render_template('dashboard.html')

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    school = data.get('school')
    username = data.get('username')
    password = data.get('password')
    
    try:
        global automation
        automation = SparxAutomation()
        success = automation.login(school, username, password)
        
        if success:
            session['logged_in'] = True
            session['school'] = school
            session['username'] = username
            progress_tracker.reset()
            return jsonify({'success': True, 'message': 'Login successful'})
        else:
            return jsonify({'success': False, 'message': 'Login failed'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/start_bot', methods=['POST'])
def start_bot():
    if 'logged_in' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    data = request.json
    min_delay = data.get('min_delay', 8)
    max_delay = data.get('max_delay', 25)
    ethical_mode = data.get('ethical_mode', False)
    
    def run_bot():
        try:
            global automation, progress_tracker
            progress_tracker.start_time = datetime.now()
            progress_tracker.status = "Running"
            
            # Start the automation
            automation.solve_homework(
                min_delay=min_delay,
                max_delay=max_delay,
                ethical_mode=ethical_mode,
                progress_callback=update_progress
            )
            
            progress_tracker.status = "Completed"
            socketio.emit('bot_completed', {
                'message': 'Homework completed!',
                'final_stats': {
                    'questions_solved': progress_tracker.questions_solved,
                    'accuracy': progress_tracker.accuracy,
                    'time_taken': str(datetime.now() - progress_tracker.start_time)
                }
            })
        
        except Exception as e:
            progress_tracker.status = "Error"
            socketio.emit('bot_error', {'message': str(e)})
    
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    return jsonify({'success': True, 'message': 'Bot started'})

def update_progress(data):
    progress_tracker.questions_solved = data.get('questions_solved', 0)
    progress_tracker.total_questions = data.get('total_questions', 0)
    progress_tracker.accuracy = data.get('accuracy', 0)
    progress_tracker.current_question = data.get('current_question', '')
    
    socketio.emit('progress_update', {
        'questions_solved': progress_tracker.questions_solved,
        'total_questions': progress_tracker.total_questions,
        'accuracy': progress_tracker.accuracy,
        'current_question': progress_tracker.current_question,
        'status': progress_tracker.status
    })

@app.route('/api/progress')
def get_progress():
    return jsonify({
        'questions_solved': progress_tracker.questions_solved,
        'total_questions': progress_tracker.total_questions,
        'accuracy': progress_tracker.accuracy,
        'current_question': progress_tracker.current_question,
        'status': progress_tracker.status,
        'start_time': progress_tracker.start_time.isoformat() if progress_tracker.start_time else None
    })

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    global automation
    if automation:
        automation.quit()
        automation = None
    return jsonify({'success': True})

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)