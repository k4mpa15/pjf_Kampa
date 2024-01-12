import webbrowser


class HelpMaterials:
    def __init__(self, translator) -> None:
        self.translator = translator

    def open_help_materials(self, eq_type):
        self.url_to_help_pl = {
            "równanie liniowe": "https://pl.wikipedia.org/wiki/Równanie_liniowe",
            "równanie kwadratowe": "https://pl.wikipedia.org/wiki/Równanie_kwadratowe",
            "układ równań liniowych": "https://pl.wikipedia.org/wiki/Układ_równań_liniowych",
            "równanie nieliniowe, metoda Newtona - Raphsona": "https://pl.wikipedia.org/wiki/Metoda_Newtona",
            "równanie nieliniowe, metoda siecznych": "https://pl.wikipedia.org/wiki/Metoda_siecznych",
            "równanie nieliniowe, metoda bisekcji": "https://pl.wikipedia.org/wiki/Metoda_równego_podziału",
            "równanie różniczkowe zwyczajne, pierwszy stopień": "https://pl.wikipedia.org/wiki/Równanie_różniczkowe_zwyczajne",
            "równanie różniczkowe zwyczajne, drugi stopień": "https://pl.wikipedia.org/wiki/Równanie_różniczkowe_zwyczajne",
            "całka oznaczona, metoda trapezów": "https://pl.wikipedia.org/wiki/Całkowanie_numeryczne",
            "całka oznaczona, metoda Simpsona": "https://pl.wikipedia.org/wiki/Całkowanie_numeryczne",
            "całka oznaczona, niewłaściwa": "https://pl.wikipedia.org/wiki/Całka",
            "pole pod wykresem": "https://blog.etrapez.pl/calki-nieoznaczone-i-pola-obszarow/",
            "objętość bryły ograniczonej funkcją": "https://www.matemaks.pl/objetosc-bryly-ograniczonej-powierzchniami.html",
        }
        self.url_to_help_en = {
            "linear equations": "https://en.wikipedia.org/wiki/Linear_equation",
            "quadratic equation": "https://en.wikipedia.org/wiki/Quadratic_equation",
            "system of l. equations": "https://en.wikipedia.org/wiki/Linear_system",
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
        if self.translator.language == "pl":
            self.url_to_help = self.url_to_help_pl
        else:
            self.url_to_help = self.url_to_help_en
        url = self.url_to_help.get(eq_type)
        webbrowser.open(url, new=0, autoraise=True)
