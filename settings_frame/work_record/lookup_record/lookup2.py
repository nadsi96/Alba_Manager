from tkinter import *

from UI import UI_setting, btn_menu

from settings_frame.work_record.lookup_record.search_type import by_date, by_staff, by_cond, by_retiree, by_month

class Lookup_Window(btn_menu.Btn_Menu):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent, title="lookup")
        
        self.open_command_list = [self.open_by_month, self.open_by_date, self.open_by_staff, self.open_by_cond, self.open_by_retiree]
        
        self.set_Buttons()
        
        return
        
    def set_Buttons(self):
        self.btn_list = []
        title_list = ["월별 조회", "날짜별 조회", "직원별 조회", "검색", "퇴직자"]
        
        for idx, title in enumerate(title_list):
            self.btn_list.append(super().new_Button(text=title))
            self.btn_list[idx].config(command=self.open_command_list[idx])
        
        for btn in self.btn_list:
            super().btn_pack(btn)
        return
    
    def open_by_month(self):
        by_month.By_Month(self.window)
        return
    def open_by_date(self):
        by_date.By_Date(self.window)
        return
    def open_by_staff(self):
        by_staff.By_Staff(self.window)
        return
    def open_by_cond(self):
        by_cond.By_Cond(self.window)
        return
    def open_by_retiree(self):
        by_retiree.By_Retiree(self.window)
        return