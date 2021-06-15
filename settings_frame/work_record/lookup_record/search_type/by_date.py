import datetime

import pandas as pd
from pandastable import Table, TableModel

from tkinter import *
import tkinter.ttk as ttk

from UI import UI_setting
from Functions import functions as f
from Functions import mongoDB

from settings_frame.work_record.lookup_record.search_type import functions

class By_Date:
    def __init__(self, parent):
        self.parent = parent
        self.window = UI_setting.new_Window(parent, title="by_date")
        
        self.font = UI_setting.get_font(f_size=10)
        
        self.selected_date = datetime.datetime.today().date()
        
        self.set_Window()
        
        self.window.grab_set()
        self.window.protocol("WM_DELETE_WINDOW", lambda : f.on_Closing(parent, self.window))
        return
    
    def set_Window(self):
        self.set_Frame_Select_Date(self.window)
        self.set_Frame_Show_Date(self.window)
        self.set_Frame_DataView(self.window)
        
        self.set_Command()
    
    def set_Command(self):
        self.btn_search.config(command=self.cmd_Update_DataView)
        
        self.chk_year.config(command=self.cmd_Update_chk_year)
        self.chk_month.config(command=self.cmd_Update_chk_month)
        
        return
    
    def set_Frame_Select_Date(self, parent):
        self.frame_select_date = UI_setting.set_frame(parent, padx=5, pady=5, relief="solid", bd=1)
        
        self.sb_year, self.sb_month, self.sb_day = UI_setting.get_Date_Spinbox(self.frame_select_date)
        
        # 0을 선택하면 해당 항목의 전체기간
        self.sb_year.config(from_=0, font=self.font)
        self.sb_month.config(from_=0, font=self.font)
        self.sb_day.config(from_=0, font=self.font)
        
        self.sb_year.set(self.selected_date.year)
        self.sb_month.set(self.selected_date.month)
        self.sb_day.set(self.selected_date.day)
        
        self.sb_year.config(command=self.sb_year_Changed)
        self.sb_month.config(command=self.sb_month_Changed)
        self.sb_day.config(command=self.sb_day_Changed)
        
        self.sb_year.pack(side="left", padx=5, pady=5)
        self.sb_month.pack(side="left", padx=5, pady=5)
        self.sb_day.pack(side="left", padx=5, pady=5)
        
        self.btn_search = Button(self.frame_select_date, text="조회", font=self.font, padx=5, pady=5)
        self.btn_search.pack(side="right")
        return
    
    def sb_year_Changed(self):
        self.selected_date = self.selected_date.replace(year = int(self.sb_year.get()))
        print("selectetd_date :", self.selected_date)
        return
    
    def sb_month_Changed(self):
        year = int(self.sb_year.get())
        month = int(self.sb_month.get())
        try:
            self.selected_date = self.selected_date.replace(month=month)
        except:
            self.selected_date = self.selected_date.replace(month=month, day=1)
        temp_date = datetime.datetime(year, month, 1)
        last_day = f.get_last_day(date=temp_date)
        self.sb_day.config(to=last_day)
        
        if int(self.sb_day.get()) > last_day:
            self.sb_day.set(last_day)
        
        print("selectetd_date :", self.selected_date)
        return
    
    def sb_day_Changed(self):
        self.selected_date = self.selected_date.replace(day=int(self.sb_day.get()))
        
        print("selectetd_date :", self.selected_date)
        return

    # table에 년도, 월 보이기/숨기기
    # check == 숨기기, uncheck == 보이기
    def set_Frame_Show_Date(self, parent):
        self.frame_show_date = UI_setting.set_frame(parent, padx=5, pady=5)
        
        self.chk_year_var = IntVar()
        self.chk_month_var = IntVar()
        
        frame_chk_btns = Frame(self.frame_show_date)
        frame_chk_btns.pack(side="right")
        
        self.chk_year = Checkbutton(frame_chk_btns, text="년도 숨기기", variable=self.chk_year_var, font=self.font)
        self.chk_month = Checkbutton(frame_chk_btns, text="월 숨기기", variable=self.chk_month_var, font=self.font)
        
        self.chk_year.pack()
        self.chk_month.pack()
        
        Label(self.frame_show_date, text="숨기기 - ", padx=5, pady=5, font=UI_setting.get_font()).pack(side="right")
        
        return
    
    def cmd_Update_chk_year(self):
        y_var = self.chk_year_var.get()
        print("y_var :", y_var)
        if y_var == 0:
            self.df_cols.insert(0, "year")
        else:
            self.df_cols.remove("year")
        
        self.cmd_Update_DataView()
        return
    def cmd_Update_chk_month(self):
        y_var = self.chk_year_var.get()
        m_var = self.chk_month_var.get()
        print("y_var :", y_var)
        print("m_var :", m_var)
        if m_var == 1:
            self.df_cols.remove("month")
        else:
            # y_var == 1이면 0, 0이면 1에 month 삽입
            self.df_cols.insert(y_var^1, "month")
        
        self.cmd_Update_DataView()
        return
    
    def set_Frame_DataView(self, parent):
        self.frame_dataview = UI_setting.set_frame(parent)
        
        self.df_cols = ["year", "month", "day", "id", "이름", "출근", "퇴근", "휴게", "근무시간"]
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
    
    def cmd_Update_DataView(self):
        data = [self.sb_year.get(), self.sb_month.get(), self.sb_day.get()]
        data = [int(x) for x in data]
        print("data :", data)
        cond_list = ["date.year", "date.month", "date.day"]
        date_list = ["year", "month", "day"]
        cond = [
                {"$match" : {"staff.empno" : {"$exists" : True}}
                },
                {"$project" : {
                        "_id" : 0,
                        "year" : "$date.year",
                        "month" : "$date.month",
                        "day" : "$date.day",
                        "id" : "$staff.empno",
                        "이름" : "$staff.name",
                        "출근" : "$time.start",
                        "퇴근" : "$time.end",
                        "휴게" : "$time.rest",
                        "근무시간" : {"$arrayElemAt" : ["$time.work_time", 2]},
                        "대타" : "$substitution"}
                },
                {"$sort" : {"year" : -1,
                            "month" : -1,
                            "day" : -1}
                }
                ]
        for idx, d in enumerate(data):
            if d == 0:
                cond[1]["$project"][date_list[idx]] = "$"+cond_list[idx]
            else:
                cond[0]["$match"][cond_list[idx]] = d
        db = mongoDB.MongoDB.instance()
        
        cursors = db.collection_Work_Record.aggregate(cond)
        df = pd.DataFrame(cursors, columns=self.df_cols)
        print(df)
        self.pt.updateModel(TableModel(df))
        self.pt = functions.set_Column_Size(dataframe=df, pt=self.pt)
        self.pt.redraw()
    
    