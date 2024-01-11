import json
import tkinter as tk

import customtkinter as ctk
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from sympy import lambdify, symbols
from mpl_toolkits.mplot3d import Axes3D


from eq_solvers.common_eq_solv import EquationSolver

with open("gui/colors.json") as f:
    colors_data = json.load(f)

COLORS = colors_data.get("COLORS", {})
FONT = "Century Gothic"


class TopLevelPlots(ctk.CTkToplevel):
    def __init__(
        self, translator, equation_content, equation_type, a, b, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.geometry("600x500")
        self.translator = translator
        self.equation_solver = EquationSolver()
        self.configure(fg_color=COLORS["BACKGROUND_COLOR"])
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.title("Wykres")
        self.equation_content = equation_content
        self.a = a
        self.b = b
        self.grab_set()
        self.equation_type = equation_type
        self.toolbar = None
        self.fig, self.ax = plt.subplots(figsize=(5, 4))
        self.create_plot()

    def on_close(self):
        if self.toolbar and self.toolbar.winfo_exists():
            self.toolbar.destroy()

        if (
            hasattr(self, "canvas")
            and self.canvas
            and self.canvas.get_tk_widget().winfo_exists()
        ):
            self.canvas.get_tk_widget().destroy()

        if self.winfo_exists():
            self.destroy()
        if (
            hasattr(self, "canvas")
            and self.canvas
            and self.canvas.get_tk_widget().winfo_exists()
        ):
            self.canvas.mpl_disconnect(self.canvas._idgcf)
            self.canvas.mpl_disconnect(self.canvas._idgca)
            self.canvas.mpl_disconnect(self.canvas._idscroll)
            self.canvas.mpl_disconnect(self.canvas._idle)

    def create_plot(self):
        eq_type_to_func_pl = {
            "równanie liniowe": self.linear_eq_plot,
            "równanie kwadratowe": self.quadratic_eq_plot,
            "układ równań liniowych": self.system_of_eq_plot,
            "równanie nieliniowe, metoda Newtona - Raphsona": self.non_linear_eq_plot,
            "równanie nieliniowe, metoda siecznych": self.non_linear_eq_plot,
            "równanie nieliniowe, metoda bisekcji": self.non_linear_eq_plot,
            "równanie różniczkowe zwyczajne, pierwszy stopień": self.no_graph,
            "całka oznaczona, metoda trapezów": self.integral_eq_plot,
            "całka oznaczona, metoda Simpsona": self.integral_eq_plot,
            "całka oznaczona, niewłaściwa": self.integral_eq_plot,
            "pole pod wykresem": self.field_eq_plot,
            "objętość bryły ograniczonej funkcją": self.volume_eq_plot,
        }
        eq_type_to_func_en = {
            "linear equations": self.linear_eq_plot,
            "quadratic eq.": self.quadratic_eq_plot,
            "system of l. eq.": self.system_of_eq_plot,
            "non linear eq., Newton - Raphson method": self.non_linear_eq_plot,
            "non linear eq., secant method": self.non_linear_eq_plot,
            "non linear eq., bisection method": self.non_linear_eq_plot,
            "ODE, first order": self.no_graph,
            "definite integral, trapeze method": self.integral_eq_plot,
            "definite integral, Simpson method": self.integral_eq_plot,
            "improper, definite integral": self.integral_eq_plot,
            "field below function": self.field_eq_plot,
            "volume of solid under curve": self.volume_eq_plot,
        }
        if self.translator.language == "pl":
            eq_type_to_func = eq_type_to_func_pl
        else:
            eq_type_to_func = eq_type_to_func_en
        selected_func = eq_type_to_func.get(self.equation_type)
        if selected_func:
            selected_func()

    def change_form(self, label):
        label = label.replace("**2", "²")
        label = label.replace("**3", "³")
        label = label.replace("**4", "⁴")
        label = label.replace("**5", "⁵")
        return label

    def show_graph(self, formula, label, *args, **kwargs):
        if self.toolbar:
            self.toolbar.destroy()

        x_vals = np.linspace(-10, 10, 100)
        y_vals = formula(x_vals)

        self.ax.clear()
        self.ax.plot(x_vals, y_vals, label=label, color="blue", **kwargs)
        for arg in args:
            self.ax.axvline(arg, color="red", linewidth=2)
        self.ax.axhline(0, color="black", linewidth=0.5)
        self.ax.axvline(0, color="black", linewidth=0.5)
        self.ax.set_title(label)
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.legend().set_visible(False)

        self.toolbar = NavigationToolbar2Tk(
            FigureCanvasTkAgg(self.fig, master=self), self
        )
        self.toolbar.update()
        self.toolbar.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.fig.tight_layout()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.canvas.mpl_connect("scroll_event", self.on_scroll)

    def linear_eq_plot(self):
        self.equation_solver.solve_linear_equation(self.equation_content)
        formula = lambda x: -self.equation_solver.imag * x + self.equation_solver.real
        label = f"y = {-self.equation_solver.imag}x + {self.equation_solver.real}"
        self.show_graph(formula, label)

    def quadratic_eq_plot(self):
        self.equation_solver.solve_quadratic_equation(self.equation_content)
        formula = (
            lambda x: self.equation_solver.a * x * x
            + self.equation_solver.b * x
            + self.equation_solver.c
        )
        label = f"y = {self.equation_solver.a}x² + {self.equation_solver.b}x + {self.equation_solver.c}"
        self.show_graph(formula, label)

    def non_linear_eq_plot(self):
        func_str = self.equation_content
        func_str = func_str.replace(" ", "")
        func_str = func_str.replace("=0", "")

        x = sp.symbols("x")
        func = sp.sympify(func_str)
        func_str = self.change_form(func_str)
        label = f"y = {func_str}"
        f = sp.lambdify(x, func)

        self.show_graph(f, label)

    def integral_eq_plot(self):
        x = symbols("x")
        equation = self.equation_content.replace(" ", "").replace("dx", "")

        expr = lambdify(x, equation, "numpy")
        equation = self.change_form(equation)
        label = f"∫ {equation} dx [{self.a}; {self.b}]"
        self.show_graph(expr, label, int(self.a), int(self.b))

    def field_eq_plot(self):
        x = symbols("x")
        equation = self.equation_content.replace(" ", "")

        expr = lambdify(x, equation, "numpy")
        equation = self.change_form(equation)
        label = f" y = {equation} [{self.a}; {self.b}]"
        self.show_graph(expr, label, int(self.a), int(self.b))

    def system_of_eq_plot(self):
        equations = self.equation_content.replace(" ", "").split(";")
        if len(equations) > 2:
            self.no_graph
        else:
            self.equation_solver.solve_system_of_equation(self.equation_content)
            x1 = self.equation_solver.A[0][0]
            y1 = self.equation_solver.A[0][1]
            c1 = self.equation_solver.B[0]
            x2 = self.equation_solver.A[1][0]
            y2 = self.equation_solver.A[1][1]
            c2 = self.equation_solver.B[1]

            formula1 = lambda x: (c1 - x1 * x) / y1
            formula2 = lambda x: (c2 - x2 * x) / y2
            label = self.equation_content

        if self.toolbar:
            self.toolbar.destroy()

        x_vals = np.linspace(-10, 10, 100)
        y_vals_eq1 = formula1(x_vals)
        y_vals_eq2 = formula2(x_vals)

        self.ax.clear()
        self.ax.plot(x_vals, y_vals_eq1, label=label, color="blue")
        self.ax.plot(x_vals, y_vals_eq2, label=label, color="blue")

        self.ax.axhline(0, color="black", linewidth=0.5)
        self.ax.axvline(0, color="black", linewidth=0.5)
        self.ax.set_title(label)
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.legend().set_visible(False)

        self.toolbar = NavigationToolbar2Tk(
            FigureCanvasTkAgg(self.fig, master=self), self
        )
        self.toolbar.update()
        self.toolbar.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.fig.tight_layout()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.canvas.mpl_connect("scroll_event", self.on_scroll)

    def volume_eq_plot(self):
        x = symbols("x")
        equation = lambdify(x, self.equation_content, "numpy")
        
        if self.toolbar:
            self.toolbar.destroy()
            
        x_vals = np.linspace(-10, 10, 100)
        y_vals = equation(x_vals)
        z_vals = np.zeros_like(x_vals)
        
        for ax in self.fig.get_axes():
            self.fig.delaxes(ax)

        self.ax = self.fig.add_subplot(111, projection='3d')

        self.ax.plot(x_vals, y_vals, z_vals)

        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        
        label_eq = self.change_form(self.equation_content)
        self.ax.set_title(f"{label_eq}, [{self.a}; {self.b}]")



        if not self.toolbar:
            self.toolbar = NavigationToolbar2Tk(
                FigureCanvasTkAgg(self.fig, master=self), self
            )
            self.toolbar.update()
            self.toolbar.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            self.fig.tight_layout()

        if not hasattr(self, 'canvas'):
            self.canvas = FigureCanvasTkAgg(self.fig, master=self)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.canvas.mpl_connect("scroll_event", self.on_scroll)
        
        
    def on_scroll(self, event):
        if event.button == "down":
            self.ax.set_xlim(self.ax.get_xlim()[0] * 1.1, self.ax.get_xlim()[1] * 1.1)
            self.ax.set_ylim(self.ax.get_ylim()[0] * 1.1, self.ax.get_ylim()[1] * 1.1)
        elif event.button == "up":
            self.ax.set_xlim(self.ax.get_xlim()[0] / 1.1, self.ax.get_xlim()[1] / 1.1)
            self.ax.set_ylim(self.ax.get_ylim()[0] / 1.1, self.ax.get_ylim()[1] / 1.1)

        self.canvas.draw()

    def no_graph(self):
        text = "is_graph"
        translated_text = self.translator.translate(text)
        ctk.CTkLabel(
            self, text=translated_text, font=(FONT, 20), text_color=COLORS["BLACK"]
        ).place(relx=0.20, rely=0.4)
