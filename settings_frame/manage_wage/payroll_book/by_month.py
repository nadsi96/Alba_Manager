from tkinter import *

import pandas as pd
from pandastable import Table, TableModel
import numpy as np

import datetime

from UI import UI_setting
from Functions import mongoDB, compute
from Functions import functions as f

class By_Month(Frame):
    def __init__(self, parent, controller, top):
        Frame.__init__(self, parent, relief="solid", bd=1)
        self.controller = controller
        self.top = top
        
        self.font = UI_setting.get_font(f_size=10)
        
        self.top.selected_date = datetime.datetime.today().date()
        
        self.set_Frame()
        self.set_Command()
        self.update_Ledger_List()
        
        
        return
    
    def set_Frame(self):
        self.set_Frame_Left(self)
        ttk.Separator(self, orient="vertical").pack(side="left", fill="y")
        self.set_Frame_Right(self)
        return
    
    def set_Frame_Left(self, parent):
        self.frame_left = UI_setting.set_frame(parent, padx=5, pady=5, side="left")
        self.set_Frame_Date(self.frame_left)
        self.set_Frame_Ledger_List(self.frame_left)
        return
    def set_Frame_Right(self, parent):
        self.frame_right = UI_setting.set_frame(parent, padx=5, pady=5, side="right")
        self.set_Frame_Record_Title(self.frame_right)
        self.set_Frame_Record_List(self.frame_right)
        return
    
    def set_Command(self):
# =============================================================================
#         self.sb_year.config(command=self.sb_year_Changed)
#         self.sb_month.config(command=self.sb_month_Changed)
#         
#         range_validation = self.controller.register(self.sb_valid)
#         self.sb_year.config(validatecommand=(range_validation, '%P', self.sb_year, 0))
#         self.sb_month.config(validatecommand=(range_validation, '%P', self.sb_month, 1))
# =============================================================================
        
        self.sb_dic = {"year" : self.sb_year,
              "month" : self.sb_month}
        
        f.set_Date_Spinbox_Command(controller=self.top, sb_dic=self.sb_dic, func=self.update_Ledger_List)
        
        range_validation = self.controller.register(self.sb_valid)
        for idx, sb in enumerate(self.sb_dic.values()):
            sb.config(validatecommand=(range_validation, '%P', sb, idx))
            
        self.pt_ledger.bind("<Button-1>", self.cmd_Select_Ledger)
        return
    
    def set_Frame_Date(self, parent):
        self.frame_date = Frame(parent, padx=5, pady=5)
        self.frame_date.pack()
        #self.frame_date = UI_setting.set_frame(parent, padx=5, pady=5)
        
        self.sb_year, self.sb_month, _ = UI_setting.get_Date_Spinbox(self.frame_date)
        
        self.sb_year.config(font=self.font)
        self.sb_month.config(font=self.font)
        
        self.sb_year.pack(side="left")
        Label(self.frame_date, text="년", font=self.font, padx=2, pady=5).pack(side="left")
        UI_setting.space_area(self.frame_date, length=3, side="left")
        self.sb_month.pack(side="left")
        Label(self.frame_date, text="월", font=self.font, padx=2, pady=5).pack(side="left")
        
        self.sb_year.set(self.top.selected_date.year)
        self.sb_month.set(self.top.selected_date.month)
        return
    
    def set_Frame_Record_Title(self, parent):
        self.frame_record_title = UI_setting.set_frame(parent, padx=5, pady=5)
        self.lbl_record_title = Label(self.frame_record_title, text="---", font=UI_setting.get_font(f_size=12, weight="bold"))
        self.lbl_record_title.pack(side="left")
        
        return
    
    def set_Frame_Ledger_List(self, parent):
        self.frame_ledger = UI_setting.set_frame(parent, padx=5, pady=5)
        
        self.cols_ledger = ["id", "이름", "지급액", "확정여부"]
        df = pd.DataFrame({}, columns=self.cols_ledger, index=[0])
        self.pt_ledger = Table(self.frame_ledger, dataframe=df, width=180)
        
        self.pt_ledger.font = "consolas"
        self.pt_ledger.fontsize=10
        self.pt_ledger.setFont()
        self.pt_ledger.autoResizeColumns()
        
        self.pt_ledger.show()
        self.set_DataTable_Column_Size(dataframe=df, pandastable=self.pt_ledger)
        
        return
    
    def set_Frame_Record_List(self, parent):
        self.frame_record = UI_setting.set_frame(parent, padx=5, pady=5)
        
        self.cols_record = ["day", "출근", "퇴근", "휴게", "근무시간", "급여액", "대타", "시간변경"]
        
        df = pd.DataFrame([], index=[0], columns=self.cols_record)
        self.pt_record = Table(self.frame_record, dataframe=df, width=330)
        
        self.pt_record.font = "consolas"
        self.pt_record.fontsize=10
        self.pt_record.setFont()
        self.pt_record.autoResizeColumns()
        
        self.pt_record.show()
        self.set_DataTable_Column_Size(dataframe=df, pandastable=self.pt_record)
        return
    
    def set_DataTable_Column_Size(self, dataframe=None, pandastable=None):
        width = 0
        for idx, col in enumerate(dataframe.columns):
            if col in ["year", "month", "day"]:
                width = 50
            elif col in ["이름", "출근", "퇴근", "근무시간", "대타"]:
                width = 60
            elif col in ["휴게", "id"]:
                width = 40
            else:
                continue
            pandastable.resizeColumn(col=idx, width=width)
#        return pandastable
        pandastable.redraw()
        return
    
    def update_Ledger_List(self):
        year = str(self.top.selected_date.year)
        month = self.top.selected_date.month
        if month < 10:
            month = "0" + str(month)
        else:
            month = str(month)
        
        db = mongoDB.MongoDB.instance()
        cursors = db.collection_ledger.find({"staff.empno" : {"$exists" : True}})
        ledgers = []
        for cursor in cursors:
            try:
                temp_dic = {}
                temp_dic["id"] = cursor["staff"]["empno"]
                temp_dic["이름"] = cursor["staff"]["name"]
                temp_dic["지급액"] = cursor["contents"][year][month]["total"]
                if "payment_date" in cursor["contents"][year][month].values():
                    temp_dic["지급일"] = cursor["contents"][year][month]["payment_date"]
                ledgers.append(temp_dic)
            except:
                continue
        print()
        print(ledgers)
        print()
        
        self.df_ledger = pd.DataFrame(ledgers, columns=self.cols_ledger)
        self.df_ledger = self.df_ledger.astype({"지급액" : int})
        self.df_ledger.sort_values(by="id", ascending=True, inplace=True)
#        self.df_ledger.fillna(value="-", inplace=True)
        self.pt_ledger.updateModel(TableModel(self.df_ledger))
        self.set_DataTable_Column_Size(dataframe=self.df_ledger, pandastable=self.pt_ledger)
        self.pt_ledger.redraw()
        return
    
    def cmd_Select_Ledger(self, event):
        rowclicked = self.pt_ledger.get_row_clicked(event)
        self.pt_ledger.setSelectedRow(rowclicked)
        print("RowClicked", rowclicked)
        selected_data = self.df_ledger.iloc[rowclicked]
        print(selected_data)
        self.lbl_record_title.config(text="{}.{}".format(self.top.selected_date.year, self.top.selected_date.month))
        self.cmd_Update_Record_List(selected_data)
        self.pt_ledger.redraw()
        return
    
    def cmd_Update_Record_List(self, selected_data):
        """selected_data = {"id", "이름", "지급액", "지급일"}"""
        print("year :", self.top.selected_date.year, type(self.top.selected_date.year))
        print("month :", self.top.selected_date.month, type(self.top.selected_date.month))
        print("이름 :", selected_data["이름"], type(selected_data["이름"]))
        print("empno :", selected_data["id"], type(selected_data["id"]))
        selected_data["id"] = int(selected_data["id"])
#        selected_data = selected_data.astype({"id" : int})
        print("empno :", selected_data["id"], type(selected_data["id"]))
        
        db = mongoDB.MongoDB.instance()
        cursors = db.collection_Work_Record.aggregate([
                {"$match" : {"date.year" : self.top.selected_date.year,
                             "date.month" : self.top.selected_date.month,
                             "staff.name" : selected_data["이름"],
                             "staff.empno" : selected_data["id"]}},
                {"$project" : {"_id" : 0,
                               "day" : "$date.day",
                               "출근" : "$time.start",
                               "퇴근" : "$time.end",
                               "휴게" : "$time.rest",
                               "근무시간" : {"$arrayElemAt" : ["$time.work_time", 2]},
                               "대타" : "$substitution",
                               "시간변경" : "$change_time"}},
                {"$sort" : {"day" : 1}}
                ])
        df_record = pd.DataFrame(cursors, columns=self.cols_record)
        for idx in range(len(df_record)):
            payment = compute.compute_pay(selected_data["이름"],
                                          df_record.loc[idx, "출근"],
                                          df_record.loc[idx, "퇴근"],
                                          df_record.loc[idx, "휴게"])
            df_record.loc[idx, "급여액"] = "{0:,}".format(payment)
#        df_record.astype({"급여액" : "str"})
        df_record.fillna(value="-", inplace=True)
        self.pt_record.updateModel(TableModel(df_record))
#        self.pt_record = self.set_DataTable_Column_Size(dataframe=df_record, pandastable=self.pt_record)
        self.set_DataTable_Column_Size(dataframe=df_record, pandastable=self.pt_record)
        self.pt_record.redraw()
        return
    
# =============================================================================
#     def sb_year_Changed(self):
#         year = int(self.sb_year.get())
#         self.selected_date = self.selected_date.replace(year=year)
#         
#         print("selectetd_date :", self.selected_date)
#         self.update_Ledger_List()
#         return
#     
#     def sb_month_Changed(self):
#         month = int(self.sb_month.get())
#         self.selected_date = self.selected_date.replace(month=month)
#         
#         print("selectetd_date :", self.selected_date)
#         self.update_Ledger_List()
#         return
# =============================================================================
    
    def sb_valid(self, user_input, sb_widget, idx):
        idx = int(idx)
        print("user_input :", user_input)
        print(type(user_input))
        if user_input.isdigit():
            
            minval = int(self.controller.nametowidget(sb_widget).config('from')[4])
            maxval = int(self.controller.nametowidget(sb_widget).config('to')[4]) + 1
            
            int_user_input = int(user_input)
            if int_user_input not in range(minval, maxval): 
                print ("Out of range") 
                return False
            
            if idx == 0:
                self.selected_date = self.selected_date.replace(year=int_user_input)
            elif idx == 1:
                self.selected_date = self.selected_date.replace(month=int_user_input)
            print(user_input)
            print("selected_date :", self.selected_date)
            self.update_Ledger_List()
            return True
        elif user_input == "":
            print(user_input)
            return True
        else:
            print("Not Numeric")
            return False
