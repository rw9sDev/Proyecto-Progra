import tkinter as tk
from tkinter import ttk
from Ejercicios.E1 import open_E1
from Ejercicios.E2 import open_E2
from Ejercicios.E3 import open_E3
from app.WoData import open_week_calendar



def open_WOList(parent: tk.Tk, return_to=None):
    win = tk.Toplevel(parent)
    win.title("Elige tu ejercicio")
    win.geometry("420x340")

    frame = ttk.Frame(win, padding=16)
    frame.pack(fill="both", expand=True)

    def open_and_close(next_func):
        win.destroy()
        next_func(parent, lambda p: open_WOList(p, return_to))

    ttk.Label(frame, text="Elije tu ejercicio", font=("Segoe UI", 12, "bold")).pack(pady=(0, 12))
    ttk.Button(frame, text="1) Ejercicio Facil", command=lambda: open_and_close(open_E1)).pack(pady=4, fill="x")
    ttk.Button(frame, text="2) Ejercicio Intermedio", command=lambda: open_and_close(open_E2)).pack(pady=4, fill="x")
    ttk.Button(frame, text="3) Ejercicio Dificil", command=lambda: open_and_close(open_E3)).pack(pady=4, fill="x")
    ttk.Separator(frame).pack(pady=6, fill="x")

    def volver():
        win.destroy()
        if return_to:
            return_to(parent)

    # footer with "racha" button (opens 7-day calendar) and Cerrar button
    footer = ttk.Frame(frame)
    footer.pack(fill="x", side="bottom", pady=(8,0))
    # open calendar as child of this WOList window
    ttk.Button(footer, text="racha", command=lambda: open_week_calendar(win)).pack(side="left")
    ttk.Button(footer, text="Cerrar", command=volver).pack(side="right", padx=(0,4))