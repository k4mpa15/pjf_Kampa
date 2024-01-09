import re

import numpy as np
import sympy as sp
from scipy.integrate import odeint


class EquationSolver:
    def solve_linear_equation(self, equation_content):
        s1 = equation_content.replace("x", "j").replace(" ", "")
        s2 = s1.replace("=", "-(")
        s = s2 + ")"
        self.s_to_show = s.replace("j", "x") + "=0"
        z = eval(s, {"j": 1j})
        real, imag = z.real, -z.imag
        self.real, self.imag = z.real, -z.imag
        self.x = round((real / imag), 2)
        if self.x == -0.0:
            self.x = 0
            return "x = 0"
        if imag:
            return f"x = {round((real / imag), 2)}"
        else:
            if real:
                return "Brak rozwiązań"
            else:
                return "Nieskończona ilosć rozwiązań"

    def solve_quadratic_equation(self, equation_content):
        try:
            equation_content = equation_content.replace(" ", "")
            pattern = re.compile(r"([-+]?\d*)x\*\*2\s*([-+]?\d*)x\s*([-+]?\d*)\s*=\s*0")
            match = pattern.match(equation_content)

            a = 0
            b = 0
            c = 0

            if match:
                a, b, c = map(lambda x: int(x) if x else 0, match.groups())
                self.a = a
                self.b = b
                self.c = c
            else:
                return "Zły format równania!"

            d = (b**2) - (4 * a * c)
            self.d = d
            if d < 0:
                return "Brak rozwiązań"
            elif d == 0:
                self.sol = -b / (2 * a)
                return f"x = {round(self.sol, 2)}"
            elif a == 0:
                return "To nie jest równanie kwadratowe"
            else:
                sol1 = (-b - d**0.5) / (2 * a)
                sol2 = (-b + d**0.5) / (2 * a)
                self.sol1 = sol1
                self.sol2 = sol2
                return f"x1 = {round(sol1, 2)}, x2 = {round(sol2, 2)} "

        except ZeroDivisionError:
            return "Brak rozwiązań"

    def solve_system_of_equation(self, equation_content):
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
        self.A = A
        B = np.array(B)
        self.B = B
        A_odw = np.linalg.inv(A).round(2)
        self.A_odw = A_odw
        x = np.linalg.solve(A, B).round(2)
        self.x = x
        return f"x, y, z ... {str(x)}"

    @staticmethod
    def solve_non_linear_equation_by_newton_raphson(
        func_str, x0, tol=1e-6, max_iter=100
    ):
        # ta metoda głównie służy do rozwiazywania równań nieliniowych f(x) = 0
        func_str = func_str.replace(" ", "")
        func_str = func_str.replace("=0", "")

        x = sp.symbols("x")
        func = sp.sympify(func_str)
        df = sp.diff(func, x)
        f_prime = sp.lambdify(x, df)
        iter_count = 0

        while iter_count < max_iter:
            f_val = func.subs(x, x0)
            f_prime_val = f_prime(x0)

            if abs(f_prime_val) < tol:
                return "Devision by 0!"

            x1 = x0 - f_val / f_prime_val

            if abs(x1 - x0) < tol:
                x1 = x1.evalf(3)
                return f"x = {x1}, iter. = {iter_count}"

            x0 = x1
            iter_count += 1

        return "End of iterations"

    @staticmethod
    def solve_non_linear_equation_by_secant(func_str, x0, x1, tol=1e-6, max_iter=100):
        x = sp.symbols("x")
        func_str = func_str.replace(" ", "")
        func_str = func_str.replace("=0", "")
        func = sp.sympify(func_str)

        f = sp.lambdify(x, func)

        iter_count = 0
        while iter_count < max_iter:
            f_x0 = f(x0)
            f_x1 = f(x1)

            if abs(f_x1 - f_x0) < tol:
                return "Devision by 0!"

            x_next = x1 - f_x1 * (x1 - x0) / (f_x1 - f_x0)

            if abs(x_next - x1) < tol:
                return f"x = {round(x_next, 3)}, iter. = {iter_count}"

            x0, x1 = x1, x_next
            iter_count += 1

        return "End of iterations"

    @staticmethod
    def solve_non_linear_equation_by_bisection(func_str, a, b, tol=1e-6, max_iter=1000):
        x = sp.symbols("x")
        func_str = func_str.replace(" ", "")
        func_str = func_str.replace("=0", "")
        func = sp.sympify(func_str)

        f = sp.lambdify(x, func)

        if f(a) * f(b) > 0:
            return "Wrong data!"

        iter_count = 0
        while iter_count < max_iter:
            c = (a + b) / 2
            f_c = f(c)

            if abs(f_c) < tol:
                return f"x = {round(c, 3)}, iter. = {iter_count}"

            if f_c * f(a) < 0:
                b = c
            else:
                a = c

            iter_count += 1

        return "End of iterations"

    def solve_first_ode(self, equation, initial_condition, a, b):
        def parse_equation(x, y):
            return eval(equation.replace("y", str(y)))

        values = np.arange(a, b + 1)

        solutions = odeint(parse_equation, initial_condition, values)

        return f"x = {values}: {solutions[:,0]}"
