from tkinter import *

import datetime
from dateutil.relativedelta import relativedelta

import pandas as pd

from Functions import mongoDB
from Functions import functions as f

from UI import UI_setting

import sys, traceback
#logging.basicConfig(level=logging.ERROR)
class Memo:
    def __init__(self, parent, content=None):
        self.window = UI_setting.new_Window(parent, "Memo")
        
#        self.content = content
        self.selected_date = datetime.datetime.today().date()
        
        self.font = UI_setting.get_font()
        
        db = mongoDB.MongoDB.instance()
        cursors = db.collection_memo.find({},{"_id" : 0})
        self.df = pd.DataFrame(cursors)
        self.df.sort_values(by=["year", "month", "day"], ascending=False, inplace=True)
        self.df.index = range(self.df.shape[0])
        
        print(self.df)
        print()
        self.cursor_idx = -1
        
        self.set_Frame()
        self.set_Command()
        return
    
    def set_Frame(self):
        self.set_Frame_date(self.window)
        self.set_Frame_memo(self.window)
        
        return
    
    def set_Command(self):
        
        self.date_dic = {"year" : lambda x : relativedelta(years=x),
               "month" : lambda x : relativedelta(months=x),
               "day" : lambda x : relativedelta(days=x)}
        
        f.set_Date_Spinbox_Command(controller=self, sb_dic=self.sb_dic, func=self.update_Memo)
        
        range_validation = self.window.register(self.sb_valid)
        for idx, sb in enumerate(self.sb_dic.values()):
            sb.config(validatecommand=(range_validation, '%P', sb, idx))
# =============================================================================
#         range_validation = self.window.register(self.sb_valid)
#         for idx, (key, value) in enumerate(self.sb_dic.items()):
#             print("idx :", idx)
#             print("key :", key)
#             print("value :", value)
#             value.config(validatecommand=(range_validation, '%P', value, idx))
#             value.bind("<<Increment>>", lambda x, y=key : self.sb_Incr(x, y))
#             value.bind("<<Decrement>>", lambda x, y=key : self.sb_Decr(x, y))
#             value.config(command=self.set_sb_date)
# =============================================================================
        
        self.btn_left.config(command=lambda : self.cmd_Btn_Side(key=1))
        self.btn_right.config(command=lambda : self.cmd_Btn_Side(key=-1))
        return
    
    def set_Frame_date(self, parent):
        frame_date = UI_setting.set_frame(parent, padx=5, pady=5)
        inner_frame_date = Frame(frame_date, padx=5, pady=5)
        inner_frame_date.pack()
        
        self.sb_year, self.sb_month, self.sb_day = UI_setting.get_Date_Spinbox(parent=inner_frame_date)
        
        self.sb_year.pack(side="left")
        Label(inner_frame_date, text="년 ", font=self.font, padx=3).pack(side="left")
        self.sb_month.pack(side="left")
        Label(inner_frame_date, text="월 ", font=self.font, padx=3).pack(side="left")
        self.sb_day.pack(side="left")
        Label(inner_frame_date, text="일", font=self.font, padx=3).pack(side="left")
        
        self.sb_year.set(self.selected_date.year)
        self.sb_month.set(self.selected_date.month)
        self.sb_day.set(self.selected_date.day)
        
        self.sb_year.config(font=self.font)
        self.sb_month.config(font=self.font)
        self.sb_day.config(font=self.font)
        
        self.sb_dic = {"year" : self.sb_year,
                       "month" : self.sb_month,
                       "day" : self.sb_day}
        return
    
    def set_Frame_memo(self, parent):
        frame_memo = UI_setting.set_frame(parent, padx=5, pady=5)
        
        self.img_left_arrow = self.setting_image("Resource/Images/left_arrow.png", frame_memo, 25, 25)
        self.img_right_arrow = self.setting_image("Resource/Images/right_arrow.png", frame_memo, 25, 25)
        self.btn_left = Button(frame_memo, image=self.img_left_arrow, padx=5, pady=5)
        self.btn_right = Button(frame_memo, image=self.img_right_arrow, padx=5, pady=5)
        
        self.btn_left.pack(side="left")
        self.btn_right.pack(side="right")
        
        frame_memo_txt = UI_setting.set_frame(frame_memo, side="top")
        txt_x_scroll = Scrollbar(frame_memo_txt, orient="horizontal")
        txt_x_scroll.pack(side="bottom", fill="x")
        txt_y_scroll = Scrollbar(frame_memo_txt, orient="vertical")
        txt_y_scroll.pack(side="right", fill="y")
        
        self.txt_memo = Text(frame_memo_txt, width=30, height = 10, font=self.font,
                        xscrollcommand=txt_x_scroll.set, yscrollcommand=txt_y_scroll.set)
        self.txt_memo.pack(fill="both", expand=True)
        
        txt_x_scroll.config(command=self.txt_memo.xview)
        txt_y_scroll.config(command=self.txt_memo.yview)
        
        self.update_Memo()
        return
    
    def setting_image(self, path, master, x, y):
        img = PhotoImage(file=path, master=master)
        # img.zoom(비율) # 확대
        resized_img = img.subsample(x, y) # (비율) 축소
        return resized_img
    
    def update_Memo(self):
        print("update_Memo")
        
#        cursor = self.db.collection_memo.find_one({"year" : self.selected_date.year,
#                                                   "month" : self.selected_date.month,
#                                                   "day" : self.selected_date.day})
        df = self.df[self.df["year"] == self.selected_date.year]
        df = df[df["month"] == self.selected_date.month]
        df = df[df["day"] == self.selected_date.day]
        self.txt_memo.delete("1.0", END)
        
        if not(df.empty):
            print("df")
            print(df)
            _idx = df.index[0]
            print(_idx)
            
    #        if cursor:
    #            self.txt_memo.insert(END, cursor["content"])
            
            print(df.loc[_idx, "content"])
            print(type(df.loc[_idx, "content"]))
            self.txt_memo.insert(END, df.loc[_idx, "content"])
        return
    
    def cmd_Btn_Side(self, key):
        print("##############")
        print("self.df")
        print(self.df)
        print("---------------")
        print("key :", key)
        df = self.df[self.df["year"] == self.selected_date.year]
        df = df[df["month"] == self.selected_date.month]
        df = df[df["day"] == self.selected_date.day]
        try:
            idx = df.index[0] + key
        except:
            if key - 1:
                df = self.df[self.df["year"] >= self.selected_date.year]
                df = df[df["month"] >= self.selected_date.month]
                df = df[df["day"] >= self.selected_date.day]
            else:
                df = self.df[self.df["year"] <= self.selected_date.year]
                print("\ny")
                print(df)
                df = df[((df["year"] == self.selected_date.year) & (df["month"] <= self.selected_date.month)) |
                        (df["year"] < self.selected_date.year)]
                print("\nm")
                print(df)
#                df = df[df["day"] <= self.selected_date.day]
                df = df[((df["year"] == self.selected_date.year) &
                             (((df["month"] == self.selected_date.month) & (df["day"] <= self.selected_date.day)) |
                             (df["month"] < self.selected_date.month))) |
                        (df["year"] < self.selected_date.year)]
                print("\nd")
                print(df)
            print("exeption df")
            print(df)
            if df.empty:
                return
            idx = df.index[0]
        print("cmd_Btn_Side")
        print(df)
        print("idx :", idx)
        print()
        
        if idx < 0 or idx >= self.df.shape[0]:
            return
        
        self.txt_memo.delete("1.0", END)
        content = self.df.loc[idx, "content"]
        print(content)
        self.selected_date = self.selected_date.replace(year=int(self.df.loc[idx, "year"]),
                                                        month=int(self.df.loc[idx, "month"]),
                                                        day=int(self.df.loc[idx, "day"]))
#        test
# =============================================================================
#         try:
# #            content = self.df.iloc[idx + key]
#             content = self.df.iloc[idx]
#             print(content)
#             print("year")
#             print(self.df.loc[idx, "year"])
#             self.selected_date = self.selected_date.replace(year=int(self.df.loc[idx, "year"]),
#                                                             month=int(self.df.loc[idx, "month"]),
#                                                             day=int(self.df.loc[idx, "day"]))
#         except:
#             print("except")
#             traceback.print_exc()
#             return
# =============================================================================
        self.txt_memo.insert(END, content)
        print(self.selected_date)
#        self.set_sb_date()
        f.set_sb_date(self, self.sb_dic)
        return
    
    
# =============================================================================
#     def sb_Incr(self, event, arg):
#         print("sb_Incr")
#         self.selected_date += self.date_dic[arg](1)
#         print("selected_date :", self.selected_date)
#         return
#     
#     def sb_Decr(self, event, arg):
#         print("sb_Decr")
#         self.selected_date -= self.date_dic[arg](1)
#         print("selected_date :", self.selected_date)
#         return
#     
#     def set_sb_date(self):
#         print("set_sb_date")
#         self.sb_dic["year"].set(self.selected_date.year)
#         self.sb_dic["month"].set(self.selected_date.month)
#         self.sb_dic["day"].set(self.selected_date.day)
#         print(self.sb_year.get(), self.sb_month.get(), self.sb_day.get())
#         print(self.selected_date)
#         print()
#         
#         self.update_Memo()
#         return
# =============================================================================
    
    def sb_valid(self, user_input, sb_widget, idx):
        idx = int(idx)
        print("user_input :", user_input)
        print(type(user_input))
        if user_input.isdigit():
            
            minval = int(self.window.nametowidget(sb_widget).config('from')[4])
            maxval = int(self.window.nametowidget(sb_widget).config('to')[4]) + 1
            
            int_user_input = int(user_input)
            if int_user_input not in range(minval, maxval): 
                print ("Out of range") 
                return False
            
            if idx == 0:
                self.selected_date = self.selected_date.replace(year=int_user_input)
            elif idx == 1:
                self.selected_date = self.selected_date.replace(month=int_user_input)
            elif idx == 2:
                self.selected_date = self.selected_date.replace(day=int_user_input)
            print(user_input)
            print("selected_date :", self.selected_date)
            self.update_Memo()
            return True
        elif user_input == "":
            print(user_input)
            return True
        else:
            print("Not Numeric")
            return False
