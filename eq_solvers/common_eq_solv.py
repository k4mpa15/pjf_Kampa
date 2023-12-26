import cmath
import re


class EquationSolver:
    @staticmethod
    def solve_linear_equation(equation_content):
        s1 = equation_content.replace("x", "j").replace(" ", "")
        s2 = s1.replace("=", "-(")
        s = s2 + ")"
        z = eval(s, {"j": 1j})
        real, imag = z.real, -z.imag
        if imag:
            return round((real / imag), 2)
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

            print(a, b, c)

            d = (b**2) - (4 * a * c)
            if d < 0:
                return "Brak rozwiązań"
            elif d == 0:
                sol = -c / b
                return round(sol, 2)
            elif a == 0:
                return "To nie jest równanie kwadratowe"
            else:
                sol1 = (-b - d**0.5) / (2 * a)
                sol2 = (-b + d**0.5) / (2 * a)
                return round(sol1, 2), round(sol2, 2)

        except ZeroDivisionError:
            return "Brak rozwiązań"

    def is_valid_coefficient(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False
