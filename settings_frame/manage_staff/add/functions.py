import tkinter.messagebox as msgbox
from tkinter import *

from Functions import mongoDB, functions, compute

def check_Data_Integrity(entered_data):
    datas = [entered_data["empno"], entered_data["wage"]]
    
    for data in datas:
        if not functions.check_Integrity_numeric(data.get()):
            msgbox.showwarning("잘못된 내용", data.get() + "\n숫자만 입력하세요")
            get_Focus(data)
            return False
    
    for item, content in entered_data.items():
        if content.get() == "":
            msgbox.showwarning("null", "입력되지 않은 항목이 있습니다.\n" + item)
            get_Focus(content)
            return False
        
    return True

# 중복된 정보가 있다면 True 반환
def check_Duplication(entered_data):
    db = mongoDB.MongoDB.instance()
    #data_type = ["empno", "name", "phone"]
    
    data = entered_data["empno"].get()
    searched_data = list(db.collection_staff.find({"empno" : int(data)}))
    if len(searched_data) > 0:
        get_Focus(entered_data["empno"])
        return True, ("empno", data)
    
    data = entered_data["phone"].get()
    data = functions.format_Phone(data)
    searched_data = list(db.collection_staff.find({"phone" : data}))
    if len(searched_data) > 0:
        get_Focus(entered_data["phone"])
        return True, ("phone", data)
    
    data = entered_data["name"].get()
    searched_data = list(db.collection_staff.find({"name" : data}))
    if len(searched_data) > 0:
        get_Focus(entered_data["name"])
        return True, ("name", data)

    return False, None

def get_Focus(widget):
    widget.focus()
    widget.select_range(0, END)
    

def add_Staff(text_dic, chk_insurances,
              chk_days_var, cmb_attend_hour, cmb_attend_min, cmb_leave_hour, cmb_leave_min, cmb_rest):
    data = {}
    
    try:
        data["empno"] = int(text_dic["empno"].get())
        data["name"] = text_dic["name"].get()
        data["phone"] = functions.format_Phone(text_dic["phone"].get())
        data["payroll_account"] = {"bank" : text_dic["bank"].get(), "account" : text_dic["account"].get()}
        data["wage"] = int(text_dic["wage"].get())
        data["weekly_holiday_allowance"] = compute.check_Weekly_Holiday_Allowance(chk_days_var, 
            cmb_attend_hour, cmb_attend_min, cmb_leave_hour, cmb_leave_min, cmb_rest)
        data["contracted_work_time"] = {}
        #temp = {}
        for idx, day in enumerate(chk_days_var.values()):
            if day.get() == 1:
                temp = {}
                temp["start"] = cmb_attend_hour[idx].get() + cmb_attend_min[idx].get()
                temp["end"] = cmb_leave_hour[idx].get() + cmb_leave_min[idx].get()
                temp["rest"] = int(cmb_rest[idx].get())
                data["contracted_work_time"][functions.get_Weekday_by_Num(idx)] = temp
        
        insurances = {}
        for chk in chk_insurances.values():
            if chk[1].get() == 1:
                insurances[chk[0]["text"]] = chk[2]
        if len(insurances.keys()) > 0:
            data["insurances"] = insurances
        
        db = mongoDB.MongoDB.instance()
        db.collection_staff.insert(data)
        db.collection_ledger.insert(create_Ledger(name=data["name"], empno=data["empno"]))
    except:
        msgbox.showwarning("경고", "오류가 발생했습니다.\n")
        return False
    
    msgbox.showinfo("", "저장되었습니다.")
    return True

def create_Ledger(name, empno):
    ledger = {}
    ledger["staff"] = {"empno" : empno, "name" : name}
    ledger["contents"] = {}
    return ledger
