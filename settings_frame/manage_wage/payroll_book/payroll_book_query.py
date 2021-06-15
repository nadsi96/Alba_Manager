from tkinter import *

#import tkinter.ttk as ttk

from UI import UI_setting

#from settings_frame.manage_wage.payroll_book import by_month, by_staff, retiree
from settings_frame.manage_wage.payroll_book import by_month2, by_staff, retiree

from Functions import functions as f


class Payroll_Book_Query:
    def __init__(self, parent):
        self.window = UI_setting.new_Window(parent, "Payroll_Book_Query")
        
        self.font = UI_setting.get_font(f_size=10)
        
#        self.sb_dic = {}
        self.selected_date = None
        
        self.set_Window()
        
        self.window.grab_set()
        self.window.protocol("WM_DELETE_WINDOW", lambda : f.on_Closing(parent, self.window))
        return
    
    def set_Window(self):
        self.set_Select_Frame(self.window)
        self.set_Data_Frame(self.window)
        return
    
    def set_Select_Frame(self, parent):
        self.frame_select = UI_setting.set_frame(parent)
        
        self.frame_btns = Frame(self.frame_select, padx=5, pady=5)
        self.frame_btns.pack()
        
        self.btn_by_month = Button(self.frame_btns, text="월별 조회", font=self.font, command=lambda : self.show_frame("By_Month"))
        self.btn_by_staff = Button(self.frame_btns, text="직원별 조회", font=self.font, command=lambda : self.show_frame("By_Staff"))
        self.btn_by_retiree = Button(self.frame_btns, text="퇴직자 조회", font=self.font, command=lambda : self.show_frame("Retiree"))
        
        self.btn_by_month.pack(side="left")
        self.btn_by_staff.pack(side="left")
        self.btn_by_retiree.pack(side="left")
        
        self.btn_list = [self.btn_by_month, self.btn_by_staff, self.btn_by_retiree]
        return
    
    def set_Data_Frame(self, parent):
        self.frame_data = UI_setting.set_frame(parent)
        
        self.frame_data.grid_rowconfigure(0, weight=1)
        self.frame_data.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        for F in (by_month2.By_Month, by_staff.By_Staff, retiree.Retiree):
            page_name = F.__name__
            print("page name :", page_name)
            frame = F(parent=self.frame_data, controller=self.window, top=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
# =============================================================================
#         idx=0
#         for key in self.frames.keys():
#             self.btn_list[idx].config(command=lambda : self.show_frame(key))
#             idx += 1
# =============================================================================
        print("\n\n")
        print(self.frames)
        print("\n\n")
        
        
        self.show_frame("By_Month")
        
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        print(frame)
        print()
        frame.tkraise()
        return