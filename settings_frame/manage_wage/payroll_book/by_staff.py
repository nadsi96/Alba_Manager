from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox

import pandas as pd
from pandastable import Table, TableModel

import datetime

from UI import UI_setting
from Functions import functions as f
from Functions import compute, mongoDB

from settings_frame.manage_wage.payroll_book import pay_stub

class By_Staff(Frame):
    def __init__(self, parent, controller, top):
        Frame.__init__(self, parent, relief="solid", bd=1)
        self.controller = controller
        
        self.font = UI_setting.get_font(f_size=10)
        
        #Label(self, text="By_Staff").pack()
        self.set_Frame()
        self.set_Command()
    
    def set_Frame(self):
        self.set_Frame_Left()
        ttk.Separator(self, orient="vertical").pack(side="left", fill="y")
        self.set_Frame_Right()
        return
    
    def set_Command(self):
        self.cmb_staffs.bind("<<ComboboxSelected>>", self.cmd_Update_Ledger_List)
        self.pt_ledger.bind("<Button-1>", self.cmd_Select_Ledger)
        self.btn_payment_detail.config(command=self.cmd_Show_Payment_Detail)
        return
    
    def set_Frame_Left(self):
        self.frame_left = UI_setting.set_frame(self, padx=5, pady=5, side="left")
        self.set_Frame_Name(self.frame_left)
        self.set_Staff()
        self.set_Frame_Ledger_List(self.frame_left)
        return
    
    def set_Frame_Right(self):
        self.frame_right = UI_setting.set_frame(self, padx=5, pady=5, side="right")
        self.set_Frame_Record_Title(self.frame_right)
        self.set_Frame_Record_List(self.frame_right)
        return
    
    def set_Frame_Name(self, parent):
        self.frame_name = Frame(parent, padx=5, pady=5)
        self.frame_name.pack()
        #self.frame_name = UI_setting.set_frame(parent, padx=5, pady=5)
        
        self.cmb_staffs = ttk.Combobox(self.frame_name, value=["안녕"], font=self.font, width=7)
        self.cmb_staffs.pack()
        
        return
    
    def set_Frame_Ledger_List(self, parent):
        self.frame_ledger = UI_setting.set_frame(parent, padx=5, pady=5)
        
        # ListBox
# =============================================================================
#         self.y_scroll = Scrollbar(self.frame_ledger)
#         self.y_scroll.pack(side="right", fill="y")
#         
#         self.lb_ledger = Listbox(self.frame_ledger, selectmode="single", height=12, yscrollcommand=self.y_scroll.set)
#         self.lb_ledger.pack()
#         
#         self.y_scroll.config(command=self.lb_ledger.yview)
# =============================================================================
        self.columns_ledger = ["year", "month", "지급액", "확정여부"]
        
        df = pd.DataFrame([], columns=self.columns_ledger, index=[0])
        self.pt_ledger = Table(self.frame_ledger, dataframe=df, width=270)
        self.pt_ledger.font="consolas"
        self.pt_ledger.fontsize=10
        self.pt_ledger.setFont()
        
        self.pt_ledger.show()
        self.set_DataTable_Column_Size(dataframe=df, pandastable=self.pt_ledger)
        return
    
    def set_Frame_Record_Title(self, parent):
        self.frame_record_title = UI_setting.set_frame(parent, padx=5, pady=5)
        self.lbl_record_title = Label(self.frame_record_title, text="---", font=UI_setting.get_font(f_size=12, weight="bold"))
        self.lbl_record_title.pack(side="left")
        
        self.btn_payment_detail = Button(self.frame_record_title, text="급여명세서", font=self.font, padx=5, pady=5)
        self.btn_payment_detail.pack(side="right")
        return
    
    def set_Frame_Record_List(self, parent):
        self.frame_table = UI_setting.set_frame(parent, padx=5, pady=5)
        
        self.columns_record = ["day", "출근", "퇴근", "휴게", "근무시간", "급여액", "대타", "시간변경"]
        df = pd.DataFrame([], index=[0], columns=self.columns_record)
        self.pt_record = Table(self.frame_table, dataframe=df, width=360)
        
        self.pt_record.font = "consolas"
        self.pt_record.fontsize=10
        self.pt_record.setFont()
        self.pt_record.autoResizeColumns()
        
        self.pt_record.show()
        self.set_DataTable_Column_Size(dataframe=df, pandastable=self.pt_record)
        return
    
    def set_Staff(self):
        db = mongoDB.MongoDB.instance()
        staff_list = db.get_Staff_name()
        print("staff_list :", staff_list)
        self.cmb_staffs.config(value=staff_list)
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
    
    def cmd_Update_Ledger_List(self, event):
        staff_name = self.cmb_staffs.get()
        print(staff_name)
        
        db = mongoDB.MongoDB.instance()
        self.staff = db.collection_staff.find_one({"name" : staff_name})
        print(self.staff)
        ledger = db.collection_ledger.find_one({"staff.name" : staff_name, "staff.empno" : self.staff["empno"]})
        
        data = []
        for year, month in ledger["contents"].items():
            for m_k in month.keys():
                temp_dic = {}
                temp_dic["year"] = int(year)
                temp_dic["month"] = int(m_k)
                temp_dic["지급액"] = month[m_k]["total"]
                if "setted" in month[m_k].keys():
                    temp_dic["확정여부"] = month[m_k]["setted"]
                else:
                    temp_dic["확정여부"] = "-"
                data.append(temp_dic)
        print()
        print(staff_name)
        print(data)
        print()
        self.df_ledger = pd.DataFrame(data, columns=self.columns_ledger)
        self.df_ledger = self.df_ledger.astype({"지급액" : int})
        self.df_ledger.sort_values(by=["year", "month"], ascending=False, inplace=True)
#        self.df_ledger.fillna(value="-", inplace=True)
        self.pt_ledger.updateModel(TableModel(self.df_ledger))
#        self.pt_ledger = self.set_DataTable_Column_Size(dataframe=self.df_ledger, pandastable=self.pt_ledger)
        self.set_DataTable_Column_Size(dataframe=self.df_ledger, pandastable=self.pt_ledger)
#        self.pt = functions.set_Column_Size(dataframe=df, pt=self.pt)
        self.pt_ledger.redraw()
        return
    
    def cmd_Select_Ledger(self, event):
        rowclicked = self.pt_ledger.get_row_clicked(event)
        self.pt_ledger.setSelectedRow(rowclicked)
        print("RowClicked", rowclicked)
        selected_data = self.df_ledger.iloc[rowclicked]
        print(selected_data)
        print("year :", selected_data["year"], type(selected_data["year"]))
        self.lbl_record_title.config(text="{}.{}".format(int(selected_data["year"]), int(selected_data["month"])))
        self.cmd_Update_Record_List(selected_data)
        self.pt_ledger.redraw()
        return
    
    def cmd_Update_Record_List(self, selected_data):
        """selected_data = {year, month, 지급액, 확정여부}"""
        print("\nselected_data")
        print(selected_data)
        print()
        db = mongoDB.MongoDB.instance()
        cursors = db.collection_Work_Record.aggregate([
                {"$match" : {"date.year" : int(selected_data["year"]),
                             "date.month" : int(selected_data["month"]),
                             "staff.name" : self.staff["name"],
                             "staff.empno" : self.staff["empno"]}},
                {"$project" : {"_id" : 0,
                               "day" : "$date.day",
                               "출근" : "$time.start",
                               "퇴근" : "$time.end",
                               "휴게" : "$time.rest",
                               "근무시간" : {"$arrayElemAt" : ["$time.work_time", 2]},
#                               "대타" : "$substitution",
                               "대타" : {"$ifNull" : ["$substitution", "-"]},
                               "시간변경" : {"$ifNull" : ["$change_time", "-"]}}},
#                               "시간변경" : {"$ifNull" : ["$change_time", "-"]}
                {"$sort" : {"day" : 1}}
                ])
        df_record = pd.DataFrame(cursors, columns=self.columns_record)
        for idx in range(len(df_record)):
            payment = compute.compute_pay(self.cmb_staffs.get(),
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
    
    def cmd_Show_Payment_Detail(self):
        if self.lbl_record_title["text"] == "---":
            msgbox.showwarning(title=None, message="조회할 년/월을 선택하세요")
            return
        date = self.lbl_record_title["text"].split(".")
        year = str(date[0])
        month = int(date[1])
        if month < 10:
            month = "0" + str(month)
        else:
            month = str(month)
        
        db = mongoDB.MongoDB.instance()
        
        ledger = db.collection_ledger.find_one({"staff.name" : self.staff["name"], "staff.empno" : self.staff["empno"]})
#        ledger_contents = ledger["contents"]
        data = ledger["contents"][year][month]
        print()
        print(self.staff["name"])
        print(data)
        print()
        
        pay_stub.Pay_Stub(self.controller, data, year, month)
        return

