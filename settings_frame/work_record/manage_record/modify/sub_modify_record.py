from tkinter import *
import tkinter.ttk as ttk

import datetime
import pandas as pd
from pandastable import Table

from UI import UI_setting, check_input
from Functions import mongoDB
from Functions import functions as f

from settings_frame.work_record.manage_record.modify import functions
from settings_frame.work_record.manage_record.add import add_record

class Sub_Modify_Record_Window(add_record.Add_Record):
    def __init__(self, parent, data, top):
        super().__init__(parent)
        self.window.title("modify_Record")
        self.parent = parent
        self.top = top
        self.data = data
        
        print("\n\nSub_Modify_Record_Window\ngetted_data :")
        print(data)
        self.set_Default()
        self.btn_input.config(command=self.btn_Input)
        return

    def set_Default(self):
        year = self.data["date"]["year"]
        month = self.data["date"]["month"]
        day = self.data["date"]["day"]
        
        self.sb_year.set(year)
        self.sb_month.set(month)
        self.sb_day.set(day)
        self.selected_date = self.selected_date.replace(year=int(year), month=int(month), day=int(day))
        
        self.cmb_select_staff.set(self.data["staff"]["name"])
        self.cmb_start_hour.set(self.data["time"]["start"][:2])
        self.cmb_start_minute.set(self.data["time"]["start"][2:])
        self.cmb_end_hour.set(self.data["time"]["end"][:2])
        self.cmb_end_minute.set(self.data["time"]["end"][2:])
        self.cmb_rest.set(self.data["time"]["rest"])
        
        return
    
    def btn_Input(self):
        print("Button Clicked")
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
        
        check_input_window = check_input.Check_Input(parent=self.window, data=data, top=self, original_data=self.data)