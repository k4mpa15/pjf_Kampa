import json

import customtkinter as ctk
from PIL import Image

with open("gui/colors.json") as f:
    colors_data = json.load(f)

COLORS = colors_data.get("COLORS", {})


class TopLevelInstructions(ctk.CTkToplevel):
    def __init__(self, translator ,eq_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("600x350")
        self.translator = translator
        self.eq_type = eq_type
        self.create_widgets()
        self.resizable(True, True)
        self.configure(fg_color=COLORS["BACKGROUND_COLOR"])
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.title("Instrukcje")
        self.grab_set()

    def on_close(self):
        self.destroy()
        
    def get_image(self):
        self.images_to_help_pl = {
            "równanie liniowe": "gui\instructions\instructions_linear_eq.png",
            #"równanie kwadratowe": "https://pl.wikipedia.org/wiki/Równanie_kwadratowe",
            #"układ równań liniowych": "https://pl.wikipedia.org/wiki/Układ_równań_liniowych",
            #"układ równań nieliniowych": "https://pl.wikipedia.org/wiki/Układ_nieliniowy",
            #"równanie nieliniowe, metoda Newtona - Raphsona": "https://pl.wikipedia.org/wiki/Metoda_Newtona",
            #"równanie nieliniowe, metoda siecznych": "https://pl.wikipedia.org/wiki/Metoda_siecznych",
            #"równanie nieliniowe, metoda bisekcji": "https://pl.wikipedia.org/wiki/Metoda_równego_podziału",
            #"równanie różniczkowe zwyczajne, pierwszy stopień": "https://pl.wikipedia.org/wiki/Równanie_różniczkowe_zwyczajne",
            #"równanie różniczkowe zwyczajne, drugi stopień": "https://pl.wikipedia.org/wiki/Równanie_różniczkowe_zwyczajne",
            #"całka oznaczona, metoda trapezów": "https://pl.wikipedia.org/wiki/Całkowanie_numeryczne",
            #"całka oznaczona, metoda Simpsona": "https://pl.wikipedia.org/wiki/Całkowanie_numeryczne",
            #"całka oznaczona, niewłaściwa": "https://pl.wikipedia.org/wiki/Całka",
            #"pole pod wykresem": "https://blog.etrapez.pl/calki-nieoznaczone-i-pola-obszarow/",
            #"objętość bryły ograniczonej funkcją": "https://www.matemaks.pl/objetosc-bryly-ograniczonej-powierzchniami.html",
        }
        self.images_to_help_eng = {
            "linear equations": "https://en.wikipedia.org/wiki/Linear_equation",
            "quadratic equation": "https://en.wikipedia.org/wiki/Quadratic_equation",
            "system of l. equations": "https://en.wikipedia.org/wiki/Linear_system",
            "system of non linear equations": "https://en.wikipedia.org/wiki/Nonlinear_control",
            "non linear eq., Newton - Raphson method": "https://en.wikipedia.org/wiki/Newton%27s_method",
            "non linear eq., secant method": "https://en.wikipedia.org/wiki/Secant_method",
            "non linear eq., bisection method": "https://en.wikipedia.org/wiki/Bisection_method",
            "ODE, first order": "https://en.wikipedia.org/wiki/Ordinary_differential_equation",
            "ODE, second order": "https://en.wikipedia.org/wiki/Ordinary_differential_equation",
            "definite integral, trapeze method": "https://en.wikipedia.org/wiki/Numerical_integration",
            "definite integral, Simpson method": "https://en.wikipedia.org/wiki/Numerical_integration",
            "improper, definite integral": "https://en.wikipedia.org/wiki/Integral",
            "field below function": "https://revisionmaths.com/advanced-level-maths-revision/pure-maths/calculus/area-under-curve",
            "volume of solid under curve": "https://revisionmaths.com/advanced-level-maths-revision/pure-maths/calculus/volumes-revolution",
        }
        try:
            if self.translator.language == "pl":
                self.images_to_help = self.images_to_help_pl
            else:
                self.images_to_help = self.images_to_help_eng
            img = self.images_to_help.get(self.eq_type)
            return img
        except TypeError:
            return
    
    def create_widgets(self):
        img = self.get_image()
        my_image = ctk.CTkImage(
            light_image=Image.open(img),
            dark_image=None,
            size=(600, 500),
        )

        ctk.CTkLabel(self, image=my_image, text="", anchor = "center").place(relx=0.0, rely=0.0)
