from tkinter import *

from UI import UI_setting
from UI import btn_menu

#from settings_frame.work_record.lookup_record import lookup
from settings_frame.work_record.lookup_record import lookup2
from settings_frame.work_record.manage_record import manage_record

class Work_Record(btn_menu.Btn_Menu):
    def __init__(self, parent):
        super().__init__(parent, title="Work_Record")
        
        self.open_command_list = [self.open_Lookup_Record, self.open_Manage_Record]
        self.set_Buttons()
    
    def set_Buttons(self):
        self.btn_list = []
        
        self.btn_list.append(super().new_Button(text="조회"))
        self.btn_list.append(super().new_Button(text="수정"))
        
        for idx, btn in enumerate(self.btn_list):
            super().btn_pack(btn)
            btn.config(command=self.open_command_list[idx])
    
    def open_Lookup_Record(self):
        print("open_lookup() method called")
#        _lr = lookup.Lookup_Window(self.window, title="Lookup")
        _lr = lookup2.Lookup_Window(self.window)
        #lookup.Lookup_Window(self.window)
    def open_Manage_Record(self):
        print("open_manage_record() method called")
        _mr = manage_record.Manage_Record_Window(self.window)


# =============================================================================
# def open_Work_record(self):
#         size = (15, 2)
#         frame_size = "170x120"
#         self.work_record_window = UI_setting.new_Window(self.window, title="Work_Record", frame_size=frame_size)
#         
#         def open_lookup_record():
#             print("open_lookup() method called")
#             self.lookup_record_window = lookup.Lookup_Window(self.window, title="Lookup")
#         self.btn_lookup_record = Button(self.work_record_window, text="조회", width=size[0], height=size[1], command=open_lookup_record)
#         
#         def open_manage_record():
#             print("open_manage_record() method called")
#             self.manage_record_window = manage_record.Manage_Record_Window(self.window)
#         self.btn_manage_record = Button(self.work_record_window, text="수정", width=size[0], height=size[1], command=open_manage_record)
#             
#         self.btn_lookup_record.pack(padx=5, pady=5)
#         self.btn_manage_record.pack(padx=5, pady=5)
# =============================================================================
