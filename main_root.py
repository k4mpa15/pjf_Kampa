import tkinter as tk
import customtkinter
from tkinter import filedialog

# from PIL import Image, ImageTk

COLORS = {
    "MAIN_BUTTONS_COLOR": "#1B36CD",
    "BACKGROUND_COLOR": "#BAC0E4",
    "LIGHT_ENTRY_COLOR": "#B7AAD2",
    "TEXT_GREY_COLOR": "#5A5A5A",
}

FONT = "Century Gothic"


class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")
        self.label = customtkinter.CTkLabel(
            self,
            text="Wybierz plik ze zdjęciem równania",
            bg_color=COLORS["BACKGROUND_COLOR"],
            fg_color=COLORS["BACKGROUND_COLOR"],
            corner_radius=10,
            text_color="black",
        )
        self.label.pack(padx=20, pady=20)
        self.create_widgets()
        self.master.resizable(True, True)
        self.configure(fg_color=COLORS["BACKGROUND_COLOR"])
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.title("Wybór zdjęcia")

    def on_close(self):
        self.destroy()

    def create_widgets(self):
        load_button = customtkinter.CTkButton(
            self,
            text="Wczytaj plik",
            command=self.load_file,
            corner_radius=10,
            bg_color=COLORS["BACKGROUND_COLOR"],
        )
        load_button.pack(pady=10)

    def load_file(self):
        file_path = filedialog.askopenfilename(
            title="Wybierz plik",
            filetypes=[("Pliki obrazów", "*.png;*.jpg;*.jpeg;*.gif")],
        )
        if file_path:
            print(f"Wczytano plik: {file_path}")


class CalculatorApp(customtkinter.CTk):
    def __init__(self, master, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.master = master
        self.master.title("Kalkulator równań")
        self.master.geometry("1200x700")
        self.master.resizable(True, True)
        self.master.configure(background=COLORS["BACKGROUND_COLOR"])
        self.toplevel_window = None
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        self.create_widgets()

    def on_close(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            pass
        else:
            self.toplevel_window.destroy()

        self.master.destroy()
        self.master.quit()

    def create_widgets(self):
        self.create_label(
            "Kalkulator równań",
            0.0,
            0.0,
            961,
            90,
            (FONT, 28),
            "white",
            COLORS["BACKGROUND_COLOR"],
            COLORS["MAIN_BUTTONS_COLOR"],
            5000,
            "w",
        )

        self.create_option_button(
            "PL EN",
            0.8,
            0.0,
            120,
            COLORS["MAIN_BUTTONS_COLOR"],
            COLORS["MAIN_BUTTONS_COLOR"],
            "white",
        )

        # img_history = customtkinter.CTkFrame(Image.open("history_icon.png"), size=(26, 26))
        # history_button = customtkinter.CTkButton(master = root_tk, image = img_history)
        # history_button.place(relx = 0.95, rely = 0.0)

        # img_camera = customtkinter.CTkFrame(Image.open("camera_icon.jpg"), size=(26, 26))
        # camera_button = customtkinter.CTkButton(master = root_tk, image = img_camera)
        # camera_button.place(relx = 0.95, rely = 0.0)

        # img_export = customtkinter.CTkFrame(Image.open("export_icon.jpg"), size=(26, 26))
        # export_button = customtkinter.CTkButton(master = root_tk, image = img)
        # export_button.place(relx = 0.95, rely = 0.0)

        eq_types = ["Wybierz typ", "1", "2", "3"]
        self.create_combobox(
            eq_types,
            150,
            COLORS["BACKGROUND_COLOR"],
            COLORS["MAIN_BUTTONS_COLOR"],
            COLORS["MAIN_BUTTONS_COLOR"],
            (FONT, 14),
            0.084,
            0.2,
            (FONT, 14),
            COLORS["MAIN_BUTTONS_COLOR"],
        )

        self.create_entry(0.084, 0.33, 600, 100)

        self.create_main_button("Rozwiąż", 0.15, 0.6, 120, 32, tk.CENTER)

        self.create_main_button("Rozwiąż krok po kroku", 0.385, 0.6, 250, 32, tk.CENTER)
        self.create_main_button(
            "Pokaż graficzne przedstawienie", 0.7, 0.6, 260, 32, tk.CENTER
        )

        self.create_label(
            "Rozwiązanie równania... ",
            0.085,
            0.7,
            500,
            100,
            (FONT, 20),
            COLORS["TEXT_GREY_COLOR"],
            COLORS["BACKGROUND_COLOR"],
            COLORS["LIGHT_ENTRY_COLOR"],
            10,
            None,
        )

        self.create_option_button(
            "Materiały pomocnicze",
            0.085,
            0.9,
            180,
            COLORS["BACKGROUND_COLOR"],
            COLORS["BACKGROUND_COLOR"],
            "black",
        )

        self.create_label(
            "app version 1.0",
            0.43,
            0.95,
            120,
            20,
            None,
            COLORS["TEXT_GREY_COLOR"],
            COLORS["BACKGROUND_COLOR"],
            COLORS["BACKGROUND_COLOR"],
            0,
            None,
        )

        self.create_image_button(
            0.65, 0.33, 6, lambda: self.display_scan_eq_opt()
        )  # skanuj zdj
        self.create_image_button(0.9, 0.0, 6, None)  # historia
        self.create_image_button(0.52, 0.7, 6, None)  # export

    def display_scan_eq_opt(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(self)
        else:
            self.toplevel_window.focus()

    def create_image_button(self, x, y, wid, command):
        return customtkinter.CTkButton(master=self.master, command=command).place(
            relx=x, rely=y
        )

    def create_option_button(self, text, x, y, wid, bg_color, fg_color, text_color):
        return customtkinter.CTkButton(
            master=self.master,
            text=text,
            width=wid,
            border_color="white",
            bg_color=bg_color,
            fg_color=fg_color,
            hover_color="#B7AAD2",
            font=(FONT, 13),
            text_color=text_color,
        ).place(relx=x, rely=y)

    def create_main_button(self, text, x, y, wid, hei, anchor, command=None):
        return customtkinter.CTkButton(
            fg_color=COLORS["MAIN_BUTTONS_COLOR"],
            bg_color=COLORS["BACKGROUND_COLOR"],
            master=self.master,
            text=text,
            corner_radius=10,
            width=wid,
            font=(FONT, 14),
            height=hei,
            text_color="#AEC9F2",
            hover_color="#596CD0",
        ).place(relx=x, rely=y, anchor=anchor)

    def create_label(
        self,
        text,
        x,
        y,
        wid,
        hei,
        text_font,
        text_color,
        bg_color,
        fg_color,
        corner_radius,
        anchor,
    ):
        customtkinter.CTkLabel(
            master=self.master,
            text=text,
            width=wid,
            height=hei,
            corner_radius=corner_radius,
            font=text_font,
            bg_color=bg_color,
            text_color=text_color,
            fg_color=fg_color,
            anchor=anchor,
        ).place(relx=x, rely=y)

    def create_entry(self, x, y, wid, hei):
        return customtkinter.CTkEntry(
            master=self.master,
            width=wid,
            height=hei,
            font=(FONT, 20),
            corner_radius=10,
            fg_color=COLORS["LIGHT_ENTRY_COLOR"],
            bg_color=COLORS["BACKGROUND_COLOR"],
            placeholder_text="Wpisz równanie",
            placeholder_text_color=COLORS["TEXT_GREY_COLOR"],
        ).place(relx=x, rely=y)

    def create_combobox(
        self,
        values,
        wid,
        bg_color,
        fg_color,
        border_color,
        font,
        x,
        y,
        dropdown_font,
        button_color,
    ):
        combobox = customtkinter.CTkComboBox(
            master=self.master,
            values=values,
            width=wid,
            corner_radius=10,
            bg_color=bg_color,
            fg_color=fg_color,
            border_color=border_color,
            font=font,
            dropdown_font=dropdown_font,
            button_color=button_color,
        ).place(relx=x, rely=y)
        return combobox


def main():
    root_tk = tk.Tk()
    app = CalculatorApp(root_tk)
    root_tk.mainloop()


if __name__ == "__main__":
    main()
