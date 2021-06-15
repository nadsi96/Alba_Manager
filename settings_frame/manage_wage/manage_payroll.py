from tkinter import *

from UI import btn_menu

from settings_frame.manage_wage.payroll_book import payroll_book_query
from settings_frame.manage_wage.analysis import analysis_wage

class Manage_Payroll(btn_menu.Btn_Menu):
    def __init__(self, parent):
        super().__init__(parent, "Manage_Payroll")
        
        self.open_command_list = [self.open_payroll_book_query, self.open_analysis]
        self.set_Window()
        
    def set_Window(self):
        self.set_Buttons()
    
    def set_Buttons(self):
        self.btn_list = []
        
        self.btn_list.append(super().new_Button(text="급여 장부 조회"))
        self.btn_list.append(super().new_Button(text="뭐할까.."))
        for idx, btn in enumerate(self.btn_list):
            super().btn_pack(btn)
            btn.config(command=self.open_command_list[idx])
            
    def open_analysis(self):
        print("open_analysis")
        analysis_wage.Analysis_Wage(self.window)
        return
    def open_payroll_book_query(self):
        print("open_payroll_book_query")
        _pbq = payroll_book_query.Payroll_Book_Query(self.window)
        return