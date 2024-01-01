import customtkinter as ctk

from gui.calculator_app_gui import CalculatorApp


def main():
    root_tk = ctk.CTk()
    app = CalculatorApp(root_tk)
    root_tk.mainloop()


if __name__ == "__main__":
    main()
