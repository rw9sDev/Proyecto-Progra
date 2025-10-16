import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from Ejercicios.E1 import open_E1
from Ejercicios.E2 import open_E2
from Ejercicios.E3 import open_E3
from app.WoData import open_week_calendar
import urllib.request
import urllib.parse
import json
import random


def open_exercise_advisor(parent_win):
    """Ventana de Consejos de Ejercicio usando ExerciseDB API"""
    advisor_win = tk.Toplevel(parent_win)
    advisor_win.title("💪 Virtual Choach")
    advisor_win.geometry("650x600")
    advisor_win.resizable(False, False)
    
    # Colores
    BG_COLOR = "#f0f0f0"
    CARD_BG = "#ffffff"
    PRIMARY_COLOR = "#0066cc"
    ADVICE_COLOR = "#28a745"
    TEXT_COLOR = "#212529"
    
    advisor_win.configure(bg=BG_COLOR)
    
    # Estilos
    style = ttk.Style()
    style.configure('Advice.TButton', background=ADVICE_COLOR, foreground='white', 
                   font=('Segoe UI', 10, 'bold'), borderwidth=0, padding=(20, 12))
    style.map('Advice.TButton', background=[('active', '#218838')])
    
    style.configure('Search.TButton', background=PRIMARY_COLOR, foreground='white', 
                   font=('Segoe UI', 10, 'bold'), borderwidth=0, padding=(20, 12))
    style.map('Search.TButton', background=[('active', '#0052a3')])
    
    style.configure('AdviceCard.TFrame', background=CARD_BG)
    style.configure('AdviceTitle.TLabel', background=CARD_BG, foreground=TEXT_COLOR, 
                   font=('Segoe UI', 14, 'bold'))
    style.configure('AdviceInfo.TLabel', background='#d4edda', foreground='#155724', 
                   font=('Segoe UI', 8), padding=10)
    
    style.configure('Close.TButton', background='#e9ecef', foreground='#212529', 
                   font=('Segoe UI', 9), borderwidth=0, padding=(15, 10))
    style.map('Close.TButton', background=[('active', '#dee2e6')])
    
    # Contenedor
    container = tk.Frame(advisor_win, bg=BG_COLOR)
    container.pack(fill="both", expand=True, padx=20, pady=20)
    
    card = ttk.Frame(container, style='AdviceCard.TFrame', padding=20)
    card.pack(fill="both", expand=True)
    
    # Título
    ttk.Label(card, text="💡 Consejos de Ejercicio", style='AdviceTitle.TLabel').pack(pady=(0, 10))
    
    # Info box
    info_frame = ttk.Frame(card, style='AdviceCard.TFrame')
    info_frame.pack(fill="x", pady=(0, 15))
    
    info_label = ttk.Label(info_frame, 
                          text="✨ Powered by ExerciseDB - 1300+ ejercicios profesionales",
                          style='AdviceInfo.TLabel')
    info_label.pack(fill="x")
    
    ttk.Separator(card, orient='horizontal').pack(fill='x', pady=(10, 15))
    
    # Frame para filtros
    filter_frame = ttk.Frame(card, style='AdviceCard.TFrame')
    filter_frame.pack(fill="x", pady=(0, 15))
    
    ttk.Label(filter_frame, text="Selecciona el grupo muscular:", background=CARD_BG, 
             foreground=TEXT_COLOR, font=('Segoe UI', 10, 'bold')).pack(anchor="w", pady=(0, 8))
    
    # Grupos musculares disponibles en ExerciseDB
    muscle_groups = {
        "🔙 Espalda": "back",
        "🫁 Cardio": "cardio",
        "🫀 Pecho": "chest",
        "🦵 Piernas": "lower legs",
        "💪 Brazos": "upper arms",
        "🦴 Antebrazo": "lower arms",
        "🎯 Core": "waist",
        "🦴 Cuello": "neck",
        "💪 Hombros": "shoulders"
    }
    
    # Combobox para seleccionar músculo
    muscle_combo = ttk.Combobox(filter_frame, values=list(muscle_groups.keys()), 
                               font=('Segoe UI', 11), state='readonly', width=28)
    muscle_combo.set("🫀 Pecho")
    muscle_combo.pack(fill="x", pady=(0, 15))
    
    # Botón de buscar
    btn_search = ttk.Button(filter_frame, text="🔍 Buscar Ejercicio", 
                           style='Search.TButton')
    btn_search.pack(fill="x")
    
    ttk.Separator(card, orient='horizontal').pack(fill='x', pady=(15, 10))
    
    # Área de ejercicios
    ttk.Label(card, text="📋 Ejercicio recomendado:", background=CARD_BG, 
             foreground=TEXT_COLOR, font=('Segoe UI', 10, 'bold')).pack(anchor="w", pady=(0, 5))
    
    exercise_text = scrolledtext.ScrolledText(card, height=13, width=50, 
                                             font=('Segoe UI', 10), wrap="word",
                                             relief="solid", borderwidth=1, state="disabled")
    exercise_text.pack(fill="both", expand=True, pady=(0, 15))
    
    def get_exercise_from_api():
        """Obtener ejercicios desde ExerciseDB API en RapidAPI"""
        # Obtener valores seleccionados
        muscle_display = muscle_combo.get()
        body_part = muscle_groups[muscle_display]
        
        # Deshabilitar botón mientras procesa
        btn_search.config(state="disabled", text="⏳ Buscando...")
        advisor_win.update()
        
        try:
            # RapidAPI - ExerciseDB (GRATIS)
            # Regístrate gratis en: https://rapidapi.com/justin-WFnsXH_t6/api/exercisedb
            RAPIDAPI_KEY = "4ff799e70cmsh9d43fe4de05a16dp1c69c7jsncea1e17ad287"  # Reemplaza con tu key de RapidAPI
            
            # Buscar por parte del cuerpo
            api_url = f"https://exercisedb.p.rapidapi.com/exercises/bodyPart/{body_part}"
            
            print(f"Consultando: {api_url}")  # Debug
            print(f"Grupo muscular: {muscle_display}")  # Debug
            
            # Headers requeridos por RapidAPI
            headers = {
                'X-RapidAPI-Key': RAPIDAPI_KEY,
                'X-RapidAPI-Host': 'exercisedb.p.rapidapi.com'
            }
            
            # Hacer petición HTTP
            req = urllib.request.Request(api_url, headers=headers)
            
            with urllib.request.urlopen(req, timeout=15) as response:
                result = response.read().decode('utf-8')
                print(f"Código: {response.getcode()}")  # Debug
                
                exercises = json.loads(result)
                
                if exercises and len(exercises) > 0:
                    print(f"Ejercicios encontrados: {len(exercises)}")  # Debug
                    
                    # Seleccionar un ejercicio aleatorio
                    exercise = random.choice(exercises[:30])  # De los primeros 30
                    
                    # Formatear la respuesta
                    exercise_text.config(state="normal")
                    exercise_text.delete("1.0", tk.END)
                    
                    # Título del ejercicio
                    name = exercise.get('name', 'Sin nombre').upper()
                    exercise_text.insert(tk.END, f"🏋️ {name}\n\n", "title")
                    
                    # Información básica
                    exercise_text.insert(tk.END, "📊 INFORMACIÓN\n", "subtitle")
                    exercise_text.insert(tk.END, f"• Zona: {muscle_display}\n")
                    
                    target = exercise.get('target', 'N/A').replace('_', ' ').title()
                    exercise_text.insert(tk.END, f"• Músculo objetivo: {target}\n")
                    
                    equip = exercise.get('equipment', 'N/A').replace('_', ' ').title()
                    exercise_text.insert(tk.END, f"• Equipo: {equip}\n\n")
                    
                    # Músculos secundarios
                    secondary = exercise.get('secondaryMuscles', [])
                    if secondary:
                        secondary_names = [s.replace('_', ' ').title() for s in secondary]
                        exercise_text.insert(tk.END, f"• Músculos secundarios: {', '.join(secondary_names)}\n\n")
                    
                    # Separador
                    exercise_text.insert(tk.END, "─" * 65 + "\n\n")
                    
                    # Instrucciones
                    exercise_text.insert(tk.END, "📝 INSTRUCCIONES\n\n", "subtitle")
                    instructions = exercise.get('instructions', [])
                    
                    if instructions:
                        for i, instruction in enumerate(instructions, 1):
                            exercise_text.insert(tk.END, f"{i}. {instruction}\n\n")
                    else:
                        exercise_text.insert(tk.END, "No hay instrucciones disponibles.\n\n")
                    
                    # Separador
                    exercise_text.insert(tk.END, "─" * 65 + "\n\n")
                    
                    # Imagen GIF
                    gif_url = exercise.get('gifUrl', '')
                    if gif_url:
                        exercise_text.insert(tk.END, "🎬 DEMOSTRACIÓN\n\n", "subtitle")
                        exercise_text.insert(tk.END, f"Ver animación del ejercicio:\n{gif_url}\n\n")
                        exercise_text.insert(tk.END, "─" * 65 + "\n\n")
                    
                    # Consejos generales
                    exercise_text.insert(tk.END, "💡 CONSEJOS IMPORTANTES\n\n", "subtitle")
                    exercise_text.insert(tk.END, 
                        "• Realiza un calentamiento de 5-10 minutos antes de comenzar.\n"
                        "• Mantén una buena técnica para evitar lesiones.\n"
                        "• Mantente hidratado durante todo el entrenamiento.\n"
                        "• Si sientes dolor (no molestia), detente inmediatamente.\n"
                        "• Descansa 48 horas entre entrenamientos del mismo grupo muscular.")
                    
                    # Configurar estilos de texto
                    exercise_text.tag_config("title", font=('Segoe UI', 12, 'bold'), foreground='#0066cc')
                    exercise_text.tag_config("subtitle", font=('Segoe UI', 10, 'bold'), foreground='#28a745')
                    
                    exercise_text.config(state="disabled")
                    
                    print("✓ Ejercicio mostrado exitosamente")  # Debug
                    
                else:
                    raise Exception("No se encontraron ejercicios")
                    
        except urllib.error.HTTPError as e:
            error_body = ""
            try:
                error_body = e.read().decode('utf-8')
            except:
                pass
            
            error_msg = f"Error HTTP {e.code}: {e.reason}"
            print(f"❌ {error_msg}\n{error_body}")  # Debug
            
            if e.code == 401 or e.code == 403:
                messagebox.showerror("Error de autenticación", 
                                   "Tu API Key de RapidAPI es inválida o no está configurada.\n\n"
                                   "Pasos para obtener tu key GRATIS:\n"
                                   "1. Ve a rapidapi.com\n"
                                   "2. Regístrate gratis\n"
                                   "3. Busca 'ExerciseDB'\n"
                                   "4. Suscríbete al plan GRATIS (sin tarjeta)\n"
                                   "5. Copia tu API Key y reemplázala en el código",
                                   parent=advisor_win)
            elif e.code == 429:
                messagebox.showerror("Límite excedido", 
                                   "Has excedido el límite de peticiones gratuitas.\n\n"
                                   "El plan gratuito permite 10,000 peticiones/mes.\n"
                                   "Espera un momento antes de intentar de nuevo.",
                                   parent=advisor_win)
            else:
                messagebox.showerror("Error", error_msg, parent=advisor_win)
        
        except urllib.error.URLError as e:
            print(f"❌ Error de conexión: {str(e.reason)}")
            messagebox.showerror("Error de conexión", 
                               "No se pudo conectar a internet.\n\n"
                               "Verifica tu conexión y vuelve a intentar.",
                               parent=advisor_win)
        
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            exercise_text.config(state="normal")
            exercise_text.delete("1.0", tk.END)
            exercise_text.insert(tk.END, "❌ SIN RESULTADOS\n\n", "error")
            exercise_text.insert(tk.END, 
                f"No se encontraron ejercicios para:\n\n"
                f"• Zona: {muscle_display}\n\n"
                f"Por favor, intenta con otro grupo muscular o revisa tu conexión.")
            exercise_text.tag_config("error", font=('Segoe UI', 12, 'bold'), foreground='#dc3545')
            exercise_text.config(state="disabled")
        
        finally:
            btn_search.config(state="normal", text="🔍 Buscar Ejercicio")
    
    # Asignar comando al botón de buscar
    btn_search.config(command=get_exercise_from_api)
    
    # Frame de botones inferiores
    btn_frame = ttk.Frame(card, style='AdviceCard.TFrame')
    btn_frame.pack(fill="x", pady=(10, 0))
    
    ttk.Button(btn_frame, text="✕ Cerrar", command=advisor_win.destroy, 
              style='Close.TButton').pack(fill="x")


def open_WOList(parent: tk.Tk, return_to=None):
    win = tk.Toplevel(parent)
    win.title("Elige tu ejercicio")
    win.geometry("500x450")
    win.resizable(False, False)
    
    # Colores
    BG_COLOR = "#f0f0f0"
    CARD_BG = "#ffffff"
    PRIMARY_COLOR = "#0066cc"
    SUCCESS_COLOR = "#28a745"
    WARNING_COLOR = "#ffc107"
    DANGER_COLOR = "#dc3545"
    TEXT_COLOR = "#212529"
    ADVICE_COLOR = "#28a745"
    
    win.configure(bg=BG_COLOR)
    
    # Estilos
    style = ttk.Style()
    style.theme_use('clam')
    
    style.configure('Card.TFrame', background=CARD_BG)
    style.configure('Footer.TFrame', background=CARD_BG)
    style.configure('Title.TLabel', background=CARD_BG, foreground=TEXT_COLOR, 
                   font=('Segoe UI', 14, 'bold'))
    
    # Botones de ejercicios
    style.configure('Easy.TButton', background=SUCCESS_COLOR, foreground='white', 
                   font=('Segoe UI', 10, 'bold'), borderwidth=0, padding=(20, 12))
    style.map('Easy.TButton', background=[('active', '#218838')])
    
    style.configure('Medium.TButton', background=WARNING_COLOR, foreground='#212529', 
                   font=('Segoe UI', 10, 'bold'), borderwidth=0, padding=(20, 12))
    style.map('Medium.TButton', background=[('active', '#e0a800')])
    
    style.configure('Hard.TButton', background=DANGER_COLOR, foreground='white', 
                   font=('Segoe UI', 10, 'bold'), borderwidth=0, padding=(20, 12))
    style.map('Hard.TButton', background=[('active', '#c82333')])
    
    # Botones del footer
    style.configure('Streak.TButton', background=PRIMARY_COLOR, foreground='white', 
                   font=('Segoe UI', 9, 'bold'), borderwidth=0, padding=(15, 10))
    style.map('Streak.TButton', background=[('active', '#0052a3')])
    
    style.configure('Advice.TButton', background=ADVICE_COLOR, foreground='white', 
                   font=('Segoe UI', 9, 'bold'), borderwidth=0, padding=(15, 10))
    style.map('Advice.TButton', background=[('active', '#218838')])
    
    style.configure('Close.TButton', background='#e9ecef', foreground='#212529', 
                   font=('Segoe UI', 9), borderwidth=0, padding=(15, 10))
    style.map('Close.TButton', background=[('active', '#dee2e6')])
    
    # Contenedor exterior
    outer_container = tk.Frame(win, bg=BG_COLOR)
    outer_container.pack(fill="both", expand=True, padx=30, pady=30)
    
    # Card principal
    frame = ttk.Frame(outer_container, style='Card.TFrame', padding=25)
    frame.pack(fill="both", expand=True)
    
    # Funciones
    def open_and_close(next_func):
        win.destroy()
        next_func(parent, lambda p: open_WOList(p, return_to))
    
    def volver():
        win.destroy()
        if return_to:
            return_to(parent)
    
    # Título
    ttk.Label(frame, text="💪 Elije tu ejercicio", style='Title.TLabel').pack(pady=(0, 20))
    
    # Separador superior
    ttk.Separator(frame, orient='horizontal').pack(fill='x', pady=(0, 20))
    
    # Botones de ejercicios
    ttk.Button(frame, text="🟢  Ejercicio Facil", 
              command=lambda: open_and_close(open_E1), 
              style='Easy.TButton').pack(pady=6, fill="x")
    
    ttk.Button(frame, text="🟡  Ejercicio Intermedio", 
              command=lambda: open_and_close(open_E2), 
              style='Medium.TButton').pack(pady=6, fill="x")
    
    ttk.Button(frame, text="🔴  Ejercicio Dificil", 
              command=lambda: open_and_close(open_E3), 
              style='Hard.TButton').pack(pady=6, fill="x")
    
    # Separador
    ttk.Separator(frame).pack(pady=20, fill="x")
    
    # Footer con 3 botones
    footer = ttk.Frame(frame, style='Footer.TFrame')
    footer.pack(fill="x", side="bottom", pady=(8, 0))
    
    # Botón racha (izquierda)
    ttk.Button(footer, text="🔥 racha", 
              command=lambda: open_week_calendar(win),
              style='Streak.TButton').pack(side="left", padx=(0, 5))
    
    # Botón Consejos (centro)
    ttk.Button(footer, text="💡 Consejos", 
              command=lambda: open_exercise_advisor(win),
              style='Advice.TButton').pack(side="left", padx=5)
    
    # Botón Cerrar (derecha)
    ttk.Button(footer, text="✕  Cerrar", 
              command=volver,
              style='Close.TButton').pack(side="right")
