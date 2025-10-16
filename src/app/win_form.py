import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from app.WOList import open_WOList
import os


def open_win_form(parent: tk.Tk, return_to=None):
    win = tk.Toplevel(parent)
    win.title("Gestión de Perfiles")
    win.geometry("550x600")
    win.resizable(False, False)
    
    # Colores
    BG_COLOR = "#f0f0f0"
    CARD_BG = "#ffffff"
    PRIMARY_COLOR = "#0066cc"
    SUCCESS_COLOR = "#28a745"
    SECONDARY_COLOR = "#6c757d"
    TEXT_COLOR = "#212529"
    
    win.configure(bg=BG_COLOR)
    
    # Estilos
    style = ttk.Style()
    style.theme_use('clam')
    
    style.configure('Card.TFrame', background=CARD_BG)
    style.configure('Label.TLabel', background=CARD_BG, foreground='#495057', font=('Segoe UI', 10))
    style.configure('Title.TLabel', background=CARD_BG, foreground=TEXT_COLOR, font=('Segoe UI', 14, 'bold'))
    style.configure('Subtitle.TLabel', background=CARD_BG, foreground=SECONDARY_COLOR, font=('Segoe UI', 9))
    
    style.configure('Custom.TEntry', fieldbackground='white', padding=6)
    
    style.configure('Primary.TButton', background=PRIMARY_COLOR, foreground='white', 
                   font=('Segoe UI', 10, 'bold'), borderwidth=0, padding=(20, 10))
    style.map('Primary.TButton', background=[('active', '#0052a3')])
    
    style.configure('Success.TButton', background=SUCCESS_COLOR, foreground='white', 
                   font=('Segoe UI', 10, 'bold'), borderwidth=0, padding=(20, 10))
    style.map('Success.TButton', background=[('active', '#218838')])
    
    style.configure('Secondary.TButton', background='#e9ecef', foreground='#212529', 
                   font=('Segoe UI', 9), borderwidth=0, padding=(20, 10))
    style.map('Secondary.TButton', background=[('active', '#dee2e6')])
    
    # Contenedor principal
    container = tk.Frame(win, bg=BG_COLOR)
    container.pack(fill="both", expand=True, padx=30, pady=30)
    
    frm = ttk.Frame(container, style='Card.TFrame', padding=25)
    frm.pack(fill="both", expand=True)
    
    # Título principal
    ttk.Label(frm, text="👤 Gestión de Perfiles", style='Title.TLabel').pack(pady=(0, 5))
    ttk.Label(frm, text="Crea un nuevo perfil o carga uno existente", style='Subtitle.TLabel').pack(pady=(0, 15))
    
    # Separador
    ttk.Separator(frm, orient='horizontal').pack(fill='x', pady=(0, 15))
    
    # Frame para el formulario
    form_frame = ttk.Frame(frm, style='Card.TFrame')
    form_frame.pack(fill="both", expand=True, pady=(0, 15))
    
    # Campos del formulario
    ttk.Label(form_frame, text="Nombre completo:", style='Label.TLabel').grid(row=0, column=0, sticky="w", pady=8, padx=(0, 10))
    ent_nombre = ttk.Entry(form_frame, width=30, style='Custom.TEntry')
    ent_nombre.grid(row=0, column=1, pady=8, sticky="ew")
    
    ttk.Label(form_frame, text="Edad:", style='Label.TLabel').grid(row=1, column=0, sticky="w", pady=8, padx=(0, 10))
    ent_edad = ttk.Entry(form_frame, width=15, style='Custom.TEntry')
    ent_edad.grid(row=1, column=1, sticky="w", pady=8)
    
    ttk.Label(form_frame, text="Peso (kg):", style='Label.TLabel').grid(row=2, column=0, sticky="w", pady=8, padx=(0, 10))
    ent_peso = ttk.Entry(form_frame, width=15, style='Custom.TEntry')
    ent_peso.grid(row=2, column=1, sticky="w", pady=8)
    
    ttk.Label(form_frame, text="Altura (cm):", style='Label.TLabel').grid(row=3, column=0, sticky="w", pady=8, padx=(0, 10))
    ent_altura = ttk.Entry(form_frame, width=15, style='Custom.TEntry')
    ent_altura.grid(row=3, column=1, sticky="w", pady=8)
    
    # Configurar columna para que se expanda
    form_frame.columnconfigure(1, weight=1)
    
    # Separador
    ttk.Separator(frm, orient='horizontal').pack(fill='x', pady=15)
    
    # Funciones
    def crear_perfil():
        """Crear y guardar un nuevo perfil"""
        nombre = ent_nombre.get().strip()
        edad_txt = ent_edad.get().strip()
        peso = ent_peso.get().strip()
        altura = ent_altura.get().strip()
        
        # Validaciones
        if not nombre:
            messagebox.showerror("Campo vacío", "El nombre es requerido.", parent=win)
            ent_nombre.focus()
            return
        
        if not edad_txt:
            messagebox.showerror("Campo vacío", "La edad es requerida.", parent=win)
            ent_edad.focus()
            return
        
        if not edad_txt.isdigit():
            messagebox.showerror("Error", "La edad debe ser un número entero.", parent=win)
            ent_edad.focus()
            return
        
        edad_int = int(edad_txt)
        if edad_int < 1 or edad_int > 120:
            messagebox.showerror("Error", "La edad debe estar entre 1 y 120 años.", parent=win)
            ent_edad.focus()
            return
        
        if not peso:
            messagebox.showerror("Campo vacío", "El peso es requerido.", parent=win)
            ent_peso.focus()
            return
        
        try:
            peso_float = float(peso)
            if peso_float < 20 or peso_float > 300:
                messagebox.showerror("Error", "El peso debe estar entre 20 y 300 kg.", parent=win)
                ent_peso.focus()
                return
        except ValueError:
            messagebox.showerror("Error", "El peso debe ser un número.", parent=win)
            ent_peso.focus()
            return
        
        if not altura:
            messagebox.showerror("Campo vacío", "La altura es requerida.", parent=win)
            ent_altura.focus()
            return
        
        try:
            altura_float = float(altura)
            if altura_float < 50 or altura_float > 250:
                messagebox.showerror("Error", "La altura debe estar entre 50 y 250 cm.", parent=win)
                ent_altura.focus()
                return
        except ValueError:
            messagebox.showerror("Error", "La altura debe ser un número.", parent=win)
            ent_altura.focus()
            return
        
        # Crear directorio de perfiles si no existe
        profiles_dir = "perfiles"
        if not os.path.exists(profiles_dir):
            os.makedirs(profiles_dir)
        
        # Crear nombre de archivo seguro
        safe_name = "".join(c for c in nombre if c.isalnum() or c in (' ', '-', '_'))
        filename = os.path.join(profiles_dir, f"{safe_name}.txt")
        
        # Verificar si el archivo ya existe
        if os.path.exists(filename):
            overwrite = messagebox.askyesno("Perfil existe", 
                                           f"Ya existe un perfil con el nombre '{nombre}'.\n\n"
                                           "¿Deseas sobrescribirlo?", 
                                           parent=win)
            if not overwrite:
                return
        
        # Guardar el perfil
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"Nombre: {nombre}\n")
                f.write(f"Edad: {edad_txt}\n")
                f.write(f"Peso: {peso}\n")
                f.write(f"Altura: {altura}\n")
            
            messagebox.showinfo("¡Éxito!", 
                              f"Perfil creado exitosamente.\n\n"
                              f"Guardado en: {filename}", 
                              parent=win)
            
            # Abrir WOList
            win.destroy()
            open_WOList(parent, lambda p: open_win_form(p, return_to))
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el perfil:\n{str(e)}", parent=win)
    
    def cargar_perfil():
        """Cargar un perfil existente desde archivo"""
        profiles_dir = "perfiles"
        
        # Crear directorio si no existe
        if not os.path.exists(profiles_dir):
            os.makedirs(profiles_dir)
            messagebox.showinfo("Sin perfiles", 
                              "No hay perfiles guardados aún.\n\n"
                              "Crea tu primer perfil llenando el formulario.", 
                              parent=win)
            return
        
        # Abrir selector de archivos
        filename = filedialog.askopenfilename(
            parent=win,
            title="Selecciona un perfil",
            initialdir=profiles_dir,
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        
        if not filename:
            return  # Usuario canceló
        
        # Leer el archivo
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Parsear la información
            profile_data = {}
            for line in lines:
                line = line.strip()
                if ':' in line:
                    key, value = line.split(':', 1)
                    profile_data[key.strip()] = value.strip()
            
            # Validar que tenga los campos necesarios
            required_fields = ['Nombre', 'Edad', 'Peso', 'Altura']
            missing_fields = [field for field in required_fields if field not in profile_data]
            
            if missing_fields:
                messagebox.showerror("Archivo inválido", 
                                   f"El archivo no tiene todos los campos requeridos.\n\n"
                                   f"Campos faltantes: {', '.join(missing_fields)}\n\n"
                                   "Formato esperado:\n"
                                   "Nombre: [nombre]\n"
                                   "Edad: [edad]\n"
                                   "Peso: [peso]\n"
                                   "Altura: [altura]", 
                                   parent=win)
                return
            
            # Mostrar confirmación
            nombre = profile_data['Nombre']
            edad = profile_data['Edad']
            peso = profile_data['Peso']
            altura = profile_data['Altura']
            
            resultado = messagebox.showinfo("Perfil Cargado", 
                                           f"✅ Perfil cargado exitosamente:\n\n"
                                           f"👤 Nombre: {nombre}\n"
                                           f"🎂 Edad: {edad} años\n"
                                           f"⚖️ Peso: {peso} kg\n"
                                           f"📏 Altura: {altura} cm\n\n"
                                           f"Presiona OK para continuar al panel de ejercicios.", 
                                           parent=win)
            
            # Abrir WOList
            win.destroy()
            open_WOList(parent, lambda p: open_win_form(p, return_to))
            
        except Exception as e:
            messagebox.showerror("Error al cargar", 
                               f"No se pudo cargar el perfil:\n{str(e)}", 
                               parent=win)
    
    def volver():
        """Volver a la ventana anterior"""
        win.destroy()
        if return_to:
            return_to(parent)
    
    # Frame de botones
    btn_frame = ttk.Frame(frm, style='Card.TFrame')
    btn_frame.pack(fill="x", pady=(5, 0))
    
    # Botón Crear Perfil
    ttk.Button(btn_frame, text="➕ Crear Perfil", command=crear_perfil, 
              style='Success.TButton').pack(fill="x", pady=(0, 8))
    
    # Botón Cargar Perfil
    ttk.Button(btn_frame, text="📁 Cargar Perfil Existente", command=cargar_perfil, 
              style='Primary.TButton').pack(fill="x", pady=(0, 8))
    
    # Botón Cerrar
    ttk.Button(btn_frame, text="✕ Cerrar", command=volver, 
              style='Secondary.TButton').pack(fill="x")
    
    # Focus en el primer campo
    ent_nombre.focus()
