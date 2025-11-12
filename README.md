# Sparx Shadow - Elite Mathematics Automation

A sophisticated, visually stunning web application for automated mathematics homework completion with advanced AI-powered solving capabilities and ethical learning modes.

## Features

### 🔧 Core Functionality
- **Automated Login**: Secure authentication with Sparx Maths
- **Homework Detection**: Intelligent detection of current assignments
- **Universal Math Solver**: Advanced problem-solving engine
- **Smart Answer Input**: Human-like interaction patterns
- **Real-time Progress Tracking**: Live dashboard with statistics

### 🧠 AI-Powered Math Engine
- **SymPy Integration**: Symbolic mathematics solving
- **OCR Technology**: Image-based question extraction
- **Trigonometry Solver**: Advanced trigonometric functions
- **Geometry Calculator**: Shape and area calculations
- **Algebraic Processing**: Equation solving and simplification
- **Calculus Support**: Derivatives and integrals

### 🎨 Obsidian Glass Design
- **Futuristic UI**: Premium cyber aesthetic with glassmorphism
- **Real-time Animations**: Smooth transitions and particle effects
- **Responsive Design**: Works on all devices
- **Dark Theme**: Professional dark mode interface
- **Interactive Elements**: Hover effects and micro-animations

### 🔒 Anti-Detection & Ethics
- **Human-like Timing**: Configurable delays between actions
- **Random Micro-delays**: Natural interaction patterns
- **Ethical Mode**: Shows solution steps for learning
- **Educational Focus**: Designed for understanding, not cheating

## Installation

### Prerequisites
- Python 3.8+
- Chrome Browser
- Tesseract OCR
- Git

### Step-by-Step Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/sparx-shadow.git
   cd sparx-shadow
   ```

2. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Tesseract OCR**
   
   **Windows:**
   - Download from: https://github.com/UB-Mannheim/tesseract/wiki
   - Install to default location (C:\Program Files\Tesseract-OCR\
   - Add to PATH: `setx PATH "%PATH%;C:\Program Files\Tesseract-OCR"`
   
   **macOS:**
   ```bash
   brew install tesseract
   ```
   
   **Linux (Ubuntu/Debian):**
   ```bash
   sudo apt-get install tesseract-ocr
   ```

4. **Install ChromeDriver**
   ```bash
   # The webdriver-manager will handle this automatically
   # But you can manually install if needed
   ```

5. **Configure Environment**
   ```bash
   # Copy environment template (if available)
   cp .env.example .env
   
   # Edit .env file with your settings
   # FLASK_SECRET_KEY=your-secret-key
   # TESSERACT_PATH=/usr/bin/tesseract  # Adjust for your system
   ```

6. **Run the Application**
   ```bash
   python app.py
   ```
   
   The application will be available at: `http://localhost:5000`

## Usage

### 1. Authentication
- Navigate to the main page
- Enter your Sparx Maths credentials:
  - School name
  - Username
  - Password
- Toggle "Ethical Mode" if you want to see solution steps

### 2. Dashboard Controls
- **Min Delay**: Minimum time between questions (3-30 seconds)
- **Max Delay**: Maximum time between questions (5-60 seconds)
- **Ethical Mode**: Show mathematical steps for learning

### 3. Start Automation
- Click "START AUTOMATION" to begin
- Monitor progress in real-time
- View live logs and statistics
- Stop anytime using "STOP AUTOMATION"

### 4. Monitor Progress
- **Questions Solved**: Current completion count
- **Accuracy Rate**: Success percentage
- **Time Remaining**: Session duration
- **Live Log**: Real-time activity tracking

## Configuration

### Environment Variables
```env
FLASK_SECRET_KEY=your-secret-key-here
TESSERACT_PATH=/usr/bin/tesseract
FLASK_ENV=development
FLASK_DEBUG=True
```

### Customization Options
- Modify delays in the dashboard
- Enable/disable ethical mode
- Adjust OCR confidence thresholds
- Configure mathematical solver parameters

## Mathematical Capabilities

### Supported Problem Types
- **Algebraic Equations**: Linear, quadratic, polynomial
- **Trigonometry**: sin, cos, tan, identities
- **Geometry**: Triangles, circles, area, perimeter
- **Calculus**: Derivatives, integrals
- **Word Problems**: Natural language to equations
- **Graphing**: Function visualization

### Solver Features
- Step-by-step solutions
- Multiple solution methods
- Exact and numerical answers
- Graph generation
- Error handling and fallbacks

## Ethical Considerations

### Educational Purpose
This tool is designed for:
- **Learning Enhancement**: Understanding mathematical concepts
- **Practice Support**: Additional problem-solving practice
- **Concept Reinforcement**: Visualizing solution steps
- **Academic Support**: Homework assistance, not replacement

### Responsible Use
- Use in "Ethical Mode" to learn solution methods
- Don't rely solely on automation for learning
- Review and understand the solution steps
- Use as a supplement to regular study

### Academic Integrity
- Designed for educational understanding
- Shows complete solution process
- Encourages learning over cheating
- Includes ethical warnings and guidelines

## Troubleshooting

### Common Issues

1. **Tesseract Not Found**
   ```bash
   # Check Tesseract installation
   tesseract --version
   
   # Update path in ocr_parser.py if needed
   pytesseract.pytesseract.tesseract_cmd = '/path/to/tesseract'
   ```

2. **ChromeDriver Issues**
   ```bash
   # Update webdriver-manager
   pip install --upgrade webdriver-manager
   ```

3. **Login Problems**
   - Check internet connection
   - Verify credentials
   - Ensure school name is exact
   - Check for CAPTCHA requirements

4. **Math Solver Errors**
   - Update SymPy: `pip install --upgrade sympy`
   - Check OCR image quality
   - Verify mathematical expression format

### Performance Optimization
- Increase delay times to avoid detection
- Use ethical mode for better learning
- Clear browser cache regularly
- Monitor system resources

## Security Features

### Data Protection
- No password storage
- Session-based authentication
- Local processing only
- No external data transmission

### Anti-Detection Measures
- Human-like timing patterns
- Random micro-delays
- Natural mouse movements
- Browser fingerprint protection

## Development

### Project Structure
```
sparx-shadow/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── utils/                 # Core utilities
│   ├── sparx_automation.py
│   ├── math_solver.py
│   └── ocr_parser.py
├── templates/             # HTML templates
│   ├── index.html
│   └── dashboard.html
└── README.md
```

### Adding New Features
1. Modify appropriate utility module
2. Update UI templates
3. Add API endpoints in app.py
4. Test thoroughly
5. Update documentation

## Contributing

### Development Guidelines
- Follow PEP 8 style guidelines
- Add comprehensive error handling
- Include user feedback mechanisms
- Maintain ethical standards
- Test across different platforms

### Code Quality
- Use meaningful variable names
- Add docstrings to functions
- Include error handling
- Test edge cases
- Document changes

## License

This project is created for educational purposes. Users are responsible for ethical and appropriate use.

## Disclaimer

**Educational Use Only**: This tool is designed to help students understand mathematical concepts and should be used responsibly. The developers are not responsible for any misuse of this software.

## Support

For issues, questions, or contributions:
- Create an issue in the repository
- Check the troubleshooting section
- Review existing documentation
- Test with sample problems

---

**Built with ❤️ for Mathematics Education**