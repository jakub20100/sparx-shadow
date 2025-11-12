import sympy as sp
import numpy as np
import re
from sympy import symbols, solve, sin, cos, tan, pi, sqrt, simplify, expand, factor
from sympy.geometry import Triangle, Point, Circle, Line
import matplotlib.pyplot as plt
import io
import base64

class MathSolver:
    def __init__(self):
        self.setup_symbols()
        
    def setup_symbols(self):
        """Setup common mathematical symbols"""
        self.x, self.y, self.z = symbols('x y z', real=True)
        self.a, self.b, self.c = symbols('a b c', real=True)
        self.theta, self.phi = symbols('theta phi', real=True)
        self.n = symbols('n', integer=True)
        
    def solve(self, parsed_question):
        """Main solving function that routes to appropriate solver"""
        question_type = parsed_question.get('type', 'unknown')
        content = parsed_question.get('content', '')
        
        if question_type == 'equation':
            return self.solve_equation(content)
        elif question_type == 'trigonometry':
            return self.solve_trigonometry(content)
        elif question_type == 'geometry':
            return self.solve_geometry(content)
        elif question_type == 'algebra':
            return self.solve_algebra(content)
        elif question_type == 'calculus':
            return self.solve_calculus(content)
        else:
            return self.solve_general(content)
    
    def solve_equation(self, equation_str):
        """Solve algebraic equations"""
        try:
            # Parse equation
            lhs, rhs = equation_str.split('=')
            equation = sp.Eq(sp.sympify(lhs), sp.sympify(rhs))
            
            # Solve for variables
            solutions = solve(equation, self.x)
            
            # Format solutions
            formatted_solutions = []
            for sol in solutions:
                if sol.is_real:
                    formatted_solutions.append(float(sol))
                else:
                    formatted_solutions.append(str(sol))
            
            return {
                'type': 'equation',
                'original': equation_str,
                'answer': formatted_solutions[0] if formatted_solutions else None,
                'all_solutions': formatted_solutions,
                'steps': self.generate_equation_steps(equation)
            }
        
        except Exception as e:
            return self.fallback_solve(equation_str)
    
    def solve_trigonometry(self, trig_str):
        """Solve trigonometric problems"""
        try:
            # Handle trigonometric equations
            if '=' in trig_str:
                return self.solve_equation(trig_str)
            
            # Evaluate trigonometric expressions
            expr = sp.sympify(trig_str)
            simplified = sp.simplify(expr)
            
            # Convert to numerical value if possible
            numerical_value = float(simplified.evalf())
            
            return {
                'type': 'trigonometry',
                'original': trig_str,
                'answer': numerical_value,
                'exact': str(simplified),
                'steps': self.generate_trig_steps(expr)
            }
        
        except Exception as e:
            return self.fallback_solve(trig_str)
    
    def solve_geometry(self, geometry_info):
        """Solve geometry problems"""
        try:
            # Extract geometric information
            shape = geometry_info.get('shape', '').lower()
            properties = geometry_info.get('properties', {})
            
            if shape == 'triangle':
                return self.solve_triangle(properties)
            elif shape == 'circle':
                return self.solve_circle(properties)
            elif shape == 'pythagoras':
                return self.solve_pythagoras(properties)
            else:
                return self.solve_general_geometry(properties)
        
        except Exception as e:
            return self.fallback_solve(str(geometry_info))
    
    def solve_triangle(self, properties):
        """Solve triangle problems"""
        try:
            # Extract triangle properties
            sides = properties.get('sides', {})
            angles = properties.get('angles', {})
            
            # Solve for missing elements
            if 'a' in sides and 'b' in sides and 'c' in sides:
                # All sides known - calculate area using Heron's formula
                a, b, c = sides['a'], sides['b'], sides['c']
                s = (a + b + c) / 2
                area = sqrt(s * (s - a) * (s - b) * (s - c))
                
                return {
                    'type': 'triangle',
                    'answer': float(area),
                    'properties': {
                        'area': float(area),
                        'perimeter': float(a + b + c)
                    }
                }
            
            elif 'angle_a' in angles and 'side_b' in sides and 'side_c' in sides:
                # Two sides and included angle - calculate area
                angle_a = angles['angle_a']
                side_b = sides['side_b']
                side_c = sides['side_c']
                
                area = 0.5 * side_b * side_c * sin(angle_a * pi / 180)
                
                return {
                    'type': 'triangle',
                    'answer': float(area),
                    'properties': {'area': float(area)}
                }
            
            else:
                return self.fallback_solve(str(properties))
        
        except Exception as e:
            return self.fallback_solve(str(properties))
    
    def solve_pythagoras(self, properties):
        """Solve Pythagorean theorem problems"""
        try:
            a = properties.get('a')
            b = properties.get('b')
            c = properties.get('c')
            
            if a is not None and b is not None:
                # Find hypotenuse
                c = sqrt(a**2 + b**2)
                return {
                    'type': 'pythagoras',
                    'answer': float(c),
                    'steps': [f"c² = a² + b²", f"c² = {a}² + {b}²", f"c = √({a**2 + b**2}) = {float(c)}"]
                }
            
            elif a is not None and c is not None:
                # Find missing side
                b = sqrt(c**2 - a**2)
                return {
                    'type': 'pythagoras',
                    'answer': float(b),
                    'steps': [f"b² = c² - a²", f"b² = {c}² - {a}²", f"b = √({c**2 - a**2}) = {float(b)}"]
                }
            
            else:
                return self.fallback_solve(str(properties))
        
        except Exception as e:
            return self.fallback_solve(str(properties))
    
    def solve_algebra(self, algebra_str):
        """Solve algebraic problems"""
        try:
            # Expand and simplify expressions
            expr = sp.sympify(algebra_str)
            expanded = expand(expr)
            simplified = simplify(expanded)
            factored = factor(simplified)
            
            return {
                'type': 'algebra',
                'original': algebra_str,
                'answer': str(simplified),
                'expanded': str(expanded),
                'factored': str(factored)
            }
        
        except Exception as e:
            return self.fallback_solve(algebra_str)
    
    def solve_calculus(self, calc_info):
        """Solve calculus problems"""
        try:
            operation = calc_info.get('operation', '')
            function = calc_info.get('function', '')
            
            expr = sp.sympify(function)
            
            if operation == 'derivative':
                derivative = sp.diff(expr, self.x)
                return {
                    'type': 'calculus',
                    'operation': 'derivative',
                    'answer': str(derivative),
                    'steps': self.generate_calculus_steps(expr, derivative)
                }
            
            elif operation == 'integral':
                integral = sp.integrate(expr, self.x)
                return {
                    'type': 'calculus',
                    'operation': 'integral',
                    'answer': str(integral),
                    'steps': self.generate_calculus_steps(expr, integral)
                }
            
            else:
                return self.fallback_solve(str(calc_info))
        
        except Exception as e:
            return self.fallback_solve(str(calc_info))
    
    def solve_general(self, problem_str):
        """General problem solver with fallback methods"""
        try:
            # Try to parse as expression
            expr = sp.sympify(problem_str)
            simplified = sp.simplify(expr)
            numerical = float(simplified.evalf())
            
            return {
                'type': 'general',
                'original': problem_str,
                'answer': numerical,
                'exact': str(simplified)
            }
        
        except Exception as e:
            return self.fallback_solve(problem_str)
    
    def fallback_solve(self, problem_str):
        """Fallback solver for unrecognized problems"""
        return {
            'type': 'unknown',
            'original': problem_str,
            'answer': None,
            'error': 'Could not solve this problem automatically',
            'needs_manual_review': True
        }
    
    def generate_equation_steps(self, equation):
        """Generate step-by-step solution for equations"""
        steps = []
        
        # Basic steps for linear equations
        if isinstance(equation, sp.Eq):
            lhs, rhs = equation.lhs, equation.rhs
            steps.append(f"Original equation: {lhs} = {rhs}")
            
            # Move all terms to one side
            combined = lhs - rhs
            steps.append(f"Rearrange: {combined} = 0")
            
            # Solve
            solutions = solve(equation, self.x)
            steps.append(f"Solutions: {solutions}")
        
        return steps
    
    def generate_trig_steps(self, expr):
        """Generate step-by-step solution for trigonometry"""
        steps = []
        steps.append(f"Original expression: {expr}")
        
        # Apply trigonometric identities
        simplified = sp.simplify(expr)
        steps.append(f"Simplified: {simplified}")
        
        return steps
    
    def generate_calculus_steps(self, original, result):
        """Generate step-by-step solution for calculus"""
        steps = []
        steps.append(f"Original function: {original}")
        steps.append(f"Result: {result}")
        return steps
    
    def create_graph(self, function_str, x_range=(-10, 10)):
        """Create a graph of a mathematical function"""
        try:
            x_vals = np.linspace(x_range[0], x_range[1], 400)
            
            # Convert sympy expression to numpy function
            expr = sp.sympify(function_str)
            f = sp.lambdify(self.x, expr, 'numpy')
            
            y_vals = f(x_vals)
            
            plt.figure(figsize=(8, 6))
            plt.plot(x_vals, y_vals, 'b-', linewidth=2, label=f'y = {function_str}')
            plt.grid(True, alpha=0.3)
            plt.xlabel('x')
            plt.ylabel('y')
            plt.title(f'Graph of {function_str}')
            plt.legend()
            
            # Save to base64 string
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            graph_base64 = base64.b64encode(buffer.read()).decode()
            plt.close()
            
            return graph_base64
        
        except Exception as e:
            print(f"Graph creation error: {e}")
            return None