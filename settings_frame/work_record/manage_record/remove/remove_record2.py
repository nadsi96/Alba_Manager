from settings_frame.work_record.manage_record.modify import modify_record

from tkinter import *
import tkinter.messagebox as msgbox

from Functions import mongoDB, compute


class Remove_Record(modify_record.Modify_Record):
    def __init__(self, parent):
        super().__init__(parent)
        self.window.title("Remove_Record")
        
        self.btn_input.config(command=self.show_MsgBox, text="선택")
    
    def update_Ledger(self):
        db = mongoDB.MongoDB.instance()
        year = str(self.data["date"]["year"])
        month = self.data["date"]["month"]
        if month < 10:
            month = "0" + str(month)
        else:
            month = str(month)
        
        
        basic = compute.compute_pay(staff_name=self.data["staff"]["name"],
                                    start_time=self.data["time"]["start"],
                                    end_time=self.data["time"]["end"],
                                    rest_time=self.data["time"]["rest"])
        staff = db.collection_staff.find_one({"name" : self.data["staff"]["name"], "empno" : self.data["staff"]["empno"]})
        
        # 기본 수당
        db.collection_ledger.update({"staff.name" : staff["name"], "staff.empno" : staff["empno"]},
                                     {"$inc" : {"contents.{0}.{1}.payment_details.basic_pay".format(year, month) : -basic}})
        
        # 주휴수당
        
        # 추가근로수당
        
        # 야간근로수당
        
        # 세금계산
        ledger = db.collection_ledger.find_one({"staff.name" : staff["name"], "staff.empno" : staff["empno"]})
        payment_detail = ledger["contents"][year][month]["payment_details"]
        payment = payment_detail["basic_pay"] + payment_detail["additional_work"] + payment_detail["night_work"] + payment_detail["weekly_holiday_allowance"][0]
        for insurance, tax in staff["insurances"].items():
            db.collection_ledger.update({"staff.name" : staff["name"], "staff.empno" : staff["empno"]},
                                         {"$set" : {"contents.{0}.{1}.deduction_details.{2}".format(year, month, insurance) : compute.compute_Tax(payment, tax)}})
        
        # total
        ledger = db.collection_ledger.find_one({"staff.name" : staff["name"], "staff.empno" : staff["empno"]})
        payment_detail = ledger["contents"][year][month]["payment_details"]
        payment = payment_detail["basic_pay"] + payment_detail["additional_work"] + payment_detail["night_work"] + payment_detail["weekly_holiday_allowance"][0]
        deduction_detail = ledger["contents"][year][month]["deduction_details"]
        tax = 0
        for t in deduction_detail.values():
            tax += t
        total = payment - tax
        db.collection_ledger.update({"staff.name" : staff["name"], "staff.empno" : staff["empno"]},
                                     {"$set" : {"contents.{0}.{1}.total".format(year, month) : total}})
        return
    
    def show_MsgBox(self):
        response = msgbox.askyesno(title=None, message="삭제하시겠습니까?")
        if response == 1:
            print("yes")
            print()
            db = mongoDB.MongoDB.instance()
            self.update_Ledger()
            print(db.collection_Work_Record.remove(self.data))
            # 삭제 후 정보화면 빈 값으로
            print()
            
            self.sb_Changed()
            
            self.lbl_name.config(text="")
            self.lbl_attend_hour.config(text="--")
            self.lbl_attend_min.config(text="--")
            self.lbl_leave_hour.config(text="--")
            self.lbl_leave_min.config(text="--")
            self.lbl_rest.config(text="--")
            self.lbl_work_hour.config(text="--")
            self.lbl_work_min.config(text="--")
            
            self.lbl_additional.config(text="-")
            self.lbl_additional_title.config(text="-")
            
            msgbox.showinfo("", "삭제되었습니다")
            return
        else:
            print("no")
            return
# =============================================================================
# def yes_no():
#     msgbox.askyesno("제목", "내용")
# Button(root, command=yes_no, text="예 / 아니요").pack()
# =============================================================================
