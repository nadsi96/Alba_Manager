from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox

import datetime

from UI import UI_setting, check_input_sub
from Functions import functions as f
from Functions import mongoDB, compute

class Check_Input:
    def __init__(self, parent, top, data, original_data=None):
        self.parent = parent
        self.top = top
        #self.window = UI_setting.new_Window(parent, title="Check_Input")
        self.window = Toplevel(parent)
        self.window.title("Check_Input")
        
        self.data = data
        self.original_data = original_data
        self.selected_date = self.data["date"]
        
        self.font = UI_setting.get_font()
        
        self.set_Window()
        
        self.window.grab_set()
        self.window.protocol("WM_DELETE_WINDOW", lambda : f.on_Closing(parent, self.window))
        return
    
    def set_Window(self):
        self.set_Date_Spinbox(self.window)
        self.set_Info(self.window)
        self.set_Button(self.window)
        
        self.set_Command()
        return
    
    
    def set_Date_Spinbox(self, parent):
        self.frame_show_date = UI_setting.set_frame(parent, padx=5, pady=5)
# =============================================================================
#         self.lbl_selected_date = Label(self.frame_show_date, text=self.selected_date, font=self.font)
#         self.lbl_selected_date.pack()
# =============================================================================
        self.sb_year, self.sb_month, self.sb_day = UI_setting.get_Date_Spinbox(self.frame_show_date)
        self.sb_year.config(font=self.font)
        self.sb_month.config(font=self.font)
        self.sb_day.config(font=self.font)
        self.sb_year.pack(side="left")
        Label(self.frame_show_date, text="년 ", font=self.font).pack(side="left")
        self.sb_month.pack(side="left")
        Label(self.frame_show_date, text="월 ", font=self.font).pack(side="left")
        self.sb_day.pack(side="left")
        Label(self.frame_show_date, text="일", font=self.font).pack(side="left")
        
        self.sb_year.set(self.selected_date.year)
        self.sb_month.set(self.selected_date.month)
        self.sb_day.set(self.selected_date.day)
        return
    
    def set_Command(self):
# =============================================================================
#         self.sb_year.config(command=self.sb_year_Changed)
#         self.sb_month.config(command=self.sb_month_Changed)
#         self.sb_day.config(command=self.sb_day_Changed)
# =============================================================================
        
        range_validation = self.window.register(self.sb_valid)
# =============================================================================
#         self.sb_year.config(validatecommand=(range_validation, '%P', self.sb_year, 0))
#         self.sb_month.config(validatecommand=(range_validation, '%P', self.sb_month, 1))
#         self.sb_day.config(validatecommand=(range_validation, '%P', self.sb_day, 2))
# =============================================================================
        
        self.sb_dic = {"year" : self.sb_year,
              "month" : self.sb_month,
              "day" : self.sb_day}
        f.set_Date_Spinbox_Command(controller=self, sb_dic=self.sb_dic)
        
        for idx, sb in enumerate(self.sb_dic.values()):
            sb.config(validatecommand=(range_validation, '%P', sb, idx))
        
        self.btn_input.config(command=self.cmd_Input_Button)
        self.btn_cancel.config(command=lambda : f.on_Closing(self.parent, self.window))
        return
    
    def set_Info(self, parent):
        self.frame_Info = UI_setting.set_frame(parent, padx=5, pady=5)
        
        self.frame_name = UI_setting.set_frame(self.frame_Info)
        self.lbl_name = Label(self.frame_name, text=self.data["name"], font=self.font)
        self.lbl_name.pack()
        
        
        
        self.frame_time = UI_setting.set_frame(self.frame_Info, relief="solid", bd=1)
        self.frame_attend_time = UI_setting.set_frame(self.frame_time)
        Label(self.frame_attend_time, text="출근", font=self.font).pack(side="left")
        UI_setting.space_area(parent=self.frame_attend_time, side="left", length=3)
        self.lbl_attend_hour = Label(self.frame_attend_time, text=self.data["attend_hour"], font=self.font, padx=5)
        self.lbl_attend_min = Label(self.frame_attend_time, text=self.data["attend_min"], font=self.font, padx=5)
        
        Label(self.frame_attend_time, text="분", font=self.font).pack(side="right")
        self.lbl_attend_min.pack(side="right")
        UI_setting.space_area(self.frame_attend_time, side="right", length=3)
        Label(self.frame_attend_time, text="시", font=self.font).pack(side="right")
        self.lbl_attend_hour.pack(side="right")
        
        
        self.frame_leave_time = UI_setting.set_frame(self.frame_time)
        Label(self.frame_leave_time, text="퇴근", font=self.font).pack(side="left")
        UI_setting.space_area(parent=self.frame_leave_time, side="left", length=3)
        self.lbl_leave_hour = Label(self.frame_leave_time, text=self.data["leave_hour"], font=self.font, padx=5)
        self.lbl_leave_min = Label(self.frame_leave_time, text=self.data["leave_min"], font=self.font, padx=5)
        
        Label(self.frame_leave_time, text="분", font=self.font).pack(side="right")
        self.lbl_leave_min.pack(side="right")
        UI_setting.space_area(parent=self.frame_leave_time, side="right", length=3)
        Label(self.frame_leave_time, text="시", font=self.font).pack(side="right")
        self.lbl_leave_hour.pack(side="right")
        
        self.frame_rest_time = UI_setting.set_frame(self.frame_time)
        Label(self.frame_rest_time, text="휴게", font=self.font).pack(side="left")
        self.lbl_rest = Label(self.frame_rest_time, text=self.data["rest"], font=self.font, padx=5)
        
        Label(self.frame_rest_time, text="분", font=self.font).pack(side="right")
        self.lbl_rest.pack(side="right")
        
        
        self.frame_work_time = UI_setting.set_frame(self.frame_time)
        Label(self.frame_work_time, text="근무시간", font=self.font).pack(side="left")
        self.work_hour = Label(self.frame_work_time, text=self.data["work_hour"], font=self.font, padx=5)
        self.work_min = Label(self.frame_work_time, text=self.data["work_min"], font=self.font, padx=5)
        
        Label(self.frame_work_time, text="분", font=self.font).pack(side="right")
        self.work_min.pack(side="right")
        UI_setting.space_area(parent=self.frame_work_time, side="right", length=1)
        Label(self.frame_work_time, text="시간", font=self.font).pack(side="right")
        self.work_hour.pack(side="right")
        
    def set_Button(self, parent):
        self.frame_btns = UI_setting.set_frame(parent, padx=5, pady=5)
        self.btn_input = Button(self.frame_btns, text="입력", font=UI_setting.get_font(f_size=10), padx=5, pady=5)
        self.btn_cancel = Button(self.frame_btns, text="뒤로", font=UI_setting.get_font(f_size=10), padx=5, pady=5)
        
        self.btn_input.pack(side="right")
        self.btn_cancel.pack(side="left")
        return
    
    def cmd_Input_Button(self):
        
        if not self.check_Date():
            return
        
        staff_name = self.data["name"]
        attend_time = self.data["attend_hour"] + self.data["attend_min"]
        leave_time = self.data["leave_hour"] + self.data["leave_min"]
        rest_time = int(self.data["rest"])
        
        db = mongoDB.MongoDB.instance()
        staff_info = db.collection_staff.find_one({"name" : staff_name})
        
        # 기록 중복 확인
        flag_duplicated = f.check_Duplicated_Work_Time(staff_name=staff_name, start_time=attend_time,
                                                       end_time=leave_time, date=self.selected_date,
                                                       original_data=self.original_data)
        print("flag_duplicated :", flag_duplicated)
        if flag_duplicated:
            msgbox.showwarning("", "중복되는 기록이 있습니다.")
            return
        
        # 본인 근무시간인지 확인
        flag_change_work_time = f.check_Changed_Work_Time(staff_name, self.selected_date, attend_time, leave_time, rest_time)
        
        temp_dic = {}
        
        temp_dic["date"] = {}
        temp_dic["date"]["year"] = self.selected_date.year
        temp_dic["date"]["month"] = self.selected_date.month
        temp_dic["date"]["day"] = self.selected_date.day
        temp_dic["date"]["yweek"] = datetime.datetime.isocalendar(self.selected_date)
        
        temp_dic["staff"] = {}
        temp_dic["staff"]["empno"] = staff_info["empno"]
        temp_dic["staff"]["name"] = staff_name
        
        temp_dic["time"] = {}
        temp_dic["time"]["start"] = attend_time
        temp_dic["time"]["end"] = leave_time
        temp_dic["time"]["rest"] = rest_time
        temp_dic["time"]["work_time"] = [self.data["work_hour"], self.data["work_min"], self.data["work_hour"]*60 + self.data["work_min"]]
        
        if flag_change_work_time:
            # 시간변경, 대타
            self.destroy_flag = False
            self.content = [0]

            check_input_sub.Check_Input_Sub(self.window, self, temp_dic)
            
        else:
            # 본래 근무시간인 경우
            temp_dic["my_work_time"] = 1
            self.check_and_save_Data(temp_dic)
        return
    
    def check_and_save_Data(self, temp_dic):
        if "my_work_time" not in temp_dic.keys():
            if self.content[0] == 1:
                temp_dic["substitution"] = self.content[1]
            elif self.content[0] == 2:
                temp_dic["change_time"] = self.content[1]
        else:
            self.destroy_flag = True
            print("\nmy_Work_Time\n")
        
        print()
        print("temp_dic")
        for key, value in temp_dic.items():
            print(key)
            print(value)
        
        if self.destroy_flag:
            db = mongoDB.MongoDB.instance()
            
            try:
                if self.original_data:
                    # 기록 수정하는 경우
                    print(db.collection_Work_Record.update(self.original_data, temp_dic))
                    self.top.top.sb_Changed()
                    self.update_Ledger(temp_dic, original_data=self.original_data, db=db)
                else:
                    # 신규 기록인 경우
                    print(db.collection_Work_Record.insert_one(temp_dic))
                    self.update_Ledger(temp_dic, db=db)
                
            except:
                msgbox.showwarning("", "에러 발생\n다시 시도하세요")
                return
            
            self.parent.grab_set()
            self.top.cmb_start_hour.set("")
            self.top.cmb_start_minute.set("")
            self.top.cmb_end_hour.set("")
            self.top.cmb_end_minute.set("")
            self.top.cmb_rest.set("")
            
            if self.parent.title() == "modify_Record":
                self.top.parent.grab_set()
                self.parent.destroy()
            
            msgbox.showinfo("", "입력되었습니다")
            
            self.window.destroy()
        return
    
    def update_Ledger(self, data, original_data=None, db=mongoDB.MongoDB.instance()):
        year = str(data["date"]["year"])
        month = str(data["date"]["month"])
        if data["date"]["month"] < 10:
            month = "0" + month
            
        basic = compute.compute_pay(staff_name=data["staff"]["name"], 
                                  start_time=data["time"]["start"], end_time=data["time"]["end"], rest_time=data["time"]["rest"])
        print("basic :", basic)
        print("flag1")
        record_data = db.collection_ledger.find_one({"staff.name" : data["staff"]["name"], "staff.empno" : data["staff"]["empno"]})
        staff = db.collection_staff.find_one({"name" : data["staff"]["name"], "empno" : data["staff"]["empno"]})
        print("staff :")
        print(staff)
        print()
        try:
            print("flag2 try")
            record_data["contents"][year][month]
        except:
            print("flag2 except1")
            contents = {"payment_details" : {
                                    "basic_pay" : 0,
                                    "weekly_holiday_allowance" : [0],
                                    "additional_work" : 0,
                                    "night_work" : 0},
                              "deduction_details" : {
                                    "국민연금" : 0,
                                    "건강보험" : 0,
                                    "고용보험" : 0,
                                    "소득세" : 0},
                            "total" : 0
                              }
            print("flag2 except2")
            if year not in record_data["contents"].keys():
                record_data["contents"][year] = {}
            print("flag2 except3")
            record_data["contents"][year][month] = contents
            print("flag2 except4")
            print(record_data)
#            print(db.collection_ledger.update({"staff.name" : staff["name"],
#                                         "staff.empno" : staff["empno"]},
#                                        record_data))
            print(db.collection_ledger.update({"_id" : record_data["_id"]}, record_data))
            
            # 수정하는 경우
        if original_data:
            print("수정하는 경우")
            print("original data")
            print(original_data)
            
            print("modify1")
            ori_basic = compute.compute_pay(staff_name=original_data["staff"]["name"],
                                            start_time=original_data["time"]["start"],
                                            end_time=original_data["time"]["end"],
                                            rest_time=original_data["time"]["rest"])
            print("modify2")
            ori_year = str(original_data["date"]["year"])
            print(ori_year)
            ori_month = str(original_data["date"]["month"])
            print(ori_month)
            
            print("modify3")
            ori_staff = db.collection_staff.find_one({"name" : original_data["staff"]["name"], "empno" : original_data["staff"]["empno"]})
            
            if original_data["date"]["month"] < 10:
                ori_month = "0" + ori_month
            # 수정될 데이터의 기본급 차감
            db.collection_ledger.update({"staff.empno" : staff["empno"],
                                         "staff.name" : staff["name"]},
                                    {"$inc" : {"contents.{0}.{1}.payment_details.basic_pay".format(ori_year, ori_month) : -(ori_basic)}})
            print("modify4")
            # 수정될 데이터의 주휴수당
#            wha = f.check_Weekly_Holiday_Allowance()
            
            ori_record_data = db.collection_ledger.find_one({"staff.name" : ori_staff["name"], "staff.empno" : ori_staff["empno"]})
            payment_details = ori_record_data["contents"][ori_year][ori_month]["payment_details"]
            print("modify5")
            # 수정될 데이터의 추가근로수당
            
            # 수정될 데이터의 야간근무 수당
            
            payment = payment_details["basic_pay"] + payment_details["additional_work"] + payment_details["night_work"] + payment_details["weekly_holiday_allowance"][0]
            print("modify6")
            print("payment :", payment, "\n")
            # 수정될 데이터의 세금 계산
            for insurance, tax in ori_staff["insurances"].items():
                print("insurance :")
                print(insurance)
                print()
                db.collection_ledger.update({"staff.empno" : staff["empno"],
                                             "staff.name" : staff["name"]},
                {"$set" : {"contents.{0}.{1}.deduction_details.{2}".format(ori_year, ori_month, insurance) : 
                    compute.compute_Tax(payment, tax)}})
            
            print("modify7")
            ori_record_data = db.collection_ledger.find_one({"staff.name" : ori_staff["name"], "staff.empno" : ori_staff["empno"]})
            deduction_details = ori_record_data["contents"][ori_year][ori_month]["deduction_details"]
            deduction = 0
            print("modify8")
            for tax in deduction_details.values():
                print(tax)
                deduction += tax
            # 수정될 데이터 total
            print("modify9")
            total = payment - deduction
            print("deduction :", deduction)
            print("total :", total)
            db.collection_ledger.update({"_id" : ori_record_data["_id"]}, {"$set" : {"contents.{0}.{1}.total".format(ori_year, ori_month) : total}})
            print("modify10")
        else:
            pass
        # additional_work
        # night_work
        # weekly_holiday_allowance
        
        # 국민연금 4.5  월 60시간 이상만
        # 건강보험 3.06   월 60시간 이상만
        # 고용보험 0.65   3개월 이상 근무하는 사람은 모두
        
        # 소득세
        try:
            print("flag3")
            contents = record_data["contents"][year][month]
            
            print("flag4")
            # 기본급 증가(시간당 수당)
            db.collection_ledger.update({"staff.empno" : staff["empno"],
                                             "staff.name" : staff["name"]},
                                        {"$inc" : {"contents.{0}.{1}.payment_details.basic_pay".format(year, month) : basic}})
            
            print("flag5")
            # 주휴수당 확인
            if staff["weekly_holiday_allowance"] == 1:
                db.collection_ledger.update({"staff.empno" : staff["empno"],
                                             "staff.name" : staff["name"]}, 
                                            {"$inc" : {"contents.{0}.{1}.payment_details".format(year, month) : f.check_Weekly_Holiday_Allowance(data)}})
    #            contents["weekly_holiday_allowance"] += f.check_Weekly_Holiday_Allowance(data)
    # =============================================================================
    #         # 추가수당 확인"$inc" : {"contents.{0}.{1}.payment_details".format(yea
    # =============================================================================
    # =============================================================================
    #         # 야간수당 확인
    # =============================================================================
            record_data = db.collection_ledger.find_one({"_id" : record_data["_id"]})
            payment_detail = record_data["contents"][year][month]["payment_details"]
            payment = payment_detail["basic_pay"] + payment_detail["additional_work"] + payment_detail["night_work"] + payment_detail["weekly_holiday_allowance"][0]
            # 세금 적용
            for insurance, tax in staff["insurances"].items():
                print("insurance :")
                print(insurance)
                print()
                db.collection_ledger.update({"staff.empno" : staff["empno"],
                                             "staff.name" : staff["name"]},
                    {"$set" : {"contents.{0}.{1}.deduction_details.{2}".format(year, month, insurance) : 
                                        compute.compute_Tax(payment, tax)}})
                    
            # total
            record_data = db.collection_ledger.find_one({"_id" : record_data["_id"]})
            deduction = record_data["contents"][year][month]["deduction_details"]
            total = int(payment) - int(deduction["국민연금"] + deduction["건강보험"] + deduction["고용보험"] + deduction["소득세"])
            db.collection_ledger.update({"_id" : record_data["_id"]}, {"$set" : {"contents.{0}.{1}.total".format(year, month) : total}})
        except Exception as e:
            print("Exception Occured")
            print(e)
        
    
# =============================================================================
#     def sb_year_Changed(self):
#         year = int(self.sb_year.get())
#         month = int(self.sb_month.get())
#         
#         temp_date = datetime.datetime(year, month, 1)
#         last_day = f.get_last_day(date=temp_date)
#         self.sb_day.config(to=last_day)
#         
#         try:
#             self.selected_date = self.selected_date.replace(year=year)
#         except:
#             self.selected_date = self.selected_date.replace(year=year, day=last_day)
#         
#         if int(self.sb_day.get()) > last_day:
#             self.sb_day.set(last_day)
# 
#         print("selectetd_date :", self.selected_date)
#         return
#     
#     def sb_month_Changed(self):
#         year = int(self.sb_year.get())
#         month = int(self.sb_month.get())
#         
#         temp_date = datetime.datetime(year, month, 1)
#         last_day = f.get_last_day(date=temp_date)
#         self.sb_day.config(to=last_day)
#         
#         try:
#             self.selected_date = self.selected_date.replace(month=month)
#         except:
#             self.selected_date = self.selected_date.replace(month=month, day=last_day)
#         
#         
#         if int(self.sb_day.get()) > last_day:
#             self.sb_day.set(last_day)
# 
#         print("selectetd_date :", self.selected_date)
#         return
#     
#     def sb_day_Changed(self):
#         self.selected_date = self.selected_date.replace(day=int(self.sb_day.get()))
#         
#         print("selectetd_date :", self.selected_date)
#         return
# =============================================================================
    
    def sb_valid(self, user_input, sb_widget, idx):
        idx = int(idx)
        print("user_input :", user_input)
        print(type(user_input))
        if user_input.isdigit():
            
            minval = int(self.window.nametowidget(sb_widget).config('from')[4])
            maxval = int(self.window.nametowidget(sb_widget).config('to')[4]) + 1
            
            int_user_input = int(user_input)
            if int_user_input not in range(minval, maxval): 
                print ("Out of range") 
                return False
            
            if idx == 0:
                self.selected_date = self.selected_date.replace(year=int_user_input)
            elif idx == 1:
                self.selected_date = self.selected_date.replace(month=int_user_input)
            elif idx == 2:
                self.selected_date = self.selected_date.replace(day=int_user_input)
            print(user_input)
            print("selected_date :", self.selected_date)
            return True
        elif user_input == "":
            print(user_input)
            return True
        else:
            print("Not Numeric")
            return False
        
    def check_Date(self):
        today = datetime.datetime.today().date()
        if today < self.selected_date:
            msgbox.showwarning("", "입력되는 날짜가 미래가 될 수 없습니다.")
            return False
        else:
            return True