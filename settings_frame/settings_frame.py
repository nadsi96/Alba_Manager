from tkinter import *

from UI import UI_setting
from UI import btn_menu

# =============================================================================
# from settings_frame.work_record.lookup_record import lookup
# from settings_frame.work_record.manage_record import manage_record
# =============================================================================
from settings_frame.manage_staff import manage_staff
from settings_frame.manage_wage import manage_payroll
from settings_frame.work_record import work_record

class Setting_Frame(btn_menu.Btn_Menu):
    def __init__(self, parent):
        super().__init__(parent, title="setting")
        self.open_command_list = [self.open_Work_record, self.open_Manage_Staff, self.open_Manage_Payroll]
        
        self.set_Buttons()
    
    
    def set_Buttons(self):
        self.btn_list = []
        
        self.btn_list.append(super().new_Button(text="근무기록"))
        self.btn_list.append(super().new_Button(text="직원관리"))
        self.btn_list.append(super().new_Button(text="급여관리"))
#        self.btn_list.append(super().new_Button(text="매장설정"))
        for idx, btn in enumerate(self.btn_list):
            super().btn_pack(btn)
            btn.config(command=self.open_command_list[idx])
            
    
    def open_Work_record(self):
        _wr = work_record.Work_Record(self.window)
# =============================================================================
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

    def open_Manage_Staff(self):
        _ms = manage_staff.Manage_Staff(self.window)
    
    def open_Manage_Payroll(self):
        _mp = manage_payroll.Manage_Payroll(self.window)

