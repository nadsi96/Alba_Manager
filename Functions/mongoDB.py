from pymongo import MongoClient
import pymongo
from pymongo.cursor import CursorType

class SingletonInstance:
    __instance = None
    
    @classmethod
    def __getInstance(cls):
        return cls.__instance
    
    @classmethod
    def instance(cls, *args, **kwargs):
        cls.__instance = cls(*args, **kwargs)
        cls.instance = cls.__getInstance
        return cls.__instance
    
class MongoDB(SingletonInstance):
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client["alba_manage"]
        
        self.collection_staff = self.db["staff"]
        self.collection_ledger = self.db["ledger"]
        self.collection_Log = self.db["Log"]
        self.collection_Work_Record = self.db["Work_Record"]
        self.collection_memo = self.db["memo"]
    
    def get_Staff_name(self):
        name_cursors = self.collection_staff.find({}, {"_id" : 0, "name" : 1, "empno" : 1}).sort("empno",1)
        staff_names = []
        for name in name_cursors:
            staff_names.append(name["name"])
        print("MongoDB() >> staff_names :", staff_names)
        return staff_names
    
    def get_Staff_Data(self, empno=None, name=None):
        cond = {}
        if empno != None:
            cond["empno"] = empno
        if name != None:
            cond["name"] = name
        
        data_cursors = self.collection_staff.find(cond, {"_id" : 0})
        data_list = {}
        for data in data_cursors:
            name = data["name"]
            data_list[name] = data
        return data_list
    
    def init_Dataframe(self, boolean):
        cond = [
                {"$match" : {"staff.empno" : {"$exists" : boolean}}},
                {"$project" : {
                        "_id" : 0,
                        "year" : "$date.year",
                        "month" : "$date.month",
                        "day" : "$date.day",
                        "id" : "$staff.empno",
                        "이름" : "$staff.name",
                        "출근" : "$time.start",
                        "퇴근" : "$time.end",
                        "근무시간" : {"$arrayElemAt" : ["$time.work_time", 2]},
                        "휴게" : "$time.rest",
                        "대타" : "$substitution",
                        "시간변경" : "$change_time"}},
                {"$sort" : {"year" : -1,
                            "month" : -1,
                            "day" : -1}}
            ]
        cursors = self.collection_Work_Record.aggregate(cond)
        return cursors


# =============================================================================
# db = MongoDB()
# #db.staff.find({"_id" : {$not : {$eq : 1}}}).pretty()
# od = db.collection_staff.find_one({"empno" : 1})
# print(od)
# 
# print(od["_id"])
# cursors = db.collection_staff.find({"_id" : {"$not" : {"$eq" : od["_id"]}}})
# for cursor in cursors:
#     print(cursor)
#     print()
# =============================================================================

# =============================================================================
# db = MongoDB()
# cursors = db.collection_Work_Record.find({}).sort([("date.year", -1), ("date.month", -1), ("date.day", -1)])
# for cursor in cursors:
#     print(cursor)
#     print()
# =============================================================================
