"""
main_ui  main_frame


왼쪽 프레임

콤보박스에서 근무자 선택
-> 출근시간, 퇴근시간, 휴게시간에 db에 저장된 근무시간 자동 입력
-> 현재 요일이 계약된 근무일이 아닌 경우 기본값 입력

출근시간, 퇴근시간, 휴게시간은 수정하여 입력 가능

시간 기입 후 '입력'버튼을 누르면 db에 입력, 처리

-------------------------------------

오른쪽 프레임
메모 확인
자유롭게 작성 가능한 텍스트박스
프로그램을 새로 시작하는 경우, 마지막에 입력되어있던 내용 호출하여 입력
'지난 메모 보기' 버튼을 통해 과거의 내용 확인 가능(이 때, 나타나는 텍스트박스는 수정 불가)
"""
import sys, os

from tkinter import *
import tkinter.ttk as ttk
import tkinter.font as tkFont
import tkinter.messagebox as msgbox
# =============================================================================
# from PIL import Image
# from PIL import ImageTk
# =============================================================================

import datetime

from main_frame import functions, memo
#from main_frame import to_setting
from UI  import UI_setting
from UI import check_input

from Functions import functions as f

class Frame_Main:
    def __init__(self, parent):
        
        self.parent = parent
       
        self.size_cmb_name_width = 10
        self.size_cmb_time_width = 7
        self.font = UI_setting.get_font()
        self.set_Window()
        self.set_Command()
    
# =============================================================================
#     # 여백 주기 위한 빈 라벨
#     def space_area(self, parent, side, length=1):
#         string = ' ' * length
#         Label(parent, text=string).pack(side=side)
#         return
# =============================================================================
    
    # 설정 버튼 이미지
    # resized_img를 self로 한 이유
    # self로 하지 않으면 이미지가 나타나지 않음
    # garbage collecter에 의해 없어진다고..
    def setting_image(self, path, master, x, y):
        img = PhotoImage(file=path, master=master)
        # img.zoom(비율) # 확대
        resized_img = img.subsample(x, y) # (비율) 축소
        return resized_img
    
    def set_Window(self):
        # 근무시간 입력 공간
        self.left = UI_setting.set_frame(self.parent, "left", padx=5, pady=3)
        self.set_left_frame()
        
        
        ttk.Separator(self.parent, orient="vertical").pack(side="left", fill="y")
        
        
        # 메모 공간
        self.right = UI_setting.set_frame(self.parent, "right", padx=5, pady=3)
        self.set_right_frame()
        return
    
    def set_left_frame(self):
        
        hours = [str(x) if x >= 10 else "0"+str(x) for x in range(25)]
        minutes = [str(x) if x >= 10 else "0"+str(x) for x in range(0, 60, 5)]
        rest = [0, 30, 35, 40, 45, 50, 55, 60]
        
        space_area = 2 # 내용간 간격 옵션
        padx = 5
        pady = 5
        
        # staff_list = functions.call_staff_list()
        
        # 직원 이름 콤보박스
        frame_cmb_staff = UI_setting.set_frame(self.left, side=None, padx=padx, pady=pady)
        Label(frame_cmb_staff, text="이름", font=self.font).pack(side="left", padx=padx, pady=pady)
        
        #self.space_area(frame_cmb_staff, side="left", length=space_area)
        UI_setting.space_area(frame_cmb_staff, side="left", length=space_area)
        
        
        self.cmb_staff = ttk.Combobox(frame_cmb_staff, font=self.font,
                                      width=self.size_cmb_name_width, height=5, value=functions.call_Staff_List())
        self.cmb_staff.pack(side="left")
        self.img_refresh = self.setting_image("Resource/Images/refresh.png", frame_cmb_staff, 25, 25)
        UI_setting.space_area(frame_cmb_staff, side="left", length=space_area)
        self.btn_refresh = Button(frame_cmb_staff, image=self.img_refresh)
        self.btn_refresh.pack(side="left")
        
        # 출근시간 입력
        frame_start = UI_setting.set_frame(self.left, side=None, padx=padx, pady=pady)
        Label(frame_start, text="출근", font=self.font).pack(side="left", padx=padx, pady=pady)
        
        #self.space_area(frame_start, side="left", length=space_area)
        UI_setting.space_area(frame_start, side="left", length=space_area)
        
        self.cmb_start_hour = ttk.Combobox(frame_start, font=self.font,
                                           width=self.size_cmb_time_width, height = 7, value=hours)
        self.cmb_start_hour.pack(side="left")
        Label(frame_start, text="시", font=self.font).pack(side="left")
        
        #self.space_area(frame_start, side="left", length=space_area)
        UI_setting.space_area(frame_start, side="left", length=space_area)
        
        self.cmb_start_minute = ttk.Combobox(frame_start, font=self.font,
                                             width=self.size_cmb_time_width, height = 7, value=minutes)
        self.cmb_start_minute.pack(side="left")
        Label(frame_start, text="분", font=self.font).pack(side="left")
        
        
        # 퇴근시간 입력
        frame_end = UI_setting.set_frame(self.left, side=None, padx=padx, pady=pady)
        Label(frame_end, text="퇴근", font=self.font).pack(side="left", padx=padx, pady=pady)
        
        #self.space_area(frame_end, side="left", length=space_area)
        UI_setting.space_area(frame_end, side="left", length=space_area)
        
        self.cmb_end_hour = ttk.Combobox(frame_end, font=self.font,
                                         width=self.size_cmb_time_width, height = 7, value=hours)
        self.cmb_end_hour.pack(side="left")
        Label(frame_end, text="시", font=self.font).pack(side="left")
        
        #self.space_area(frame_end, side="left", length=space_area)
        UI_setting.space_area(frame_end, side="left", length=space_area)
        
        self.cmb_end_minute = ttk.Combobox(frame_end, font=self.font,
                                           width=self.size_cmb_time_width, height = 7, value=minutes)
        self.cmb_end_minute.pack(side="left")
        Label(frame_end, text="분", font=self.font).pack(side="left")
        
        
        # 휴게시간 입력
        frame_rest = UI_setting.set_frame(self.left, side=None, padx=padx, pady=pady)
        Label(frame_rest, text="휴게", font=self.font).pack(side="left", padx=padx, pady=pady)
        
        #self.space_area(frame_rest, side="left", length=space_area)
        UI_setting.space_area(frame_rest, side="left", length=space_area)
        
        self.cmb_rest = ttk.Combobox(frame_rest, font=self.font,
                                     width=self.size_cmb_time_width, height = 7, value=rest)
        self.cmb_rest.pack(side = "left")
        Label(frame_rest, text="분", font=self.font).pack(side="left")
        
        
        self.main_left_cmb = [[self.cmb_staff, "staff_name"], 
                              [self.cmb_start_hour, "start_hour"], 
                              [self.cmb_start_minute, "start_minute"], 
                              [self.cmb_end_hour, "end_hour"], 
                              [self.cmb_end_minute, "end_minute"], 
                              [self.cmb_rest, "rest_time"]]
        
        
        # 입력 버튼
        frame_input = UI_setting.set_frame(self.left, side = None, padx=padx, pady=pady)
        
        self.btn_input_work_time = Button(frame_input, text="입력", font=self.font, width=self.size_cmb_time_width,
                                          command=self.btn_Input)
        self.btn_input_work_time.pack(side="right")
        
        self.img_setting = self.setting_image(path="Resource/Images/settings.png", master=self.parent, x=10, y=10)
        self.btn_setting = Button(frame_input, image=self.img_setting, command=lambda : functions.open_settings(self.parent))
        self.btn_setting.pack(side="left")
        
        # 콥보박스 항목 선택만 가능하도록
        for cmb in self.main_left_cmb:
            cmb[0].config(state="readonly")
        return
    
    def btn_Input(self):
        work_result = functions.get_work_result(self.main_left_cmb)
        if work_result == None:
            return
        work_hour, work_min, pay = work_result
        
        data = {}
        data["name"] = self.main_left_cmb[0][0].get()
        data["attend_hour"] = self.main_left_cmb[1][0].get()
        data["attend_min"] = self.main_left_cmb[2][0].get()
        data["leave_hour"] = self.main_left_cmb[3][0].get()
        data["leave_min"] = self.main_left_cmb[4][0].get()
        data["rest"] = self.main_left_cmb[5][0].get()
        work_hour, work_min, pay = functions.get_work_result(self.main_left_cmb)
        data["work_hour"] = work_hour
        data["work_min"] = work_min
        data["date"] = datetime.datetime.today().date()
        
        check_input.Check_Input(self.parent, self, data)
        
    def set_right_frame(self):
        self.frame_memo = UI_setting.set_LabelFrame(parent=self.right, text="memo", font=self.font)
        
# =============================================================================
#         self.frame_memo = LabelFrame(self.right, text="memo", font=UI_setting.get_font())
#         self.frame_memo.pack(fill="both", expand=True)
# =============================================================================
        
        txt_x_scroll = Scrollbar(self.frame_memo, orient="horizontal")
        txt_x_scroll.pack(side="bottom", fill="x")
        txt_y_scroll = Scrollbar(self.frame_memo, orient="vertical")
        txt_y_scroll.pack(side="right", fill="y")
        
        self.txt_memo = Text(self.frame_memo, width=30, height = 10, font = self.font,
                        xscrollcommand=txt_x_scroll.set, yscrollcommand=txt_y_scroll.set)
        self.txt_memo.pack(fill="both", expand=True)
        functions.get_Recent_Memo(self.txt_memo)
        
        txt_x_scroll.config(command=self.txt_memo.xview)
        txt_y_scroll.config(command=self.txt_memo.yview)
        
        frame_show_memo_btn = UI_setting.set_frame(self.right, padx=5, pady=5)
        self.btn_save_memo = Button(self.right, text="저장", font=UI_setting.get_font(f_size=10))
        self.btn_save_memo.pack(side="right", padx=5, pady=5)
        self.btn_show_past_memo = Button(self.right, text="이전 메모 조회", font=UI_setting.get_font(f_size=10))
        self.btn_show_past_memo.pack(side="right", padx=5, pady=5)
        return
    
    def set_Command(self):
        self.cmb_staff.bind("<<ComboboxSelected>>", self.cmd_Select_Staff)
        self.btn_refresh.config(command=self.update_Staff_List)
        self.btn_show_past_memo.config(command=lambda : memo.Memo(self.parent, self.txt_memo.get("1.0", END)))
        self.btn_save_memo.config(command=lambda : functions.save_Memo(self.txt_memo.get("1.0", END), datetime.datetime.today().date()))
        return
    
    def cmd_Select_Staff(self, event):
        name = self.cmb_staff.get()
        contracted_work_time = functions.get_Staff_Contracted_Work_Time(name)
        if contracted_work_time == None:
            return
        
        today = datetime.datetime.today()
        weekday = datetime.datetime.weekday(today)
        weekday = f.get_Weekday_by_Num(weekday)
        
        if weekday in contracted_work_time:
            self.cmb_start_hour.set(contracted_work_time[weekday]["start"][:2])
            self.cmb_start_minute.set(contracted_work_time[weekday]["start"][2:])
            self.cmb_end_hour.set(contracted_work_time[weekday]["end"][:2])
            self.cmb_end_minute.set(contracted_work_time[weekday]["end"][2:])
            self.cmb_rest.set(contracted_work_time[weekday]["rest"])
        else:
            return
    
    def update_Staff_List(self):
        self.cmb_staff.config(value=functions.call_Staff_List())
        print("Staff_CMB List Updated!")
        return

