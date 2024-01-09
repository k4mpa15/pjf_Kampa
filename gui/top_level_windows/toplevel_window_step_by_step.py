import json
import math
import os

import customtkinter as ctk
from PIL import Image

from eq_solvers.common_eq_solv import EquationSolver
from options.translator import Translator

with open("gui/colors.json") as f:
    colors_data = json.load(f)

COLORS = colors_data.get("COLORS", {})
FONT = "Century Gothic"


class TopLevelWindowStepByStep(ctk.CTkToplevel):
    def __init__(self, language_manager, entry_content, type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("600x400")
        self.entry_content = entry_content
        self.type = type
        self.language_manager = language_manager
        self.translator = Translator(self.language_manager)
        self.equation_solver = EquationSolver()
        self.solve_eq()
        self.create_widgets()
        self.index_to_update = 0
        self.configure(fg_color=COLORS["BACKGROUND_COLOR"])
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.title("Rozwiązanie krok po kroku")
        self.grab_set()
        self.resizable(True, True)

    def on_close(self):
        self.destroy()

    def solve_eq(self):
        if self.type == "równanie kwadratowe" or self.type == "quadratic eq.":
            self.equation_solver.solve_quadratic_equation(self.entry_content)

        if self.type == "równanie liniowe" or self.type == "linear equations":
            self.equation_solver.solve_linear_equation(self.entry_content)

        elif self.type == "układ równań liniowych" or self.type == "system of l. eq.":
            self.equation_solver.solve_system_of_equation(self.entry_content)

    def create_label_with_step(self, text, font):
        return ctk.CTkLabel(
            master=self, text=text, text_color=COLORS["BLACK"], font=font
        )

    def update_label(self):
        if self.type == "równanie kwadratowe" or self.type == "quadratic eq.":
            if self.equation_solver.d < 0:
                new_text = self.dm0_labels_text[self.current_index]
                self.dm0_labels[self.current_index].configure(text=new_text)
                self.current_index = (self.current_index + 1) % len(self.dm0_labels)
                if self.current_index == 0:
                    self.no_next_button()

            if self.equation_solver.d == 0:
                new_text = self.d0_labels_text[self.current_index]
                self.d0_labels[self.current_index].configure(text=new_text)
                self.current_index = (self.current_index + 1) % len(self.d0_labels)
                if self.current_index == 0:
                    self.no_next_button()

            if self.equation_solver.d > 0:
                new_text = self.dw0_labels_text[self.current_index]
                self.dw0_labels[self.current_index].configure(text=new_text)
                self.current_index = (self.current_index + 1) % len(self.dw0_labels)
                if self.current_index == 0:
                    self.no_next_button()

        elif self.type == "równanie liniowe" or self.type == "linear equations":
            new_text = self.labels_text[self.current_index]
            self.labels[self.current_index].configure(text=new_text)
            self.current_index = (self.current_index + 1) % len(self.labels_text)
            if self.current_index == 0:
                self.no_next_button()
        elif self.type == "układ równań liniowych" or self.type == "system of l. eq.":
            new_text = self.sys_labels_text[self.current_index]
            self.sys_labels[self.current_index].configure(text=new_text)
            self.current_index = (self.current_index + 1) % len(self.sys_labels_text)
            if self.current_index == 0:
                self.no_next_button()

    def no_next_button(self):
        img_no_next = ctk.CTkImage(
            Image.open(os.path.join(self.image_path, "no_next.png"))
        )
        self.next_button.configure(image=img_no_next)

    def create_widgets(self):
        self.image_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "icons"
        )

        img_n = ctk.CTkImage(Image.open(os.path.join(self.image_path, "next.png")))

        self.next_button = ctk.CTkButton(
            master=self,
            image=img_n,
            command=lambda: self.update_label(),
            text="",
            width=14,
            height=14,
            bg_color=COLORS["BACKGROUND_COLOR"],
            fg_color=COLORS["BACKGROUND_COLOR"],
            hover_color=COLORS["BACKGROUND_COLOR"],
        )
        self.next_button.place(relx=0.9, rely=0.9)
        self.current_index = 0
        if self.type == "równanie liniowe" or self.type == "linear equations":
            eq = self.create_label_with_step(
                self.entry_content,
                (FONT, 20),
            )
            eq.place(relx=0.4, rely=0.05)
            self.labels = []
            self.labels_text = [
                f"1.    {self.equation_solver.s_to_show}",
                f"2.    {-self.equation_solver.imag} x - {-self.equation_solver.real} = 0",
                f"3.    {-self.equation_solver.imag} x = {-self.equation_solver.real}",
                f"4.    x = {-self.equation_solver.real} / {-self.equation_solver.imag}",
                f"5.        x = {self.equation_solver.x}",
            ]
            step1 = self.create_label_with_step(
                "",
                (FONT, 16),
            )
            self.labels.append(step1)
            step1.place(relx=0.05, rely=0.15)

            step2 = self.create_label_with_step(
                "",
                (FONT, 16),
            )
            self.labels.append(step2)
            step2.place(relx=0.05, rely=0.22)

            step3 = self.create_label_with_step("", (FONT, 16))
            self.labels.append(step3)
            step3.place(relx=0.05, rely=0.29)

            step4 = self.create_label_with_step(
                "",
                (FONT, 16),
            )
            self.labels.append(step4)
            step4.place(relx=0.05, rely=0.36)

            step5 = self.create_label_with_step("", (FONT, 16))
            self.labels.append(step5)
            step5.place(relx=0.05, rely=0.50)

        if self.type == "równanie kwadratowe" or self.type == "quadratic eq.":
            eq = self.create_label_with_step(
                f"{self.equation_solver.a}x² + {self.equation_solver.b}x + {self.equation_solver.c} = 0",
                (FONT, 20),
            )
            eq.place(relx=0.4, rely=0.05)
            self.dm0_labels = []
            self.d0_labels = []
            self.dw0_labels = []
            self.dm0_labels_text = [
                f"1.    a = {self.equation_solver.a}, b = {self.equation_solver.b}, c = {self.equation_solver.c}",
                f"2.    △ = b² - 4ac        >>>    {self.equation_solver.b}² - 4· {self.equation_solver.a}· {self.equation_solver.c}",
                f"3.    △ = {self.equation_solver.d}",
                "4.    △ < 0        >>>  x ∉ R",
            ]

            step1 = self.create_label_with_step(
                "",
                (FONT, 16),
            )
            self.dm0_labels.append(step1)
            self.d0_labels.append(step1)
            self.dw0_labels.append(step1)
            step1.place(relx=0.05, rely=0.15)
            step2 = self.create_label_with_step(
                "",
                (FONT, 16),
            )
            self.dm0_labels.append(step2)
            self.d0_labels.append(step2)
            self.dw0_labels.append(step2)
            step2.place(relx=0.05, rely=0.22)
            step3 = self.create_label_with_step("", (FONT, 16))
            self.dm0_labels.append(step3)
            self.d0_labels.append(step3)
            self.dw0_labels.append(step3)
            step3.place(relx=0.05, rely=0.29)

            if self.equation_solver.d < 0:
                step4m0 = self.create_label_with_step("", (FONT, 16))
                self.dm0_labels.append(step4m0)
                step4m0.place(relx=0.05, rely=0.43)

            if self.equation_solver.d == 0:
                self.d0_labels_text = [
                    f"1.    a = {self.equation_solver.a}, b = {self.equation_solver.b}, c = {self.equation_solver.c}",
                    f"2.    △ = b² - 4ac        >>>    {self.equation_solver.b}² - 4· {self.equation_solver.a}· {self.equation_solver.c}",
                    f"3.    △ = {self.equation_solver.d}",
                    f"4.    x = -b / 2a        >>>    x = -{self.equation_solver.b}/ (2· {self.equation_solver.a})",
                    f"5.        x = {round(self.equation_solver.sol)}",
                ]
                step4_0 = self.create_label_with_step(
                    "",
                    (FONT, 16),
                )
                self.d0_labels.append(step4_0)
                step4_0.place(relx=0.05, rely=0.37)
                step5_0 = self.create_label_with_step("", (FONT, 16))
                self.d0_labels.append(step5_0)
                step5_0.place(relx=0.05, rely=0.50)

            if self.equation_solver.d > 0:
                self.dw0_labels_text = [
                    f"1.    a = {self.equation_solver.a}, b = {self.equation_solver.b}, c = {self.equation_solver.c}",
                    f"2.    △ = b² - 4ac        >>>    {self.equation_solver.b}² - 4· {self.equation_solver.a}· {self.equation_solver.c}",
                    f"3.    △ = {self.equation_solver.d}",
                    f"4.    x₁ = (-b + √△) / 2a        >>>    x₁ = (-{self.equation_solver.b}+√{round(math.sqrt(self.equation_solver.d),2)}) / (2· {self.equation_solver.a})\n",
                    f"5.    x₂ = (-b - √△) / 2a        >>>    x₂ = (-{self.equation_solver.b}-√{round(math.sqrt(self.equation_solver.d),2)}) / (2· {self.equation_solver.a})\n",
                    f"6.        x₁ =     {round(self.equation_solver.sol1,2)},   x₂ =     {round(self.equation_solver.sol2, 2)}\n",
                ]
                step4w0 = self.create_label_with_step(
                    "",
                    (FONT, 16),
                )
                self.dw0_labels.append(step4w0)
                step4w0.place(relx=0.05, rely=0.37)
                step5w0 = self.create_label_with_step(
                    "",
                    (FONT, 16),
                )
                self.dw0_labels.append(step5w0)
                step5w0.place(relx=0.05, rely=0.44)
                step6w0 = self.create_label_with_step(
                    "",
                    (FONT, 16),
                )
                self.dw0_labels.append(step6w0)
                step6w0.place(relx=0.05, rely=0.57)

        if self.type == "układ równań liniowych" or self.type == "system of l. eq.":
            eq = self.create_label_with_step(
                self.entry_content,
                (FONT, 20),
            )
            eq.place(relx=0.1, rely=0.05)
            self.sys_labels = []
            self.sys_labels_text = [
                "1.   A ⋅ x = B",
                "2.   A = ",
                f"{self.equation_solver.A}",
                f"3.   B =      {self.equation_solver.B}",
                "4.   x = A⁻¹ ⋅ B",
                "5.   A⁻¹ =  ",
                f"{self.equation_solver.A_odw}",
                f"6.        x = {self.equation_solver.x}",
            ]
            step1 = self.create_label_with_step(
                "",
                (FONT, 16),
            )
            self.sys_labels.append(step1)
            step1.place(relx=0.05, rely=0.20)

            step2 = self.create_label_with_step(
                "",
                (FONT, 16),
            )
            self.sys_labels.append(step2)
            step2.place(relx=0.05, rely=0.27)

            step2_1 = self.create_label_with_step(
                "",
                (FONT, 16),
            )
            self.sys_labels.append(step2_1)
            step2_1.place(relx=0.05, rely=0.32)

            step3 = self.create_label_with_step("", (FONT, 16))
            self.sys_labels.append(step3)
            step3.place(relx=0.05, rely=0.47)

            step4 = self.create_label_with_step(
                "",
                (FONT, 16),
            )
            self.sys_labels.append(step4)
            step4.place(relx=0.05, rely=0.54)

            step5 = self.create_label_with_step("", (FONT, 16))
            self.sys_labels.append(step5)
            step5.place(relx=0.05, rely=0.61)

            step5_1 = self.create_label_with_step(
                "",
                (FONT, 16),
            )
            self.sys_labels.append(step5_1)
            step5_1.place(relx=0.05, rely=0.66)

            step6 = self.create_label_with_step("", (FONT, 16))
            self.sys_labels.append(step6)
            step6.place(relx=0.05, rely=0.83)
