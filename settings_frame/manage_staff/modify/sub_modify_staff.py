from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox

from UI import UI_setting

from Functions import functions as f

from settings_frame.manage_staff.add import add_staff
from settings_frame.manage_staff.modify import functions

class Sub_Modify_Staff(add_staff.Add_Staff):
    
    #original_data = empno, name
    def __init__(self, parent, original_data, upperLevel):
        super().__init__(parent)
        self.upperLevel = upperLevel
        self.window.title("modify_staff")
        self.set_Origin_Data(original_data)
        
    def set_Origin_Data(self, original_data):
        self.original_data = functions.get_Original_Data(original_data[0], original_data[1])
        
        self.txt_name.insert(0, self.original_data["name"])
        self.txt_id.insert(0, self.original_data["empno"])
        self.txt_phone.insert(0, self.original_data["phone"])
        self.txt_bank.insert(0, self.original_data["payroll_account"]["bank"])
        self.txt_account.insert(0, self.original_data["payroll_account"]["account"])
        self.txt_wage.insert(0, self.original_data["wage"])
        
        for insurance in self.original_data["insurances"].keys():
            self.chk_insurances[insurance][0].select()
            
        contracted_time = self.original_data["contracted_work_time"]
        days = list(contracted_time.keys())
        for day in days:
            idx = f.get_Weekday_by_Str(day)
            
            self.chk_days[idx].select()
            
            self.cmb_attend_hour[idx].set(contracted_time[day]["start"][:2])
            self.cmb_attend_min[idx].set(contracted_time[day]["start"][2:])
            self.cmb_leave_hour[idx].set(contracted_time[day]["end"][:2])
            self.cmb_leave_min[idx].set(contracted_time[day]["end"][2:])
            self.cmb_rest[idx].set(contracted_time[day]["rest"])
            self.cmd_Time_Select(event=None, idx=idx)
        
        self.cmd_Check_Days()
        return
    
    def cmd_Input_Button(self):
        #if f.check_is_Empty([value for value in self.text_dic.values()]):
        if f.check_is_Empty(self.text_dic.values()):
            msgbox.showwarning("", "입력되지 않은 값이 있습니다.")
            return
        
        if not functions.check_Data_Integrity(self.text_dic):
            return
        
        new_data = functions.set_New_Data(self.text_dic, self.chk_insurances,
                                          self.chk_days_var, self.cmb_attend_hour, self.cmb_attend_min, self.cmb_leave_hour, self.cmb_leave_min, self.cmb_rest)
        flag = functions.check_Data_Duplication(self.original_data, new_data)
        if flag:
            functions.update_Data(self.original_data, new_data)
            self.upperLevel.cmb_names.set(new_data["name"])
            self.upperLevel.cmd_Name_Changed(event=None)
            self.parent.grab_set()
            self.upperLevel.cmb_names.config(value=functions.get_Staff_Name_List())
            self.window.destroy()
        return