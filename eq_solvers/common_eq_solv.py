import cmath


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
            s = equation_content.replace("x", " ").replace("=0", "").split()
            a, b, c = 0, 0, 0
            if len(s) == 3:
                a, b, c = int(s[0]), int(s[1]), int(s[2])
            if len(s) == 2:
                a, b = int(s[0]), int(s[1])
            if len(s) == 1:
                a = int(s[0])
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
