import datetime
from dateutil.relativedelta import relativedelta

from Functions import mongoDB, compute

def get_last_day(date=datetime.datetime.today().date()):
    print("getted_date :", date)
    last_day = 0
    if date.month < 12:
        last_day = date.replace(month=date.month+1, day=1) - datetime.timedelta(days=1)
    else:
        last_day = date.replace(year=date.year+1, month=1, day=1) - datetime.timedelta(days=1)
    print("last_day :", last_day.day)
    return last_day.day

def format_Phone(phone):
    if phone.isdecimal():
        return formatting_phone(phone)
    
    split_phone = phone.split("-")
    for idx, nums in enumerate(split_phone):
        if nums.find(" ") != -1:
            split_phone[idx] = nums.split()
    phone = ""

    for nums in split_phone:
        for num in nums:
            phone += num
    return formatting_phone(phone)

def formatting_phone(numeric_phone):
    sperater = (3, -4)
    p = list(numeric_phone)
    for idx in sperater:
        p.insert(idx, "-")
    
    formed_phone = ""
    for n in p:
        formed_phone += n
        
    return formed_phone

def check_Integrity_nulls(datas):
    for data in datas:
        if check_Integrity_null(data):
            continue
        else:
            return False, data
    return True


# == check_is_Empty(data, datas)
def check_Integrity_null(data):
    if data == "" or data == None:
        return False
    else:
        return True

# 입력한 데이터가 숫자형인지
def check_Integrity_numeric(data):
    try:
        int(data)
    except:
        return False
    return True

def get_Weekday_by_Num(day=None):
    print("day :", day)
    day_dic = {0 : "mon", 1 : "tue", 2 : "wed", 3 : "thu", 4 : "fri", 5 : "sat", 6 : "sun"}
    return day_dic[day]

def get_Weekday_by_Str(day=None):
    print("day :", day)
    day_dic = {"mon" : 0, "tue" : 1, "wed" : 2, "thu" : 3, "fri" : 4, "sat" : 5, "sun" : 6}
    return day_dic[day]

#저장하려는 데이터에 입력하지 않은 빈 칸이 있는지 확인
def check_is_Empty(data):
    print("\ndata:")
    print(data)
    print()
    for d in data:
        if d.get() == "" or d.get() == None:
            return True
# =============================================================================
#     if data == "":
#         return True
#     for d in datas:
#         if d == "":
#             return True
# =============================================================================
    return False

# 입력/수정하는 근무시간이 중복된 시간인지 확인
# 중복된 내용이 있다면 True 반환
# 아니라면 False 반환
def check_Duplicated_Work_Time(staff_name, start_time, end_time, date=None, original_data=None):
    
    db = mongoDB.MongoDB.instance()
    
    temp_start_time = int(start_time)
    temp_end_time = int(end_time)
    if temp_end_time < temp_start_time:
        temp_end_time += 2400
        
    cursors = []
    
    if original_data:
        #수정하는 경우
        cursors = db.collection_Work_Record.find({"_id" : {"$not" : {"$eq" : original_data["_id"]}}, 
                                                "date.year" : date.year, "date.month" : date.month, "date.day" : date.day,
                                                "staff.s_name" : staff_name})
    else:
        # 새로 입력하는 경우
        cursors = db.collection_Work_Record.find({"date.year" : date.year, "date.month" : date.month, "date.day" : date.day, "staff.name" : staff_name})
        
    for cursor in cursors:
        print(cursor)
        print()
        compare_start = int(cursor["time"]["start"])
        compare_end = int(cursor["time"]["end"])
        if compare_end < compare_start:
            compare_end += 2400
        
        if compare_start >= temp_start_time and compare_start < temp_end_time:
            return True
        elif compare_end > temp_start_time and compare_end <= temp_end_time:
            return True
        elif compare_start == temp_start_time and compare_end == temp_end_time:
            return True
        elif compare_start > temp_start_time and compare_end < temp_end_time:
            return True
        elif compare_start < temp_start_time and compare_end > temp_end_time:
            return True
    
    return False

# 변동된 근무시간인지 확인
# 변동된 근무시간이라면 True
# ㄴㄴ? => False
def check_Changed_Work_Time(staff_name, date, start_time, end_time, rest_time):
    db = mongoDB.MongoDB.instance()
    weekday = get_Weekday_by_Num(datetime.datetime.weekday(date))
    print("weekday :", weekday)
    staff = db.collection_staff.find_one({"name" : staff_name})
    print(staff)
    
    print()
    print("start_time :", start_time)
    print("end_time :", end_time)
    print("rest_time :", type(rest_time))
#    print(staff["contracted_work_time"][weekday]["start"])
#    print(staff["contracted_work_time"].keys())
#    print(weekday in staff["contracted_work_time"].keys())
    if weekday in staff["contracted_work_time"].keys():
        print(1)
        if staff["contracted_work_time"][weekday]["start"] != start_time:
            print(2)
            return True
        if staff["contracted_work_time"][weekday]["end"] != end_time:
            print(3)
            return True
        if staff["contracted_work_time"][weekday]["rest"] != rest_time:
            print(4)
            print(staff["contracted_work_time"][weekday]["rest"])
            print(type(staff["contracted_work_time"][weekday]["rest"]))
            print(rest_time)
            
            return True
    else:
        return True
    return False

# 창을 닫을 때, 부모 화면이 나타나도록
def on_Closing(parent, window):
    parent.grab_set()
    window.destroy()
    return

# data = work_record_data
# type = dic
# Work_Record에 먼저 기록된 후 진행
# 주휴수당이 기록된 주라면 근무기록에 표시
def check_Weekly_Holiday_Allowance(data, original_data=None):
    db = mongoDB.MongoDB.instance()
    
    staff = db.collection_staff.find_one({"empno" : data["staff"]["empno"], "name" : data["staff"]["name"]})
    cursors = db.collection_Work_Record.find({"date.yweek.0" : data["date"]["yweek"][0],
                                              "date.yweek.1" : data["date"]["yweek"][1],
                                              "staff.name" : staff["name"],
                                              "staff.empno" : staff["empno"]})
    
    if not original_data:
        for cursor in cursors:
            if cursor["weekly_holiday_allowance_compute"] == 1:
                return 0
    
    my_work_cnt = 0
    have_to_work_cnt = len(staff["contracted_work_time"])
    for cursor in cursors:
        if "my_work_time" in cursor.keys():
            my_work_cnt += 1
    print()
    print("my_work_cnt :", my_work_cnt)
    print("have_to_work_cnt :", have_to_work_cnt)
    print()
    if my_work_cnt == have_to_work_cnt:
        for cursor in cursors:
            cursor["weekly_holiday_allowance_compute"] = 1
            db.collection_Work_Record.update({"staff.empno" : staff["empno"],
                                              "staff.name" : staff["name"],
                                              "date.year" : data["date"]["year"],
                                              "date.month" : data["date"]["month"],
                                              "date.day" : data["date"]["day"],
                                              "time.start" : data["time"]["start"],
                                              "time.end" : data["time"]["end"],
                                              "time.rest" : data["time"]["rest"]}, cursor)
    
        return compute.compute_Weekly_Holiday_Allowance(staff)
    return 0

# 날짜 표시할 spinbox 기능, 유효성 검사 설정
# =============================================================================

def sb_Incr(event=None, controller=None, func=None):
    print("============")
    print("sb_Incr")
    controller.selected_date += func
    print("selected_date :", controller.selected_date)
    return
    
def sb_Decr(event=None, controller=None, func=None):
    print("============")
    print("sb_Decr")
    controller.selected_date -= func
    print("selected_date :", controller.selected_date)
    return

# 왜 때문에 매개변수가 다 str로 넘어갔는데
# 왜 그렇게 됐더라..
# =============================================================================
# def sb_valid(user_input, controller, sb_widget, idx):
#     print("sb_Valid")
#     print("idx :", idx, type(idx))
#     idx = int(idx)
#     print("user_input :", user_input)
#     print(type(user_input))
#     print("controller :", controller, type(controller))
#     print("sb_widget :", sb_widget, type(controller))
#     print("idx :", idx, type(controller))
#     if user_input.isdigit():
#         
#         minval = int(controller.window.nametowidget(sb_widget).config('from')[4])
#         maxval = int(controller.window.nametowidget(sb_widget).config('to')[4]) + 1
#         
#         int_user_input = int(user_input)
#         if int_user_input not in range(minval, maxval): 
#             print ("Out of range") 
#             return False
#         
#         if idx == 0:
#             controller.selected_date = controller.selected_date.replace(year=int_user_input)
#         elif idx == 1:
#             controller.selected_date = controller.selected_date.replace(month=int_user_input)
#         elif idx == 2:
#             controller.selected_date = controller.selected_date.replace(day=int_user_input)
#         print(user_input)
#         print("selected_date :", controller.selected_date)
#         return True
#     elif user_input == "":
#         print(user_input)
#         return True
#     else:
#         print("Not Numeric")
#         return False
# =============================================================================

def set_sb_date(controller, sb_dic, func=None):
    print("set_sb_date")
    
    # 월까지만 조회하는 경우
    # day에서 에러가 나겠죠?
    # 그냥 이렇게 넘기면 안될까요?
    sb_dic["year"].set(controller.selected_date.year)
    sb_dic["month"].set(controller.selected_date.month)
    
    print("sb_year :", sb_dic["year"].get())
    print("sb_month :", sb_dic["month"].get())
#    try:
#        sb_dic["day"].set(controller.selected_date.day)
#    except:
#        pass
    if "day" in sb_dic.keys():
        sb_dic["day"].set(controller.selected_date.day)
        print("sb_day :", sb_dic["day"].get())
    
    if func:
        func()
        print("set_sb_date func End")
#    print(controller.sb_year.get(), controller.sb_month.get(), controller.sb_day.get())
#    print(controller.selected_date)
#    print()
    
    return print("set_sb_date End")

def set_Date_Spinbox_Command(controller, sb_dic, func=None):
    print("set_Date_Spinbox_Command")
    date_dic = {"year" : lambda x : relativedelta(years=x),
               "month" : lambda x : relativedelta(months=x),
               "day" : lambda x : relativedelta(days=x)}
        
#    range_validation = controller.window.register(sb_valid)
    for idx, (key, value) in enumerate(sb_dic.items()):
        print("idx :", idx)
        print("key :", key)
        print("value :", value)
#        value.config(validatecommand=(range_validation, '%P', value, idx))
#        value.config(validatecommand=(range_validation, '%P', controller, sb_dic[key], idx))
#        value.config(validatecommand=lambda w=controller, x='%P', y=sb_dic[key], z=idx : range_validation(w, x, y, z))
        value.bind("<<Increment>>", lambda x, y=key : sb_Incr(event=x, controller=controller, func=date_dic[y](1)))
        value.bind("<<Decrement>>", lambda x, y=key : sb_Decr(event=x, controller=controller, func=date_dic[y](1)))
        value.config(command=lambda : set_sb_date(controller, sb_dic, func))
    return
# =============================================================================
