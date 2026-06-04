import pyautogui
from tkinter import *
from tkinter import ttk
import threading
import time
from pynput import mouse, keyboard

pyautogui.FAILSAFE = True
root = Tk() #Janela
root.title("Fast Mouse")
root.geometry("500x300")
root.iconbitmap("rat_icon.ico")
root.resizable(width=False, height=False)

# --- Variáveis para transferir a posição com segurança ---
captured_x = 0
captured_y = 0

# --- Função ativada pelo Evento Virtual ---
def atualizar_interface_captura(event=None):
    Value1_entry.set(str(int(captured_x)))
    Value1_entry2.set(str(int(captured_y)))
    Value1.set(1) # Muda a bolinha para "Pick Location" automaticamente
    root.deiconify()   # Restaura a janela
    root.focus_force() # Puxa a janela para a frente de tudo

# --- Criando o evento customizado ---
root.bind("<<LocationPicked>>", atualizar_interface_captura)

#----------------------------------Functions---------------------------------------------------#
start_btn = None
stop_btn = None
running = False
total_sec = 0
hotkey_atual = "f6" 

def start_clicking():
    global running, total_sec
    if running: return 
    running = True
    total_sec = (float(hr_val.get())*3600) + (float(min_val.get())*60) + (float(sec_val.get())) + (float(mili_val.get())/1000)
    thread = threading.Thread(target=loop_clicking, daemon=True)
    thread.start()

def loop_clicking():
    while running:
        if Value1.get() == 0:
            pyautogui.click(interval=total_sec)
        elif Value1.get() == 1:
            pyautogui.click(x=int(Entry_x.get()) , y=int(Entry_y.get()), interval=total_sec)

def stop_cliking():
    global running
    running = False

def capturar_tecla(event):
    htk.set(event.keysym)
    hotkey_label.config(state="readonly")
    nova_janela.unbind("<Key>")

def aguardar_hotkey():
    global hotkey_label
    hotkey_label.config(state="normal")
    htk.set("Waiting...")
    hotkey_label.config(state="readonly")
    nova_janela.bind("<Key>", capturar_tecla)

def salvar_hotkey():
    global hotkey_atual
    key = htk.get()
    hotkey_atual = key.lower()
    
    start_btn.config(text=f"Start ({key})")
    stop_btn.config(text=f"Stop ({key})")
    nova_janela.destroy()

def abrir_nova_janela():
    global nova_janela, hotkey_label, htk, waiting_label
    nova_janela = Toplevel(root)
    nova_janela.title("Hotkeys Settings")
    nova_janela.geometry("300x150")
    nova_janela.iconbitmap("rat_icon.ico")
    
    htk = StringVar(value=hotkey_atual.upper()) 
    hotkey_label = ttk.Entry(nova_janela, textvariable=htk, width=10)
    hotkey_label.grid(column=1, row=0, padx=10, pady=10)
    hotkey_label.config(state="readonly")

    waiting_label = ttk.Label(nova_janela, text="")
    waiting_label.grid(column=0, row=2, columnspan=2)

    stt = ttk.Button(nova_janela, text="Start / Stop", command=aguardar_hotkey)
    stt.grid(column=0, row=0, padx=10, pady=10)
    ok = ttk.Button(nova_janela, text="Ok", command=salvar_hotkey)
    ok.grid(column=0, row=1, padx=10, pady=10)
    cancel = ttk.Button(nova_janela, text="Cancel", command=nova_janela.destroy)
    cancel.grid(column=1, row=1, padx=10, pady=10)
    
def pick_location():
    thread = threading.Thread(target=_pick_location_thread, daemon=True)
    thread.start()

def _pick_location_thread():
    global captured_x, captured_y
    stop_cliking()
    root.after(0, root.iconify) 
    time.sleep(0.2) # Apenas 0.2s para a janela minimizar
    
    def on_click(x, y, button, pressed):
        global captured_x, captured_y
        if pressed and button == mouse.Button.left:
            captured_x, captured_y = x, y
            root.event_generate("<<LocationPicked>>", when="tail")
            return False # Encerra o listener no primeiro clique
    
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

#----------------------------------------------------------------------------------------------#
hr_val = StringVar(value="0")
min_val = StringVar(value="0")
sec_val = StringVar(value="0")
mili_val = StringVar(value="100")
frm = ttk.Labelframe(root, padding=10, text="Click Interval") 
frm.grid(row=0, sticky='ew')

Entry_hr = ttk.Entry(frm, width=10, justify="left", textvariable=hr_val) 
Entry_hr.grid(column=0, row=0) 
ttk.Label(frm, text="Hours").grid(column=1, row=0) 
Entry_min = ttk.Entry(frm, width=10, justify="left", textvariable=min_val)
Entry_min.grid(column=2, row=0) 
ttk.Label(frm, text="Minutes").grid(column=3, row=0)
Entry_sec = ttk.Entry(frm, width=10, justify="left", textvariable=sec_val) 
Entry_sec.grid(column=4, row=0)
ttk.Label(frm, text="Seconds").grid(column=5, row=0)
Entry_milisec = ttk.Entry(frm, width=10, justify="left", textvariable=mili_val)
Entry_milisec.grid(column=6, row=0)
ttk.Label(frm, text="Miliseconds").grid(column=7, row=0)
#----------------------------------------------------------------------------------------------#

frm_mouse = ttk.Labelframe(root, padding=10, text="Cursor position")
frm_mouse.grid(pady=10, sticky="ew", row=1) 

Value1 = IntVar()
check_current_location = ttk.Radiobutton(frm_mouse, text="Current location",variable=Value1, value=0)
check_current_location.grid(column=0, row=0) 

Value1_entry = StringVar(value="0")
Value1_entry2 = StringVar(value="0")

pick_location_radio_button = ttk.Radiobutton(frm_mouse, variable=Value1, value=1)
pick_location_radio_button.grid(column=1, row=0, padx=(60,0)) 
pick_location_btn = ttk.Button(frm_mouse, text="Pick Location", command=pick_location)
pick_location_btn.grid(column=2, row=0, ipady=5, padx=(0, 10))

ttk.Label(frm_mouse, text="X").grid(column=3, row=0)
Entry_x = ttk.Entry(frm_mouse, width=10,textvariable=Value1_entry)
Entry_x.grid(column=4, row=0,)

ttk.Label(frm_mouse, text="Y").grid(column=5, row=0)
Entry_y = ttk.Entry(frm_mouse, width=10, textvariable=Value1_entry2)
Entry_y.grid(column=6, row=0)

#----------------------------------------------------------------------------------------------#
frm_buttons = ttk.Labelframe(root, padding=10, text="Options")
frm_buttons.grid(row=2, sticky="ew")
frm_buttons.columnconfigure(0, weight=1)
frm_buttons.columnconfigure(1, weight=1)

start_btn = ttk.Button(frm_buttons, text=f"Start (F6)", command=start_clicking)
start_btn.grid(column=0, row=0, ipady=10, sticky="ew", padx=5)
stop_btn = ttk.Button(frm_buttons, text=f"Stop (F6)", command=stop_cliking)
stop_btn.grid(column=1, row=0, ipady=10, sticky="ew", padx=5)
hotkey_btn = ttk.Button(frm_buttons, text=f"Hotkey Setting", command=abrir_nova_janela)
hotkey_btn.grid(column=0, row=1, ipady=10, sticky="ew", padx=5)
quit_btn = ttk.Button(frm_buttons, text=f"Quit", command=root.destroy)
quit_btn.grid(column=1, row=1, ipady=10, sticky="ew", padx=5)

#------------------------------GLOBAL HOTKEY LISTENER------------------------------------------#
def on_press(key):
    try:
        alvo = hotkey_atual.lower()
        
        if hasattr(key, 'name') and key.name is not None:
            tecla_pressionada = key.name.lower()
        elif hasattr(key, 'char') and key.char is not None:
            tecla_pressionada = key.char.lower()
        else:
            tecla_pressionada = ""

        if tecla_pressionada == alvo:
            if not running:
                root.after(0, start_clicking) 
            else:
                root.after(0, stop_cliking)
    except Exception as e:
        pass # Removi o print do erro para o terminal ficar limpo

listener_kb = keyboard.Listener(on_press=on_press, daemon=True)
listener_kb.start()

root.mainloop()