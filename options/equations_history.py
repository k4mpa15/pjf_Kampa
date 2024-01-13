from datetime import datetime

from options.translator import Translator


class EquationHistory:
    def __init__(self, language_manager):
        self.language_manager = language_manager
        self.history_file_path = "eq_history.txt"
        self.translator = Translator(self.language_manager)

    def add_equation(self, equation, result):
        time = datetime.now()
        formatted_time = time.strftime("%d/%m/%Y; %H:%M:%S")
        with open(self.history_file_path, "a") as f:
            f.write(f"{equation} > > > {result},   [{formatted_time}]\n")

    def get_history(self):
        with open(self.history_file_path, "r") as f:
            history_content = f.read()
        return history_content

    def get_all_equations_with_timestamp(self):
        with open(self.history_file_path, "r") as f:
            lines = f.readlines()

        equations = []
        for line in lines:
            equation, result, timestamp = self.parse_history_line(line)
            equations.append((equation, result, timestamp))

        return equations

    def parse_history_line(self, line):
        parts = line.strip().rsplit("> > >", 1)

        if len(parts) == 2:
            equation = parts[0].strip()
            result, timestamp = [part.strip() for part in parts[1].rsplit(",", 1)]
            timestamp = datetime.strptime(timestamp[1:-1], "%d/%m/%Y; %H:%M:%S")
            return equation, result, timestamp
        else:
            return None, None, None
