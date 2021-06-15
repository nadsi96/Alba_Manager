from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox

import datetime

from UI import UI_setting
from Functions import mongoDB
from UI import check_input
from Functions import functions as f

from settings_frame.work_record.manage_record.add import functions

class Add_Record:
    def __init__(self, parent):
        self.parent = parent
        self.window = UI_setting.new_Window(parent, title="Add_Record", frame_size=None)
        
        self.font = UI_setting.get_font(f_size=10)
        self.size_cmb_time_width = 3
        self.space_area = 2
        
        self.hours = [str(x) if x >= 10 else "0"+str(x) for x in range(25)]
        self.minutes = [str(x) if x >= 10 else "0"+str(x) for x in range(0, 60, 5)]
        self.rest = [0, 30, 35, 40, 45, 50, 55, 60]
        
        self.set_Window()
        
        self.window.grab_set()
        self.window.protocol("WM_DELETE_WINDOW", lambda : f.on_Closing(parent, self.window))
        return
    
    def set_Window(self):
        self.frame_input_data = UI_setting.set_frame(self.window)
        
        self.set_Date_Frame(self.frame_input_data)
        self.set_Staff_Frame(self.frame_input_data)
        
        self.frame_input_time = UI_setting.set_frame(self.frame_input_data, padx=5, pady=5, relief="solid", bd=1)
        
        self.set_Attend_Time_Frame(self.frame_input_time)
        self.set_Leave_Time_Frame(self.frame_input_time)
        self.set_Rest_Time_Frame(self.frame_input_time)
        
        self.set_Button_Frame(self.frame_input_data)
        self.set_Command()
        return
    
    def set_Command(self):
# =============================================================================
#         self.sb_year.config(command=self.sb_year_Changed)
#         self.sb_month.config(command=self.sb_month_Changed)
#         self.sb_day.config(command=self.sb_day_Changed)
#         
#         range_validation = self.window.register(self.sb_valid)
#         self.sb_year.config(validatecommand=(range_validation, '%P', self.sb_year))
#         self.sb_month.config(validatecommand=(range_validation, '%P', self.sb_month))
#         self.sb_day.config(validatecommand=(range_validation, '%P', self.sb_day))
# =============================================================================
        self.sb_dic = {"year" : self.sb_year,
              "month" : self.sb_month,
              "day" : self.sb_day}
        f.set_Date_Spinbox_Command(controller=self, sb_dic=self.sb_dic)
        
        range_validation = self.window.register(self.sb_valid)
        for idx, sb in enumerate(self.sb_dic.values()):
            sb.config(validatecommand=(range_validation, '%P', sb, idx))
        
        self.btn_input.config(command=self.cmd_btn_input)
        self.btn_cancel.config(command=lambda : f.on_Closing(self.parent, self.window))
        
    def set_Date_Frame(self, parent):
        self.frame_select_date = UI_setting.set_frame(parent, padx=5, pady=5)
        
        #current_date = datetime.datetime.today()
        self.selected_date = datetime.datetime.today()
        
# =============================================================================
#         self.sb_year = ttk.Spinbox(self.frame_select_date, from_=2021, to=current_date.year, width=6)
#         self.sb_month = ttk.Spinbox(self.frame_select_date, from_=1, to=12, width=3)
#         self.sb_day = ttk.Spinbox(self.frame_select_date, from_=1, to=functions.get_last_day(current_date), width=3)
# =============================================================================
        self.sb_year, self.sb_month, self.sb_day = UI_setting.get_Date_Spinbox(self.frame_select_date)
        
        self.sb_year.pack(side="left")
        Label(self.frame_select_date, text="년").pack(side="left")
        UI_setting.space_area(self.frame_select_date, side="left")
        
        self.sb_month.pack(side="left")
        Label(self.frame_select_date, text="월").pack(side="left")
        UI_setting.space_area(self.frame_select_date, side="left")
        
        self.sb_day.pack(side="left")
        Label(self.frame_select_date, text="일").pack(side="left")
        UI_setting.space_area(self.frame_select_date, side="left")
        
        self.sb_year.set(self.selected_date.year)
        self.sb_month.set(self.selected_date.month)
        self.sb_day.set(self.selected_date.day)
        
# =============================================================================
#     def sb_year_Changed(self):
#         year = int(self.sb_year.get())
#         month = int(self.sb_month.get())
#         
#         temp_date = datetime.datetime(year, month, 1)
#         last_day = f.get_last_day(date=temp_date)
#         self.sb_day.config(to=last_day)
#         
#         try:
#             self.selected_date = self.selected_date.replace(year=year)
#         except:
#             self.selected_date = self.selected_date.replace(year=year, day=last_day)
#         
#         if int(self.sb_day.get()) > last_day:
#             self.sb_day.set(last_day)
#         print("selectetd_date :", self.selected_date)
#         return
#     
#     def sb_month_Changed(self):
#         year = int(self.sb_year.get())
#         month = int(self.sb_month.get())
#         
#         temp_date = datetime.datetime(year, month, 1)
#         last_day = f.get_last_day(date=temp_date)
#         self.sb_day.config(to=last_day)
#         
#         try:
#             self.selected_date = self.selected_date.replace(month=month)
#         except:
#             self.selected_date = self.selected_date.replace(month=month, day=last_day)
#         
#         if int(self.sb_day.get()) > last_day:
#             self.sb_day.set(last_day)
# # =============================================================================
# #         year = int(self.sb_year.get())
# #         month = int(self.sb_month.get())
# #         try:
# #             self.selected_date = self.selected_date.replace(month=month)
# #         except:
# #             self.selected_date = self.selected_date.replace(month=month, day=1)
# #         temp_date = datetime.datetime(year, month, 1)
# #         last_day = f.get_last_day(date=temp_date)
# #         self.sb_day.config(to=last_day)
# #         
# #         if int(self.sb_day.get()) > last_day:
# #             self.sb_day.set(last_day)
# # =============================================================================
#         
#         print("selectetd_date :", self.selected_date)
#         return
#     
#     def sb_day_Changed(self):
#         self.selected_date = self.selected_date.replace(day=int(self.sb_day.get()))
#         
#         print("selectetd_date :", self.selected_date)
#         return
# =============================================================================
        
    def sb_valid(self, user_input, sb_widget):
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
            return True
        elif user_input == "":
            print(user_input)
            return True
        else:
            print("Not Numeric")
            return False
        
    def set_Staff_Frame(self, parent):
        self.frame_select_staff = UI_setting.set_frame(parent, padx=5, pady=5)
        
        self.cmb_select_staff = ttk.Combobox(self.frame_select_staff, value=functions.get_Staff_name(), state="readonly",
                                             width = 10, height=7, font=self.font)
        
        Label(self.frame_select_staff, text="이름", font=self.font).pack(side="left")
        UI_setting.space_area(self.frame_select_staff, side="left", length=1)
        self.cmb_select_staff.pack(side="left")
    
    def set_Attend_Time_Frame(self, parent):
         # 출근시간 입력
        frame_attend = UI_setting.set_frame(parent, pady=5)
        
        Label(frame_attend, text="출근", font=self.font).pack(side="left")
        
        self.cmb_start_hour = ttk.Combobox(frame_attend, font=self.font, state="readonly",
                                           width=self.size_cmb_time_width, height = 7, value=self.hours)
        
        self.cmb_start_minute = ttk.Combobox(frame_attend, font=self.font, state="readonly",
                                             width=self.size_cmb_time_width, height = 7, value=self.minutes)
        
        Label(frame_attend, text="분", font=self.font).pack(side="right")
        self.cmb_start_minute.pack(side="right")
        
        UI_setting.space_area(frame_attend, side="right", length=self.space_area)
        
        Label(frame_attend, text="시", font=self.font).pack(side="right")
        self.cmb_start_hour.pack(side="right")
    
    def set_Leave_Time_Frame(self, parent):
        # 퇴근시간 입력
        frame_leave = UI_setting.set_frame(parent, pady=5)
        
        Label(frame_leave, text="퇴근", font=self.font).pack(side="left")
        
        self.cmb_end_hour = ttk.Combobox(frame_leave, font=self.font, state="readonly",
                                         width=self.size_cmb_time_width, height = 7, value=self.hours)
        
        self.cmb_end_minute = ttk.Combobox(frame_leave, font=self.font, state="readonly",
                                           width=self.size_cmb_time_width, height = 7, value=self.minutes)
        
        Label(frame_leave, text="분", font=self.font).pack(side="right")
        self.cmb_end_minute.pack(side="right")
    
        UI_setting.space_area(frame_leave, side="right", length=self.space_area)
        
        Label(frame_leave, text="시", font=self.font).pack(side="right")
        self.cmb_end_hour.pack(side="right")
        
        
        
    def set_Rest_Time_Frame(self, parent):
        # 휴게시간 입력
        frame_rest = UI_setting.set_frame(parent, pady=5)
        
        Label(frame_rest, text="휴게", font=self.font).pack(side="left")
        
        self.cmb_rest = ttk.Combobox(frame_rest, font=self.font, state="readonly",
                                     width=self.size_cmb_time_width, height = 7, value=self.rest)
        
        Label(frame_rest, text="분", font=self.font).pack(side="right")
        self.cmb_rest.pack(side = "right")
    
    def set_Button_Frame(self, parent):
        # 입력버튼
        frame_btns = UI_setting.set_frame(parent, padx=5, pady=5)
        
        self.btn_input = Button(frame_btns, text="입력", font=self.font,
                                width=10, height=2)
        self.btn_cancel = Button(frame_btns, text="뒤로", font=self.font,
                                 width=10, height=2)
        
        self.btn_input.pack(side="right")
        self.btn_cancel.pack(side="left")
    
    def cmd_btn_input(self):
        
        # 빈칸 확인
        flag_is_empty = f.check_is_Empty([self.cmb_start_hour, self.cmb_start_minute,
                                          self.cmb_end_hour, self.cmb_end_minute,
                                          self.cmb_rest, self.cmb_select_staff])
        if flag_is_empty:
            msgbox.showwarning("", "입력하지 않은 내용이 있습니다.")
            return
        
        work_hour, work_min = functions.get_work_result(start_hour=self.cmb_start_hour, start_min=self.cmb_start_minute, 
                                                end_hour=self.cmb_end_hour, end_min=self.cmb_end_minute,
                                                rest=self.cmb_rest)
        data = {}
        data["name"] = self.cmb_select_staff.get()
        data["attend_hour"] = self.cmb_start_hour.get()
        data["attend_min"] = self.cmb_start_minute.get()
        data["leave_hour"] = self.cmb_end_hour.get()
        data["leave_min"] = self.cmb_end_minute.get()
        data["rest"] = self.cmb_rest.get()
        data["work_hour"] = work_hour
        data["work_min"] = work_min
        data["date"] = self.selected_date.date()
        
        check_input_window = check_input.Check_Input(parent=self.window, data=data, top=self)
# =============================================================================
#     
#     def btn_Input(self):
#         work_result = functions.get_work_result(self.main_left_cmb)
#         if work_result == None:
#             return
#         work_hour, work_min, pay = work_result
#         
#         data = {}
#         data["name"] = self.main_left_cmb[0][0].get()
#         data["attend_hour"] = self.main_left_cmb[1][0].get()
#         data["attend_min"] = self.main_left_cmb[2][0].get()
#         data["leave_hour"] = self.main_left_cmb[3][0].get()
#         data["leave_min"] = self.main_left_cmb[4][0].get()
#         data["rest"] = self.main_left_cmb[5][0].get()
#         work_hour, work_min, pay = functions.get_work_result(self.main_left_cmb)
#         data["work_hour"] = work_hour
#         data["work_min"] = work_min
#         data["date"] = datetime.datetime.today().date()
#         
#         check_input.Check_Input(self.parent, self, data)
# =============================================================================
