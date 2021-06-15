from tkinter import *

from UI import btn_menu

from Functions import functions
from settings_frame.manage_staff.lookup import lookup_staff
from settings_frame.manage_staff.add import add_staff
from settings_frame.manage_staff.modify import modify_staff
from settings_frame.manage_staff.remove import remove_staff


class Manage_Staff(btn_menu.Btn_Menu):
    def __init__(self, parent):
        super().__init__(parent, "Manage_Staff")
        self.open_command_list = [self.open_lookup, self.open_add, self.open_modify, self.open_remove]
        self.set_Window()
        
    def set_Window(self):
        self.set_Buttons()
    
    def set_Buttons(self):
# =============================================================================
#         self.btn_lookup = self.new_Button(text="조회")
#         self.btn_add = self.new_Button(text="추가")
#         self.btn_modify = self.new_Button(text="수정")
#         self.btn_remove = self.new_Button(text="삭제")
# =============================================================================
        
        self.btn_list = []
        
        self.btn_list.append(super().new_Button(text="조회"))
        self.btn_list.append(super().new_Button(text="추가"))
        self.btn_list.append(super().new_Button(text="수정"))
        self.btn_list.append(super().new_Button(text="삭제"))
        
        for idx, btn in enumerate(self.btn_list):
            super().btn_pack(btn)
            btn.config(command=self.open_command_list[idx])
            
    def open_lookup(self):
        print("open_staff_lookup")
        _ls = lookup_staff.Lookup_Staff(self.window)
        return
    def open_add(self):
        print("open_add_staff")
        _as = add_staff.Add_Staff(self.window)
        return
    def open_modify(self):
        print("open_modify_staff")
        _ms = modify_staff.Modify_Staff(self.window)
        return
    def open_remove(self):
        print("open_remove_staff")
        _rs = remove_staff.Remove_Staff(self.window)
        return