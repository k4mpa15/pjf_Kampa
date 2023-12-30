import openpyxl
from pylatex import Document, Section, Math
import customtkinter as ctk


class FileExporter:
    def export_to_excel(self, result):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws["A1"] = "Wyniki równania:"
        ws["A2"] = result

        file_path = self.ask_save_file(
            defaultextension=".xlsx",
            filetypes=[("Pliki Excela", "*.xlsx")],
            title="Zapisz plik Excela",
        )
        if file_path:
            wb.save(file_path)
            print(f"Plik Excela został zapisany jako: {file_path}")

    def export_to_latex(self, result):
        doc = Document()
        with doc.create(Section("Wyniki równania")):
            with doc.create(Math()):
                doc.append(result)

        file_path = self.ask_save_file(
            defaultextension=".tex",
            filetypes=[("Pliki LaTeX", "*.tex")],
            title="Zapisz plik LaTeX",
        )
        if file_path:
            doc.generate_tex(file_path)
            print(f"Plik LaTeX został zapisany jako: {file_path}")

    def ask_save_file(self, defaultextension, filetypes, title):
        return ctk.filedialog.asksaveasfilename(
            defaultextension=defaultextension,
            filetypes=filetypes,
            title=title,
        )
