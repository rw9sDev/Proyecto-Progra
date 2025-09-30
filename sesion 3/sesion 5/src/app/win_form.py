import tkinter as tk
from tkinter import ttk, filedialog, messagebox

def open_win_form(parent: tk.Tk):
    win = tk.Toplevel(parent)
    win.title("Formulario")
    win.geometry("420x260")
    frm = ttk.Frame(win, padding=16)
    frm.pack(fill="both", expand=True)

    ttk.Label(frm, text="Nombre:").grid(row=0, column=0, sticky="w")
    ent_nombre = ttk.Entry(frm, width=28)
    ent_nombre.grid(row=0, column=1, pady=4)

    ttk.Label(frm, text="Edad:").grid(row=1, column=0, sticky="w")
    ent_edad = ttk.Entry(frm, width=10)
    ent_edad.grid(row=1, column=1, sticky="w", pady=4)

    def validar_y_guardar():
        nombre = ent_nombre.get().strip()
        edad_txt = ent_edad.get().strip()
        if not nombre:
            messagebox.showerror("Error", "El nombre es requerido.")
            return
        if not edad_txt.isdigit():
            messagebox.showerror("Error", "La edad debe ser un número entero.")
            return
        ruta = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Texto", "*.txt")])
        if ruta:
            with open(ruta, "w", encoding="utf-8") as f:
                f.write(f"Nombre: {nombre}\nEdad: {edad_txt}\n")
            messagebox.showinfo("OK", "Datos guardados.")

    ttk.Button(frm, text="Guardar", command=validar_y_guardar)\
        .grid(row=3, column=0, pady=12)
    ttk.Button(frm, text="Cerrar", command=win.destroy)\
        .grid(row=3, column=1, sticky="e", pady=12)