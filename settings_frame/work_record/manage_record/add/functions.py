import datetime

from Functions import mongoDB, compute

def get_Staff_name():
    names = mongoDB.MongoDB.instance().get_Staff_name()
    print("staff_names :")
    print(names)
    return names

def get_work_result(start_hour, start_min, end_hour, end_min, rest):
    start_time = start_hour.get() + start_min.get()
    end_time = end_hour.get() + end_min.get()
    
    result_h, result_m = compute.compute_time(start_time, end_time, rest.get())
    return result_h, result_m