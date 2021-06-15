from tkinter import *
import tkinter.ttk as ttk

import datetime
from dateutil.relativedelta import relativedelta

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.font_manager as fm

from Functions import functions as f
from Functions import mongoDB

from UI import UI_setting

from settings_frame.manage_wage.analysis import functions

import sys, traceback

class By_Month(Frame):
    def __init__(self, parent, controller, top):
        Frame.__init__(self, parent, relief="solid", bd=1)
        self.controller = controller
        self.top = top
        
        self.font = UI_setting.get_font(f_size=10)
        
        self.db = mongoDB.MongoDB().instance()
        self.top.selected_date = datetime.datetime.today().date().replace(day=1)
        
        self.set_Frame()
        self.set_Command()
        
        return
    
    def set_Frame(self):
        self.set_Frame_Top(self)
        self.set_Frame_Bottom(self)
        return
    def set_Command(self):
        print("\nset_Command()")
#        self.sb_dic = {"year" : self.sb_year,
#              "month" : self.sb_month}
#        print(self.sb_dic)
#        print()
#        f.set_Date_Spinbox_Command(controller=self.top, sb_dic=self.sb_dic, func=self.update_Staffs_Chk)
#        
#        range_validation = self.controller.register(self.sb_valid)
#        print("for")
#        for idx, sb in enumerate(self.sb_dic.values()):
#            print("idx :", idx)
#            print("sb :", sb)
#            sb.config(validatecommand=(range_validation, '%P', sb, idx))
        
        self.date_dic = {"year" : lambda x : relativedelta(years=x),
                    "month" : lambda x : relativedelta(months=x)}
        self.sb_year.bind("<<ActualIncrement>>", lambda x, y=self.date_dic["year"](1) : self.cmd_Incr(x, y))
        self.sb_year.bind("<<ActualDecrement>>", lambda x, y=self.date_dic["year"](1) : self.cmd_Decr(x, y))
        self.sb_month.bind("<<ActualIncrement>>", lambda x, y=self.date_dic["month"](1) : self.cmd_Incr(x, y))
        self.sb_month.bind("<<ActualDecrement>>", lambda x, y=self.date_dic["month"](1) : self.cmd_Decr(x, y))
        
        self.sb_year.config(command=self.update_Sb_Date)
        self.sb_month.config(command=self.update_Sb_Date)
        
        range_validation = self.controller.register(self.sb_valid)
        self.sb_year.config(validatecommand=(range_validation, '%P', self.sb_year, 0))
        self.sb_month.config(validatecommand=(range_validation, '%P', self.sb_month, 1))
            
        return
    
    def set_Frame_Top(self, parent):
        self.frame_date = Frame(parent, padx=5, pady=5)
        self.frame_date.pack()
        #self.frame_date = UI_setting.set_frame(parent, padx=5, pady=5)
        
#        self.sb_year, self.sb_month, _ = UI_setting.get_Date_Spinbox(self.frame_date)
        self.sb_year, self.sb_month = self.get_Date_Spinbox(self.frame_date)
        
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
    def set_Frame_Bottom(self, parent):
        frame_bottom = UI_setting.set_frame(parent, padx=5, pady=5, side="bottom", relief="solid", bd=1)
        self.set_Frame_Graph(frame_bottom)
        ttk.Separator(frame_bottom, orient="vertical").pack(side="left", fill="y")
        self.set_Frame_Staffs_Chk(frame_bottom)
        return
    
    def set_Frame_Graph(self, parent):
        frame_graph = UI_setting.set_frame(parent, padx=5, pady=5, side="left")
        try:
            self.figure = plt.Figure(figsize=(5,4), dpi=100)
            self.ax = self.figure.add_subplot(111)
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
    
    def set_Frame_Staffs_Chk(self, parent):
        self.frame_staffs = UI_setting.set_frame(parent, padx=5, pady=5)
        self.chks_staff = []
        self.chkvars_staff = []
        
        self.update_Staffs_Chk()
        return
    
    def init_Data(self):
        self.graph_dic = {}
        for name in list(self.df.index):
            self.graph_dic[name] = 1
#        for idx in range(df.shape[0]):
#            self.graph_dic[df.iloc[idx].name] = [pd.DataFrame(df.iloc[idx]).T, 1]
        
        print()
        print("init_Data")
        print("graph_dic :")
        print(self.graph_dic)
        print()
        self.update_Graph()
        print("init_Data End")
        return
    
    def update_Staffs_Chk(self):
        year = str(self.top.selected_date.year)
        month = self.top.selected_date.month
        if month < 10:
            month = "0{}".format(month)
        else:
            month = str(month)
        cond = [{"$match" : {"contents.{}.{}".format(year, month) : {"$exists" : True}}},
                {"$project" : {"_id" : 0,
                               "name" : "$staff.name",
                               "empno" : {"$ifNull" : ["$staff.empno", "-"]},
                               "wage" : "$contents.{}.{}.total".format(year, month)}},
                {"$sort" : {"empno" : 1}}]
        
        cursors = self.db.collection_ledger.aggregate(cond)
        self.df = pd.DataFrame(cursors)
        print()
        print("df")
        print(self.df)
        print()
#        df = df.astype({"empno" : str})
        for chk_staff in self.chks_staff:
            chk_staff.destroy()
        
        if self.df.empty:
            print("Empy_DataFrame------")
            return
        
        self.df["re_name"] = None
        self.chks_staff = []
        self.chkvars_staff = []
        for idx in range(self.df.shape[0]):
            name = "{}.{}".format(self.df.loc[idx, "empno"], self.df.loc[idx, "name"])
            self.chkvars_staff.append(IntVar())
            self.chks_staff.append(Checkbutton(self.frame_staffs, text=name,
                                               variable=self.chkvars_staff[idx], font=self.font))
            self.chks_staff[idx].pack(side="top", anchor="w")
            self.chks_staff[idx].select()
            self.df.loc[idx, "re_name"] = name
        self.df.drop(columns=["name", "empno"], inplace=True)
        self.df = self.df[["re_name", "wage"]].groupby("re_name").sum()
        
        for idx, chk_staff in enumerate(self.chks_staff):
            chk_staff.config(command=lambda x=idx : self.cmd_Chk_Staffs(x))
        
        print()
        print("re_df")
        print(self.df)
        print()
        self.init_Data()
        print("update_Staffs_chk End")
        return
    
    def update_Graph(self):
        try:
            print("\nupdate_Graph()\n")
            show_lst = [key for key, value in self.graph_dic.items() if value]
            show_df = self.df.loc[show_lst, :]
            
    #        graph_dic = {"staff_name" : (1 or 0)}
    #        functions.update_Graph(figure=self.figure, line=self.line, ax=self.ax, dic=self.graph_dic, kind="bar")
            self.ax.clear() # 수행 전, 그려진 그래프 지움. 안하면 기존 그래프에 덧그림
    #        show_df.plot.bar(legend=True, fontsize=10)
            width = .5
            self.ax.bar(x=show_df.index, height=show_df["wage"], width=width, label=show_df["wage"])
            
            for tick in self.ax.get_xticklabels():
                tick.set_fontproperties(self.fontprop)
            for idx, text in enumerate(show_df.iloc[:, 0]):
                self.ax.annotate("{0:,}".format(int(text)), (show_df.iloc[:, 0].index[idx], show_df.iloc[idx, 0]))
    #        for self.value in self.graph_dic.values():
    #            if value[1]:
    ##                value[0].plot(kind="bar", legend=True, ax=ax, marker='o', fontsize=10)
    #                value[0].plot.bar()
            
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
    
    def cmd_Chk_Staffs(self, idx):
        print()
        print("cmd_Chk_Staffs")
        print("idx :", idx)
        print("graph_dic :")
        print(self.graph_dic)
        print()
        print(self.graph_dic[self.chks_staff[idx]["text"]])
        print()
        self.graph_dic[self.chks_staff[idx]["text"]] = self.chkvars_staff[idx].get()
        self.update_Graph()
        return
    
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
                self.top.selected_date = self.top.selected_date.replace(year=int_user_input)
            elif idx == 1:
                self.top.selected_date = self.top.selected_date.replace(month=int_user_input)
            print(user_input)
            print("selected_date :", self.top.selected_date)
#            self.update_Staffs_Chk()
            return True
        elif user_input == "":
            print(user_input)
            return True
        else:
            print("Not Numeric")
            return False
    
    def get_Date_Spinbox(self, parent):
        current_date = datetime.datetime.today()
            
        sb_year = MyTtkSpinbox(parent, from_=2020, to=current_date.year, width=6, validate="key")
        sb_month = MyTtkSpinbox(parent, from_=1, to=12, width=3, validate="key")
        
        return sb_year, sb_month
    
    def cmd_Incr(self, event, func):
        self.top.selected_date += func
        print(self.top.selected_date)
        return
    def cmd_Decr(self, event, func):
        self.top.selected_date -= func
        print(self.top.selected_date)
        return
    def update_Sb_Date(self):
        self.sb_year.set(self.top.selected_date.year)
        self.sb_month.set(self.top.selected_date.month)
        self.update_Staffs_Chk()
        return

# 데이터가 있는 년.월이 선택되는 경우,
# ttk.spinbox가 자동으로 증감되는 현상방지위함
class MyTtkSpinbox(ttk.Spinbox):
    def __init__(self, master=None, delay=500, **kwargs):
        ttk.Spinbox.__init__(self, master, **kwargs)
        self.delay = delay  # repeatdelay in ms
        self.bind('<<Increment>>', self._on_increment)
        self.bind('<<Decrement>>', self._on_decrement)
        self._increment_lock = False
        self._decrement_lock = False

    def _unlock_increment(self):
        self._increment_lock = False

    def _on_increment(self, event):
        if self._increment_lock:
            return "break"  # stop the increment
        else:
            # generate a virtual event corresponding to when the spinbox
            # is actually incremented
            self.event_generate('<<ActualIncrement>>')
            self._increment_lock = True
            self.after(self.delay, self._unlock_increment)

    def _unlock_decrement(self):
        self._decrement_lock = False

    def _on_decrement(self, event):
        if self._decrement_lock:
            return "break"  # stop the increment
        else:
            # generate a virtual event corresponding to when the spinbox
            # is actually decremented
            self.event_generate('<<ActualDecrement>>')
            self._decrement_lock = True
            self.after(self.delay, self._unlock_decrement)