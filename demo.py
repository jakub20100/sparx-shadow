#!/usr/bin/env python3
"""
Sparx Shadow Demo Script
Demonstrates the mathematical solving capabilities
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.math_solver import MathSolver
from utils.ocr_parser import OCRParser
import numpy as np

class SparxShadowDemo:
    def __init__(self):
        self.math_solver = MathSolver()
        self.ocr_parser = OCRParser()
        
    def run_demo(self):
        """Run comprehensive demonstration"""
        print("🚀 SPARX SHADOW - MATHEMATICAL SOLVER DEMO")
        print("="*60)
        
        self.demo_equation_solving()
        self.demo_trigonometry()
        self.demo_geometry()
        self.demo_algebra()
        self.demo_word_problems()
        self.demo_ocr_parsing()
        
        print("\n🎉 Demo completed!")
        print("Ready to integrate with Sparx Maths automation.")
    
    def demo_equation_solving(self):
        """Demonstrate equation solving capabilities"""
        print("\n📐 EQUATION SOLVING")
        print("-" * 30)
        
        equations = [
            "2*x + 5 = 13",
            "x^2 - 5*x + 6 = 0",
            "3*x - 7 = 2*x + 8",
            "x/2 + 3 = 7"
        ]
        
        for equation in equations:
            print(f"\nSolving: {equation}")
            result = self.math_solver.solve_equation(equation)
            if result['answer'] is not None:
                print(f"  ✅ Solution: {result['answer']}")
                if result.get('steps'):
                    print(f"  📋 Steps: {len(result['steps'])} step(s)")
            else:
                print(f"  ❌ Could not solve")
    
    def demo_trigonometry(self):
        """Demonstrate trigonometric calculations"""
        print("\n📊 TRIGONOMETRY")
        print("-" * 30)
        
        trig_problems = [
            "sin(pi/6)",
            "cos(pi/4)",
            "tan(pi/3)",
            "sin(30*pi/180)"
        ]
        
        for problem in trig_problems:
            print(f"\nCalculating: {problem}")
            result = self.math_solver.solve_trigonometry(problem)
            if result['answer'] is not None:
                print(f"  ✅ Result: {result['answer']:.6f}")
                print(f"  📋 Exact: {result['exact']}")
    
    def demo_geometry(self):
        """Demonstrate geometric calculations"""
        print("\n📐 GEOMETRY")
        print("-" * 30)
        
        # Pythagorean theorem
        print("\nPythagorean Theorem:")
        pythagoras_props = {'a': 3, 'b': 4}
        result = self.math_solver.solve_pythagoras(pythagoras_props)
        print(f"  Triangle with sides a=3, b=4")
        print(f"  ✅ Hypotenuse: {result['answer']}")
        
        # Triangle area
        print("\nTriangle Area:")
        triangle_props = {
            'sides': {'side_b': 5, 'side_c': 7},
            'angles': {'angle_a': 60}
        }
        result = self.math_solver.solve_triangle(triangle_props)
        print(f"  Triangle with sides b=5, c=7, angle A=60°")
        print(f"  ✅ Area: {result['answer']:.4f}")
    
    def demo_algebra(self):
        """Demonstrate algebraic manipulation"""
        print("\n📝 ALGEBRA")
        print("-" * 30)
        
        expressions = [
            "(x + 2)*(x - 3)",
            "x^2 + 2*x + 1",
            "(x + y)^2"
        ]
        
        for expr in expressions:
            print(f"\nSimplifying: {expr}")
            result = self.math_solver.solve_algebra(expr)
            print(f"  ✅ Simplified: {result['answer']}")
            if result.get('factored'):
                print(f"  📋 Factored: {result['factored']}")
    
    def demo_word_problems(self):
        """Demonstrate word problem parsing"""
        print("\n📖 WORD PROBLEMS")
        print("-" * 30)
        
        word_problems = [
            "If a triangle has a base of 8 units and a height of 5 units, what is its area?",
            "The sum of two numbers is 15 and their difference is 3. Find the numbers.",
            "A circle has a radius of 4 units. What is its area?"
        ]
        
        for problem in word_problems:
            print(f"\nProblem: {problem}")
            parsed = self.ocr_parser.parse_word_problem(problem)
            print(f"  🔍 Parsed as: {parsed['type']}")
            print(f"  🔢 Numbers found: {parsed['numbers']}")
            print(f"  📝 Operation: {parsed['operation']}")
    
    def demo_ocr_parsing(self):
        """Demonstrate OCR text parsing capabilities"""
        print("\n🔍 OCR PARSING")
        print("-" * 30)
        
        sample_texts = [
            "Solve for x: 2x + 5 = 13",
            "Find the area of a triangle with base 6 and height 4",
            "Calculate sin(30°) + cos(60°)",
            "What is the derivative of x²?"
        ]
        
        for text in sample_texts:
            print(f"\nText: {text}")
            parsed = self.ocr_parser.parse_question(None, text)
            print(f"  🏷️  Type: {parsed['type']}")
            print(f"  📋 Content: {parsed['content']}")
    
    def demo_graphing(self):
        """Demonstrate graphing capabilities"""
        print("\n📈 GRAPHING")
        print("-" * 30)
        
        functions = [
            "sin(x)",
            "x^2",
            "1/x",
            "sqrt(x)"
        ]
        
        for func in functions:
            print(f"\nGraphing: {func}")
            try:
                graph_data = self.math_solver.create_graph(func)
                if graph_data:
                    print(f"  ✅ Graph generated successfully")
                    print(f"  📊 Base64 encoded image: {len(graph_data)} characters")
                else:
                    print(f"  ❌ Failed to generate graph")
            except Exception as e:
                print(f"  ❌ Graphing error: {e}")

def main():
    """Main demo function"""
    demo = SparxShadowDemo()
    demo.run_demo()

if __name__ == "__main__":
    main()