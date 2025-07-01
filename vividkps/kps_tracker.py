## KPS Tracker
import tkinter as tk
import PIL
import tkextrafont
import os
import PIL.ImageTk
import PIL.Image
import keyboard
import time
import configparser
from keyboard._keyboard_event import KEY_DOWN, KEY_UP
from tkinter import font
from ctypes import windll
### Flags
### Global Image Mode Flags: Allows the setting of images as keys.
Image_Mode_Flag = True
Disable_Topbar_Flag = True

### Helper function for local file addresses 
def local_file_address(filename): 
    directory = os.path.dirname(__file__) #gets parent directory of script
    return directory + "\\" + filename

###Tkinter Definition
window = tk.Tk()
window.title("vivid/kps")
window.resizable(width=False,height=False)
window.config(bg="black")
window.attributes("-topmost", True)
### Custom Font
custom_font = tkextrafont.Font(file=local_file_address('monaco-9.ttf'),family="Monaco 9")

# Image Path Configuration
# expected to be PIL images from the getgo. 
class Image_Paths: 
    #the overall file structure should be good with Python\vividkps\filename; however in case it dosent work; 
    #the overall code structure is PIL.Image.open("fileaddress")
    # note that python escapes backslashes (\), so you need two like this \\ to properly make it work
    #if you want to add more images, without knowing what this does
    # just do PIL.Image.open(f"{image_folder}filenamehere"")
    image_folder = ""
    def Path_to_Pil(path): 
        return PIL.ImageTk.PhotoImage(PIL.Image.open(path).resize((130,130),1))
    image1_idle = Path_to_Pil(local_file_address(f"{image_folder}smart_shit.jpg"))
    image1_pressed = Path_to_Pil(local_file_address(f"{image_folder}smart_fuck.jpg"))
    image2_idle = Path_to_Pil(local_file_address(f"{image_folder}stupid_shit.jpg"))
    image2_pressed = Path_to_Pil(local_file_address(f"{image_folder}stupid_fuck.jpg"))
## Image Definition Function
def Image_Discrimination(key_index, pressed_state): 
    ## Manually set these when pertaining to Image_Paths. 
    ## key_index pertains to the direct indexes of the keys pertained; which can be obtained by:
    ## RG_Configs.keys.index(widget_to_edit.key)
    ## state relates to if this is meant to return a "pressed" or a "idle" sprite.
    global Image_Paths
    ## if looking for an pressed image 
    if pressed_state == True: 
        if key_index in [0,1]: 
            return Image_Paths.image1_pressed
        elif key_index in [2,3]: 
            return Image_Paths.image2_pressed
    elif pressed_state == False: 
        if key_index in [0,1]: 
            return Image_Paths.image1_idle
        elif key_index in [2,3]: 
            return Image_Paths.image2_idle

###Data Classes
class kps_button: 
    #Contains the following Data:
    #Data: .key, .color, .text_color, .key_position
    #Tkinter: .button_frame, .label
    # .label only exists if Image_Mode_Flag is false; else it does NOT exist. 
    # 
    def __init__(self, key, color, key_position,window,text_color,image_path=""):
        global Image_Mode_Flag
        global custom_font
        ## .key value can be used to index position of key within structure. 
        self.key = key
        self.color = color
        self.text_color = text_color
        self.key_position = key_position
        
        ## Image Path only required if Image_Mode_Flag is active.
        self.image_path = image_path
        ##Tkinter Styling - Frame Styling  
        if Image_Mode_Flag == False: 
            self.button_frame = tk.Frame(window, bg=self.color, width=130, height=50)
            self.button_frame.grid(row=0,rowspan=2,column=self.key_position,sticky="nsew",padx=0,pady=0,)
            ##Label Styling
            self.label = tk.Label(self.button_frame,text=self.key, bg=self.color,fg=self.text_color)
            self.label.pack(expand=True)
            self.label.config(font=("Monaco 9",-40),width=7,height=4)
            window.grid_columnconfigure(self.key_position,weight=1,minsize=130)
            window.grid_rowconfigure(0,weight=1,minsize=130)
        elif Image_Mode_Flag == True: 
            self.button_frame = tk.Frame(window, width=130, height=50,bg=self.color)
            self.button_frame.grid(row=0,rowspan=2,column=self.key_position,sticky="nsew",padx=0,pady=0,)
            self.label = tk.Label(self.button_frame, image=self.image_path, bg=self.color)
            self.label.pack(expand=True)
            window.grid_columnconfigure(self.key_position,weight=1,minsize=130)
            window.grid_rowconfigure(0,weight=1,minsize=130)

class rhythm_game_configs: 
    def __init__(self,keys): 
        
        buffer = []

        self.keys = keys #allowed / accepted keys
        for i in range (len(keys)): 
            buffer.append(0)
        self.keys_pressed = buffer

    keys_pressed_log = []
    #default colors
    key_bg_color = "black"
    key_text_color = "white"

    #onclick colors
    on_key_click_bg = "white"
    on_key_click_fg = "black"

class kps_component: 
    global rhythm_game_configs
    kps_label = tk.Label(window,text="testing",bg="black",fg="white")
    kps_label.grid(row=2,column=0,columnspan=2,pady=6)
    keys_pressed_label = tk.Label(window,text="testing",bg="black",fg="white")
    keys_pressed_label.grid(row=2,column=2,columnspan=2,pady=6)

input_keys = "qw[]"
RG_Configs = rhythm_game_configs(input_keys)

KeyButtonTable = []
### Key Population Function
### Uses config class object to populate set.. hopefully.
def generate_keys(config  = RG_Configs, state = False):
    global rhythm_game_configs
    global window
    global KeyButtonTable
    counter = 0 #set to initial position
    for i in config.keys: 
        
        KeyButtonTable.append(kps_button(i,rhythm_game_configs.key_bg_color,counter,window,rhythm_game_configs.key_text_color,image_path=Image_Discrimination(config.keys.index(i),False)))
        if state: 
            KeyButtonTable[counter].label.config(text=f"{KeyButtonTable[counter].key}\n{RG_Configs.keys_pressed[counter]}")
        counter += 1
    




#Basically changes the color, then reverts it back after an interval
def key_button_press_highlight(widget_to_edit, bg_color=RG_Configs.on_key_click_bg, foreground_color=RG_Configs.on_key_click_fg,state=False):
    global RG_Configs
    global Image_Mode_Flag
    global window
    #widget_to_edit.button_frame.config(bg=bg_color)
    widget_to_edit.label.config(bg=bg_color)
    #widget_to_edit.label.config(fg=foreground_color)
    if Image_Mode_Flag == False: 
        
        

        widget_to_edit.label.config(text=f"{widget_to_edit.key}\n{RG_Configs.keys_pressed[RG_Configs.keys.index(widget_to_edit.key)]}",fg=foreground_color)
    elif Image_Mode_Flag == True: 
        widget_to_edit.label.config(image=Image_Discrimination(RG_Configs.keys.index(widget_to_edit.key),state))


#rhythm game input section
class kps_values:
    kps=0
    peak_kps = 0
    total_keys_pressed = 0
    def set_kps(value): 
        kps_values.kps = value
        kps_component.kps_label.config(text=f"KPS: {kps_values.kps}\nPeak:{kps_values.peak_kps}\nTotal:{kps_values.total_keys_pressed}")
    def set_peak_kps(value):
        kps_values.peak_kps = value
        kps_component.kps_label.config(text=f"KPS: {kps_values.kps}\nPeak:{kps_values.peak_kps}\nTotal:{kps_values.total_keys_pressed}")
    def set_total_keys_pressed(value):
        kps_values.total_keys_pressed = value
        kps_component.kps_label.config(text=f"KPS: {kps_values.kps}\nPeak:{kps_values.peak_kps}\nTotal:{kps_values.total_keys_pressed}")
        print("test")

def rg_keyinput(event):
    global RG_Configs
    global KeyButtonTable
    global Image_Mode_Flag
    if event.name.lower() in RG_Configs.keys: 
        key_button_press_highlight(KeyButtonTable[RG_Configs.keys.index(event.name)],state=True)
    
def rg_keyrelease(event):
    global RG_Configs
    global KeyButtonTable
    global Image_Mode_Flag
    if event.name.lower() in RG_Configs.keys: 
        print(event.name)
        RG_Configs.keys_pressed[RG_Configs.keys.index(event.name)] += 1
        RG_Configs.keys_pressed_log.append([event.name,event.time])
        key_button_press_highlight(KeyButtonTable[RG_Configs.keys.index(event.name)],RG_Configs.key_bg_color,RG_Configs.key_text_color,False)
        kps_values.total_keys_pressed += 1
### KPS managing code

     
def update_kps(): 
    global kps_component
    global window
    global kps_values
    global custom_font
    current_time=time.time()
    global RG_Configs
    for i in RG_Configs.keys_pressed_log: 
        if abs(current_time-i[1]) > 1: #checks if key was pressed more than a second ago
            RG_Configs.keys_pressed_log.remove(i) #if so, remove key from list
    kps_values.kps = len(RG_Configs.keys_pressed_log)
    if kps_values.kps > kps_values.peak_kps: 
        kps_values.peak_kps = kps_values.kps

    kps_component.kps_label.config(text=f"KPS: {kps_values.kps} (Peak: {kps_values.peak_kps})",font=("Monaco 9",-20))
    kps_component.keys_pressed_label.config(text=f"Total: {kps_values.total_keys_pressed}",font=("Monaco 9",-20))
    window.after(70,update_kps)

#solution for not having hooks properly work
#taken from https://stackoverflow.com/questions/74246583/python-why-cant-the-on-release-function-from-the-keyboard-module-detect-anythi
def on_action(event):
    if event.event_type == KEY_DOWN:
        rg_keyinput(event)

    elif event.event_type == KEY_UP:
        rg_keyrelease(event)

def on_press(key):
    print(f"Pressed:  {key}")

def on_release(key):
    print(f"Released: {key}")

keyboard.hook(lambda e: on_action(e))
window.after(100,update_kps)

### Menu Management
##Value Setting function

def Menu_Click_Hander(Setting_Type, state):
    global Image_Mode_Flag
    global KeyButtonTable
    global window
    if Setting_Type=="Image": 
        if state.get() == False:
            for i in KeyButtonTable: 
                i.button_frame.grid_forget()
                i.label.pack_forget()
            KeyButtonTable = []
            Image_Mode_Flag = False
            generate_keys(state=True)
        elif state.get() == True:
            for i in KeyButtonTable: 
                i.button_frame.grid_forget()
                i.label.pack_forget()
            KeyButtonTable = []
            Image_Mode_Flag = True
            generate_keys(state=True)
    elif Setting_Type == "Topbar":
        if state.get() == False: 
            print("topbar off")
            window.overrideredirect(True)
        elif state.get() == True:
            print("topbar on")
            window.overrideredirect(False)
    elif Setting_Type == "Keep Ontop": 
        window.attributes("-topmost", state.get())
        
                
Command_Menu = tk.Menu(window,tearoff=0)
Image_Setting = tk.BooleanVar(window,value=True)
Topbar_Setting = tk.BooleanVar(window,value = True)
Keep_On_Top_Setting = tk.BooleanVar(window,value=True)
Command_Menu.config()
KPS_menu = tk.Menu(Command_Menu,tearoff=0)
KPS_menu.add_command(label="Reset KPS", command=lambda:kps_values.set_kps(value=0))
KPS_menu.add_command(label="Reset Peak KPS", command=lambda:kps_values.set_peak_kps(value=0))
KPS_menu.add_command(label="Reset Total Keys Pressed", command=lambda:kps_values.set_total_keys_pressed(value=0))
Command_Menu.add_cascade(menu=KPS_menu,label="KPS Settings")

#Command_Menu.add_cascade(KPS_menu)


Command_Menu.add_checkbutton(label="Enable Images",variable=Image_Setting, onvalue=True,offvalue=False,command=lambda:Menu_Click_Hander("Image", Image_Setting) )
Command_Menu.add_checkbutton(label="Enable Topbar",variable=Topbar_Setting, onvalue=True,offvalue=False,command=lambda:Menu_Click_Hander("Topbar", Topbar_Setting) )
Command_Menu.add_checkbutton(label="Keep Ontop",variable=Keep_On_Top_Setting, onvalue=True,offvalue=False,command=lambda:Menu_Click_Hander("Keep Ontop", Keep_On_Top_Setting) )
def show_menu(event):
    Command_Menu.post(event.x_root+10, event.y_root-10)

Command_Menu.add_separator()
Command_Menu.add_command(label="Exit", command=window.quit)
window.bind("<Button-3>",show_menu)

### Draggable mecahnism
# --- Global variables to store drag state ---
# (These need to be outside any function that modifies them,
# or you'll need the 'global' keyword inside the functions)
drag_x = 0
drag_y = 0

# --- Functions for dragging ---

def start_drag(event):
    global drag_x, drag_y
    # Store the initial mouse position relative to the window's top-left corner
    # event.x and event.y are relative to the widget that received the event
    drag_x = event.x
    drag_y = event.y
    # print(f"Drag started: event.x={event.x}, event.y={event.y}")

def do_drag(event):
    # Calculate the new window position
    # event.x_root and event.y_root are absolute screen coordinates of the mouse
    # Subtract the initial click offset to keep the same grab point
    new_x = event.x_root - drag_x
    new_y = event.y_root - drag_y

    # Update the window's position
    window.geometry(f"+{new_x}+{new_y}")
    # print(f"Dragging to: {new_x}, {new_y}")

def stop_drag(event):
    global drag_x, drag_y
    # Reset drag variables (optional, good practice)
    drag_x = 0
    drag_y = 0
    # print("Drag stopped")
window.bind("<Button-1>", start_drag)
window.bind("<B1-Motion>", do_drag)
window.bind("<ButtonRelease-1>", stop_drag)


### main Program

generate_keys()
#KeyButtonTable[0].label.config(image=PIL.ImageTk.PhotoImage(PIL.Image.open("C:\\Users\\plcau\\Documents\\vividkps\\image-68.jpg")))
#keyboard.on_press(rg_keyinput)
#keyboard.on_release(rg_keyrelease,)
#@button1 = kps_button("A","red",0,window)
#button2 = kps_button("b","blue",1,window)
window.mainloop()