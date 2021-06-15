import pandas as pd
from pandastable import Table, TableModel

#{"$project" : {
#                        "year" : "$date.year",
#                        "month" : "$date.month",
#                        "day" : "$date.day",
#                        "id" : "$staff.empno",
#                        "이름" : "$staff.name",
#                        "출근" : "$time.start",
#                        "퇴근" : "$time.end",
#                        "근무시간" : {"$arrayElemAt" : ["$time.work_time", 2]},
#                        "휴게" : "$time.rest",
#                        "대타" : "$substitution",
#                        "시간변경" : "$change_time"}}
def set_Column_Size(dataframe, pt):
    width = 0
    for idx, col in enumerate(dataframe.columns):
        if col in ["year", "month", "day"]:
            width = 50
        elif col in ["이름", "출근", "퇴근", "근무시간", "대타"]:
            width = 60
        elif col in ["휴게", "id"]:
            width = 40
        else:
            continue
        pt.resizeColumn(col=idx, width=width)
    return pt


def init_Dataframe(db, boolean=True):
    cursors = db.init_Dataframe(boolean)
    data = []
    
    for cursor in cursors:
            temp_data = {}
            for key, value in cursor.items():
                temp_data[key] = value
            data.append(temp_data)
        
    print("\ndata :")
    for d in data:
        print(d)
        print()
    
    df = pd.DataFrame(data)
    
    return df