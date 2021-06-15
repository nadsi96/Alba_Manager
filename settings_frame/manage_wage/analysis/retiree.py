from tkinter import *
import tkinter.ttk as ttk

from Functions import functions as f
from Functions import mongoDB

from UI import UI_setting

from settings_frame.manage_wage.analysis import functions
from settings_frame.manage_wage.analysis import by_staff
class Retiree(by_staff.By_Staff):
    def __init__(self, parent, controller, top):
#        Frame.__init__(self, parent, relief="solid", bd=1)
        super().__init__(parent, controller, top, is_exists=False)
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
        names = ["{}.{}".format("-", staff["name"]) for staff in staffs]
        for idx, name in enumerate(names):
            self.chkvar_staffs[name.split(".")[1]] = IntVar()
            self.chk_staffs.append(Checkbutton(frame_staffs, text=name, variable=self.chkvar_staffs[name.split(".")[1]], font=self.font))
            self.chk_staffs[idx].pack(side="top", anchor="w")
            self.chk_staffs[idx].select()
        return