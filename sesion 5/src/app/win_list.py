import tkinter as tk
from tkinter import ttk, messagebox

def open_win_list(parent: tk.Tk):
    win = tk.Toplevel(parent)
    win.title("Lista (CRUD básico)")
    win.geometry("420x300")

    frm = ttk.Frame(win, padding=12)
    frm.pack(fill="both", expand=True)

    lb = tk.Listbox(frm, height=10)
    lb.grid(row=0, column=0, rowspan=4, sticky="nsew", padx=(0, 8))
    frm.columnconfigure(0, weight=1)
    frm.rowconfigure(0, weight=1)

    ent_item = ttk.Entry(frm)
    ent_item.grid(row=0, column=1, sticky="ew")

    def agregar():
        v = ent_item.get().strip()
        if v:
            lb.insert("end", v)
            ent_item.delete(0, "end")
        else:
            messagebox.showwarning("Aviso", "Escribe un texto para agregar.")

    def eliminar():
        sel = lb.curselection()
        if sel:
            lb.delete(sel[0])

    def limpiar():
        lb.delete(0, "end")

    ttk.Button(frm, text="Agregar", command=agregar).grid(row=1, column=1, sticky="ew", pady=4)
    ttk.Button(frm, text="Eliminar seleccionado", command=eliminar).grid(row=2, column=1, sticky="ew", pady=4)
    ttk.Button(frm, text="Limpiar", command=limpiar).grid(row=3, column=1, sticky="ew", pady=4)

    ttk.Button(frm, text="Cerrar", command=win.destroy).grid(row=4, column=0, columnspan=2, pady=10, sticky="e")