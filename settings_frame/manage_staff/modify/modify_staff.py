from tkinter import *
import tkinter.ttk as ttk

from UI import UI_setting

from settings_frame.manage_staff.lookup import lookup_staff
from settings_frame.manage_staff.modify import sub_modify_staff

class Modify_Staff(lookup_staff.Lookup_Staff):
    def __init__(self, parent):
        super().__init__(parent)
        self.window.title("Modify_Staff")
        
        self.set_Bottom_Frame()
        return
    
    def set_Bottom_Frame(self):
        self.frame_bottom = UI_setting.set_frame(self.frame_right, side="bottom", padx=5, pady=5)
        self.set_Button(self.frame_bottom)
        return
    
    def set_Button(self, parent):
        self.btn_select = Button(parent, text="선택", font=self.font, padx=5, pady=5,
                                 command=self.cmd_Select_Button)
        self.btn_select.pack(side="right")
        
    def cmd_Select_Button(self):
        name = self.cmb_names.get()
        empno = self.lbl_id["text"]
        print("name :", name)
        print("empno :", empno)
        if name != "":
            sub_modify_staff.Sub_Modify_Staff(self.window, (empno, name), self)