from tkinter import *
import tkinter.ttk as ttk

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.font_manager as fm

import datetime
from dateutil.relativedelta import relativedelta

from Functions import functions as f
from Functions import mongoDB

from UI import UI_setting

import sys, traceback

class By_Staff(Frame):
    def __init__(self, parent, controller, top, is_exists=True):
        Frame.__init__(self, parent, relief="solid", bd=1)
        self.controller = controller
        self.top = top
        
        self.font = UI_setting.get_font(f_size=10)
        self.is_exists = is_exists
        
        self.db = mongoDB.MongoDB().instance()
        
        self.set_Frame()
        self.set_Command()
        
        return
    
    def set_Frame(self):
        frame_main = UI_setting.set_frame(self, relief='solid', bd=1)
        self.set_Frame_Top(frame_main)
        self.set_Frame_Bottom(frame_main)
        
        self.init_Data()
        return
    
    def set_Command(self):
        
#        range_validation_staff = self.controller.register(self.sb_valid_staff)
        for _from_to in ["from", "to"]:
            for idx, (key, value) in enumerate(self.sb_date[_from_to].items()):
                value.bind("<<Increment>>", lambda x, y=_from_to, z=self.date_dic[key](1) : self.sb_Incr(event=x, from_to=y, func=z))
                value.bind("<<Decrement>>", lambda x, y=_from_to, z=self.date_dic[key](1) : self.sb_Decr(event=x, from_to=y, func=z))
#                value.config(validatecommand=(range_validation_staff, '%P', value, idx))
                value.config(command=lambda x=_from_to : self.update_sb_Date(x))
        
        for staff in self.chk_staffs:
            staff.config(command=self.update_Graph)
        return
    
    # select period, staff
    def set_Frame_Top(self, parent):
        frame_top = UI_setting.set_frame(parent, padx=5, pady=5, relief='solid', bd=1, side='top')
        
        frame_select_period = Frame(frame_top)
        frame_select_period.pack(padx=5, pady=5)
        
        self.sb_year_from, self.sb_month_from, _ = UI_setting.get_Date_Spinbox(frame_select_period)
        self.sb_year_to, self.sb_month_to, _ = UI_setting.get_Date_Spinbox(frame_select_period)
        
        self.date_to = DateNode(datetime.datetime.today().date().replace(day=1))
        self.date_from = DateNode(self.date_to.date - relativedelta(months=10))
        
        self.sel_date_dic = {"from" : self.date_from,
                         "to" : self.date_to}
        
        self.sb_date_from = {"year" : self.sb_year_from,
                             "month" : self.sb_month_from}
        self.sb_date_to = {"year" : self.sb_year_to,
                           "month" : self.sb_month_to}
        self.sb_date = {"from" : self.sb_date_from,
                        "to" : self.sb_date_to}
        
        self.year_month = {"year" : lambda x : x.year,
                           "month" : lambda x : x.month}
        
        self.date_dic = {"year" : lambda x : relativedelta(years=x),
               "month" : lambda x : relativedelta(months=x)}
        
        self.sb_year_from.pack(side="left")
        Label(frame_select_period, text="년 ", font=self.font).pack(side="left", padx=3)
        self.sb_month_from.pack(side="left")
        Label(frame_select_period, text="월 ", font=self.font).pack(side="left", padx=3)
        
        Label(frame_select_period, text="~ ", font=self.font).pack(side="left", padx=3)
        
        self.sb_year_to.pack(side="left")
        Label(frame_select_period, text="년 ", font=self.font).pack(side="left", padx=3)
        self.sb_month_to.pack(side="left")
        Label(frame_select_period, text="월 ", font=self.font).pack(side="left", padx=3)
        
        self.sb_year_from.set(self.date_from.date.year)
        self.sb_month_from.set(self.date_from.date.month)
        
        self.sb_year_to.set(self.date_to.date.year)
        self.sb_month_to.set(self.date_to.date.month)
        
        for value in self.sb_date.values():
            for v in value.values():
                v.config(font=self.font, state='readonly')
        
        return
    
    
    # plot data
    def set_Frame_Bottom(self, parent):
        frame_bottom = UI_setting.set_frame(parent, padx=5, pady=5, side='bottom')
        self.set_Frame_Graph(frame_bottom)
        self.set_Frame_Staffs(frame_bottom)
        return
    
    def set_Frame_Staffs(self, parent):
        frame_staffs = UI_setting.set_frame(parent, padx=5, pady=5, side="right")
        self.chk_staffs = []
        self.chkvar_staffs = {}
        
        staffs = self.db.collection_ledger.aggregate([
                {"$match" : {"staff.empno" : {"$exists" : self.is_exists}}},
                {"$project" : {"_id" : 0,
                               "name" : "$staff.name",
                               "empno" : "$staff.empno"}}
                ])
        names = ["{}.{}".format(staff["empno"], staff["name"]) for staff in staffs]
        for idx, name in enumerate(names):
            self.chkvar_staffs[name.split(".")[1]] = IntVar()
            self.chk_staffs.append(Checkbutton(frame_staffs, text=name, variable=self.chkvar_staffs[name.split(".")[1]], font=self.font))
            self.chk_staffs[idx].pack(side="top", anchor="w")
            self.chk_staffs[idx].select()
        return
        
# =============================================================================
#     def cmd_Chk_Staff(self):
#         self.update_Graph()
#         return
# =============================================================================
    
    def set_Frame_Graph(self, parent):
        frame_graph = UI_setting.set_frame(parent, padx=5, pady=5, side="left")
        try:
            self.figure = plt.Figure(figsize=(5,4), dpi=100)
            self.ax = self.figure.add_subplot(111)
#            self.ax2 = self.ax.twinx()
            
#            self.ax.set_zorder(self.ax2.get_zorder() + 10)
            self.line = FigureCanvasTkAgg(self.figure, frame_graph)
            self.line.get_tk_widget().pack(side="left", fill="both")
            
            self.plt_font_path = "Resource/Font/NanumSquareRoundR.ttf"
            self.fontprop = fm.FontProperties(fname=self.plt_font_path, size=10)
            
        except:
            print("============")
            print()
            print("set_Frame_Graph")
            print("ERROR Occured!")
            print()
            traceback.print_exc()
            print()
            print("============")
        return

    def init_Data(self):
        self.staffs_dic = {}
        total_cnt = self.month_delta(self.sel_date_dic["from"].date, self.sel_date_dic["to"].date) + 1
        
        print("_from :", self.sel_date_dic["from"].date)
        print("_to :", self.sel_date_dic["to"].date)
        
        for chk_staff in self.chk_staffs:
            name = chk_staff["text"].split(".")[1]
            cursor = self.db.collection_ledger.find_one({"staff.name" : name, "staff.empno" : {"$exists" : self.is_exists}})
            if not cursor:
                continue
            temp_date = self.sel_date_dic["to"].date
            data={}
            data["date"] = []
            data[name] = []
            for idx in range(total_cnt):
                temp_date = self.sel_date_dic["to"].date - relativedelta(months=idx)
                year = str(temp_date.year)
                month = "{0:0>2}".format(temp_date.month)
                try:
                    total = cursor["contents"][year][month]["total"]
                except:
                    total = 0
                print(total)
                data["date"].append("{}.{}".format(year, month))
                data[name].append(total)
                
            
            df = pd.DataFrame(data, index=data["date"])
            df.drop(columns="date", inplace=True)
            self.staffs_dic[name] = df
#        integrate_df = pd.DataFrame([], index=self.staffs_dic[self.chk_staffs[0]["text"].split(".")[1]].index)
#        for key, value in self.staffs_dic.items():
#            integrate_df
        self.integrate_df = pd.concat([value for value in self.staffs_dic.values()], axis=1)
        print("\n\nintegerate")
        print(self.integrate_df)
        print("\n\n")
        
        self.update_Graph()
        return
    
    def month_delta(self, start, end):
        delta = relativedelta(end, start)
        return 12 * delta.years + delta.months

# =============================================================================
#     def update_Graph(self):
#         try:
#             print("\nupdate_Graph()\n")
#             self.ax.clear() # 수행 전, 그려진 그래프 지움. 안하면 기존 그래프에 덧그림
#             for name, df in self.staffs_dic.items():
#                 if self.chkvar_staffs[name].get():
#                     df.plot(kind="line", legend=True, ax=self.ax, color=value[1], marker='o', fontsize=10)
#                     for idx, text in enumerate(df.iloc[:, 0]):
#                         print(text)
#                         self.ax.annotate(text, (df.iloc[:, 0].index[idx], df.iloc[idx, 0]))
#                     print()
#             for tick in self.ax.get_xticklabels():
#                 tick.set_fontproperties(self.fontprop)
#             
#             self.figure.canvas.draw()
#             self.figure.canvas.flush_events()
#         except:
#             print("============")
#             print()
#             print("ERROR Occured!")
#             print()
#             traceback.print_exc()
#             print()
#             print("============")
#         print("update_Graph End")
#         return
# =============================================================================
    
    def update_Graph(self):
        temp_df = self.integrate_df.copy()
        try:
            print("\nupdate_Graph()\n")
            self.ax.clear() # 수행 전, 그려진 그래프 지움. 안하면 기존 그래프에 덧그림
#            self.ax2.clear()
            
            for name, df in self.staffs_dic.items():
                if not self.chkvar_staffs[name].get():
                    temp_df.drop(columns=name, inplace=True)
#                    df.plot(kind="line", legend=True, ax=self.ax, color=value[1], marker='o', fontsize=10)
#                    for idx, text in enumerate(df.iloc[:, 0]):
#                        print(text)
#                        self.ax.annotate(text, (df.iloc[:, 0].index[idx], df.iloc[idx, 0]))
#                    print()
#            temp_df.plot(kind='line', legend=True, ax=self.ax, marker='o', fontsize=10)
            print(temp_df)
            
            temp_df.plot(kind="line", legend=True, ax=self.ax, marker='o')
            
#            total_df = pd.DataFrame([None for x in temp_df.index], index=temp_df.index, columns=["total"])
#            print("\ntotal df")
#            print(total_df)
#            for col in temp_df.columns:
#                self.ax.plot(temp_df.index, temp_df.loc[:, col], label=col)
#            for idx in total_df.index:
#                total_df.loc[idx, "total"] = sum([x for x in temp_df.loc[idx, :]])
#            print("\ntotal df")
#            print(total_df)
#            self.ax2.bar(total_df.index, total_df["total"], label="total")
            for tick in self.ax.get_xticklabels():
                tick.set_fontproperties(self.fontprop)
            
            self.ax.legend(prop=self.fontprop)
#            self.ax2.legend(prop=self.fontprop)
            
            self.figure.canvas.draw()
            self.figure.canvas.flush_events()
        except:
            print("============")
            print()
            print("ERROR Occured!")
            print()
            traceback.print_exc()
            print()
            print("============")
        print("update_Graph End")
        return
    
    def sb_Incr(self, event, from_to, func):
        print("============")
        print("sb_Incr")
        print(func, type(func))
        self.sel_date_dic[from_to].date += func
        print(from_to, "manipulate")
        print("self.sel_date_dic.{}".format(from_to), self.sel_date_dic[from_to].date)
        print("from :", self.date_from.date)
        print("to :", self.date_to.date)
        # key : ["year", "month"]
        # value : ["year_spinbox", "month_spinbox"]
#        for key, value in self.sb_date[from_to].items():
#            value.set(self.year_month[key](self.sel_date_dic[from_to]))
        return
    
    def sb_Decr(self, event, from_to, func):
        print("============")
        print("sb_Decr")
        print(func, type(func))
        self.sel_date_dic[from_to].date -= func
        print(from_to, "manipulate")
        print("self.sel_date_dic.{}".format(from_to), self.sel_date_dic[from_to].date)
        print("from :", self.date_from.date)
        print("to :", self.date_to.date)
        return
    
    def update_sb_Date(self, from_to):
        print("update_sb_Date")
        print("from_to :", from_to)
        for key, value in self.sb_date[from_to].items():
            value.set(self.year_month[key](self.sel_date_dic[from_to].date))
        
        self.init_Data()
        return
    
# =============================================================================
#     def sb_valid_staff(self, user_input, sb_widget, idx):
#         idx = int(idx)
#         print("user_input :", user_input)
#         print(type(user_input))
#         if user_input.isdigit():
#             
#             minval = int(self.controller.nametowidget(sb_widget).config('from')[4])
#             maxval = int(self.controller.nametowidget(sb_widget).config('to')[4]) + 1
#             
#             int_user_input = int(user_input)
#             if int_user_input not in range(minval, maxval): 
#                 print ("Out of range") 
#                 return False
#             
#             if idx == 0:
#                 self.top.selected_date = self.top.selected_date.replace(year=int_user_input)
#             elif idx == 1:
#                 self.top.selected_date = self.top.selected_date.replace(month=int_user_input)
#             print(user_input)
# #            print("selected_date :", self.top.selected_date)
# #            self.update_Staffs_Chk()
#             return True
#         elif user_input == "":
#             print(user_input)
#             return True
#         else:
#             print("Not Numeric")
#             return False
# =============================================================================

class DateNode:
    def __init__(self, data):
        self.__date = data
    @property
    def date(self):
        return self.__date
    @date.setter
    def date(self, data):
        self.__date = data