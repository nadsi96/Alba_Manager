import datetime

import pandas as pd
from pandastable import Table, TableModel

from tkinter import *
import tkinter.ttk as ttk

from UI import UI_setting
from Functions import functions as f
from Functions import mongoDB

from settings_frame.work_record.lookup_record.search_type import by_staff
from settings_frame.work_record.lookup_record.search_type import functions

class By_Retiree(by_staff.By_Staff):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.set_Staff()
        
    def set_Staff(self):
        db = mongoDB.MongoDB.instance()
        cursors = db.collection_Work_Record.find({"staff.empno" : {"$exists" : False}})
        self.names = {}
        names = []
        for cursor in cursors:
            temp = cursor["staff"]["name"] + " " + cursor["staff"]["phone"]
            if temp in names:
                continue
            names.append(temp)
            self.names[temp] = [cursor["staff"]["name"], cursor["staff"]["phone"]]
        self.cmb_Staff.config(value=names, width=10)
        return
    def set_Frame_DataView(self, parent):
        self.frame_dataview = UI_setting.set_frame(parent)
        self.df_cols = ["year", "month", "day", "출근", "퇴근", "휴게", "근무시간"]
        df = functions.init_Dataframe(mongoDB.MongoDB.instance(), False)
        
        self.pt = Table(self.frame_dataview, dataframe=df, width=480, height=540)
        
        self.pt.font="consolas"
        self.pt.fontsize=10
        self.pt.setFont()
        
        self.pt.autoResizeColumns()
        
        self.pt.show()
        self.pt = functions.set_Column_Size(dataframe=df, pt=self.pt)
        self.pt.redraw()
        return
    def cmd_Update_DataView(self, event):
        staff = self.names[self.cmb_Staff.get()][0]
        phone = self.names[self.cmb_Staff.get()][1]
        
        db = mongoDB.MongoDB.instance()
        
        cond = [
        {"$match" : {"staff.empno" : {"$exists" : False}}},
        {"$match" : {"staff.phone" : phone, "staff.name" : staff}},
        {"$project" : {
                "_id" : 0,
                "year" : "$date.year",
                "month" : "$date.month",
                "day" : "$date.day",
                "출근" : "$time.start",
                "퇴근" : "$time.end",
                "휴게" : "$time.rest",
                "근무시간" : {"$arrayElemAt" : ["$time.work_time", 2]}
                }
        },
        {"$sort" : {"year" : -1,
                    "month" : -1,
                    "day" : -1}}
    
        ]
        cursors = db.collection_Work_Record.aggregate(cond)
        df = pd.DataFrame(cursors, columns=self.df_cols)
        self.pt.updateModel(TableModel(df))
        self.pt = functions.set_Column_Size(dataframe=df, pt=self.pt)
        self.pt.redraw()
