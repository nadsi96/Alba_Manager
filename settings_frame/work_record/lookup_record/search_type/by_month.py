import datetime
from dateutil.relativedelta import relativedelta

import pandas as pd
from pandastable import Table, TableModel

from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox

from UI import UI_setting
from Functions import functions as f
from Functions import mongoDB

from settings_frame.work_record.lookup_record.search_type import functions

class By_Month:
    def __init__(self, parent):
        self.parent = parent
        self.window = UI_setting.new_Window(parent, title="by_month")
        
        self.font = UI_setting.get_font(f_size=10)
        
        self.today = datetime.datetime.today().date()
        self.selected_date = self.today.replace(day=1)
        
        self.set_Window()
        
        self.window.grab_set()
        self.window.protocol("WM_DELETE_WINDOW", lambda : f.on_Closing(parent, self.window))
        return
    
    def set_Window(self):
        self.set_Frame_Select_Date(self.window)
#        self.set_Frame_Show_Date(self.window)
        self.set_Frame_Rb_Staff(self.window)
        self.set_Frame_DataView(self.window)
        
        self.cmd_Update_DataView()
        
        self.set_Command()
    
    def set_Command(self):
        self.btn_set.config(command=self.cmd_Set_Record)
        
        
        self.sb_dic = {"year" : self.sb_year,
                  "month" : self.sb_month}
        self.date_dic = {"year" : lambda x : relativedelta(years=x),
               "month" : lambda x : relativedelta(months=x)}
        for key, value in self.sb_dic.items():
            value.bind("<<Increment>>", lambda x, y=key : self.sb_Incr(x, y))
            value.bind("<<Decrement>>", lambda x, y=key : self.sb_Decr(x, y))
            value.config(command=self.set_sb_Date)
        return
    
    def set_Frame_Select_Date(self, parent):
        self.frame_select_date = UI_setting.set_frame(parent, side="top", padx=5, pady=5, relief="solid", bd=1)
        
        self.sb_year, self.sb_month, _ = UI_setting.get_Date_Spinbox(self.frame_select_date)
        
        # 0을 선택하면 해당 항목의 전체기간
        self.sb_year.config(from_=0, font=self.font)
        self.sb_month.config(from_=0, font=self.font)
        
        self.sb_year.set(self.selected_date.year)
        self.sb_month.set(self.selected_date.month)
        
        self.sb_year.pack(side="left", padx=5, pady=5)
        self.sb_month.pack(side="left", padx=5, pady=5)
        
        self.btn_set = Button(self.frame_select_date, text="set", font=self.font, padx=5, pady=5, state="disabled")
        self.btn_set.pack(side="right")
        
        self.lbl_date = Label(self.frame_select_date, text="{}.{}".format(self.selected_date.year, "{0:0>2}".format(self.selected_date.month)),
                              font=UI_setting.get_font(f_size=12, weight="bold"))
        self.lbl_date.pack(side="top")
        return
    
    def sb_Incr(self, event, key):
        self.selected_date += self.date_dic[key](1)
#        self.set_sb_Date()
        return
    def sb_Decr(self, event, key):
        print("key", key)
        self.selected_date += self.date_dic[key](-1)
#        self.set_sb_Date()
        return
    def set_sb_Date(self):
        print("selected_date", self.selected_date)
        self.sb_year.set(self.selected_date.year)
        self.sb_month.set(self.selected_date.month)
        
        date = "{}.{}".format(self.selected_date.year, "{0:0>2}".format(self.selected_date.month))
#        self.lbl_date.config(text=date)
        self.lbl_date["text"] = date
        
        self.cmd_Update_DataView()
        
        content = "contents.{}".format(date)
        
        db = mongoDB.MongoDB().instance()
        setted = db.collection_ledger.find_one({"{}.setted".format(content) : {"$exists" : True}})
        if setted or (self.selected_date >= self.today.replace(day=1)):
            self.btn_set.config(state="disabled")
        else:
            self.btn_set.config(state="normal")
        
        return
        
    # 직원이름 라디오버튼 생성
    # 리스트에 직원 이름들을 저장하고, 
    def set_Frame_Rb_Staff(self, parent):
        print("set_Frame_Rb_Staff")
        frame_rb_staffs = UI_setting.set_frame(parent, padx=5, pady=5, side="right")
        
        self.db = mongoDB.MongoDB.instance()
        cond = [{"$project" : 
                    {"name" : "$name",
                     "empno" : {"$ifNull" : ["$empno", "_"]},
                     "phone" : {"$ifNull" : ["$phone", "_"]}
                     }
                },
                {"$sort" : {"empno" : 1}}]
    
        cursors = self.db.collection_staff.aggregate(cond)
        self.staff_dic = {}
        for cursor in cursors:
            name = ""
            temp_dic = {}
            if cursor["empno"] == "_":
                name = "{}.{}".format(cursor["phone"][:-4], cursor["name"])
                temp_dic = {"name" : cursor["name"],
                            "phone" : cursor["phone"]}
            else:
                name = "{}.{}".format(cursor["empno"], cursor["name"])
                temp_dic = {"name" : cursor["name"],
                            "empno" : cursor["empno"]}
            self.staff_dic[name] = temp_dic
        
        self.rb_staff_lst = []
        self.staff_var = StringVar()
        for key in self.staff_dic.keys():
            self.rb_staff_lst.append(Radiobutton(frame_rb_staffs, text=key, value=key, variable=self.staff_var,
                                                 command=self.cmd_Update_DataView))
            self.rb_staff_lst[-1].pack(side="top", anchor="w")
            self.rb_staff_lst[-1].deselect()
        self.rb_staff_lst[0].select()
        return
    
    
    def set_Frame_DataView(self, parent):
        self.frame_dataview = UI_setting.set_frame(parent, side="bottom")
        
        self.df_cols = ["day", "출근", "퇴근", "휴게", "근무시간"]
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
        selected_staff = self.staff_dic[self.staff_var.get()]
        #empno, name  or phone, name
        year = int(self.sb_year.get())
        month = int(self.sb_month.get())
        
        temp_cond = {}
        if "phone" in selected_staff.keys():
            temp_cond = {"$match" : {"staff.phone" : selected_staff["phone"]}}
        else:
            temp_cond = {"$match" : {"staff.empno" : selected_staff["empno"]}}
            
        cond = [
                {"$match" : {"date.year" : year, "date.month" : month}},
                {"$match" : {"staff.name" : selected_staff["name"]}},
                temp_cond,
                {"$project" : {
                        "_id" : 0,
                        "day" : "$date.day",
                        "출근" : "$time.start",
                        "퇴근" : "$time.end",
                        "휴게" : "$time.rest",
                        "근무시간" : {"$arrayElemAt" : ["$time.work_time", 2]},
                        "대타" : "$substitution"}
                },
                {"$sort" : {"day" : -1}}
                ]
        
        db = mongoDB.MongoDB.instance()
        
        cursors = db.collection_Work_Record.aggregate(cond)
        df = pd.DataFrame(cursors, columns=self.df_cols)
        print(df)
        self.pt.updateModel(TableModel(df))
        self.pt = functions.set_Column_Size(dataframe=df, pt=self.pt)
        self.pt.redraw()
    
    def cmd_Set_Record(self):
        
        year = self.sb_year.get()
        month = "{0:0>2}".format(self.sb_month.get())
        cmd_flag = msgbox.askyesno(message="확정 후 {}년 {}월에 대한 수정이 불가합니다.\n확정처리 하시겠습니까?".format(year, month))
        if not cmd_flag:
            print("cancel")
            return
        print("do")
#        content = "contents.{}.{}".format(year, month)
#        
#        db = mongoDB.MongoDB().instance()
#        
#        cursors = db.collection_ledger.find({content : {"$exists" : True}})
#        for cursor in cursors:
#            cursor[content]["setted"] = self.selected_date
#            db.collection_ledger.update({"_id" : cursor["_id"]}, cursor)
        