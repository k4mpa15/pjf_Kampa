import tkinter as tk
import customtkinter as ctk
from calculator_app_gui import CalculatorApp

#from PIL import Image, ImageTk

def main():
    root_tk = ctk.CTk()
    app = CalculatorApp(root_tk)
    root_tk.mainloop()


if __name__ == "__main__":
    main()
