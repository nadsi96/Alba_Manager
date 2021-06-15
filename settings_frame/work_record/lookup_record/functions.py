import datetime
import pandas as pd
from Functions import mongoDB

def get_last_day(date=datetime.datetime.today()):
    last_day = date.replace(month=date.month+1, day=1) - datetime.timedelta(days=1)
    print("last_day :", last_day.day)
    return last_day.day

def get_Staff_name():
    names = mongoDB.MongoDB.instance().get_Staff_name()
    print("staff_names :")
    print(names)
    return names

def get_DataFrame(cond):
    mongo = mongoDB.MongoDB()
    
    return

