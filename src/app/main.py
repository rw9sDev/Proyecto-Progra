import tkinter as tk
from tkinter import ttk
from app.win_home import open_win_home
from app.win_form import open_win_form
from app.win_list import open_win_list
from app.win_table import open_win_table
from app.win_canvas import open_win_canvas

def main():
    root = tk.Tk()
    root.title("Proyecto Integrador - MVP")
    root.geometry("420x340")

    frame = ttk.Frame(root, padding=16)
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text="Aplicación Demo (tkinter)", font=("Segoe UI", 12, "bold")).pack(pady=(0, 12))
    ttk.Button(frame, text="1) Home / Bienvenida", command=lambda: open_win_home(root)).pack(pady=4, fill="x")
    ttk.Button(frame, text="2) Formulario", command=lambda: open_win_form(root)).pack(pady=4, fill="x")
    ttk.Button(frame, text="3) Lista (CRUD básico)", command=lambda: open_win_list(root)).pack(pady=4, fill="x")
    ttk.Button(frame, text="4) Tabla (Treeview)", command=lambda: open_win_table(root)).pack(pady=4, fill="x")
    ttk.Button(frame, text="5) Canvas (Dibujo)", command=lambda: open_win_canvas(root)).pack(pady=4, fill="x")
    ttk.Separator(frame).pack(pady=6, fill="x")
    ttk.Button(frame, text="Salir", command=root.destroy).pack(pady=6)

    root.mainloop()

if __name__ == "__main__":
    main()