class EquationSolver:
    @staticmethod
    def solve_equation(equation_content):
        s1 = equation_content.replace("x", "j").replace(" ", "")
        s2 = s1.replace("=", "-(") 
        s = s2+")"
        z = eval(s, {"j": 1j}) 
        real, imag = z.real, -z.imag 
        if imag: 
            return real/imag
        else: 
            if real: 
                return "Brak rozwiązań"
            else: 
                return "Nieskończona ilosć rozwiązań"