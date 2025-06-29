# Python3.8.10にて動作確認。
# MemoryWatcher - v1.0
# By ReaZ0n23 (2025)

from os import path
from tkinter import ttk
import customtkinter as ctk
import struct
import time
import sys
from citra import Citra

c = Citra()

#####################
# Initialize
SCRIPTNAME = "Citra Memory Watcher"
VERSION = 1.0
DEVELOPER = "ReaZ0n23"
currentDir = path.dirname(__file__)
path_appearance_color = "{}/Appearance/Colors/".format(currentDir)
path_file_history = "{}/mw-history.csv".format(currentDir)
path_file_mwconfig = "{}/mw-config.ini".format(currentDir)
List_config_Address = []
List_config_Type = []
List_config_Value = []
List_config_Note = []
Dict_config = {}
DataTypes = ["int(bit)", "int(Byte)", "int(DEC)", "int(HEX)", "short", "long",
    "uint(Byte)", "uint(HEX)", "ushort", "ulong",
     "float", "double", "char(ASCII)", "char(Unicode)", "Pointer"]
isPlay = False
# GUI
THEME_DARK_BG = "#2b2b2b"
THEME_DARK_FG = "#ffffff"
THEME_DARK_SEL = "#3a3a3a"
THEME_LIGHT_BG = "#d5d5d5"
THEME_LIGHT_FG = "#000000"
THEME_LIGHT_SEL = "#a5a5e0"
Appearance_Color =["blue", "dark-blue", "green", "red", "magenta", "purple", "torquoise"]
Appearance_Theme =["System", "Light", "Dark"]
font_normal = ("Yu Gothic Medium", 11, "normal")
font_bold = ("Yu Gothic Medium", 11, "bold")

#####################
# Window - Main
def create_window():
    global root
    try:
        ctk.set_appearance_mode(Dict_config["Theme"])
        ctk.set_default_color_theme(Dict_config["Color"] if Dict_config["Color"] in ("blue", "green", "dark-blue") else path_appearance_color + "{}.json".format(Dict_config["Color"]))
    except KeyError:
        print("mw-config.ini is broken.")
        save_mwconfig(mode="new")
    root = ctk.CTk()
    root.geometry('512x256+400+520')  # サイズと初期位置指定
    root.title("{} | v{}".format(SCRIPTNAME , VERSION))
    root.attributes("-topmost", True)  # ウインドウを常に最前面
    ctk.CTkFont._default_font = ctk.CTkFont("Yu Gothic Medium")
    root.option_add("*font", font_normal)
    # Appearance for Treeview
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview",
                    background=THEME_DARK_BG if ctk.get_appearance_mode() == "Dark" else THEME_LIGHT_BG,
                    foreground=THEME_DARK_FG if ctk.get_appearance_mode() == "Dark" else THEME_LIGHT_FG,
                    fieldbackground=THEME_DARK_BG if ctk.get_appearance_mode() == "Dark" else THEME_LIGHT_BG,
                    rowheight=25,
                    font=("Yu Gothic Medium", 11))
    style.map("Treeview",
            background=[('selected', THEME_DARK_SEL if ctk.get_appearance_mode() == "Dark" else THEME_LIGHT_SEL)],
            foreground=[('selected', THEME_DARK_FG if ctk.get_appearance_mode() == "Dark" else THEME_LIGHT_FG)])
    style.configure("Treeview.Heading",
                    background=THEME_DARK_SEL if ctk.get_appearance_mode() == "Dark" else THEME_LIGHT_BG,
                    foreground=THEME_DARK_FG if ctk.get_appearance_mode() == "Dark" else THEME_LIGHT_FG,
                    font=("Yu Gothic Medium", 11, "bold"))
    style.map("Treeview.Heading",
            background=[("active", THEME_DARK_BG if ctk.get_appearance_mode() == "Dark" else THEME_LIGHT_SEL)],
            foreground=[("active", THEME_DARK_FG if ctk.get_appearance_mode() == "Dark" else THEME_LIGHT_FG)])
# Window - popup
def create_popup(kind="column"):
    if kind == "column":
        global popup_column
        popup_column = ctk.CTkToplevel(root)
        popup_column.geometry('335x464')
        popup_column.title("New Address")
        popup_column.option_add("*font", font_normal)
        popup_column.lift()
        popup_column.focus_force()
        popup_column.transient(root)   # 前面に出す
        popup_column.grab_set()        # メインを操作できなくする
        # Like a Memory compaction
        popup_column.protocol("WM_DELETE_WINDOW", lambda:close_popup(instance=popup_column))
        # Widgets
        popup_column_frame_main = ctk.CTkFrame(popup_column)
        popup_column_frame_main.pack(fill="both", expand=True, padx=10, pady=10)
        popup_column_frame_addr = ctk.CTkFrame(popup_column_frame_main)
        popup_column_frame_addr.pack(fill="both", expand=True, padx=10, pady=10)
        popup_column_label_addr = ctk.CTkLabel(popup_column_frame_addr, text="Address:")
        popup_column_label_addr.pack(side="left", padx=(10,5), pady=10)
        popup_column_entry_addr = ctk.CTkEntry(popup_column_frame_addr, placeholder_text="Input an address to here.")
        popup_column_entry_addr.pack(side="left", fill="x", expand=True, padx=(5, 10), pady=10)
        popup_column_frame_type = ctk.CTkFrame(popup_column_frame_main)
        popup_column_frame_type.pack(fill="both", expand=True, padx=10, pady=10)
        popup_column_label_type = ctk.CTkLabel(popup_column_frame_type, text="Data Type:")
        popup_column_label_type.pack(side="left", padx=(10,5), pady=10)
        popup_column_combo_type = ctk.CTkComboBox(popup_column_frame_type, values=DataTypes)
        popup_column_combo_type.pack(side="left", fill="x", expand=True, padx=(5, 10), pady=10)
        popup_column_frame_note = ctk.CTkFrame(popup_column_frame_main)
        popup_column_frame_note.pack(fill="both", expand=True, padx=10, pady=10)
        popup_column_label_note = ctk.CTkLabel(popup_column_frame_note, text="Note:")
        popup_column_label_note.pack(side="left", padx=(10,5), pady=10)
        popup_column_entry_note = ctk.CTkEntry(popup_column_frame_note, placeholder_text="Input some notes to here.")
        popup_column_entry_note.pack(side="left", fill="x", expand=True, padx=(5, 10), pady=10)
        popup_column_button_cancel = ctk.CTkButton(master=popup_column_frame_main, width=60, text="Cancel", font=font_bold, command=lambda:close_popup(instance=popup_column))
        popup_column_button_cancel.pack(side="right", padx=(5,10))
        popup_column_button_ok = ctk.CTkButton(master=popup_column_frame_main, width=60, text="OK", font=font_bold, command=lambda:close_popup(mode="ok", instance=popup_column, kind="column", args = [popup_column_entry_addr.get(), popup_column_combo_type.get(), popup_column_entry_note.get()]))
        popup_column_button_ok.pack(side="right", padx=(10,5))
    elif kind == "config":
        global popup_config
        popup_config = ctk.CTkToplevel(root)
        popup_config.geometry('335x265')
        popup_config.title("Settings")
        popup_config.option_add("*font", font_normal)
        popup_config.lift()
        popup_config.focus_force()
        popup_config.transient(root)   # 前面に出す
        popup_config.grab_set()        # メインを操作できなくする
        # Like a Memory compaction
        popup_config.protocol("WM_DELETE_WINDOW", lambda:close_popup(instance=popup_config))
        # Widgets
        popup_config_frame_main = ctk.CTkFrame(popup_config)
        popup_config_frame_main.pack(fill="both", expand=True, padx=10, pady=10)

        popup_config_frame_title = ctk.CTkFrame(master=popup_config_frame_main, height=10)
        popup_config_frame_title.pack(fill="x", expand=True, padx=10, pady=(10,5))
        popup_config_label_title = ctk.CTkLabel(master=popup_config_frame_title, text="Settings", font=font_bold)
        popup_config_label_title.pack(side="left", padx=(10,5))

        popup_config_frame_appearance = ctk.CTkFrame(popup_config_frame_main)
        popup_config_frame_appearance.pack(fill="both", expand=True, padx=10, pady=(5,10))
        popup_config_frame_appearance_title = ctk.CTkFrame(popup_config_frame_appearance, corner_radius=0, height=10)
        popup_config_frame_appearance_title.pack(fill="x", expand=True, padx=10, pady=(10,0))
        popup_config_label_appearance = ctk.CTkLabel(master=popup_config_frame_appearance_title, text="Appearance", font=font_bold)
        popup_config_label_appearance.pack(side="left", padx=(10,5))
        popup_config_frame_appearance_theme = ctk.CTkFrame(popup_config_frame_appearance, corner_radius=0)
        popup_config_frame_appearance_theme.pack(fill="both", expand=True, padx=10)
        popup_config_label_appearance_theme = ctk.CTkLabel(master=popup_config_frame_appearance_theme, text="Themes:", font=font_normal)
        popup_config_label_appearance_theme.pack(side="left", padx=(10,5))
        popup_config_combo_appearance_theme = ctk.CTkComboBox(popup_config_frame_appearance_theme, values=Appearance_Theme)
        popup_config_combo_appearance_theme.pack(side="left", fill="x", expand=True, padx=(5, 10), pady=10)
        popup_config_frame_appearance_color = ctk.CTkFrame(popup_config_frame_appearance, corner_radius=0)
        popup_config_frame_appearance_color.pack(fill="x", expand=True, padx=10, pady=(0,10))
        popup_config_label_appearance_color = ctk.CTkLabel(master=popup_config_frame_appearance_color, text="Colors:", font=font_normal)
        popup_config_label_appearance_color.pack(side="left", padx=(10,5))
        popup_config_combo_appearance_color = ctk.CTkComboBox(popup_config_frame_appearance_color, values=Appearance_Color)
        popup_config_combo_appearance_color.pack(side="left", fill="x", expand=True, padx=(5, 10), pady=10)

        popup_config_button_cancel = ctk.CTkButton(master=popup_config_frame_main, width=60, text="Cancel", font=font_bold, command=lambda:close_popup(instance=popup_config))
        popup_config_button_cancel.pack(side="right", padx=(5,10), pady=(5,10))
        popup_config_button_ok = ctk.CTkButton(master=popup_config_frame_main, width=60, text="OK", font=font_bold, command=lambda:close_popup(mode="ok", instance=popup_config, kind="config", args = [popup_config_combo_appearance_theme.get(), popup_config_combo_appearance_color.get()]))
        popup_config_button_ok.pack(side="right", padx=(10,5), pady=(5,10))
        
def close_popup(mode="cancel", instance="", kind="", args=[]):
    instance.destroy()
    if mode == "ok":
        if kind == "column":
            update_table(mode="insert", args=args)
        elif kind == "config":
            global label_messages
            dict_tmp = {}
            dict_tmp["Theme"] = args[0]
            dict_tmp["Color"] = args[1]
            save_mwconfig(mode="overwrite", args=dict_tmp)
            label_messages.configure(text="Restart this script to apply all changes.")

#####################
# Widgets
def setup_widgets(mode="all"):
    global root, List_config_Address, List_config_Type, List_config_Value, List_config_Note, table, label_messages
    frame_main = ctk.CTkFrame(root)
    frame_main.pack(fill="both", expand=True, padx=10, pady=10)
    # buttons
    frame_buttons = ctk.CTkFrame(frame_main, height=50)
    frame_buttons.pack(fill="x", padx=10, pady=(10,5))
    button_clear_config = ctk.CTkButton(master=frame_buttons, width=60, text="📄New", font=font_bold, command=lambda:create_popup(kind="column"))
    button_clear_config.pack(side="left", padx=(10,5))
    button_clear_config = ctk.CTkButton(master=frame_buttons, width=60, text="💣Clear", font=font_bold, command=lambda:update_table(mode="clear"))
    button_clear_config.pack(side="left", padx=(5,5))
    button_load_config = ctk.CTkButton(master=frame_buttons, width=60, text="📥Load", font=font_bold, command=lambda:load_history())
    button_load_config.pack(side="left", padx=(5,5))
    button_save_config = ctk.CTkButton(master=frame_buttons, width=60, text="💾Save", font=font_bold, command=lambda:save_history())
    button_save_config.pack(side="left", padx=(5,5))
    button_config = ctk.CTkButton(master=frame_buttons, width=15, corner_radius=100, text="⚙", font=font_normal, command=lambda:create_popup(kind="config"))
    button_config.pack(side="right", padx=(5,10))
    button_play = ctk.CTkButton(master=frame_buttons, width=15, corner_radius=100, text="▶", font=font_normal, command=lambda:doPlayStop("Play", button_play, button_pause))
    button_play.pack(side="right", padx=(5,5))
    button_pause = ctk.CTkButton(master=frame_buttons, width=15, corner_radius=100, text="⏸", font=font_normal, state="disabled", command=lambda:doPlayStop("Stop", button_play, button_pause))
    button_pause.pack(side="right", padx=(5,5))
    # message labels
    frame_messages = ctk.CTkFrame(frame_main, height=10)
    frame_messages.pack(fill="x", padx=10, pady=(0,5))
    label_messages = ctk.CTkLabel(frame_messages, text="Hello World!")
    label_messages.pack(side="left", padx=(10,5), pady=10)
    # table
    frame_tree = ctk.CTkScrollableFrame(frame_main)
    frame_tree.pack(fill="both", expand=True, padx=10, pady=(0, 10))
    table = ttk.Treeview(master=frame_tree,
                        columns=('Address', 'Type', 'Value', 'Note'),
                        height=17,
                        selectmode='browse',
                        show='headings')
    table.column("#1", anchor="w", minwidth=100, width=100)
    table.column("#2", anchor="w", minwidth=80, width=80)
    table.column("#3", anchor="w", minwidth=120, width=120)
    table.column("#4", anchor="w", minwidth=120, width=120)
    table.heading('Address', text='Address')
    table.heading('Type', text='Type')
    table.heading('Value', text='Value')
    table.heading('Note', text='Note')
    table.pack(fill="both", pady=(5, 10), expand=True)
    table.bind("<Button-3>", table_copy_cell) # bind right click
    update_table()

def update_table(mode="update", args = []):
    global List_config_Address, List_config_Type, List_config_Value, List_config_Note, table
    
    if mode == "clear":
        for item in table.get_children():
            table.delete(item)
    elif mode == "insert":
        # args: addr, type, note
        table.insert("", "end", values=(args[0], args[1], "", args[2]))
    elif mode == "update":
        for item in table.get_children():
            table.delete(item)
        for i in range(len(List_config_Address)):
            table.insert("", "end", values=(List_config_Address[i], List_config_Type[i], List_config_Value[i], List_config_Note[i]))
    elif mode == "overwrite":
        # args: iid, value
        values = table.item(args[0])["values"]  # get row
        values[2] = args[1] # overwrite with value
        table.item(args[0], values=values)  # save

def table_copy_cell(event):
    global label_messages
    # Get pos of cell clicked
    row_id = table.identify_row(event.y)
    column_id = table.identify_column(event.x)

    if row_id and column_id:
        cell_value = table.item(row_id)["values"][int(column_id[1:]) - 1]
        root.clipboard_clear()
        root.clipboard_append(str(cell_value))
        label_messages.configure(text="Copied: {}".format(cell_value))

#####################
# Load / Store Files
def load_history(mode="normal"):
    global List_config_Address, List_config_Type, List_config_Value, List_config_Note

    if mode == "normal":
        try:
            List_config_Address.clear()
            List_config_Type.clear()
            List_config_Value.clear()
            List_config_Note.clear()
            with open(path_file_history, "r", encoding="UTF-8") as file_setting:
                settings = file_setting.read().splitlines() # 0行目はただの概要なので注意
                for i in range(len(settings) - 1):
                    try:
                        List_config_Address.append(settings[i + 1].split(",")[0])
                        List_config_Type.append(settings[i + 1].split(",")[1])
                        List_config_Value.append(settings[i + 1].split(",")[2])
                        List_config_Note.append(settings[i + 1].split(",")[3])
                    except IndexError:
                        print("Read all lines!")
                        break
            update_table()
        except FileNotFoundError:
            print("mw-config.txt is not found.")
            save_history(mode="new")

def save_history(mode="overwrite"):
    global List_config_Address, List_config_Type, List_config_Value, List_config_Note, table

    if mode == "new":
        with open(path_file_history, "w", encoding="UTF-8", newline='\n') as file_setting:
            file_setting.write("[Address],[Type],[Value],[Note]")
        print("Created mw-history.csv in same directory.")

    elif mode == "overwrite":
        with open(path_file_history, "w", encoding="UTF-8", newline='\n') as file_setting:
            file_setting.write("[Address],[Type],[Value],[Note]")
            for i in table.get_children():
                row = table.item(i)["values"]
                for j in range(4):
                    if j == 0: file_setting.write("\n")
                    file_setting.writelines(str(row[j]))
                    if j != 3: file_setting.write(",")

def load_mwconfig(mode="normal"):
    global Dict_config

    if mode == "normal":
        try:
            with open(path_file_mwconfig, "r", encoding="UTF-8") as file_setting:
                for i in file_setting.read().splitlines():
                    if ":" in i:
                        key, value = i.split(":", 1)
                        Dict_config[key.strip()] = value.strip()
        except FileNotFoundError:
            print("mw-config.ini is not found.")
            save_mwconfig(mode="new")
        create_window()

def save_mwconfig(mode="overwrite", args={}):
    global Dict_config

    if mode == "new":
        with open(path_file_mwconfig, "w", encoding="UTF-8", newline='\n') as file_setting:
            file_setting.write("Theme:System\nColor:blue\n")
        print("Created mw-config.ini in same directory.")
    elif mode == "overwrite":
        with open(path_file_mwconfig, "w", encoding="UTF-8", newline='\n') as file_setting:
            file_setting.write("Theme:{}\nColor:{}\n".format(args["Theme"], args["Color"]))
    load_mwconfig()

#####################
# Memory
def read_value(conv_type, address, date_size):
    error_count = 0
    data = c.read_memory(address, date_size)
    while data == None:
        error_count += 1
        if error_count > 8:  # プロセスを閉じる判定回数
            root.destroy()
            sys.exit()
        time.sleep(0.3)  # 接続復帰をしばらく待つ
        data = c.read_memory(address, date_size)
    return struct.unpack(conv_type, data)

def read_Pvalue(conv_type, address, date_size): # Get value of pointer
    return read_value(conv_type, read_value("I", address, 4)[0], date_size)

def doPlayStop(mode, button_play=None, button_pause=None):
    global isPlay
    if mode == "Play":
        isPlay = True
        button_play.configure(state="disabled")
        button_pause.configure(state="normal")
        root.after(8, update_value)
    elif mode == "Stop":
        isPlay = False
        button_play.configure(state="normal")
        button_pause.configure(state="disabled")
    elif mode == "get":
        return isPlay

def update_value():
    global root, table
    DataTypeMap = {
        "int(bit)":     ("<b", 1),
        "int(Byte)":     ("<b", 1),
        "int(DEC)":      ("<i", 4),
        "int(HEX)":      ("<i", 4),
        "short":         ("<h", 2),
        "long":          ("<q", 8),

        "uint(Byte)":    ("<B", 1),
        "uint(DEC)":     ("<I", 4),
        "uint(HEX)":     ("<I", 4),
        "ushort":        ("<H", 2),
        "ulong":         ("<Q", 8),

        "float":         ("<f", 4),
        "double":        ("<d", 8),
        "char(ASCII)":   ("<c", 1),
        "char(Unicode)": ("<H", 2),
        "Pointer":       ("<I", 4),
    }

    for item in table.get_children():
        try:
            row = table.item(item)["values"]
            conv_type, size = DataTypeMap[row[1]]
            address = int(row[0], 16)
            value = read_value(conv_type, address, size)[0]
            # 値の整形（きたないコード）
            if row[1] == "int(bit)":
                value_str = int_to_bitstring(value, 8)
            elif row[1] == "int(Byte)":
                value_str = hex(value)
            elif row[1] == "uint(Byte)":
                value_str = hex(value)
            elif row[1] == "int(HEX)":
                value_str = hex(value)
            elif row[1] == "uint(HEX)":
                value_str = hex(value)
            elif row[1] == "char(ASCII)":
                value_str = value.decode("ascii")
            elif row[1] == "char(Unicode)":
                value_str = chr(value)
            elif row[1] == "float":
                value_str = f"{value:.3f}"
            elif row[1] == "double":
                value_str = f"{value:.6f}"
            else:
                value_str = str(value)  # その他は10進数表示
            update_table(mode="overwrite", args=[item, value_str])

        except Exception as e:
            print(f"[Error] {item}: {e}")
            continue

    # Recursive
    if root.winfo_exists() and doPlayStop("get") == True:
        root.after(8, update_value)

#####################
# Other funcs
def int_to_bitstring(value, bits=32):
    return format(value if value >= 0 else (1 << bits) + value, f'0{bits}b')

def close(event):
    sys.exit()

def run():
    try:
        if c.is_connected():
            while True:
                root.after(8, update_value)  # 値の更新を行う
                root.bind('<Destroy>',close)  # 閉じる際にプロセスを完全に停止
                root.mainloop()  # ⑪イベント処理
        else:
            print("Failed to connect to Citra RPC Server")
    finally:
        pass

if "__main__" == __name__:
    load_mwconfig()
    setup_widgets()
    load_history() # アドレスと型の読み込み
    run()
