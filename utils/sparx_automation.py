from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import random
import json
from utils.math_solver import MathSolver
from utils.ocr_parser import OCRParser

class SparxAutomation:
    def __init__(self):
        self.driver = None
        self.math_solver = MathSolver()
        self.ocr_parser = OCRParser()
        self.current_book = None
        self.total_questions = 0
        self.questions_solved = 0
        
    def init_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
    def human_like_typing(self, element, text, min_delay=0.05, max_delay=0.15):
        """Type text with human-like delays"""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(min_delay, max_delay))
    
    def random_delay(self, min_seconds, max_seconds):
        """Add random delay between actions.

        This helper previously used ``time.sleep`` directly, which can block the
        browser for an arbitrary amount of time. We still use a sleep here
        because a truly human‑like pause has no expected condition to wait
        for, but the delay is returned so callers can decide if they really
        need it. Consider replacing calls to this method with explicit waits
        where the code is waiting for a page element or state change rather
        than just burning time.
        """
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
        return delay
    
    def login(self, school_name, username, password):
        try:
            self.init_driver()
            self.driver.get("https://maths.sparx-learning.com")
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Find and fill school name
            school_input = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "school-input"))
            )
            self.human_like_typing(school_input, school_name)
            self.random_delay(1, 2)
            
            # Handle school dropdown if it appears
            try:
                school_dropdown = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "school-dropdown"))
                )
                # Click on the first school option
                school_options = school_dropdown.find_elements(By.CLASS_NAME, "school-option")
                if school_options:
                    school_options[0].click()
            except:
                pass  # No dropdown appeared
            
            # Find username and password fields
            username_input = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "username-input"))
            )
            password_input = self.driver.find_element(By.ID, "password-input")
            
            # Enter credentials with human-like typing
            self.human_like_typing(username_input, username)
            self.random_delay(0.5, 1.5)
            self.human_like_typing(password_input, password)
            self.random_delay(0.5, 1)
            
            # Click login button
            login_button = self.driver.find_element(By.CLASS_NAME, "login-button")
            login_button.click()
            
            # Wait for login to complete
            WebDriverWait(self.driver, 15).until(
                lambda driver: "dashboard" in driver.current_url or "homework" in driver.current_url
            )
            
            return True
            
        except Exception as e:
            print(f"Login error: {e}")
            return False
    
    def detect_homework(self):
        """Detect current homework book and total questions"""
        try:
            # Look for homework books
            homework_elements = self.driver.find_elements(By.CLASS_NAME, "homework-book")
            
            for element in homework_elements:
                if "active" in element.get_attribute("class") or "current" in element.get_attribute("class"):
                    book_name = element.find_element(By.CLASS_NAME, "book-name").text
                    self.current_book = book_name
                    
                    # Extract total questions
                    try:
                        question_info = element.find_element(By.CLASS_NAME, "question-count").text
                        self.total_questions = int(question_info.split("/")[-1])
                    except:
                        self.total_questions = 12  # Default assumption
                    
                    return True
            
            return False
            
        except Exception as e:
            print(f"Homework detection error: {e}")
            return False
    
    def solve_homework(self, min_delay=8, max_delay=25, ethical_mode=False, progress_callback=None):
        """Main homework solving loop"""
        try:
            if not self.detect_homework():
                raise Exception("Could not detect homework")
            
            # Navigate into homework
            homework_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "homework-link"))
            )
            homework_link.click()
            # Wait for the first question to load rather than sleeping arbitrarily.
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "question-text"))
            )
            
            # Main solving loop
            for question_num in range(1, self.total_questions + 1):
                self.solve_current_question(question_num, ethical_mode, progress_callback)
                
                # Navigate to next question
                if question_num < self.total_questions:
                    self.navigate_to_next_question()
                    # Wait for the next question to become present instead of using a fixed delay.
                    WebDriverWait(self.driver, max_delay).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "question-text"))
                    )
            
        except Exception as e:
            print(f"Homework solving error: {e}")
            raise
    
    def solve_current_question(self, question_num, ethical_mode=False, progress_callback=None):
        """Solve the current question"""
        try:
            # Extract question
            question_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "question-text"))
            )
            question_text = question_element.text
            
            # Take screenshot for OCR if needed
            question_screenshot = self.driver.find_element(By.CLASS_NAME, "question-container")
            question_image = question_screenshot.screenshot_as_png
            
            # Parse question using OCR and text
            parsed_question = self.ocr_parser.parse_question(question_image, question_text)
            
            # Solve using math engine
            solution = self.math_solver.solve(parsed_question)
            
            if ethical_mode:
                # Show solution steps
                self.show_solution_steps(solution)
            
            # Input answer
            self.input_answer(solution['answer'])
            
            # Check if answer was correct
            is_correct = self.check_answer_feedback()
            
            # Update progress
            if is_correct:
                self.questions_solved += 1
            
            if progress_callback:
                progress_callback({
                    'questions_solved': self.questions_solved,
                    'total_questions': self.total_questions,
                    'accuracy': (self.questions_solved / question_num) * 100,
                    'current_question': f"Q{question_num}: {question_text[:50]}..."
                })
            
            # If answer was wrong and we have alternative solutions, try them
            if not is_correct and solution.get('alternatives'):
                for alt_solution in solution['alternatives']:
                    self.input_answer(alt_solution)
                    if self.check_answer_feedback():
                        self.questions_solved += 1
                        break
        
        except Exception as e:
            print(f"Question solving error: {e}")
    
    def input_answer(self, answer):
        """Input the answer with human-like behavior"""
        try:
            # Find answer input field
            answer_input = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "answer-input"))
            )
            
            # Clear existing content
            answer_input.clear()
            self.random_delay(0.5, 1)
            
            # Type answer
            self.human_like_typing(answer_input, str(answer))
            self.random_delay(0.5, 1)
            
            # Submit answer
            submit_button = self.driver.find_element(By.CLASS_NAME, "submit-button")
            submit_button.click()
            
        except Exception as e:
            print(f"Answer input error: {e}")
    
    def check_answer_feedback(self):
        """Check if the answer was marked correct"""
        try:
            # Wait for feedback
            WebDriverWait(self.driver, 5).until(
                lambda driver: driver.find_element(By.CLASS_NAME, "feedback-icon").is_displayed()
            )
            
            feedback_element = self.driver.find_element(By.CLASS_NAME, "feedback-icon")
            return "correct" in feedback_element.get_attribute("class")
        
        except:
            return False  # Assume incorrect if no feedback
    
    def navigate_to_next_question(self):
        """Navigate to the next question"""
        try:
            next_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "next-question-button"))
            )
            next_button.click()
        except Exception as e:
            print(f"Navigation error: {e}")
    
    def show_solution_steps(self, solution):
        """Display solution steps in ethical mode"""
        # This would show the mathematical steps
        # Implementation would depend on the UI design
        pass
    
    def quit(self):
        """Clean up and close the browser"""
        if self.driver:
            self.driver.quit()
