import customtkinter
import tkinter

root_tk = tkinter.Tk()
root_tk.geometry("500x300")
root_tk.title("kalkulatorek")

def calculate_something(a, b):
    wynik = a + b
    label = customtkinter.CTkLabel(master=root_tk, text = str(wynik), width=120, height=25, corner_radius=8)
    label.place(relx=0.4, rely=0.9)
    
def main():
    entry1 = customtkinter.CTkEntry(master = root_tk, width = 120, height=25, corner_radius=10)
    entry1.place(relx=0.1, rely=0.1)    

    entry2 = customtkinter.CTkEntry(master = root_tk, width = 120, height=25, corner_radius=10)
    entry2.place(relx=0.65, rely=0.1)    

    a = entry1.get()
    b = entry2.get()

    button = customtkinter.CTkButton(master = root_tk, text = "dodawanko", corner_radius=10, command=lambda: calculate_something(int(entry1.get()), int(entry2.get())))
    button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    root_tk.mainloop()
    
main()