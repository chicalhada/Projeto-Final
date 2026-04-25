import tkinter as tk
import gestor_de_dados as gd


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Gestor de Ginásio")
        self.geometry("800x500")

        self.inicio_frame = tk.Frame(self)
        self.clientes_frame = tk.Frame(self)
        self.planos_frame = tk.Frame(self)
        self.sessoes_frame = tk.Frame(self)
        self.estatisticas_frame = tk.Frame(self)

        self.inicio_frame.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = App()
    app.mainloop()