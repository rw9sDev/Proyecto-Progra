import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

def open_week_calendar(parent: tk.Tk):
    win = tk.Toplevel(parent)
    win.title("Calendario semanal")
    win.geometry("760x200")

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

    container = ttk.Frame(win, padding=8)
    container.pack(fill="both", expand=True)

    # cabeceras
    ttk.Label(container, text="Racha (total entrenamientos)", anchor="w", width=36).grid(row=0, column=0, padx=6, pady=6, sticky="w")
    for col, d in enumerate(days, start=1):
        ttk.Label(container, text=d, anchor="center", width=8).grid(row=0, column=col, padx=4, pady=6)

    # fila única que representa el total combinado
    ttk.Label(container, text="Completados (E1+E2+E3)", anchor="w", width=36).grid(row=1, column=0, padx=6, pady=4, sticky="w")

    # keep BooleanVar references so states persist and checkboxes consistently show left-to-right fills
    checkbox_vars = []
    for d in range(7):
        checked = d < total_capped
        var = tk.BooleanVar(value=checked)
        checkbox_vars.append(var)
        cb = ttk.Checkbutton(container, variable=var)
        cb.state(["disabled"])
        cb.grid(row=1, column=d+1, padx=6, pady=4)
    # attach to the window to ensure variables are not garbage-collected
    win._checkbox_vars = checkbox_vars

    # mostrar información de lectura para depuración y el total real
    per_text = "  ".join(read_info)
    status_text = f"{per_text}    Total real: {total}    Mostrando: {total_capped}/7"
    status = ttk.Label(win, text=status_text, anchor="w")
    status.pack(fill="x", padx=8, pady=(6,4))

    btn_frm = ttk.Frame(win)
    btn_frm.pack(fill="x", padx=8, pady=(0,8))
    ttk.Button(btn_frm, text="Cerrar", command=win.destroy).pack(side="right")

    return win