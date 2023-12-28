import cmath
import re
import numpy as np


class EquationSolver:
    @staticmethod
    def solve_linear_equation(equation_content):
        s1 = equation_content.replace("x", "j").replace(" ", "")
        s2 = s1.replace("=", "-(")
        s = s2 + ")"
        z = eval(s, {"j": 1j})
        real, imag = z.real, -z.imag
        if imag:
            return f"x = {round((real / imag), 2)}"
        else:
            if real:
                return "Brak rozwiązań"
            else:
                return "Nieskończona ilosć rozwiązań"

    @staticmethod
    def solve_quadratic_equation(equation_content):
        try:
            equation_content = equation_content.replace(" ", "")
            pattern = re.compile(r"([-+]?\d*)x\^2\s*([-+]?\d*)x\s*([-+]?\d*)\s*=\s*0")
            match = pattern.match(equation_content)

            a = 0
            b = 0
            c = 0

            if match:
                a, b, c = map(lambda x: int(x) if x else 0, match.groups())
            else:
                return "Zły format równania!"

            d = (b**2) - (4 * a * c)
            if d < 0:
                return "Brak rozwiązań"
            elif d == 0:
                sol = -b / (2 * a)
                return f"x = {round(sol, 2)}"
            elif a == 0:
                return "To nie jest równanie kwadratowe"
            else:
                sol1 = (-b - d**0.5) / (2 * a)
                sol2 = (-b + d**0.5) / (2 * a)
                return f"x1 = {round(sol1, 2)}, x2 = {round(sol2, 2)} "

        except ZeroDivisionError:
            return "Brak rozwiązań"

    @staticmethod
    def solve_system_of_equation(equation_content):
        equations = equation_content.replace(" ", "").split(";")
        A = [[] for _ in range(len(equations))]
        B = []
        for equation in equations:
            equation_pattern = re.compile(r"([-+]?\d*\.?\d+)([a-zA-Z]+)")
            match = re.search(r"=\s*([-+]?\d*\.?\d+)", equation)
            if match:
                result = match.group(1) 

            matches = equation_pattern.findall(equation)

            for i in range(0, len(equations)):
                try:
                    num = float(matches[i][0]) 
                    A[i].append(num)
                except IndexError:
                    A[i].append(0)
            
            B.append(float(result))

        A = np.array(A).transpose()
        B = np.array(B)

        x = np.linalg.solve(A, B)
        return f"x, y, z ... {str(x)}"
