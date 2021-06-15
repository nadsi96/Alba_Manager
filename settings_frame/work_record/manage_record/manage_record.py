from tkinter import *

from UI import UI_setting
from UI import btn_menu

from settings_frame.work_record.manage_record.add import add_record
from settings_frame.work_record.manage_record.modify import modify_record
from settings_frame.work_record.manage_record.remove import remove_record

# 추가, 수정, 삭제
class Manage_Record_Window(btn_menu.Btn_Menu):
    def __init__(self, parent):
        super().__init__(parent, title="Manage_Record")
        
        self.open_command_list = [self.open_Insert_record, self.open_Modify_record, self.open_Remove_record]
        self.set_Buttons()
    
    def set_Buttons(self):
        self.btn_list = []
        
        self.btn_list.append(super().new_Button(text="입력"))
        self.btn_list.append(super().new_Button(text="수정"))
        self.btn_list.append(super().new_Button(text="삭제"))
        
        for idx, btn in enumerate(self.btn_list):
            super().btn_pack(btn)
            btn.config(command=self.open_command_list[idx])
# =============================================================================
#     def __init__(self, parent):
#         self.parent = parent
#         self.manage_record_window = UI_setting.new_Window(parent, title="Work_Record")
#         
#         size = (20, 2)
#         
#         self.btn_insert_record = Button(self.manage_record_window, text="입력", width=size[0], height=size[1], command=self.open_Insert_record)
#         self.btn_modify_record = Button(self.manage_record_window, text="수정", width=size[0], height=size[1], command=self.open_Modify_record)
#         self.btn_remove_record = Button(self.manage_record_window, text="삭제", width=size[0], height=size[1], command=self.open_Remove_record)
#         
#         self.btn_insert_record.pack(padx=5, pady = 5)
#         self.btn_modify_record.pack(padx=5, pady = 5)
#         self.btn_remove_record.pack(padx=5, pady = 5)
#         
#         return
# =============================================================================
    
    def open_Insert_record(self):
        ar = add_record.Add_Record(self.window)
        
    def open_Modify_record(self):
        mr = modify_record.Modify_Record(self.window)
        
    def open_Remove_record(self):
        rr = remove_record.Remove_Record(self.window)
