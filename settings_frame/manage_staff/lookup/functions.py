import pandas as pd
from pandastable import TableModel

from Functions import mongoDB

# =============================================================================
# _data = {"요일" : "1", "출근" : "1", "퇴근" : "-", "휴게" : "-", "근무시간(분)" : "-"}
# =============================================================================


def cmb_Changed(table, name):
    db = mongoDB.MongoDB.instance()
    data = db.get_Staff_Data(name=name)[name]
    
    time = data["contracted_work_time"]
    days = list(time.keys())
    start = []
    end = []
    rest = []
    
    for day in days:
        start.append(time[day]["start"])
        end.append(time[day]["end"])
        rest.append(time[day]["rest"])
    _data = {}
    _data["요일"] = days
    _data["출근"] = start
    _data["퇴근"] = end
    _data["휴게"] = rest
    df = pd.DataFrame(_data)
    
    table.updateModel(TableModel(df))
    table.redraw()
    
    return data

def set_Staff_cmb():
    db = mongoDB.MongoDB.instance()
    names = db.get_Staff_name()
    
    return names