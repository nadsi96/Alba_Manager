import datetime
import pandas as pd

from Functions import mongoDB, compute

def get_Record(date=datetime.datetime.today()):
    mongo = mongoDB.MongoDB.instance()
    
    cond = {"year" : date.year, "month" : date.month, "day" : date.day}
    
    data = list(mongo.collection_Work_Record.find({"date.year" : cond["year"], "date.month" : cond["month"], "date.day" : cond["day"],
                                                   "staff.empno" : {"$exists" : True}}))
    print("search_data")
    for d in data:
        print(d)
    print("\n......")
    
    return data

def get_cmb_Record(date=datetime.datetime.today()):
    records = {}
    
    data = get_Record(date)
    print("\nget_data\n")
    print(data)
    for d in data:
        print(d)
    
    print("\nformating data\n")
    for d in data:
#        attend_time = str(int(d["time"]["start"][:2])) + "시 " + str(int(d["time"]["start"][2:])) + "분"
#        leave_time = str(int(d["time"]["end"][:2])) + "시 " + str(int(d["time"]["end"][2:])) + "분"
        attend_time = "{}시 {}분".format(d["time"]["start"][:2], d["time"]["start"][2:])
        leave_time = "{}시 {}분".format(d["time"]["end"][:2], d["time"]["end"][2:])
        data_str = "{0}_{1}_ {2} ~ {3}".format(d["staff"]["empno"], d["staff"]["name"], attend_time, leave_time)
        records[data_str] = d
        print(data_str)
        print()
#        string = str(int(d["staff"]["empno"])) + "_" + d["staff"]["name"] + "_" + attend_time + "_" + leave_time
#        records[string] = d
#        print(string)
#        print()
        
    print("\n.....")
    
    print("records : ")
    print(records)
    
    return records

def get_Content(data):
    d = {"년" : data["date"]["year"],
         "월" : data["date"]["month"],
         "일" : data["date"]["day"],
         "사번" : data["staff"]["empno"],
         "이름" : data["staff"]["name"],
         "출근" : str(int(data["time"]["start"][0])) + " : " + str(int(data["time"]["start"][1])),
         "퇴근" : str(int(data["time"]["end"][0])) + " : " + str(int(data["time"]["end"][1])),
         "휴게" : int(data["time"]["rest"]),
         "근무시간(분)" : int(data["time"]["work_time"][2])}
    df = pd.DataFrame(d, index=[0])
    return df
    
# =============================================================================
# def get_last_day(date=datetime.datetime.today()):
#     print("getted_date :", date)
#     last_day = date.replace(month=date.month+1, day=1) - datetime.timedelta(days=1)
#     print("last_day :", last_day.day)
#     return last_day.day
# =============================================================================

def get_work_result(start_hour, start_min, end_hour, end_min, rest):
    start_time = start_hour.get() + start_min.get()
    end_time = end_hour.get() + end_min.get()
    
    result_h, result_m = compute.compute_time(start_time, end_time, rest.get())
    return result_h, result_m