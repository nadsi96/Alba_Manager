from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox

import pandas as pd
from pandastable import TableModel

import datetime

from settings_frame.manage_staff.modify import modify_staff

from Functions import mongoDB

import sys, traceback

class Remove_Staff(modify_staff.Modify_Staff):
    def __init__(self, parent):
        super().__init__(parent)
        self.window.title("Remove_Staff")
        
        self.btn_select.config(text="삭제", command=self.cmd_Remove)
        return
    
    def cmd_Remove(self):
        if self.cmb_names.get() == "":
            msgbox.showinfo("", "직원을 먼저 선택하세요")
            return
        response = msgbox.askyesno("Remove", "정말 제거하시겠습니까?")
        if response == 1:
            print("Remove Staff")
            empno = self.lbl_id["text"]
            name = self.cmb_names.get()
            print("empno :", empno)
            print("name :", name)
            
            db = mongoDB.MongoDB.instance()
            staff_to_del = db.collection_staff.find_one({"empno" : empno, "name" : name})
#            print(db.collection_staff.remove({"empno" : empno, "name" : name}))
#            print(db.collection_Work_Record.remove({"staff.empno" : empno, "staff.name" : name}))
            try:
                temp_cur = dict(db.collection_Work_Record.find_one({"staff.empno" : empno, "staff.name" : name}))
                print()
                print("temp_cur")
                print(temp_cur)
                del temp_cur["staff"]["empno"]
                temp_cur["staff"]["phone"] = staff_to_del["phone"]
                temp_cur["staff"]["retire_date"] = {}
                today = datetime.date.today()
                temp_cur["staff"]["retire_date"]["year"] = today.year
                temp_cur["staff"]["retire_date"]["month"] = today.month
                temp_cur["staff"]["retire_date"]["day"] = today.day
                
                print()
                print(temp_cur)
                db.collection_Work_Record.update({"staff.empno" : empno, "staff.name" : name}, temp_cur)
            except:
                traceback.print_exc()
            
            try:
                temp_cur = dict(db.collection_ledger.find_one({"staff.empno" : empno, "staff.name" : name}))
                print()
                print("temp_cur")
                print(temp_cur)
                del temp_cur["staff"]["empno"]
                temp_cur["staff"]["phone"] = staff_to_del["phone"]
                temp_cur["staff"]["retire_date"] = {}
                today = datetime.date.today()
                temp_cur["staff"]["retire_date"]["year"] = today.year
                temp_cur["staff"]["retire_date"]["month"] = today.month
                temp_cur["staff"]["retire_date"]["day"] = today.day
                print()
                print(temp_cur)
                
                db.collection_ledger.update({"staff.empno" : empno, "staff.name" : name}, temp_cur)
            except:
                traceback.print_exc()
                
            print(db.collection_staff.remove({"empno" : empno, "name" : name}))
            #print(list(db.collection_staff.find({"empno" : empno, "name" : name})))
            
            self.lbl_id.config(text="-")
            self.lbl_phone.config(text="-")
            self.lbl_bank.config(text="-")
            self.lbl_account.config(text="-")
            self.lbl_wage.config(text="-")

            self.pt.updateModel(TableModel(pd.DataFrame({}, index=[0])))
            self.pt.redraw()
            self.update_Staff_Name_List(db)
            msgbox.showinfo("", "제거되었습니다.")
        else:
            print("Cancel")
    
    def update_Staff_Name_List(self, db):
        name_list = db.get_Staff_name()
        self.cmb_names.config(value=name_list)
        self.cmb_names.set("")
        return