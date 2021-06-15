from tkinter import *
import tkinter.ttk as ttk

from pandastable import Table
import pandas as pd

import datetime

from UI import UI_setting
from settings_frame.work_record.lookup_record import functions

from Functions import functions as f

class Lookup_Window:
    def __init__(self, parent, title=None):
        print("Lookup_Window")
        self.parent = parent
#        self.lookup_window = UI_setting.new_Window(parent, title, "640x480")
        self.window = UI_setting.new_Window(parent, title)
# =============================================================================
#         self.lookup_window = Toplevel(parent)
#         self.lookup_window.title(title)
#         self.lookup_window.geometry("640x480")
# =============================================================================
        title_list = ["날짜별 조회", "직원별 조회", "검색"]
        
# =============================================================================
#         self.btn_cond = [Button(self.lookup_window, text=x, command=lambda : self.set_Window(x)) for x in title_list]
#         self.btn_cond[0].config(width=20, height=3)
#         self.btn_cond[1].config(width=20, height=3)
#         self.btn_cond[2].config(width=30, height=3)
# =============================================================================
        self.btn_cond = []
        self.btn_cond.append(Button(self.window, text=title_list[0], command=lambda : self.set_Window(title_list[0])))
        self.btn_cond.append(Button(self.window, text=title_list[1], command=lambda : self.set_Window(title_list[1])))
        self.btn_cond.append(Button(self.window, text=title_list[2], command=lambda : self.set_Window(title_list[2])))
        
        self.btn_cond[0].config(width=20, height=3)
        self.btn_cond[1].config(width=20, height=3)
        self.btn_cond[2].config(width=20, height=3)
        
        for btn in self.btn_cond:
            btn.pack(padx=5, pady=5)
# =============================================================================
#         self.by_day = Button(self.lookup_window, text="날짜별 조회", font=self.font, width=20, height=3, command=lambda : self.set_Window(title_list[0]))
#         self.by_staff = Button(self.lookup_window, text="직원별 조회", font=self.font, width=20, height=3)
#         self.by_cond = Button(self.lookup_window, text="검색", font=self.font, width=30, height=3)
#         
#         self.by_day.pack(padx=5, pady=5)
#         self.by_staff.pack(padx=5, pady=5)
#         self.by_cond.pack(padx=5, pady=5)
# =============================================================================
        
        self.window.grab_set()
        self.window.protocol("WM_DELETE_WINDOW", lambda : f.on_Closing(parent, self.window))
    
    def set_Window(self, title=None):
        
        self.window = UI_setting.new_Window(parent=self.window, title=title)
        print("create new window")
        print("title : ", title)
        
        self.frame_search = UI_setting.set_frame(self.window)
        
        self.selected_date = datetime.datetime.today()
        
        if title == "날짜별 조회":
            print("날짜별 조회")
            #years = [x for x in range(2020, 3000)]
# =============================================================================
#             spinbox = ttk.Spinbox(root, from_ = 0, to = 50, validate = 'all')
#             spinbox.pack()
# =============================================================================
            #sb_years = ttk.Spinbox(self.parent, from_=2021, to=time.localtime().tm_year+1)
            
# =============================================================================
#             self.sb_year = ttk.Spinbox(self.frame_search, from_=2021, to=current_date.year, width=6)
#             self.sb_month = ttk.Spinbox(self.frame_search, values=list(range(1,13)), width=4)
#             self.sb_day = ttk.Spinbox(self.frame_search, from_=1, to=functions.get_last_day(), width=4)
# =============================================================================
            
            self.sb_year, self.sb_month, self.sb_day = UI_setting.get_Date_Spinbox(self.frame_search)
            
            self.sb_year.set(self.selected_date.year)
            self.sb_month.set(self.selected_date.month)
            self.sb_day.set(self.selected_date.day)
            
            self.sb_year.config(command=self.sb_year_Changed)
            self.sb_month.config(command=self.sb_month_Changed)
            self.sb_day.config(command=self.sb_day_Changed)
            
            self.sb_year.pack(side="left", padx=5, pady=5)
            self.sb_month.pack(side="left", padx=5, pady=5)
            self.sb_day.pack(side="left", padx=5, pady=5)
            
        elif title == "직원별 조회":
            print("직원별 조회")
            self.cmb_staff = ttk.Combobox(self.frame_search, font=UI_setting.get_font(f_size=10),
                                          width = 10, height=7, value=functions.get_Staff_name())
            self.cmb_staff.pack()
        else: # 조건 조회
            self.btn_set_cond = Button(self.frame_search, text="조건", font=UI_setting.get_font(), command=self.set_Condition)
            self.btn_set_cond.pack(side="left")
            
            
            
        
        self.btn_search = Button(self.frame_search, font=UI_setting.get_font(), padx=5, pady=5, text="검색")
        self.btn_search.pack(side="right")
        
        # 데이터 보여줄 곳
# =============================================================================
#         self.frame_dataview = UI_setting.set_frame(self.window)
#         data = []
#         self.datatable = Table(self.frame_dataview, dataframe=data)
# =============================================================================
        
        
        return
        
    def cmb_staff_Changed(self):
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
    
    
    def set_DataFrame_View(self):
        return
    def set_DataFrame(self):
        return
    
# =============================================================================
#     조건 검색시
#     조건 입력하는 창
# =============================================================================
    def set_Condition(self):
        font_size = 10
        current_date = datetime.datetime.today()
        
        self.temp_cond_window = UI_setting.new_Window(self.window, title="set_condition")
        
        # 기간 설정
        temp_frame_period = UI_setting.set_LabelFrame(self.temp_cond_window, text="기간", font=UI_setting.get_font(f_size=font_size))
        
        sb_start_year = ttk.Spinbox(temp_frame_period, from_=2021, to=current_date.year, width=6)
        sb_start_year.pack(side="left")
        Label(temp_frame_period, text="년", font=UI_setting.get_font(f_size=font_size)).pack(side="left")
        
        sb_start_month = ttk.Spinbox(temp_frame_period, from_=1, to=12, font=UI_setting.get_font(f_size=font_size),
                                     width = 3)
        sb_start_month.pack(side="left")
        Label(temp_frame_period, text="월", font=UI_setting.get_font(f_size=font_size)).pack(side="left")
        
        
        Label(temp_frame_period, text="~", font=UI_setting.get_font(f_size=font_size)).pack(side="left")
        
        
        sb_end_year = ttk.Spinbox(temp_frame_period, from_=2021, to=current_date.year+1, width=6)
        sb_end_year.pack(side="left")
        Label(temp_frame_period, text="년", font=UI_setting.get_font(f_size=font_size)).pack(side="left")
        
        sb_end_month = ttk.Spinbox(temp_frame_period, from_=1, to=12, width=3)
        sb_end_month.pack(side="left")
        Label(temp_frame_period, text="월", font=UI_setting.get_font(f_size=font_size)).pack(side="left")
        
        
        # 직원 선택
        temp_frame_staff_list = UI_setting.set_LabelFrame(self.temp_cond_window, text="직원", font=UI_setting.get_font(f_size=font_size))
        
        staff_list_yscrollbar = Scrollbar(temp_frame_staff_list)
        staff_list_yscrollbar.pack(side="right", fill="y")
        
        staff_list_xscrollbar = Scrollbar(temp_frame_staff_list, orient="horizon")
        staff_list_xscrollbar.pack(side="bottom", fill="x")
        
        list_staff = Listbox(temp_frame_staff_list, selectmode="extended", height=5, font=UI_setting.get_font(f_size=font_size),
                             yscrollcommand=staff_list_yscrollbar.set, xscrollcommand=staff_list_xscrollbar.set)
        list_staff.pack(fill="both", expand=True)
        
        staff_list_yscrollbar.config(command=list_staff.yview)
        staff_list_xscrollbar.config(command=list_staff.xview)
        
        
        
        # 시간대 설정
        temp_frame_timeslot = UI_setting.set_LabelFrame(self.temp_cond_window, text="시간대", font=UI_setting.get_font(f_size=font_size))
        sb_start_time = ttk.Spinbox(temp_frame_timeslot, from_=0, to=23, width=5)
        sb_start_time.pack(side="left")
        sb_start_time.set(0)
        Label(temp_frame_timeslot, text="시", font=UI_setting.get_font(f_size=font_size)).pack(side="left")
        
        Label(temp_frame_timeslot, text="~", font=UI_setting.get_font(f_size=font_size)).pack(side="left")
        
        sb_end_time = ttk.Spinbox(temp_frame_timeslot, from_=sb_start_time.get(), to=24, width=5)
        sb_end_time.pack(side="left")
        sb_end_time.set(24)
        Label(temp_frame_timeslot, text="시", font=UI_setting.get_font(f_size=font_size)).pack(side="left")
        
        
        # 조회할 내용 선택
        temp_frame_item_for_search = UI_setting.set_LabelFrame(self.temp_cond_window, text="조회할 내용", font=UI_setting.get_font(f_size=font_size))
        
        search_data_yscrollbar = Scrollbar(temp_frame_item_for_search)
        search_data_yscrollbar.pack(side="right", fill="y")
        
        values = ["날짜", "이름", "출근시간", "퇴근시간", "근무시간 변동", "대타"]
        list_search_data = Listbox(temp_frame_item_for_search, selectmode="extended", height=7, font=UI_setting.get_font(f_size=font_size),
                                   yscrollcommand=search_data_yscrollbar.set)
        list_search_data.pack(fill="both", expand=True)
        for v in values:
            list_search_data.insert(END, v)
        
        search_data_yscrollbar.config(command=list_search_data.yview)
        
        # 적용, 취소 버튼 위치할 프레임
        # 적용시 지정한 조건대로 검색하여 dataframe 생성
        # 취소시 창 그냥 종료
        temp_frame_btn = UI_setting.set_frame(self.temp_cond_window)
        
        btn_apply = Button(temp_frame_btn, text="적용", padx=5, pady=5)
        btn_cancel = Button(temp_frame_btn, text="취소", padx=5, pady=5, command=self.temp_cond_window.destroy)
        btn_apply.pack(side="left")
        btn_cancel.pack(side="right")