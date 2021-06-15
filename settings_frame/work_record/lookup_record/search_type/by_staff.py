import datetime

import pandas as pd
from pandastable import Table, TableModel

from tkinter import *
import tkinter.ttk as ttk

from UI import UI_setting
from Functions import functions as f
from Functions import mongoDB

from settings_frame.work_record.lookup_record.search_type import functions

class By_Staff:
    def __init__(self, parent):
        self.parent = parent
        self.window = UI_setting.new_Window(parent, title="by_staff")
        
        self.font = UI_setting.get_font(f_size=10)
        
        self.set_Window()
        self.set_Command()
        
        self.window.grab_set()
        self.window.protocol("WM_DELETE_WINDOW", lambda : f.on_Closing(parent, self.window))
    
    def set_Window(self):
        self.set_Frame_Select_Staff(self.window)
        self.set_Frame_DataView(self.window)
        return
    
    def set_Command(self):
        self.cmb_Staff.bind("<<ComboboxSelected>>", self.cmd_Update_DataView)
        return
    
    def set_Frame_Select_Staff(self, parent):
        self.frame_select_staff = UI_setting.set_frame(parent, relief="solid", bd=1, padx=5, pady=5)
        frame_sel_staff = Frame(self.frame_select_staff)
        frame_sel_staff.pack()
        Label(frame_sel_staff, text="직원 - ", font=self.font).pack(side="left")
        
        db = mongoDB.MongoDB.instance()
        
        self.cmb_Staff = ttk.Combobox(frame_sel_staff, value=db.get_Staff_name(), width=7)
        self.cmb_Staff.pack(side="right")
        return
    
    def set_Frame_DataView(self, parent):
        self.frame_dataview = UI_setting.set_frame(parent)
        
        self.df_cols = ["year", "month", "day", "출근", "퇴근", "휴게", "근무시간"]
        df = functions.init_Dataframe(mongoDB.MongoDB.instance(), True)
        
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
        staff = self.cmb_Staff.get()
        
        db = mongoDB.MongoDB.instance()
        
        cond = [
        {"$match" : {"staff.empno" : {"$exists" : True}}},
        {"$match" : {"staff.name" : staff}},
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