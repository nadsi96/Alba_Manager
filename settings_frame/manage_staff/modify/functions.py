import tkinter.messagebox as msgbox
from tkinter import *

from Functions import mongoDB, functions, compute

def get_Original_Data(empno, name):
    db = mongoDB.MongoDB.instance()
    print("find\nempno :", empno, "\nname :", name)
    original_data = db.collection_staff.find_one({"empno" : empno, "name" : name})
    print("\n")
    print(original_data)
    print("\n")
    return original_data

def update_Data(original_data, new_data):
    db = mongoDB.MongoDB.instance()
    
    
    for_input_data = {}
    for key, value in original_data.items():
        for_input_data[key] = value
    #for_input_data = original_data
    
    try:
        for key, value in new_data.items():
            for_input_data[key] = value
        print("\noriginal_data :\n",original_data)
        print("\nfor_input_data :\n",for_input_data)
    except:
        msgbox.showwarning("", "오류가 발생하였습니다.\n다시 시도하세요")
        return
    
    try:
        print(db.collection_staff.update({"_id" : original_data["_id"]}, for_input_data))
        msgbox.showinfo("", "수정되었습니다")
    except:
        msgbox.showwarning("", "오류가 발생하였습니다.\n다시 시도하세요")
    
    return

def set_New_Data(text_dic, chk_insurances,
                 chk_days_var, cmb_attend_hour, cmb_attend_min, cmb_leave_hour, cmb_leave_min, cmb_rest):
    data = {}
    print("\n======================\nSetting_New_Data\n")
    try:
        data["empno"] = int(text_dic["empno"].get())
        data["name"] = text_dic["name"].get()
        data["phone"] = functions.format_Phone(text_dic["phone"].get())
        data["payroll_account"] = {"bank" : text_dic["bank"].get(), "account" : text_dic["account"].get()}
        data["wage"] = int(text_dic["wage"].get())
        data["weekly_holiday_allowance"] = compute.check_Weekly_Holiday_Allowance(chk_days_var, 
            cmb_attend_hour, cmb_attend_min, cmb_leave_hour, cmb_leave_min, cmb_rest)
        data["contracted_work_time"] = {}
        print(data)
        for idx, day in enumerate(chk_days_var.values()):
            if day.get() == 1:
                temp = {}
                temp["start"] = cmb_attend_hour[idx].get() + cmb_attend_min[idx].get()
                temp["end"] = cmb_leave_hour[idx].get() + cmb_leave_min[idx].get()
                temp["rest"] = int(cmb_rest[idx].get())
                print()
                print(temp)
                data["contracted_work_time"][functions.get_Weekday_by_Num(idx)] = temp
                print()
                print(data)
        
        insurances = {}
        for chk in chk_insurances:
            if chk[1] == 1:
                insurances[chk["text"]] = chk[2]
        if len(insurances.keys()) > 0:
            data["insurances"] = insurances
            
        print("\nnew_Data :",data,"\n") 
    except Exception as e:
        print("set_New_Data")
        print("Error Occured")
        print(e)
    return data

def check_Data_Duplication(original_data, new_data):
    db = mongoDB.MongoDB.instance()
    print("\nNew_Data : \n",new_data)
    datas = db.collection_staff.find({"_id" : {"$not" : {"$eq" : original_data["_id"]}}}, {"_id" : 0})
    
    key_for_check = ["empno", "name", "phone"]
    for data in datas:
        print()
        print(data)
        for key in key_for_check:
            if new_data[key] == data[key]:
                print(key)
                print(new_data[key])
                print("Duplicated!")
                msgbox.showwarning("", "다른 직원과 중복된 정보가 있습니다\n" + key + "\n" + new_data[key])
                return False
            else:
                print(key, "Checked")
    return True

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

def get_Focus(widget):
    widget.focus()
    widget.select_range(0, END)

def get_Staff_Name_List():
    db = mongoDB.MongoDB.instance()
    return db.get_Staff_name()