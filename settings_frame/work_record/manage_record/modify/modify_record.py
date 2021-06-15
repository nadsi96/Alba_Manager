from tkinter import *
import tkinter.ttk as ttk

import datetime
import pandas as pd
from pandastable import Table

from UI import UI_setting
from Functions import mongoDB
from Functions import functions as f

from settings_frame.work_record.manage_record.modify import functions
from settings_frame.work_record.manage_record.modify import sub_modify_record

class Modify_Record:
    def __init__(self, parent):
        self.parent = parent
        self.window = UI_setting.new_Window(parent, title="Modify_Record")
        
        self.font = UI_setting.get_font(f_size=10)
        
        self.selected_date = datetime.datetime.today()
        
        self.search_data = {} #{이름, 출근, 퇴근 : 해당 기록}
        self.data = {} # 콤보박스에서 선택된 기록
        
        self.set_Window()
        
        self.window.grab_set()
        self.window.protocol("WM_DELETE_WINDOW", lambda : f.on_Closing(parent, self.window))
        return
        
        
    def set_Window(self):
        self.set_Date_Frame(self.window)
        self.set_Record_List_Frame(self.window)
        self.set_Content_Frame(self.window)
        self.set_Button_Frame(self.window)
        
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
        
        f.set_Date_Spinbox_Command(controller=self, sb_dic=self.sb_dic, func=self.sb_Changed)
        
        self.cmb_records.bind("<<ComboboxSelected>>", self.update_Dataframe)
        return
    def set_Date_Frame(self, parent):
        self.frame_outer_select_date = UI_setting.set_frame(parent, padx=5, pady=5)
        self.frame_select_date = UI_setting.set_frame(self.frame_outer_select_date)
        
        current_date = datetime.datetime.today()
        
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
        
        self.sb_year.set(current_date.year)
        self.sb_month.set(current_date.month)
        self.sb_day.set(current_date.day)
        
        return
    
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
#         
#         self.sb_Changed()
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
#         
#         #self.cmb_records.config(value=[])
#         self.sb_Changed()
#         
#         print("selectetd_date :", self.selected_date)
#         return
#     
#     def sb_day_Changed(self):
#         self.selected_date = self.selected_date.replace(day=int(self.sb_day.get()))
# # =============================================================================
# #         self.cmb_records.config(value=list(functions.get_cmb_Record(self.selected_date).keys()))
# #         
# #         self.search_data = functions.get_cmb_Record(self.selected_date)
# # =============================================================================
#         self.sb_Changed()
#         
#         print("selectetd_date :", self.selected_date)
#         return
# =============================================================================
    
        
    def sb_Changed(self):
        self.search_data = functions.get_cmb_Record(self.selected_date)
        
        self.cmb_records.config(value=list(self.search_data.keys()))
        self.cmb_records.set("")
        
        #self.update_Dataframe()
        
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
        
    # 이름, 출,퇴근시간
    def set_Record_List_Frame(self, parent):
        self.frame_select_record = UI_setting.set_frame(parent, padx=5, pady=5)
        
        self.search_data = functions.get_cmb_Record(self.selected_date)
        self.cmb_records = ttk.Combobox(self.frame_select_record, font=self.font, state="readonly",
                                        value=list(self.search_data.keys()))
        
        self.cmb_records.pack(fill="both")
        return
    
    def set_Content_Frame(self, parent):
        self.frame_show_content = UI_setting.set_frame(parent, padx=5, pady=5, width=320, height=400)
        self.lbl_content_date = Label(self.frame_show_content, text="", padx=5, pady=5)
        self.lbl_content_date.pack()
        
        self.frame_data_field = UI_setting.set_frame(self.frame_show_content)
        
        self.set_DataFrame()
        
        return
    
    def set_Date_Label(self):
        self.lbl_content_date.config(text=self.selected_date.date())
        return

    def set_DataFrame(self):
        
        self.frame_name = UI_setting.set_frame(self.frame_data_field, padx=5, pady=5)
        Label(self.frame_name, text="이름", font=self.font).pack(side="left")
        self.lbl_name = Label(self.frame_name, text="", font=self.font)
        self.lbl_name.pack(side="right")
        
        
        self.frame_time = UI_setting.set_frame(self.frame_data_field, padx=5, pady=5)
        
        self.frame_attend = UI_setting.set_frame(self.frame_time)
        Label(self.frame_attend, text="출근", font=self.font).pack(side="left")
        self.lbl_attend_hour = Label(self.frame_attend, text="--", font=self.font, padx=5)
        self.lbl_attend_min = Label(self.frame_attend, text="--", font=self.font, padx=5)
        
        Label(self.frame_attend, text="분", font=self.font).pack(side="right")
        self.lbl_attend_min.pack(side="right")
        UI_setting.space_area(self.frame_attend, side="right", length=5)
        Label(self.frame_attend, text="시", font=self.font).pack(side="right")
        self.lbl_attend_hour.pack(side="right")
        
        
        self.frame_leave = UI_setting.set_frame(self.frame_time)
        Label(self.frame_leave, text="퇴근", font=self.font).pack(side="left")
        self.lbl_leave_hour = Label(self.frame_leave, text="--", font=self.font, padx=5)
        self.lbl_leave_min = Label(self.frame_leave, text="--", font=self.font, padx=5)
        
        Label(self.frame_leave, text="분", font=self.font).pack(side="right")
        self.lbl_leave_min.pack(side="right")
        UI_setting.space_area(self.frame_leave, side="right", length=5)
        Label(self.frame_leave, text="시", font=self.font).pack(side="right")
        self.lbl_leave_hour.pack(side="right")
        
        
        self.frame_rest = UI_setting.set_frame(self.frame_time)
        Label(self.frame_rest, text="휴게", font=self.font).pack(side="left")
        self.lbl_rest = Label(self.frame_rest, text="--", font=self.font, padx=5)
        
        Label(self.frame_rest, text="분", font=self.font).pack(side="right")
        self.lbl_rest.pack(side="right")
        
        self.frame_work_time = UI_setting.set_frame(self.frame_time)
        Label(self.frame_work_time, text="근무시간", font=self.font).pack(side="left")
        self.lbl_work_hour = Label(self.frame_work_time, text="--", font=self.font, padx=5)
        self.lbl_work_min = Label(self.frame_work_time, text="--", font=self.font, padx=5)
        
        Label(self.frame_work_time, text="분", font=self.font).pack(side="right")
        self.lbl_work_min.pack(side="right")
        UI_setting.space_area(self.frame_work_time, side="right", length=2)
        Label(self.frame_work_time, text="시간", font=self.font).pack(side="right")
        self.lbl_work_hour.pack(side="right")
        
        self.frame_substitute = UI_setting.set_frame(self.frame_data_field, padx=5, pady=5)
        self.lbl_additional_title = Label(self.frame_substitute, text="-", font=self.font)
        self.lbl_additional_title.pack(side="left")
        self.lbl_additional = Label(self.frame_substitute, text="-", font=self.font, padx=5)
        self.lbl_additional.pack(side="right")
        
        
        self.set_Date_Label()
        
        return
    
    def update_Dataframe(self, event=None):
        
        print("\nupdate_Dataframe called\n")
        
        selected_key = self.cmb_records.get()
        print("selected_key :", selected_key )
        print("---------------------------")

        if selected_key != "":
            #data = self.search_data[self.cmb_records.get()]
            self.data = self.search_data[selected_key]
            print("data :", self.data)
        else:
            return
            
        self.lbl_name.config(text=self.data["staff"]["name"])
        
        self.lbl_attend_hour.config(text=self.get_Time_Text(self.data["time"]["start"][:2]))
        self.lbl_attend_min.config(text=self.get_Time_Text(self.data["time"]["start"][2:]))
        self.lbl_leave_hour.config(text=self.get_Time_Text(self.data["time"]["end"][:2]))
        self.lbl_leave_min.config(text=self.get_Time_Text(self.data["time"]["end"][2:]))
        self.lbl_rest.config(text=self.get_Time_Text(self.data["time"]["rest"]))
        
        self.lbl_work_hour.config(text=self.get_Time_Text(self.data["time"]["work_time"][0]))
        self.lbl_work_min.config(text=self.get_Time_Text(self.data["time"]["work_time"][1]))
        
        self.check_Substitute()
        self.set_Date_Label()
        return
    
    def check_Substitute(self):
        try:
            self.lbl_additional.config(text=self.data["substitute"])
#            self.lbl_additional_title.pack(side="left")
#            self.lbl_additional.pack(side="right")
            self.lbl_additional_title.config(text="대타")
        except:
#            self.lbl_additional.config(text="")
            print("대타 아님")
            try:
                self.lbl_additional.config(text=self.data["change_time"])
                self.lbl_additional_title.config(text="시간 변경")
            except:
                print("시간변동 아님")
                self.lbl_additional.config(text="-")
                self.lbl_additional_title.config(text="-")
        
    def get_Time_Text(self, time):
        time = str(int(time))
        if len(time) < 2:
            time = "0" + time
        return time
        
    def set_Button_Frame(self, parent):
        # 입력버튼
        frame_btns = UI_setting.set_frame(parent, padx=5, pady=5)
        
        self.btn_input = Button(frame_btns, text="선택", font=self.font,
                                width=10, height=2, command=lambda : self.btn_Input(parent))
        self.btn_cancel = Button(frame_btns, text="뒤로", font=self.font,
                                 command=lambda : f.on_Closing(self.parent, self.window), width=10, height=2)
        
        self.btn_input.pack(side="right")
        self.btn_cancel.pack(side="left")
        
        return
    
    def btn_Input(self, parent):
        print("data to send :")
        print(self.data)
        sbr = sub_modify_record.Sub_Modify_Record_Window(parent, self.data, self)