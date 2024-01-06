import customtkinter as ctk

from gui.calculator_app_gui import CalculatorApp
from options.language_manager import LanguageManager


def main():
    language_manager = LanguageManager()
    root_tk = ctk.CTk()
    CalculatorApp(root_tk, language_manager)
    root_tk.mainloop()


if __name__ == "__main__":
    main()
