import tkinter as tk
from tkinter import ttk, messagebox

def open_win_home(parent: tk.Tk):
    win = tk.Toplevel(parent)
    win.title("Home / Bienvenida")
    win.geometry("360x220")
    frm = ttk.Frame(win, padding=16)
    frm.pack(fill="both", expand=True)

    ttk.Label(frm, text="¡Bienvenid@s!", font=("Segoe UI", 11, "bold")).pack(pady=(0, 8))
    ttk.Label(frm, text="Explora las ventanas desde la pantalla principal.").pack(pady=(0, 12))
    ttk.Button(frm, text="Mostrar mensaje",
               command=lambda: messagebox.showinfo("Info", "¡Equipo listo!")).pack()
    ttk.Button(frm, text="Cerrar", command=win.destroy).pack(pady=8)