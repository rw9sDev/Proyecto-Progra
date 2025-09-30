import tkinter as tk
from tkinter import ttk

def open_win_canvas(parent: tk.Tk):
    win = tk.Toplevel(parent)
    win.title("Canvas (Dibujo)")
    win.geometry("480x340")

    frm = ttk.Frame(win, padding=12)
    frm.pack(fill="both", expand=True)

    canvas = tk.Canvas(frm, width=440, height=240, bg="white")
    canvas.pack()

    # Dibujos de ejemplo
    canvas.create_rectangle(20, 20, 120, 80, outline="black", width=2)
    canvas.create_oval(150, 20, 220, 90, fill="lightblue")
    canvas.create_line(240, 30, 360, 90, width=3)
    canvas.create_text(220, 140, text="¡Hola Canvas!", font=("Segoe UI", 12, "bold"))

    ttk.Button(frm, text="Cerrar", command=win.destroy).pack(pady=8, anchor="e")