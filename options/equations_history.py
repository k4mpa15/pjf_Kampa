from datetime import datetime


class EquationHistory:
    def __init__(self):
        self.history_file_path = "history.txt"

    def add_equation(self, equation, result):
        time = datetime.now()
        formated_time = time.strftime("%m/%d/%Y, %H:%M:%S")
        with open(self.history_file_path, "a") as f:
            f.write(f"rownanie: {equation}, wynik: {result}, [{formated_time}]\n")

    def get_history(self):
        with open(self.history_file_path, "r") as f:
            history_content = f.read()
        return history_content
