import tkinter
import customtkinter

# from PIL import Image, ImageTk


# canvas = tkinter.Canvas(root_tk, width=900, height=600)
# canvas.pack()
#
#
# pierwsza_czesc = canvas.create_rectangle(0, 0, 900, 100, fill = '#1B36CD', outline = "#1B36CD")
# druga_czesc = canvas.create_rectangle(0, 100, 900, 600, fill='#BAC0E4', outline='#BAC0E4')

COLORS = {
    "MAIN_BUTTONS_COLOR": "#1B36CD",
    "BACKGROUND_COLOR": "#BAC0E4",
    "LIGHT_ENTRY_COLOR": "#B7AAD2",
}


def create_option_button(master, text, x, y, wid, command=None):
    return customtkinter.CTkButton(
        master=master,
        text=text,
        width=wid,
        border_color="white",
        bg_color=COLORS["BACKGROUND_COLOR"],
        fg_color=COLORS["BACKGROUND_COLOR"],
        hover_color="#B7AAD2",
    ).place(relx=x, rely=y)


def create_main_button(master, text, x, y, wid, hei, anchor, command=None):
    return customtkinter.CTkButton(
        fg_color=COLORS["MAIN_BUTTONS_COLOR"],
        bg_color=COLORS["BACKGROUND_COLOR"],
        master=master,
        text=text,
        corner_radius=10,
        width=wid,
        height=hei,
        text_color="#AEC9F2",
        hover_color="#596CD0",
    ).place(relx=x, rely=y, anchor=anchor)


def create_label(master, text, x, y, wid, hei, text_font, text_color, bg_color):
    customtkinter.CTkLabel(
        master=master,
        text=text,
        width=wid,
        height=hei,
        corner_radius=8,
        text_font=text_font,
        bg_color=bg_color,
        text_color=text_color,
    ).place(relx=x, rely=y)


def create_entry(master, x, y, wid, hei):
    return customtkinter.CTkEntry(
        master=master,
        width=wid,
        height=hei,
        corner_radius=10,
        fg_color=COLORS["LIGHT_ENTRY_COLOR"],
        bg_color=COLORS["BACKGROUND_COLOR"],
    ).place(relx=x, rely=y)


def main():
    root_tk = tkinter.Tk()
    root_tk.title("Kalkulator równań")
    root_tk.geometry("900x600")
    root_tk.resizable(True, True)
    root_tk.configure(background=COLORS["BACKGROUND_COLOR"])

    #combobox = customtkinter.CTkComboBox(master=root_tk,
    #                                 values=["option 1", "option 2"])
    #combobox.pack(padx=20, pady=10)
    #combobox.set("option 2")  # set initial value


    create_label(
        root_tk,
        "Kalkulator równań",
        0.05,
        0.05,
        300,
        50,
        ("Century Gothic", 20),
        "black",
        COLORS["BACKGROUND_COLOR"],
    )

    create_option_button(root_tk, "PL EN", 0.8, 0.0, 120)

    # img_history = customtkinter.CTkFrame(Image.open("history_icon.png"), size=(26, 26))
    # history_button = customtkinter.CTkButton(master = root_tk, image = img_history)
    # history_button.place(relx = 0.95, rely = 0.0)
    
    # img_camera = customtkinter.CTkFrame(Image.open("camera_icon.jpg"), size=(26, 26))
    # camera_button = customtkinter.CTkButton(master = root_tk, image = img_camera)
    # camera_button.place(relx = 0.95, rely = 0.0)
    
    # img_export = customtkinter.CTkFrame(Image.open("export_icon.jpg"), size=(26, 26))
    # export_button = customtkinter.CTkButton(master = root_tk, image = img)
    # export_button.place(relx = 0.95, rely = 0.0)

    create_main_button(root_tk, "Wybierz typ", 0.084, 0.2, 150, 40, None)

    create_entry(root_tk, 0.084, 0.33, 600, 100)

    create_main_button(root_tk, "Rozwiąż", 0.15, 0.6, 120, 32, tkinter.CENTER)

    create_main_button(
        root_tk, "Rozwiąż krok po kroku", 0.385, 0.6, 250, 32, tkinter.CENTER
    )
    create_main_button(
        root_tk, "Pokaż graficzne przedstawienie", 0.7, 0.6, 260, 32, tkinter.CENTER
    )

    create_label(
        root_tk,
        "Rozwiązanie równania... ",
        0.085,
        0.7,
        500,
        100,
        None,
        "grey",
        COLORS["LIGHT_ENTRY_COLOR"],
    )

    create_option_button(root_tk, "Materiały pomocnicze", 0.085, 0.9, 180)

    create_label(
        root_tk, "app version 1.0", 0.43, 0.95, 120, 20, None, "grey", COLORS["BACKGROUND_COLOR"])

    root_tk.mainloop()


main()
