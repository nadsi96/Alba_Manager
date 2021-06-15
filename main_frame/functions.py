from tkinter import *
import tkinter.messagebox as msgbox
from Functions  import compute, mongoDB

from settings_frame import settings_frame

# 입력버튼 눌렀을 때
# 입력되지 않은 항목이 있는지 확인 후
# 근무시간 계산
# =============================================================================
# [[self.cmb_staff, "staff_name"], 
# [self.cmb_start_hour, "start_hour"], 
# [self.cmb_start_minute, "start_minute"], 
# [self.cmb_end_hour, "end_hour"], 
# [self.cmb_end_minute, "end_minute"], 
# [self.cmb_rest, "rest_time"]]
# =============================================================================
def get_work_result(cmb_list):
    for cmb in cmb_list:
        if cmb[0].get() == "":
            msgbox.showerror("error", "input " + cmb[1])
            return None
    print("Click")
    staff_name = cmb_list[0][0].get()
    start_time = cmb_list[1][0].get() + cmb_list[2][0].get()
    end_time = cmb_list[3][0].get() + cmb_list[4][0].get()
    rest_time = int(cmb_list[5][0].get())
    print("data_set")
    pay = compute.compute_pay(staff_name, start_time, end_time, rest_time)
    work_hour, work_min = compute.compute_time(start_time, end_time, rest_time)
    print("compute.compute_pay returned")
    print("pay :", pay)
    return work_hour, work_min, pay

# =============================================================================
# 메인 화면에서 직원 이름 선택 콤보박스에 불러올 직원의 이름 반환
# db에서 읽어서 이름만 뽑아 반환
# =============================================================================
def call_Staff_List():
    # 스태프 이름 목록 호출
    db = mongoDB.MongoDB.instance()
    name_list = db.get_Staff_name()
    return name_list

def get_Staff_Contracted_Work_Time(name):
    db = mongoDB.MongoDB.instance()
    try:
        data = db.collection_staff.find_one({"name" : name})
        print(data)
        contracted_work_time = data["contracted_work_time"]
    except:
        msgbox.showwarning("", "정보 호출 오류")
        print(db.collection_staff.find_one({"name" : name}))
        return None
    return contracted_work_time

# 설정 버튼 클릭시
# 근무기록, 직원관리, 급여관리, {분석}
def open_settings(parent):
    setting = settings_frame.Setting_Frame(parent)
    print("click")
    

#입력된 메모 오늘 날짜로 저장
#이미 저장된 메모가 있다면 내용 교체
#없다면 신규 입력
def save_Memo(content, date):
    print("save_Memo")
    print(content)
    print("date", date)
    print("==")
    db = mongoDB.MongoDB.instance()
    cond = {"year" : date.year,
            "month" : date.month,
            "day" : date.day}
    cursor = db.collection_memo.find_one(cond)
    if cursor:
        db.collection_memo.update(cond, {"$set" : {"content" : content}})
        msgbox.showinfo("메모 입력", "{}년_{}월_{}일\n내용 :\n{}\n\n 업데이트 완료.".format(date.year,
                        date.month,
                        date.day,
                        content))
        return
    cond["content"] = content
    db.collection_memo.insert(cond)
    msgbox.showinfo("메모 입력", "{}년_{}월_{}일\n내용 :\n{}\n\n입력 완료.".format(date.year,
                        date.month,
                        date.day,
                        content))
    
    return

# 가장 최근 메모 호출하여 입력
def get_Recent_Memo(txtbox):
    print("get_Recent_Memo")
    db = mongoDB.MongoDB.instance()
    cursor = db.collection_memo.find().sort([("year", -1), ("month", -1), ("day", -1)]).limit(1)
    
    if cursor:
        txtbox.insert(END, "  ___{}_{}_{}_메모___  \n".format(cursor[0]["year"],
                                                      cursor[0]["month"],
                                                      cursor[0]["day"]))
        txtbox.insert(END, cursor[0]["content"])
        print(cursor[0]["year"], type(cursor[0]["year"]))
        return
    return