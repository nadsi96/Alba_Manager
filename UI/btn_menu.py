from tkinter import *
from UI import UI_setting
from Functions import functions as f

class Btn_Menu:
    def __init__(self, parent, title=None):
        print("Btn_Menu")
        self.window = UI_setting.new_Window(parent, title)
        self.btn_size = (20,2)
        
        self.window.grab_set()
        # 닫기 버튼 클릭시 parent 창 맨 앞으로
        self.window.protocol("WM_DELETE_WINDOW", lambda : f.on_Closing(parent, self.window))
        
    def new_Button(self, text):
        print("create new Button")
        return Button(self.window, text=text, width=self.btn_size[0], height=self.btn_size[1])
    
    def btn_pack(self, btn, padx=5, pady=5):
        print("pack   - ", btn)
        btn.pack(padx=padx, pady=pady)
        return
        
        