import customtkinter
import tkinter

root_tk = tkinter.Tk()
root_tk.geometry("500x300")
root_tk.title("kalkulatorek")

def add(a, b):
    wynik = a + b
    outcome_label = customtkinter.CTkLabel(master=root_tk, text = str(wynik), width=120, height=25, corner_radius=8)
    outcome_label.place(relx=0.4, rely=0.9)
    
def sub(a, b):
    wynik = a - b
    outcome_label = customtkinter.CTkLabel(master=root_tk, text = str(wynik), width=120, height=25, corner_radius=8)
    outcome_label.place(relx=0.4, rely=0.9)
    
def main():
    number1_entry = customtkinter.CTkEntry(master = root_tk, width = 120, height=25, corner_radius=10)
    number1_entry.place(relx=0.1, rely=0.1)    

    number2_entry = customtkinter.CTkEntry(master = root_tk, width = 120, height=25, corner_radius=10)
    number2_entry.place(relx=0.65, rely=0.1)    

    adding_button = customtkinter.CTkButton(master = root_tk, text = "dodawanko", corner_radius=10, 
                                            command = lambda: add(int(number1_entry.get()), int(number2_entry.get())))
    adding_button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
    
    substraction_button = customtkinter.CTkButton(master = root_tk, text = "odejmowanko", corner_radius=10, 
                                            command = lambda: sub(int(number1_entry.get()), int(number2_entry.get())))
    substraction_button.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)
    
    root_tk.mainloop()
    
main()