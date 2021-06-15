import datetime

import pandas as pd
from pandastable import Table, TableModel

from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox

from UI import UI_setting
from Functions import functions as f
from Functions import mongoDB

from settings_frame.work_record.lookup_record.search_type import functions

class By_Cond:
    def __init__(self, parent):
        self.parent = parent
        self.window = UI_setting.new_Window(parent, title="by_cond")
        self.font = UI_setting.get_font(f_size=10)
        
        self.cond = 1
        self.cond_setting = 1
#        self.set_Condition()
        self.set_Window()
        self.set_Command()
        
        self.window.grab_set()
        self.window.protocol("WM_DELETE_WINDOW", lambda : f.on_Closing(parent, self.window))
        return
    
    def set_Window(self):
        self.set_Frame_Basic_Buttons(self.window)
        self.set_Frame_DataView(self.window)
        return
    
    def set_Command(self):
        self.btn_set_cond.config(command=self.set_Condition)
#        self.btn_search.config(command=self.cmd_Update_DataView)
        
        return
    def set_Frame_Basic_Buttons(self, parent):
        frame_basic_btns = UI_setting.set_frame(parent, padx=5, pady=5, relief="solid", bd=1)
        
        self.btn_set_cond = Button(frame_basic_btns, text="검색 조건", font=self.font)
        self.btn_set_cond.pack(side="left")
        
#        self.btn_search = Button(frame_basic_btns, text="조회", font=self.font)
#        self.btn_search.pack(side="right")
        return
    
    def set_Frame_DataView(self, parent):
        
        self.frame_dataview = UI_setting.set_frame(parent)
        
        #"날짜", "이름", "출근", "퇴근", "근무시간", "휴게시간", "시간변경", "대타"
#        df = pd.DataFrame({"년" : "-", "월" : "-", "일" : "-",
#                           "이름" : "-", "출근" : "-", "퇴근" : "-", "휴게" : "-",
#                           "근무시간" : "-", "시간 변경" : "-", "대타" : "-"}, index=[0])
        self.base_cols = {"날짜" : ["year", "month", "day"],
                          "id" : "id",
                        "이름" :"name",
                        "출근" : "start",
                        "퇴근" : "end",
                        "근무시간" : "work_time",
                        "휴게" : "rest",
                        "시간변경" : "change_time",
                        "대타" : "substitution"}
        df = functions.init_Dataframe(mongoDB.MongoDB.instance(), True)
        
        self.pt = Table(self.frame_dataview, dataframe=df, width=480, height=540)
        
        self.pt.font="consolas"
        self.pt.fontsize=10
        self.pt.setFont()
        self.pt.autoResizeColumns()
        
        self.pt.show()
        
        # 먼저 그린 다음에 resizeColumn이 정상작동
        # ==> AttributeError: 'Table' object has no attribute 'tablecolheader'
        self.pt = functions.set_Column_Size(dataframe=df, pt=self.pt)
        self.pt.redraw()
        return
    
    def cmd_Update_DataView(self, hour_from, hour_to):
        if self.cond == 1:
            return
        
        db = mongoDB.MongoDB.instance()
        
        cursors = db.collection_Work_Record.aggregate(self.cond)
        data = []
        
#        for cursor in cursors:
#            temp_data = {}
#            for key, value in cursor.items():
#                temp_data[key] = value
#            data.append(temp_data)
#        
#        print("\ndata :")
#        for d in data:
#            print(d)
#            print()
#        df = pd.DataFrame(data, columns=self.df_cols)
        df = pd.DataFrame(cursors, columns=self.df_cols)
        print("dataframe")
        print(df)
        df = self.set_time_match(df, hour_from, hour_to)
        self.pt.updateModel(TableModel(df))
        self.pt = functions.set_Column_Size(dataframe=df, pt=self.pt)
        self.pt.redraw()
        return
    
    def set_Condition(self):
        self.cond_window = UI_setting.new_Window(self.window, title="set_cond")
        
        
        # 기간 설정
        #######################################
        lbl_frame_date_period = UI_setting.set_LabelFrame(self.cond_window, text="기간", font=self.font, padx=5, pady=5)
        
        self.sb_year_from, self.sb_month_from, self.sb_day_from = UI_setting.get_Date_Spinbox(lbl_frame_date_period)
        self.sb_year_to, self.sb_month_to, self.sb_day_to = UI_setting.get_Date_Spinbox(lbl_frame_date_period)
        
        # 0을 선택하면 해당 항목의 전체기간
#        self.sb_year_.config(from_=0, font=self.font)
#        self.sb_month.config(from_=0, font=self.font)
        
        self.sb_year_from.pack(side="left", pady=5)
        Label(lbl_frame_date_period, text="년 ", font=self.font).pack(side="left")
        self.sb_month_from.pack(side="left", pady=5)
        Label(lbl_frame_date_period, text="월 ", font=self.font).pack(side="left")
        self.sb_day_from.pack(side="left", pady=5)
        Label(lbl_frame_date_period, text="일 ~ ", font=self.font).pack(side="left")
        
        self.sb_year_to.pack(side="left", pady=5)
        Label(lbl_frame_date_period, text="년 ", font=self.font).pack(side="left")
        self.sb_month_to.pack(side="left", pady=5)
        Label(lbl_frame_date_period, text="월 ", font=self.font).pack(side="left")
        self.sb_day_to.pack(side="left", pady=5)
        Label(lbl_frame_date_period, text="일", font=self.font).pack(side="left")
        
        today = datetime.datetime.today().date()
        self.sb_year_from.set(2020)
        self.sb_year_to.set(today.year)
        
        self.sb_month_from.set(1)
        self.sb_month_to.set(today.month)
        
        self.sb_day_from.set(1)
        self.sb_day_to.set(today.day)
        #######################################
        
        # 직원 선택
        #######################################
        lbl_frame_select_staff = UI_setting.set_LabelFrame(self.cond_window, text="직원", font=self.font, padx=5, pady=5)
        
        canvas_frame = Canvas(lbl_frame_select_staff)
        
        yscroll = Scrollbar(lbl_frame_select_staff, orient="vertical", command=canvas_frame.yview)
        canvas_frame.config(yscrollcommand=yscroll.set)
        yscroll.pack(side="right", fill="y")
        canvas_frame.pack()
        
        inner_frame = UI_setting.set_frame(canvas_frame)
        
        inner_left_frame = UI_setting.set_frame(inner_frame, side="left")
        inner_right_frame = UI_setting.set_frame(inner_frame, side="right")
        
        ttk.Separator(inner_frame, orient="vertical").pack(side="left", fill="y")
        
        db = mongoDB.MongoDB.instance()
        self.chk_staff_list = []
        self.chk_staff_list_var = []
        staff_names = db.get_Staff_name()
        staff_names_cnt = len(staff_names) / 2
        for idx, staff_name in enumerate(staff_names):
            self.chk_staff_list_var.append(IntVar())
            if idx < staff_names_cnt:
                self.chk_staff_list.append(Checkbutton(inner_left_frame, text=staff_name,
                                                    font=self.font, variable=self.chk_staff_list_var[idx]))
            else:
                self.chk_staff_list.append(Checkbutton(inner_right_frame, text=staff_name,
                                                    font=self.font, variable=self.chk_staff_list_var[idx]))
            self.chk_staff_list[idx].pack(anchor="w")
            self.chk_staff_list[idx].select()
        
        #######################################
        
        # 시간대 설정
        #######################################
        lbl_frame_time_period = UI_setting.set_LabelFrame(self.cond_window, text="시간대", font=self.font, padx=5, pady=5)
        
        hours = [str(x) if x > 10 else "0"+str(x) for x in range(0, 25)]
        
        self.sb_hour_from = ttk.Spinbox(lbl_frame_time_period, value=hours, font=self.font, width=5)
        self.sb_hour_to = ttk.Spinbox(lbl_frame_time_period, value=hours, font=self.font, width=5)
        
        self.sb_hour_from.pack(side="left")
        Label(lbl_frame_time_period, text="시 ~", padx=5).pack(side="left")
        self.sb_hour_to.pack(side="left")
        Label(lbl_frame_time_period, text="시", padx=5).pack(side="left")
        
        self.sb_hour_from.set(self.sb_hour_from["value"][0])
        self.sb_hour_to.set(self.sb_hour_to["value"][-1])
        #######################################
        
        #조회할 내용 선택
        #######################################
        lbl_frame_columns = UI_setting.set_LabelFrame(self.cond_window, text="조회할 내용", font=self.font, padx=5, pady=5)
        frame_inner_columns_left = UI_setting.set_frame(lbl_frame_columns, width = 50, side="left")
        frame_inner_columns_right = UI_setting.set_frame(lbl_frame_columns, width = 50, side="right")
        frame_inner_columns = [frame_inner_columns_left, frame_inner_columns_right]
        
        cols = ["날짜", "이름", "출근", "퇴근", "근무시간", "휴게", "시간변경", "대타"]
        cnt = len(cols)//2
        self.chk_cols = []
        self.chk_cols_var = []
        for idx, col in enumerate(cols):
            self.chk_cols_var.append(IntVar())
            self.chk_cols.append(Checkbutton(frame_inner_columns[idx%2], text=cols[idx], font=self.font,
                                             variable=self.chk_cols_var[idx]))
            self.chk_cols[idx].pack(anchor="w")
            self.chk_cols[idx].select()
#        self.chk_cols[-1].deselect()
#        self.chk_cols[-2].deselect()
        [chk_col.deselect() for chk_col in self.chk_cols[-2:]]
        #######################################
        
        # 버튼
        #######################################
        frame_buttons = UI_setting.set_frame(self.cond_window)
        self.btn_apply_cond = Button(frame_buttons, text="적용", font=self.font, width=5, height=2)
        self.btn_cancel = Button(frame_buttons, text="취소", font=self.font, width=5, height=2, command=self.cond_window.destroy)
        
        self.btn_apply_cond.pack(side="right")
        self.btn_cancel.pack(side="left")
        #######################################
        
        self.get_Cond_Setting()
        self.set_Validation()
        return
    
    def cmd_Update_Condition(self):
        self.cond = {}
        
        year_from = int(self.sb_year_from.get())
        year_to = int(self.sb_year_to.get())
        month_from = int(self.sb_month_from.get())
        month_to = int(self.sb_month_to.get())
        day_from = int(self.sb_day_from.get())
        day_to = int(self.sb_day_to.get())
        
        staff_list = []
        for idx, value in enumerate(self.chk_staff_list_var):
            if value.get():
                staff_list.append(self.chk_staff_list[idx]["text"])
        
        hour_from = (self.sb_hour_from.get()) + "00"
        hour_to = (self.sb_hour_to.get()) + "00"
        if len(hour_from) < 4:
            hour_from = "0" + hour_from
        if len(hour_to) < 4:
            hour_to = "0" + hour_to
        
        cols_list = []
        for idx, value in enumerate(self.chk_cols_var):
            if value.get():
                cols_list.append(self.chk_cols[idx]["text"])
        
        date_match = self.set_aggr_date_match(year_from, year_to, month_from, month_to, day_from, day_to)
        time_match = {}
        self.cond = [
                date_match,
                {"$match" : {"staff.name" : {"$in" : staff_list}}},
                {"$project" : {
                        "year" : "$date.year",
                        "month" : "$date.month",
                        "day" : "$date.day",
                        "id" : "$staff.empno",
#                        "이름" : {"$in" : ["$staff.name", staff_list]},
                        "이름" : "$staff.name",
                        "출근" : "$time.start",
                        "퇴근" : "$time.end",
                        "근무시간" : {"$arrayElemAt" : ["$time.work_time", 2]},
                        "휴게" : "$time.rest",
                        "대타" : "$substitution",
                        "시간변경" : "$change_time"}},
                {"$sort" : {"year" : -1,
                            "month" : -1,
                            "day" : -1}}
            ]
        
    
        print(year_from, month_from, day_from)
        print(year_to, month_to, day_to)
        print(staff_list)
        print(hour_from)
        print(hour_to)
#        self.update_cols = [self.df_cols[x] for x in cols_list]
        self.df_cols = []
        for idx, (key, value) in enumerate(self.base_cols.items()):
            if key in cols_list:
                if str(type(value)) == "<class 'list'>":
                    self.df_cols.extend([v for v in value])
                else:
                    self.df_cols.append(key)
        
        print("cond :")
        print(self.cond)
        msgbox.showinfo("", "적용되었습니다")
        self.set_Cond_Setting()
        self.cmd_Update_DataView(hour_from, hour_to)
        self.cond_window.destroy()
        self.window.grab_set()
        return
    
    def set_aggr_date_match(self, year_from, year_to, month_from, month_to, day_from, day_to):
        if year_from == year_to:
            if month_from == month_to:
                return {"$match" : {"$and" : [
                        {"date.year" : year_from, "date.month" : month_from},
                        {"date.day" : {"$gte" : day_from, "$lte" : day_to}}
                        ]}}
            else:
                return {"$match" : {"$and" : [
                        {"date.year" : year_from},
                        {"$or" : [{"date.month" : {"$gt" : month_from, "$lt" : month_to}},
                                  {"date.month" : month_from, "date.day" : {"$gte" : day_from}},
                                  {"date.month" : month_to, "date.day" : {"$lte" : day_to}}]}
                        ]}}
        else:
            return {"$match" : {"$and" : [
                    {"$or" : [
                            {"date.year" : year_from, "date.month" : month_from, "date.day" : {"$gte" : day_from}},
                            {"date.year" : year_from, "date.month" : {"$gt" : month_from}},
                            {"date.year" : {"$gt" : year_from}}
                            ]},
                    {"$or" : [
                            {"date.year" : year_to, "date.month" : month_to, "date.day" : {"$lte" : day_to}},
                            {"date.year" : year_to, "date.month"  :{"$lt" : month_to}},
                            {"date.year" : {"$lt" : year_to}}
                            ]}
                ]}}
    
    def set_time_match(self, df, hour_from, hour_to):
        hour_from = int(hour_from)
        hour_to = int(hour_to)
        
        temp_df = df.astype({"출근" : int, "퇴근" : int})
        print()
        print(df)
        for idx, (s, e) in enumerate(zip(temp_df["출근"], temp_df["퇴근"])):
            print(1, s, type(e))
            print(2, e, type(e))
            if s > e:
                temp_df.loc[idx, "퇴근"] += 2400
        
        print()
        print("temp_df")
        print(temp_df)
        print("df")
        print(df)
        print()
        
        temp_df_to_del = temp_df[(temp_df["출근"] >= hour_to) | (temp_df["퇴근"] <= hour_from)]
        print("temp_df_to_del")
        print(temp_df_to_del)
        df.drop(index=temp_df_to_del.index, inplace=True)
        print()
        print("df")
        print(df)
        
#        df["출근"] = str(df["출근"]).rjust(4, "0")
#        df["퇴근"] = str(df["퇴근"]).rjust(4, "0")
#        print(df)
        
        return df
#    def set_Cond_Setting(self, *kwargs):
    def set_Cond_Setting(self):
        self.cond_setting = {}
        self.cond_setting["from"] = [self.sb_year_from.get(), self.sb_month_from.get(), self.sb_day_from.get(), self.sb_hour_from.get()]
        self.cond_setting["to"] = [self.sb_year_to.get(), self.sb_month_to.get(), self.sb_day_to.get(), self.sb_hour_to.get()]
        self.cond_setting["staff"] = [x.get() for x in self.chk_staff_list_var]
        self.cond_setting["cols"] = [x.get() for x in self.chk_cols_var]
        return
    def get_Cond_Setting(self):
        if self.cond_setting != 1:
            self.sb_year_from.set(self.cond_setting["from"][0])
            self.sb_month_from.set(self.cond_setting["from"][1])
            self.sb_day_from.set(self.cond_setting["from"][2])
            self.sb_hour_from.set(self.cond_setting["from"][3])
            
            self.sb_year_to.set(self.cond_setting["to"][0])
            self.sb_month_to.set(self.cond_setting["to"][1])
            self.sb_day_to.set(self.cond_setting["to"][2])
            self.sb_hour_to.set(self.cond_setting["to"][3])
            
            [self.chk_staff_list[idx].deselect() for idx, x in enumerate(self.cond_setting["staff"]) if x == 0]
            [self.chk_cols[idx].deselect() if x == 0 else self.chk_cols[idx].select() for idx, x in enumerate(self.cond_setting["cols"])]
        return
    
    def set_Validation(self):
        range_validation = self.window.register(self.sb_valid)
        self.sb_year_from.config(validatecommand=(range_validation, '%P', self.sb_year_from))
        self.sb_month_from.config(validatecommand=(range_validation, '%P', self.sb_month_from))
        self.sb_day_from.config(validatecommand=(range_validation, '%P', self.sb_day_from))
        self.sb_year_to.config(validatecommand=(range_validation, '%P', self.sb_year_to))
        self.sb_month_to.config(validatecommand=(range_validation, '%P', self.sb_month_to))
        self.sb_day_to.config(validatecommand=(range_validation, '%P', self.sb_day_to))
        
        self.sb_hour_from.config(validatecommand=(range_validation, '%P', self.sb_hour_from))
        self.sb_hour_to.config(validatecommand=(range_validation, '%P', self.sb_hour_to))
        
        
        self.btn_apply_cond.config(command=self.cmd_Update_Condition)
#        self.btn_cancel.config(command=) 해당 창 닫아야해서 바로 입력
        return
    
    def sb_valid(self, user_input, sb_widget):
        print("user_input :", user_input)
        print(type(user_input))
        if user_input.isdigit():
            
            minval = int(self.window.nametowidget(sb_widget).config('from')[4])
            maxval = int(self.window.nametowidget(sb_widget).config('to')[4]) + 1
            
            if int(user_input) not in range(minval, maxval): 
                print ("Out of range") 
                return False
            
            print(user_input)
            return True
        elif user_input == "":
            print(user_input)
            return True
        else:
            print("Not Numeric")
            return False
        