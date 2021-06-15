from tkinter import *
import tkinter.ttk as ttk

import pandas as pd
from pandastable import Table, TableModel

from UI import UI_setting
#from Functions import mongoDB
from Functions import functions as f

from settings_frame.manage_staff.lookup import functions

class Lookup_Staff:
    def __init__(self, parent):
        self.window = UI_setting.new_Window(parent, title="조회")
        
        self.font = UI_setting.get_font(f_size=10)
        
        self.set_Window()
        self.set_Command()
        
        self.window.grab_set()
        self.window.protocol("WM_DELETE_WINDOW", lambda : f.on_Closing(parent, self.window))
        return
    
    def set_Window(self):
        self.set_Left_Frame(self.window)
        self.set_Right_Frame(self.window)
        return
    
    
# =============================================================================
#     이름, (사원번호, 연락처)
#     급여계좌 (은행, 계좌)
#     시급
# =============================================================================
    def set_Left_Frame(self, parent):
        self.frame_left = UI_setting.set_frame(parent, side="left")
        self.set_Name_Frame(self.frame_left)
        self.set_ID_Frame(self.frame_left)
        self.set_Phone_Frame(self.frame_left)
        self.set_Account_Frame(self.frame_left)
        self.set_Wage_Frame(self.frame_left)
        return
    
# =============================================================================
#     근무시간 테이블
# =============================================================================
    def set_Right_Frame(self, parent):
        self.frame_right = UI_setting.set_frame(parent, side="right")
        self.frame_table = UI_setting.set_LabelFrame(self.frame_right, text="근무시간", font=self.font)
        data = {"요일" : "-", "출근" : "-", "퇴근" : "-", "휴게" : "-", "근무시간(분)" : "-"}
        df = pd.DataFrame(data, index=[0])
        
        self.pt = Table(self.frame_table, dataframe=df)
        self.pt.fontsize = 10
        self.pt.font = "consolas"
        self.pt.setFont()
        self.pt.autoResizeColumns()
        self.pt.show()
        
# =============================================================================
#         def fix():
#             _data = {"요일" : "1", "출근" : "1", "퇴근" : "-", "휴게" : "-", "근무시간(분)" : "-"}
#             self.pt.updateModel(TableModel(pd.DataFrame(_data, index=[0])))
#             self.pt.redraw()
#             print("adsfsafasfdsadf")
#         Button(self.frame_left, text="테이블 수정", command=fix).pack()
# =============================================================================
        return
    
    def set_Name_Frame(self, parent):
        self.frame_name = UI_setting.set_frame(parent, padx=5, pady=5)
        
        self.staff_names = functions.set_Staff_cmb()
        self.cmb_names = ttk.Combobox(self.frame_name, font=self.font, width=10, state="readonly", value=self.staff_names)
        self.cmb_names.pack()
        return
    
    def cmd_Name_Changed(self, event):
        name = self.cmb_names.get()
        data = functions.cmb_Changed(self.pt, name)
        
        self.lbl_id.config(text=data["empno"])
        self.lbl_phone.config(text=data["phone"])
        self.lbl_bank.config(text=data["payroll_account"]["bank"])
        self.lbl_account.config(text=data["payroll_account"]["account"])
        self.lbl_wage.config(text="{0:,}".format(data["wage"]))
        return
    
    def set_ID_Frame(self, parent):
        self.frame_id = UI_setting.set_frame(parent, padx=5)
        
        Label(self.frame_id, text="ID", font=self.font).pack(side="left")
        UI_setting.space_area(self.frame_id, length=5, side="left")
        Label(self.frame_id, text=" - ", font=self.font).pack(side="left")
        self.lbl_id = Label(self.frame_id, text="", font=self.font, width=15, padx=5)
        self.lbl_id.pack(side="right")
        
        return
    
    def set_Phone_Frame(self, parent):
        self.frame_phone = UI_setting.set_frame(parent, padx=5, pady=5)
        
        Label(self.frame_phone, text="연락처", font=self.font).pack(side="left")
        Label(self.frame_phone, text=" - ", font=self.font).pack(side="left")
        self.lbl_phone = Label(self.frame_phone, text="", font=self.font, width=15, padx=5)
        self.lbl_phone.pack(side="right")
        return
    
    def set_Account_Frame(self, parent):
        self.frame_bank_account = UI_setting.set_LabelFrame(parent, text="급여계좌", font=self.font, padx=5, pady=5)
        
        self.frame_bank = UI_setting.set_frame(self.frame_bank_account)
        Label(self.frame_bank, text="은행", font=self.font).pack(side="left")
        self.lbl_bank = Label(self.frame_bank, text="", font=self.font, width=15, padx=5)
        self.lbl_bank.pack(side="right")
        
        self.frame_account = UI_setting.set_frame(self.frame_bank_account)
        Label(self.frame_account, text="계좌", font=self.font).pack(side="left")
        self.lbl_account = Label(self.frame_account, text="", font=self.font, width=15, padx=5)
        self.lbl_account.pack(side="right")
        
        return
    
    def set_Wage_Frame(self, parent):
        self.frame_wage = UI_setting.set_frame(parent, padx=5, pady=5)
        
        Label(self.frame_wage, text="시급", font=self.font).pack(side="left")
        self.lbl_wage = Label(self.frame_wage, text="", font=self.font, width=15, padx=5)
        self.lbl_wage.pack(side="right")
    
    def set_Command(self):
        self.cmb_names.bind("<<ComboboxSelected>>", self.cmd_Name_Changed)
        return