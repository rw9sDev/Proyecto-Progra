import tkinter as tk
from tkinter import ttk, messagebox
import csv
from pathlib import Path
import os
import io

def open_E1(parent: tk.Tk, return_to=None):
    win = tk.Toplevel(parent)
    win.title("Ejercicio 1")
    win.geometry("640x320")
    frm = ttk.Frame(win, padding=12)
    frm.pack(fill="both", expand=True)

    cols = ("Ejercicio", "Repeticiones", "Ronda")
    left = ttk.Frame(frm)
    left.pack(side="left", fill="both", expand=True)
    right = ttk.Frame(frm, width=140)
    right.pack(side="left", fill="y", padx=(8,0))

    tv = ttk.Treeview(left, columns=cols, show="headings", height=10)
    for c in cols:
        tv.heading(c, text=c)
        tv.column(c, width=140, anchor="center")
    tv.pack(fill="both", expand=True)

    ruta = Path(__file__).resolve().parents[1] / "data" / "rutina.csv"
    if not ruta.exists():
        messagebox.showwarning("Aviso", f"No se encontró {ruta}. Crea el archivo de ejemplo.")
        return

    # --- robust CSV loading: detect delimiter, handle BOM, and flexible headers ---
    items = []
    try:
        raw = ruta.read_text(encoding="utf-8-sig")
        if not raw.strip():
            messagebox.showwarning("Aviso", f"{ruta.name} está vacío.")
            return

        # detect delimiter with Sniffer; fallback to comma
        try:
            dialect = csv.Sniffer().sniff(raw[:4096])
            delim = dialect.delimiter
        except Exception:
            delim = ','

        f = io.StringIO(raw)
        reader = csv.DictReader(f, delimiter=delim)
        headers = [h.strip() for h in (reader.fieldnames or [])]

        # pick fields (flexible): try common names, otherwise use first three columns
        def pick_field(candidates, default_index):
            for cand in candidates:
                for h in headers:
                    if h.lower() == cand:
                        return h
            return headers[default_index] if len(headers) > default_index else None

        name_field = pick_field(["nombre","ejercicio","name","exercise"], 0)
        val1_field = pick_field(["valor1","repeticiones","reps","repetition","repeticion"], 1)
        val2_field = pick_field(["valor2","ronda","round"], 2)

        for row in reader:
            # guard against missing keys
            a = (row.get(name_field) if name_field else "") or ""
            b = (row.get(val1_field) if val1_field else "") or ""
            c = (row.get(val2_field) if val2_field else "") or ""
            iid = tv.insert("", "end", values=(a.strip(), b.strip(), c.strip()))
            items.append(iid)
    except Exception as e:
        messagebox.showerror("Error al leer CSV", f"Error leyendo {ruta.name}: {e}")
        return

    if not items:
        messagebox.showinfo("Info", "No hay filas válidas en el CSV.")
        return

    # per-workout counter file for E1
    data_dir = ruta.parent
    count_file = data_dir / "e1_count.txt"
    def read_count():
        try:
            if not count_file.exists():
                count_file.write_text("0", encoding="utf-8")
            text = count_file.read_text(encoding="utf-8").strip()
            return int(text) if text != "" else 0
        except Exception:
            return 0

    def write_count(n: int):
        try:
            count_file.write_text(str(n), encoding="utf-8")
        except Exception:
            pass

    def save_and_return():
        cur = read_count()
        cur += 1
        if cur > 7:
            cur = 1
        write_count(cur)
        messagebox.showinfo("Guardado", f"Contador E1 guardado: {cur}")
        win.destroy()
        if return_to:
            return_to(parent)

    # create a scrollable area for the per-row checkboxes so the number of
    # checkboxes adapts to the number of rows in the treeview
    check_vars = []
    canvas = tk.Canvas(right, width=120, highlightthickness=0)
    vscroll = ttk.Scrollbar(right, orient="vertical", command=canvas.yview)
    checks_inner = ttk.Frame(canvas)
    inner_id = canvas.create_window((0, 0), window=checks_inner, anchor="nw")
    canvas.configure(yscrollcommand=vscroll.set)
    canvas.pack(side="left", fill="both", expand=True)
    vscroll.pack(side="right", fill="y")

    def _on_inner_config(e):
        canvas.configure(scrollregion=canvas.bbox("all"))
        # ensure inner frame width matches canvas width so checkbuttons wrap nicely
        canvas.itemconfig(inner_id, width=canvas.winfo_width())

    checks_inner.bind("<Configure>", _on_inner_config)
    def _on_canvas_resize(e):
        canvas.itemconfig(inner_id, width=e.width)
    canvas.bind("<Configure>", _on_canvas_resize)

    # mousewheel support (Windows)
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    ttk.Label(checks_inner, text="Hecho").pack(anchor="center", pady=(0,4))

    # on_check_change must exist before creating checkbuttons
    def on_check_change():
        checked = sum(1 for v in check_vars if v.get())
        try:
            status_lbl.config(text=f"{checked}/{len(check_vars)} completados")
        except Exception:
            pass
        # auto-save & return when all are checked
        if len(check_vars) > 0 and all(v.get() for v in check_vars):
            save_and_return()

    # create one checkbox per CSV row (adapts automatically to items length)
    for _ in items:
        var = tk.BooleanVar(value=False)
        cb = ttk.Checkbutton(checks_inner, variable=var, command=on_check_change)
        cb.pack(anchor="center", pady=2, fill="x", expand=True)
        check_vars.append(var)

    status_lbl = ttk.Label(right, text=f"0/{len(check_vars)} completados")
    status_lbl.pack(pady=(6,0))

    def finish_manual():
        if not any(v.get() for v in check_vars):
            if not messagebox.askyesno("Confirmar", "No marcaste ningún ejercicio. ¿Deseas completar de todas formas?"):
                return
        save_and_return()

    def volver():
        win.destroy()
        if return_to:
            return_to(parent)

    btn_frm = ttk.Frame(frm)
    btn_frm.pack(fill="x", pady=(8,0))
    ttk.Button(btn_frm, text="Cerrar", command=volver).pack(side="right", padx=4)
    ttk.Button(btn_frm, text="Finalizar entrenamiento", command=finish_manual).pack(side="right")