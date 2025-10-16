import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path


def open_week_calendar(parent: tk.Tk):
    win = tk.Toplevel(parent)
    win.title("Calendario semanal")
    win.geometry("850x280")
    win.resizable(False, False)
    
    # Colores
    BG_COLOR = "#f0f0f0"
    CARD_BG = "#ffffff"
    PRIMARY_COLOR = "#0066cc"
    SUCCESS_COLOR = "#28a745"
    TEXT_COLOR = "#212529"
    SECONDARY_COLOR = "#6c757d"
    
    win.configure(bg=BG_COLOR)
    
    # Estilos
    style = ttk.Style()
    style.theme_use('clam')
    
    style.configure('Card.TFrame', background=CARD_BG)
    style.configure('Title.TLabel', background=CARD_BG, foreground=TEXT_COLOR, font=('Segoe UI', 12, 'bold'))
    style.configure('Day.TLabel', background=CARD_BG, foreground=PRIMARY_COLOR, font=('Segoe UI', 10, 'bold'))
    style.configure('Row.TLabel', background=CARD_BG, foreground=SECONDARY_COLOR, font=('Segoe UI', 10))
    style.configure('Status.TLabel', background=CARD_BG, foreground=SECONDARY_COLOR, font=('Segoe UI', 8))
    
    style.configure('Close.TButton', background='#e9ecef', foreground='#212529', 
                   font=('Segoe UI', 9), borderwidth=0, padding=(20, 10))
    style.map('Close.TButton', background=[('active', '#dee2e6')])

    data_dir = Path(__file__).resolve().parents[1] / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    # archivos que usan E1/E2/E3
    files = [
        ("E1", data_dir / "e1_count.txt"),
        ("E2", data_dir / "e2_count.txt"),
        ("E3", data_dir / "e3_count.txt"),
    ]

    def read_count(path: Path):
        try:
            if not path.exists():
                path.write_text("0", encoding="utf-8")
            text = path.read_text(encoding="utf-8").strip()
            # manejar archivos vacíos o con espacios/newlines
            if text == "":
                return 0
            return int(text)
        except Exception:
            return 0

    # leer contadores de forma robusta y limitar a 0..7
    counts = []
    read_info = []
    for name, p in files:
        v = read_count(p)
        v_clamped = max(0, min(7, v))
        counts.append(v_clamped)
        read_info.append(f"{name}={v_clamped} ({p.name})")

    # total de ejercicios completados entre E1+E2+E3 (sin sobrepasar 7 para mostrar en el calendario)
    total = sum(counts)
    total_capped = max(0, min(7, total))

    days = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
    
    # Contenedor exterior
    outer_container = tk.Frame(win, bg=BG_COLOR)
    outer_container.pack(fill="both", expand=True, padx=25, pady=25)
    
    # Card principal
    card = ttk.Frame(outer_container, style='Card.TFrame', padding=20)
    card.pack(fill="both", expand=True)
    
    # Título
    ttk.Label(card, text="📅 Racha Semanal de Entrenamientos", style='Title.TLabel').grid(row=0, column=0, columnspan=8, pady=(0, 10), sticky="w")
    
    # Separador
    sep = ttk.Separator(card, orient='horizontal')
    sep.grid(row=1, column=0, columnspan=8, sticky="ew", pady=(0, 15))

    # Cabeceras de días
    ttk.Label(card, text="Estado", style='Row.TLabel', anchor="w", width=20).grid(row=2, column=0, padx=6, pady=6, sticky="w")
    for col, d in enumerate(days, start=1):
        ttk.Label(card, text=d, style='Day.TLabel', anchor="center", width=8).grid(row=2, column=col, padx=4, pady=6)

    # Fila de checkboxes (IDÉNTICA al original)
    ttk.Label(card, text="Completados (E1+E2+E3)", style='Row.TLabel', anchor="w", width=20).grid(row=3, column=0, padx=6, pady=4, sticky="w")

    # keep BooleanVar references so states persist and checkboxes consistently show left-to-right fills
    checkbox_vars = []
    for d in range(7):
        checked = d < total_capped
        var = tk.BooleanVar(value=checked)
        checkbox_vars.append(var)
        cb = ttk.Checkbutton(card, variable=var)
        cb.state(["disabled"])
        cb.grid(row=3, column=d+1, padx=6, pady=4)
    # attach to the window to ensure variables are not garbage-collected
    win._checkbox_vars = checkbox_vars

    # Separador inferior
    sep2 = ttk.Separator(card, orient='horizontal')
    sep2.grid(row=4, column=0, columnspan=8, sticky="ew", pady=(15, 10))

    # mostrar información de lectura para depuración y el total real
    per_text = "  ".join(read_info)
    status_text = f"{per_text}    Total real: {total}    Mostrando: {total_capped}/7"
    status = ttk.Label(card, text=status_text, style='Status.TLabel', anchor="w")
    status.grid(row=5, column=0, columnspan=8, sticky="w", padx=6, pady=(0, 10))

    # Botón cerrar
    btn_frm = ttk.Frame(card, style='Card.TFrame')
    btn_frm.grid(row=6, column=0, columnspan=8, sticky="e", pady=(10, 0))
    ttk.Button(btn_frm, text="✕  Cerrar", command=win.destroy, style='Close.TButton').pack(side="right")

    return win
