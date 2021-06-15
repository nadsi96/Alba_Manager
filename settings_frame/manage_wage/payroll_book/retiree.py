from tkinter import *
import tkinter.ttk as ttk

import pandas as pd
from pandastable import Table, TableModel

import datetime

from Functions import mongoDB, compute

from UI import UI_setting
from settings_frame.manage_wage.payroll_book import by_staff, pay_stub

class Retiree(by_staff.By_Staff):
    def __init__(self, parent, controller, top):
        super().__init__(parent, controller, top)
        #Frame.__init__(self, parent)
        #self.controller = controller
        #Label(self, text="by_Retiree").pack()
    
    def set_Staff(self):
        db = mongoDB.MongoDB.instance()
        cursors = db.collection_ledger.find({"staff.phone" : {"$exists" : True}}, {"_id" : 0, "staff.name" : 1, "staff.phone" : 1})
        self.staff_list = {}
        for cursor in cursors:
            key = "{0}  {1}".format(cursor["staff"]["name"], cursor["staff"]["phone"][-4:])
            print("key :", key)
            self.staff_list[key] = [cursor["staff"]["name"], cursor["staff"]["phone"]]
        print("staff_list :", self.staff_list)
        self.cmb_staffs.config(value=list(self.staff_list.keys()))
    
    def cmd_Update_Ledger_List(self, event):
        self.staff = self.staff_list[self.cmb_staffs.get()]
        print(self.staff[0], self.staff[1])
        
        db = mongoDB.MongoDB.instance()
        ledger = db.collection_ledger.find_one({"staff.name" : self.staff[0], "staff.phone" : self.staff[1]})
        
        data = []
        for year, month in ledger["contents"].items():
            for m_k in month.keys():
                temp_dic = {}
                temp_dic["year"] = int(year)
                temp_dic["month"] = int(m_k)
                temp_dic["지급액"] = month[m_k]["total"]
                if "payment_date" in month[m_k].values():
                    temp_dic["지급일"] = month[m_k]["payment_date"]
                data.append(temp_dic)
        print()
        print(self.staff[0])
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
    
    def cmd_Update_Record_List(self, selected_data):
        """selected_data = {year, month, 지급액, 지급일}"""
        db = mongoDB.MongoDB.instance()
        cursors = db.collection_Work_Record.aggregate([
                {"$match" : {"date.year" : int(selected_data["year"]),
                             "date.month" : int(selected_data["month"]),
                             "staff.name" : self.staff[0],
                             "staff.phone" : self.staff[1]}},
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
        self.columns_record = ["day", "출근", "퇴근", "휴게", "근무시간", "대타", "시간변경"]
        df_record = pd.DataFrame(cursors, columns=self.columns_record)
        
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
        
        ledger = db.collection_ledger.find_one({"staff.name" : self.staff[0], "staff.phone" : self.staff[1]})
#        ledger_contents = ledger["contents"]
        data = ledger["contents"][year][month]
        print()
        print(self.staff[0])
        print(data)
        print()
        
        pay_stub.Pay_Stub(self.controller, data, year, month)
        return