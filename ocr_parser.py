import pytesseract
import cv2
import numpy as np
from PIL import Image
import io
import re
from sympy import symbols, sympify

class OCRParser:
    def __init__(self):
        self.setup_tesseract()
        self.math_patterns = self.compile_math_patterns()
        
    def setup_tesseract(self):
        """Setup Tesseract configuration"""
        self.tesseract_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789+-*/=()xyzabcsintanlog√πθφ'
        
    def compile_math_patterns(self):
        """Compile regex patterns for mathematical expressions"""
        patterns = {
            'equation': re.compile(r'(.+?)\s*=\s*(.+)'),
            'trigonometry': re.compile(r'(sin|cos|tan)\s*\(?\s*([^)]+)\s*\)?', re.IGNORECASE),
            'square_root': re.compile(r'√\s*\(?\s*([^)]+)\s*\)?'),
            'fraction': re.compile(r'(\d+)\s*/\s*(\d+)'),
            'decimal': re.compile(r'\d+\.\d+'),
            'variable': re.compile(r'[xyzabcθφ]'),
            'angle': re.compile(r'(\d+)\s*°'),
            'triangle': re.compile(r'triangle|Δ', re.IGNORECASE),
            'circle': re.compile(r'circle', re.IGNORECASE),
            'pythagoras': re.compile(r'pythagoras|right\s+triangle', re.IGNORECASE),
            'area': re.compile(r'area', re.IGNORECASE),
            'perimeter': re.compile(r'perimeter', re.IGNORECASE),
            'derivative': re.compile(r'derivative|d/dx', re.IGNORECASE),
            'integral': re.compile(r'integral|∫', re.IGNORECASE)
        }
        return patterns
    
    def parse_question(self, image_data, text_data=""):
        """Main parsing function that extracts mathematical information"""
        try:
            # Extract text from image using OCR
            ocr_text = self.extract_text_from_image(image_data)
            
            # Combine OCR text with provided text
            combined_text = f"{ocr_text} {text_data}".strip()
            
            # Clean and normalize text
            cleaned_text = self.clean_text(combined_text)
            
            # Determine question type and extract content
            question_type = self.determine_question_type(cleaned_text)
            content = self.extract_content(cleaned_text, question_type)
            
            return {
                'type': question_type,
                'content': content,
                'original_text': cleaned_text,
                'ocr_confidence': self.get_ocr_confidence(image_data)
            }
        
        except Exception as e:
            return {
                'type': 'unknown',
                'content': text_data,
                'error': str(e),
                'needs_manual_review': True
            }
    
    def extract_text_from_image(self, image_data):
        """Extract text from image using OCR"""
        try:
            # Convert image data to PIL Image
            if isinstance(image_data, bytes):
                image = Image.open(io.BytesIO(image_data))
            else:
                # Assume it's already a PIL Image
                image = image_data
            
            # Preprocess image for better OCR
            processed_image = self.preprocess_image(image)
            
            # Extract text
            text = pytesseract.image_to_string(processed_image, config=self.tesseract_config)
            
            return text.strip()
        
        except Exception as e:
            print(f"OCR extraction error: {e}")
            return ""
    
    def preprocess_image(self, image):
        """Preprocess image for better OCR accuracy"""
        try:
            # Convert to numpy array if needed
            if isinstance(image, Image.Image):
                image = np.array(image)
            
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) if len(image.shape) == 3 else image
            
            # Apply denoising
            denoised = cv2.fastNlMeansDenoising(gray)
            
            # Apply adaptive threshold
            thresh = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                         cv2.THRESH_BINARY, 11, 2)
            
            # Morphological operations to clean up
            kernel = np.ones((1, 1), np.uint8)
            cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
            
            return Image.fromarray(cleaned)
        
        except Exception as e:
            print(f"Image preprocessing error: {e}")
            return Image.fromarray(image) if isinstance(image, np.ndarray) else image
    
    def clean_text(self, text):
        """Clean and normalize extracted text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Fix common OCR errors
        text = re.sub(r'[lI1]\s*\(\s*\)', '1', text)  # Fix 1 being read as l or I
        text = re.sub(r'[O0]\s*\(\s*\)', '0', text)  # Fix 0 being read as O
        text = re.sub(r'\b[Z2]\b', '2', text)  # Fix 2 being read as Z
        
        # Normalize mathematical symbols
        text = re.sub(r'sqr|sqrt', '√', text, flags=re.IGNORECASE)
        text = re.sub(r'theta', 'θ', text, flags=re.IGNORECASE)
        text = re.sub(r'phi', 'φ', text, flags=re.IGNORECASE)
        text = re.sub(r'pi', 'π', text, flags=re.IGNORECASE)
        
        # Fix spacing around operators
        text = re.sub(r'\s*([+\-*/=])\s*', r' \1 ', text)
        
        return text.strip()
    
    def determine_question_type(self, text):
        """Determine the type of mathematical question"""
        text_lower = text.lower()
        
        # Check for calculus
        if self.math_patterns['derivative'].search(text_lower):
            return 'calculus'
        if self.math_patterns['integral'].search(text_lower):
            return 'calculus'
        
        # Check for geometry
        if self.math_patterns['pythagoras'].search(text_lower):
            return 'geometry'
        if self.math_patterns['triangle'].search(text_lower):
            return 'geometry'
        if self.math_patterns['circle'].search(text_lower):
            return 'geometry'
        
        # Check for trigonometry
        if self.math_patterns['trigonometry'].search(text):
            return 'trigonometry'
        
        # Check for equations
        if self.math_patterns['equation'].search(text):
            return 'equation'
        
        # Check for algebraic expressions
        if any(var in text for var in ['x', 'y', 'z']) and not '=' in text:
            return 'algebra'
        
        # Default type
        return 'general'
    
    def extract_content(self, text, question_type):
        """Extract relevant mathematical content based on question type"""
        if question_type == 'equation':
            return self.extract_equation(text)
        elif question_type == 'trigonometry':
            return self.extract_trigonometry(text)
        elif question_type == 'geometry':
            return self.extract_geometry(text)
        elif question_type == 'calculus':
            return self.extract_calculus(text)
        else:
            return text
    
    def extract_equation(self, text):
        """Extract equation from text"""
        match = self.math_patterns['equation'].search(text)
        if match:
            lhs, rhs = match.groups()
            return f"{lhs.strip()} = {rhs.strip()}"
        return text
    
    def extract_trigonometry(self, text):
        """Extract trigonometric expressions"""
        matches = self.math_patterns['trigonometry'].findall(text)
        if matches:
            trig_functions = []
            for match in matches:
                func, arg = match
                trig_functions.append(f"{func}({arg})")
            return trig_functions[0] if len(trig_functions) == 1 else trig_functions
        return text
    
    def extract_geometry(self, text):
        """Extract geometric information"""
        geometry_info = {
            'shape': '',
            'properties': {}
        }
        
        # Determine shape
        if self.math_patterns['triangle'].search(text.lower()):
            geometry_info['shape'] = 'triangle'
        elif self.math_patterns['circle'].search(text.lower()):
            geometry_info['shape'] = 'circle'
        elif self.math_patterns['pythagoras'].search(text.lower()):
            geometry_info['shape'] = 'pythagoras'
        
        # Extract numerical values
        numbers = re.findall(r'\d+\.?\d*', text)
        if len(numbers) >= 1:
            geometry_info['properties']['values'] = [float(n) for n in numbers]
        
        # Extract angle values
        angles = self.math_patterns['angle'].findall(text)
        if angles:
            geometry_info['properties']['angles'] = [int(a) for a in angles]
        
        return geometry_info
    
    def extract_calculus(self, text):
        """Extract calculus information"""
        calc_info = {
            'operation': '',
            'function': ''
        }
        
        # Determine operation
        if self.math_patterns['derivative'].search(text.lower()):
            calc_info['operation'] = 'derivative'
        elif self.math_patterns['integral'].search(text.lower()):
            calc_info['operation'] = 'integral'
        
        # Extract function (simplified - look for expressions with x)
        x_pattern = re.compile(r'[xy]\s*[+\-*/^]\s*[^=]+', re.IGNORECASE)
        matches = x_pattern.findall(text)
        if matches:
            calc_info['function'] = matches[0].strip()
        
        return calc_info
    
    def get_ocr_confidence(self, image_data):
        """Get OCR confidence score"""
        try:
            if isinstance(image_data, bytes):
                image = Image.open(io.BytesIO(image_data))
            else:
                image = image_data
            
            # Get detailed OCR data
            data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
            
            # Calculate average confidence
            confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
            
            return sum(confidences) / len(confidences) if confidences else 0
        
        except Exception as e:
            print(f"OCR confidence calculation error: {e}")
            return 0
    
    def parse_word_problem(self, text):
        """Parse word problems and convert to mathematical expressions"""
        # Common word problem patterns
        patterns = {
            'total': re.compile(r'total|altogether|sum', re.IGNORECASE),
            'difference': re.compile(r'difference|more than|less than', re.IGNORECASE),
            'product': re.compile(r'product|times', re.IGNORECASE),
            'quotient': re.compile(r'quotient|divided by', re.IGNORECASE),
            'perimeter': re.compile(r'perimeter|around', re.IGNORECASE),
            'area': re.compile(r'area', re.IGNORECASE)
        }
        
        # Extract numbers
        numbers = re.findall(r'\d+\.?\d*', text)
        
        # Determine operation based on keywords
        operation = 'unknown'
        for op, pattern in patterns.items():
            if pattern.search(text):
                operation = op
                break
        
        return {
            'type': 'word_problem',
            'operation': operation,
            'numbers': [float(n) for n in numbers],
            'text': text
        }