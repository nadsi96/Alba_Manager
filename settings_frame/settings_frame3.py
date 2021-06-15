from tkinter import *

from UI import UI_setting
from UI import btn_menu

from settings_frame.work_record.lookup_record import lookup
from settings_frame.work_record.manage_record import manage_record
from settings_frame.manage_staff import manage_staff
from settings_frame.manage_wage import manage_payroll

class Setting_Frame:
    def __init__(self, parent):
        self.parent = parent
        
        size = (20, 2)

        self.btn_work_record = Button(parent, text="근무기록", width=size[0], height=size[1],
                                      command=self.open_Work_record)
        self.btn_manage_staff = Button(parent, text="직원관리", width=size[0], height=size[1],
                                       command=self.open_Manage_Staff)
        self.btn_manage_pay = Button(parent, text = "급여관리", width=size[0], height=size[1],
                                     command=self.open_Manage_Payroll)
        #self.btn_analysis = Button(parent, text="분석", width=size[0], height=size[1])
        
        self.btn_work_record.pack(padx=5, pady = 5)
        self.btn_manage_staff.pack(padx=5, pady = 5)
        self.btn_manage_pay.pack(padx=5, pady = 5)
        #self.btn_analysis.pack(padx=5, pady = 5)
        
    def open_Work_record(self):
        size = (15, 2)
        frame_size = "170x120"
        self.work_record_window = UI_setting.new_Window(self.parent, title="Work_Record", frame_size=frame_size)
        
        def open_lookup_record():
            print("open_lookup() method called")
            self.lookup_record_window = lookup.Lookup_Window(self.parent, title="Lookup")
        self.btn_lookup_record = Button(self.work_record_window, text="조회", width=size[0], height=size[1], command=open_lookup_record)
        
        def open_manage_record():
            print("open_manage_record() method called")
            self.manage_record_window = manage_record.Manage_Record_Window(self.parent)
        self.btn_manage_record = Button(self.work_record_window, text="수정", width=size[0], height=size[1], command=open_manage_record)
            
        self.btn_lookup_record.pack(padx=5, pady=5)
        self.btn_manage_record.pack(padx=5, pady=5)

    def open_Manage_Staff(self):
        ms = manage_staff.Manage_Staff(self.parent)
    
    def open_Manage_Payroll(self):
        mp = manage_payroll.Manage_Payroll(self.parent)