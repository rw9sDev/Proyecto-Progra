import tkinter as tk
from tkinter import ttk, messagebox
import csv
from pathlib import Path


def open_win_table(parent: tk.Tk, return_to=None):
    win = tk.Toplevel(parent)
    win.title("Tabla de Datos")
    win.geometry("700x550")
    win.resizable(False, False)
    
    # Colores modernos
    BG_COLOR = "#f0f0f0"
    CARD_BG = "#ffffff"
    PRIMARY_COLOR = "#0066cc"
    SECONDARY_COLOR = "#6c757d"
    TEXT_COLOR = "#212529"
    HEADER_BG = "#0052a3"
    ROW_BG = "#ffffff"
    ALT_ROW_BG = "#f8f9fa"
    SELECT_BG = "#e3f2fd"
    SELECT_FG = "#0d47a1"
    BORDER_COLOR = "#dee2e6"
    
    win.configure(bg=BG_COLOR)
    
    # Configurar estilos
    style = ttk.Style()
    style.theme_use('clam')
    
    # Estilo para frame principal
    style.configure('Table.TFrame', 
                   background=CARD_BG)
    
    # Estilo para labels
    style.configure('TableTitle.TLabel', 
                   background=CARD_BG, 
                   foreground=TEXT_COLOR, 
                   font=('Segoe UI', 16, 'bold'))
    
    style.configure('TableInfo.TLabel', 
                   background=CARD_BG, 
                   foreground=SECONDARY_COLOR, 
                   font=('Segoe UI', 9))
    
    # Estilo personalizado para Treeview
    style.configure('Custom.Treeview',
                   background=ROW_BG,
                   foreground=TEXT_COLOR,
                   fieldbackground=ROW_BG,
                   borderwidth=1,
                   relief='solid',
                   rowheight=35,
                   font=('Segoe UI', 10))
    
    # Estilo para los encabezados del Treeview
    style.configure('Custom.Treeview.Heading',
                   background=HEADER_BG,
                   foreground='white',
                   borderwidth=1,
                   relief='flat',
                   font=('Segoe UI', 10, 'bold'))
    
    # Mapeo de estados para el Treeview
    style.map('Custom.Treeview',
             background=[('selected', SELECT_BG)],
             foreground=[('selected', SELECT_FG)])
    
    style.map('Custom.Treeview.Heading',
             background=[('active', '#003d82')],
             relief=[('pressed', 'flat')])
    
    # Estilo para botón
    style.configure('TableButton.TButton', 
                   background='#e9ecef', 
                   foreground=TEXT_COLOR, 
                   font=('Segoe UI', 10),
                   borderwidth=0,
                   focuscolor='none',
                   padding=(20, 12))
    
    style.map('TableButton.TButton',
             background=[('active', '#dee2e6'), ('pressed', '#dee2e6')])
    
    # Contenedor principal
    container = tk.Frame(win, bg=BG_COLOR)
    container.pack(fill="both", expand=True, padx=30, pady=30)
    
    # Card principal
    frm = ttk.Frame(container, style='Table.TFrame', padding=30)
    frm.pack(fill="both", expand=True)
    
    # Header de la ventana
    header_frame = ttk.Frame(frm, style='Table.TFrame')
    header_frame.pack(fill="x", pady=(0, 20))
    
    # Título
    title = ttk.Label(header_frame, 
                     text="📊 Tabla de Datos", 
                     style='TableTitle.TLabel')
    title.pack(anchor="w")
    
    # Información adicional
    info_label = ttk.Label(header_frame, 
                          text="Visualización de datos desde archivo CSV", 
                          style='TableInfo.TLabel')
    info_label.pack(anchor="w", pady=(5, 0))
    
    # Separador
    separator = ttk.Separator(frm, orient='horizontal')
    separator.pack(fill='x', pady=(0, 20))
    
    # Frame para el Treeview con scrollbar
    tree_frame = ttk.Frame(frm, style='Table.TFrame')
    tree_frame.pack(fill="both", expand=True, pady=(0, 20))
    
    # Scrollbar vertical
    scrollbar_y = ttk.Scrollbar(tree_frame, orient="vertical")
    scrollbar_y.pack(side="right", fill="y")
    
    # Scrollbar horizontal
    scrollbar_x = ttk.Scrollbar(tree_frame, orient="horizontal")
    scrollbar_x.pack(side="bottom", fill="x")
    
    # Treeview
    cols = ("nombre", "valor1", "valor2")
    tv = ttk.Treeview(tree_frame, 
                     columns=cols, 
                     show="headings", 
                     style='Custom.Treeview',
                     yscrollcommand=scrollbar_y.set,
                     xscrollcommand=scrollbar_x.set)
    
    # Configurar scrollbars
    scrollbar_y.config(command=tv.yview)
    scrollbar_x.config(command=tv.xview)
    
    # Configurar columnas y encabezados
    column_widths = {"nombre": 250, "valor1": 180, "valor2": 180}
    for c in cols:
        tv.heading(c, text=c.capitalize())
        tv.column(c, width=column_widths[c], anchor="center", minwidth=100)
    
    tv.pack(fill="both", expand=True)
    
    # Configurar colores alternos para las filas
    tv.tag_configure('oddrow', background=ROW_BG)
    tv.tag_configure('evenrow', background=ALT_ROW_BG)
    
    # Cargar datos del CSV
    ruta = Path(__file__).resolve().parents[1] / "data" / "sample.csv"
    if not ruta.exists():
        messagebox.showwarning("Advertencia", 
                              f"No se encontró el archivo:\n{ruta}\n\nPor favor, crea el archivo de ejemplo.",
                              parent=win)
        win.destroy()
        if return_to:
            return_to(parent)
        return
    
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            row_count = 0
            for row in reader:
                # Alternar colores de filas
                tag = 'evenrow' if row_count % 2 == 0 else 'oddrow'
                tv.insert("", "end", 
                         values=(row["nombre"], row["valor1"], row["valor2"]),
                         tags=(tag,))
                row_count += 1
        
        # Mostrar contador de registros
        count_label = ttk.Label(frm, 
                               text=f"Total de registros: {row_count}", 
                               style='TableInfo.TLabel')
        count_label.pack(anchor="w", pady=(0, 15))
        
    except Exception as e:
        messagebox.showerror("Error", 
                           f"Error al leer el archivo CSV:\n{str(e)}",
                           parent=win)
        win.destroy()
        if return_to:
            return_to(parent)
        return

    def volver():
        win.destroy()
        if return_to:
            return_to(parent)

    # Botón cerrar
    btn_cerrar = ttk.Button(frm, 
                           text="✕  Cerrar", 
                           command=volver,
                           style='TableButton.TButton')
    btn_cerrar.pack(anchor="e")
