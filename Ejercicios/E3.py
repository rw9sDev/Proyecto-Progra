import tkinter as tk
from tkinter import ttk, messagebox
import csv
from pathlib import Path
import io


def open_E3(parent: tk.Tk, return_to=None):
    win = tk.Toplevel(parent)
    win.title("Ejercicio 3 - Rutina de Entrenamiento")
    win.geometry("800x500")
    win.resizable(True, True)
    
    # Configurar tema moderno
    style = ttk.Style(win)
    try:
        style.theme_use('clam')  # Tema más moderno
    except:
        pass
    
    # Estilos personalizados
    style.configure('Treeview',
                   rowheight=28,
                   font=('Segoe UI', 10))
    style.configure('Treeview.Heading',
                   font=('Segoe UI', 10, 'bold'),
                   background='#FF9800',
                   foreground='white')
    style.map('Treeview.Heading',
             background=[('active', '#F57C00')])
    
    # Frame principal con padding
    frm = ttk.Frame(win, padding=15)
    frm.pack(fill="both", expand=True)
    
    # Título
    title_lbl = ttk.Label(frm, text="📋 Mi Rutina de Entrenamiento (E3)", 
                         font=('Segoe UI', 14, 'bold'))
    title_lbl.pack(pady=(0, 10))
    
    # Frame contenedor para tabla y controles
    content_frm = ttk.Frame(frm)
    content_frm.pack(fill="both", expand=True)
    
    # Frame izquierdo para la tabla
    left = ttk.Frame(content_frm)
    left.pack(side="left", fill="both", expand=True, padx=(0, 10))
    
    # Frame derecho para checkboxes y estado
    right = ttk.Frame(content_frm, width=160)
    right.pack(side="left", fill="y")
    right.pack_propagate(False)
    
    # === TREEVIEW MEJORADO ===
    cols = ("Ejercicio", "Repeticiones", "Ronda")
    
    # Frame para treeview con scrollbars
    tree_frame = ttk.Frame(left)
    tree_frame.pack(fill="both", expand=True)
    
    # Scrollbars
    vsb = ttk.Scrollbar(tree_frame, orient="vertical")
    hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
    
    # Treeview con scrollbars
    tv = ttk.Treeview(tree_frame, columns=cols, show="headings",
                     yscrollcommand=vsb.set,
                     xscrollcommand=hsb.set,
                     selectmode='browse')
    
    vsb.config(command=tv.yview)
    hsb.config(command=tv.xview)
    
    # Grid layout para treeview y scrollbars
    tv.grid(row=0, column=0, sticky='nsew')
    vsb.grid(row=0, column=1, sticky='ns')
    hsb.grid(row=1, column=0, sticky='ew')
    
    tree_frame.grid_rowconfigure(0, weight=1)
    tree_frame.grid_columnconfigure(0, weight=1)
    
    # Configurar columnas con mejor tamaño
    column_widths = {
        "Ejercicio": 280,
        "Repeticiones": 120,
        "Ronda": 100
    }
    
    for c in cols:
        tv.heading(c, text=c)
        tv.column(c, width=column_widths.get(c, 150), 
                 minwidth=80, 
                 anchor="center",
                 stretch=True)
    
    # === CARGAR DATOS CSV ===
    # CORRECCIÓN: "rtuina3.csv" -> "rutina3.csv"
    ruta = Path(__file__).resolve().parents[1] / "data" / "rutina3.csv"
    if not ruta.exists():
        messagebox.showwarning("Aviso", f"No se encontró {ruta}.\nCrea el archivo de ejemplo.")
        win.destroy()
        return
    
    items = []
    try:
        raw = ruta.read_text(encoding="utf-8-sig")
        if not raw.strip():
            messagebox.showwarning("Aviso", f"{ruta.name} está vacío.")
            win.destroy()
            return
        
        # Detectar delimitador
        try:
            dialect = csv.Sniffer().sniff(raw[:4096])
            delim = dialect.delimiter
        except Exception:
            delim = ','
        
        f = io.StringIO(raw)
        reader = csv.DictReader(f, delimiter=delim)
        headers = [h.strip() for h in (reader.fieldnames or [])]
        
        # Función para seleccionar campos
        def pick_field(candidates, default_index):
            for cand in candidates:
                for h in headers:
                    if h.lower() == cand.lower():
                        return h
            return headers[default_index] if len(headers) > default_index else None
        
        name_field = pick_field(["nombre", "ejercicio", "name", "exercise"], 0)
        val1_field = pick_field(["valor1", "repeticiones", "reps", "repetition", "repeticion"], 1)
        val2_field = pick_field(["valor2", "ronda", "round"], 2)
        
        for idx, row in enumerate(reader):
            a = (row.get(name_field) if name_field else "") or ""
            b = (row.get(val1_field) if val1_field else "") or ""
            c = (row.get(val2_field) if val2_field else "") or ""
            
            # Insertar con etiquetas alternas para colorear filas
            tags = ('oddrow',) if idx % 2 else ('evenrow',)
            iid = tv.insert("", "end", values=(a.strip(), b.strip(), c.strip()), tags=tags)
            items.append(iid)
        
        # Colores alternados para filas
        tv.tag_configure('oddrow', background='#f0f0f0')
        tv.tag_configure('evenrow', background='white')
        
    except Exception as e:
        messagebox.showerror("Error al leer CSV", f"Error leyendo {ruta.name}:\n{e}")
        win.destroy()
        return
    
    if not items:
        messagebox.showinfo("Info", "No hay filas válidas en el CSV.")
        win.destroy()
        return
    
    # === CONTADOR DE ENTRENAMIENTOS ===
    data_dir = ruta.parent
    count_file = data_dir / "e3_count.txt"
    
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
    
    # === ÁREA DE CHECKBOXES ===
    check_vars = []
    
    # Header para checkboxes
    check_header = ttk.Label(right, text="✓ Completado", 
                            font=('Segoe UI', 10, 'bold'))
    check_header.pack(pady=(0, 8))
    
    # Separador
    ttk.Separator(right, orient='horizontal').pack(fill='x', pady=(0, 8))
    
    # Canvas scrollable para checkboxes
    canvas = tk.Canvas(right, highlightthickness=0, bg='#f5f5f5')
    vscroll = ttk.Scrollbar(right, orient="vertical", command=canvas.yview)
    checks_inner = ttk.Frame(canvas)
    
    inner_id = canvas.create_window((0, 0), window=checks_inner, anchor="nw")
    canvas.configure(yscrollcommand=vscroll.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    vscroll.pack(side="right", fill="y")
    
    def _on_inner_config(e):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(inner_id, width=canvas.winfo_width())
    
    checks_inner.bind("<Configure>", _on_inner_config)
    
    def _on_canvas_resize(e):
        canvas.itemconfig(inner_id, width=e.width)
    canvas.bind("<Configure>", _on_canvas_resize)
    
    # Mousewheel
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    # Función de cambio de checkbox
    def on_check_change():
        checked = sum(1 for v in check_vars if v.get())
        status_lbl.config(text=f"✅ {checked}/{len(check_vars)} completados")
        progress['value'] = (checked / len(check_vars)) * 100 if check_vars else 0
        
        # Auto-guardar cuando todos completados
        if len(check_vars) > 0 and all(v.get() for v in check_vars):
            win.after(500, save_and_return)
    
    # Crear checkboxes
    for i, _ in enumerate(items):
        var = tk.BooleanVar(value=False)
        cb = ttk.Checkbutton(checks_inner, text=f"#{i+1}", variable=var, 
                           command=on_check_change)
        cb.pack(anchor="w", pady=3, padx=10, fill="x")
        check_vars.append(var)
    
    # === BARRA DE PROGRESO ===
    progress_frame = ttk.Frame(right)
    progress_frame.pack(pady=10, padx=5, fill='x')
    
    progress = ttk.Progressbar(progress_frame, mode='determinate', 
                              length=140)
    progress.pack(fill='x')
    progress['value'] = 0
    
    status_lbl = ttk.Label(right, text=f"✅ 0/{len(check_vars)} completados",
                          font=('Segoe UI', 9))
    status_lbl.pack(pady=(5, 0))
    
    # === FUNCIONES DE GUARDADO ===
    def save_and_return():
        cur = read_count()
        cur += 1
        if cur > 7:
            cur = 1
        write_count(cur)
        messagebox.showinfo("¡Excelente! 💪", 
                          f"Entrenamiento completado.\nContador E3: {cur}/7")
        win.destroy()
        if return_to:
            return_to(parent)
    
    def finish_manual():
        if not any(v.get() for v in check_vars):
            if not messagebox.askyesno("Confirmar", 
                                      "No marcaste ningún ejercicio.\n¿Deseas completar de todas formas?"):
                return
        save_and_return()
    
    def volver():
        win.destroy()
        if return_to:
            return_to(parent)
    
    # === BOTONES ===
    ttk.Separator(frm, orient='horizontal').pack(fill='x', pady=(10, 10))
    
    btn_frm = ttk.Frame(frm)
    btn_frm.pack(fill="x")
    
    ttk.Button(btn_frm, text="❌ Cerrar", command=volver).pack(side="right", padx=4)
    ttk.Button(btn_frm, text="✓ Finalizar entrenamiento", 
              command=finish_manual).pack(side="right", padx=4)
    
    # Info del entrenamiento actual
    current_count = read_count()
    info_lbl = ttk.Label(btn_frm, 
                        text=f"📊 Entrenamientos completados: {current_count}/7",
                        font=('Segoe UI', 9))
    info_lbl.pack(side="left")
