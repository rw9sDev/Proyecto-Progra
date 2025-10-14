import tkinter as tk
from tkinter import ttk, messagebox
from app.win_form import open_win_form
def open_win_home(parent: tk.Tk, return_to=None):
        win = tk.Toplevel(parent)
        win.title("Home / Bienvenida")
        win.geometry("360x220")
        frm = ttk.Frame(win, padding=16)
        frm.pack(fill="both", expand=True)

        def open_and_close():
                win.destroy()
                # Pass a lambda that reopens this window as return_to for win_form
                open_win_form(parent, lambda p: open_win_home(p, return_to))

        def volver():
                win.destroy()
                if return_to:
                        return_to(parent)

        ttk.Label(frm, text="¡Bienvenid@s!", font=("Segoe UI", 11, "bold")).pack(pady=(0, 8))
        ttk.Label(frm, text="Explora las ventanas desde la pantalla principal.").pack(pady=(0, 12))
        ttk.Button(frm, text="Iniciar Sesion",
                        command=open_and_close).pack(pady=4, fill="x")
        ttk.Button(frm, text="Cerrar", command=volver).pack(pady=8)