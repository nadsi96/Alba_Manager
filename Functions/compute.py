from Functions import mongoDB







# =============================================================================
# 출근시간, 퇴근시간, 휴게시간을 받아서 급여 계산
# staff = 직원 이름
# =============================================================================
def compute_pay(staff_name, start_time, end_time, rest_time):
    print("\ndef compute_pay start")
    work_h, work_m = compute_time(start_time, end_time, rest_time)
    
    print("\ncreate mongodb_Instance")
    db = mongoDB.MongoDB.instance()
    
    print("\nsearch_data..")
    staff = db.collection_staff.find_one({"name" : staff_name})
    print("search_done")
    print(staff)
    
    print("\n\n")
    print("work_time :", work_h, work_m)
    pay = (staff["wage"] * work_h) + int(staff["wage"] / 60 * work_m)
    return pay



# =============================================================================
# 시간 연산
# "1200", "1530" 형식의 시간이 주어졌을 때
# 이를 계산하여 "0330" 이라는 결과 도출
# 시간과 분을 나눠서 튜플로 반환 (3, 30)
# 
# 0시 ~ 24시
# time2에서 time1을 뺌
# time2가 time1보다 작다면 날짜가 바뀌었다는 의미
# =============================================================================
def compute_time(start_time, end_time, rest_time = 0):
    print("compute_time called")
    time1 = int(start_time)
    time2 = int(end_time)
    rest_time = int(rest_time)
    print("time1 :", time1)
    print("time2 :", time2)
    if time2 < time1:
        time2 += 2400
    
    time1_h = time1 // 100
    time1_m = time1 % 100
    
    time2_h = time2 // 100
    time2_m = time2 % 100
    
    print("time1_h, time1_m :", time1_h, time1_m)
    print("time2_h, time2_m :", time2_h, time2_m)
    
    result_h = time2_h - time1_h
    result_m = time2_m - time1_m - rest_time
    
    print("result_h :", result_h)
    print("result_m :", result_m)
#    if(result_m < 0):
#        result_h -= 1
#        result_m += 60
    while result_m < 0:
        result_h -= 1
        result_m += 60
    
    return result_h, result_m


# 주 15시간 이상 근로인지 확인하여
# 주휴수당이 지급되어야 하는지 확인
# 발생 = 금액, ㄴㄴ = 0
def check_Weekly_Holiday_Allowance(chk_days_var, cmb_attend_hour, cmb_attend_min, cmb_leave_hour, cmb_leave_min, cmb_rest):
    
    total_h = 0
    total_m = 0
    cond = 15 * 60
    
    for idx, day in enumerate(chk_days_var.values()):
        if day.get() == 1:
            start_time = cmb_attend_hour[idx].get() + cmb_attend_min[idx].get()
            end_time = cmb_leave_hour[idx].get() + cmb_leave_min[idx].get()
            rest_time = int(cmb_rest[idx].get())
            
            work_h, work_m = compute_time(start_time, end_time, rest_time)
            total_h += work_h
            total_m += work_m
    total = total_h * 60 + total_m
    
    if total >= cond:
        return 1
    else:
        return 0

# staff = mongodb dic
def compute_Weekly_Holiday_Allowance(staff):
    basic = 0
    for value in staff["contracted_work_time"].values():
        basic += compute_pay(staff["name"], value[0], value[1], value[2])
    print()
    print("basic :", basic)
    
    total = basic // 40 * 8 * staff["wage"]
    print("total :", total)
    print()
    return total

def compute_Tax(pay, tax):
    return (pay*(tax*0.01))