from tkinter import *
import tkinter.messagebox as msgbox

from UI import UI_setting
from Functions import compute
from Functions import functions as f

from settings_frame.manage_staff.add import functions

class Add_Staff:
    def __init__(self, parent):
        self.parent = parent
        self.window = UI_setting.new_Window(parent, title="add_Staff")
        self.window.grab_set()
        self.font = UI_setting.get_font(f_size=10)
        self.font_selected = UI_setting.get_font(f_size=10, weight="bold")
        self.day_list = ["월", "화", "수", "목", "금", "토", "일"]
        self.text_dic = {}
        
        self.set_Window()
        self.set_Commands()
        
        self.window.grab_set()
        self.window.protocol("WM_DELETE_WINDOW", lambda : f.on_Closing(parent, self.window))
        return
    
    def set_Window(self):
        self.set_Left_Frame() # 기본 정보
        self.set_Bottom_Frame() # 버튼
        self.set_Right_Frame() # 근무시간
        
        return
    
    def set_Left_Frame(self):
        self.frame_left = UI_setting.set_frame(self.window, side="left")
        
        self.set_Name_Frame(self.frame_left)
        self.set_ID_Frame(self.frame_left)
        self.set_Phone_Frame(self.frame_left)
        self.set_Account_Frame(self.frame_left)
        self.set_Wage_Frame(self.frame_left)
        self.set_Insurance_Frame(self.frame_left)
        return
    
    def set_Name_Frame(self, parent):
        self.frame_name = UI_setting.set_frame(parent, padx=5, pady=5)
        
        Label(self.frame_name, text="이름", font=self.font).pack(side="left")
        UI_setting.space_area(self.frame_name, length=3, side="left")
        Label(self.frame_name, text=" - ", font=self.font).pack(side="left")
        self.txt_name = Entry(self.frame_name, font=self.font, width = 15)
        self.txt_name.pack(side="right")
        
        self.text_dic["name"] = self.txt_name
        return
    
    def set_ID_Frame(self, parent):
        self.frame_id = UI_setting.set_frame(parent, padx=5)
        
        Label(self.frame_id, text="ID", font=self.font).pack(side="left")
        UI_setting.space_area(self.frame_id, length=5, side="left")
        Label(self.frame_id, text=" - ", font=self.font).pack(side="left")
        self.txt_id = Entry(self.frame_id, width = 15, font=self.font)
        self.txt_id.pack(side="right")
        
        self.text_dic["empno"] = self.txt_id
        return
    
    def set_Phone_Frame(self, parent):
        self.frame_phone = UI_setting.set_frame(parent, padx=5, pady=5)
        
        Label(self.frame_phone, text="연락처", font=self.font).pack(side="left")
        Label(self.frame_phone, text=" - ", font=self.font).pack(side="left")
        self.txt_phone = Entry(self.frame_phone, width = 15, font=self.font)
        self.txt_phone.pack(side="right")
        
        self.text_dic["phone"] = self.txt_phone
        return
    
    def set_Account_Frame(self, parent):
        self.frame_bank_account = UI_setting.set_LabelFrame(parent, text="급여계좌", font=self.font, padx=5, pady=5)
        
        self.frame_bank = UI_setting.set_frame(self.frame_bank_account)
        Label(self.frame_bank, text="은행", font=self.font).pack(side="left")
        self.txt_bank = Entry(self.frame_bank, width = 20, font=self.font)
        self.txt_bank.pack(side="right")
        
        self.frame_account = UI_setting.set_frame(self.frame_bank_account)
        Label(self.frame_account, text="계좌", font=self.font).pack(side="left")
        self.txt_account = Entry(self.frame_account, width = 20, font=self.font)
        self.txt_account.pack(side="right")
        
        self.text_dic["bank"] = self.txt_bank
        self.text_dic["account"] = self.txt_account
        return
    
    def set_Wage_Frame(self, parent):
        self.frame_wage = UI_setting.set_frame(parent, padx=5, pady=5)
        
        Label(self.frame_wage, text="시급", font=self.font).pack(side="left")
        Label(self.frame_wage, text=" 원", font=self.font).pack(side="right")
        self.txt_wage = Entry(self.frame_wage, width = 7, font=self.font)
        self.txt_wage.pack(side="right")
        
        self.text_dic["wage"] = self.txt_wage
        return
    
    def set_Insurance_Frame(self, parent):
        self.frame_insurance = UI_setting.set_LabelFrame(parent, text="보험", font=self.font, padx=5, pady=5)
        
        insurances = ["국민연금", "건강보험", "고용보험"]
        # 국민연금 4.5  월 60시간 이상만
        # 건강보험 3.06   월 60시간 이상만
        # 고용보험 0.65   3개월 이상 근무하는 사람은 모두
        tax = [4.5, 3.06, 0.65]
        self.chk_insurance_vars = [IntVar() for x in range(len(insurances))]
        self.chk_insurance_btns = []
        self.chk_insurances = {}
        
        for idx, insurance in enumerate(insurances):
            temp_chk = Checkbutton(self.frame_insurance, text=insurance, variable=self.chk_insurance_vars[idx], font=self.font)
            temp_chk.pack()
            self.chk_insurance_btns.append(temp_chk)
            self.chk_insurances[insurances[idx]] = [self.chk_insurance_btns[idx], self.chk_insurance_vars[idx], tax[idx]]
        
        
        return
    
    
    def set_Right_Frame(self):
        self.frame_right = UI_setting.set_LabelFrame(self.window, text="근무시간", side="right")
        self.frame_day = [] # 요일 버튼 선택시 해당하는 요일에 대한 입력 정보 프레임 저장할 배열
        #self.frame_day = {}
        
        self.set_Check_to_Same_Frame(self.frame_right)
        self.set_Check_Day_Frame(self.frame_right)
        self.set_Button_Day_Frame(self.frame_right)

        self.frame_days = UI_setting.set_frame(self.frame_right, padx=5, pady=5, relief="solid", bd=1)
        
        self.cmb_attend_hour = []
        self.cmb_attend_min = []
        self.cmb_leave_hour = []
        self.cmb_leave_min = []
        self.cmb_rest = []
        self.lbl_work_hour = []
        self.lbl_work_min = []
        self.lbl_work_time = []
        
        for idx in range(7):
            temp_frame = Frame(self.frame_days, padx=5, pady=5)
            temp_frame.grid(row=0, column=0, sticky="news")
            self.set_Day_Frame(temp_frame, idx)
            #self.frame_day[self.day_list[idx]] = temp_frame
            self.frame_day.append(temp_frame)
        
        
        self.frame_day[0].tkraise()
        
        return
    
    def set_Check_to_Same_Frame(self, parent):
        self.frame_make_to_same = UI_setting.set_frame(parent, padx=5, pady=5)
        
        self.chk_same_var = IntVar()
        # 체크했다면 1, 아니면 0
# =============================================================================
#         self.chkbox_same = Checkbutton(self.frame_make_to_same, text="모든 요일 동일하게", variable=self.chk_same_var,
#                                        command=self.cmd_Check_to_Same, font=self.font)
# =============================================================================
# =============================================================================
#         self.chkbox_same = Checkbutton(self.frame_make_to_same, text="모든 요일 동일하게", variable=self.chk_same_var,
#                                        font=self.font)
#         
#         self.chkbox_same.pack(side="right")
# =============================================================================
        
        self.btn_same = Button(self.frame_make_to_same, text="모든 요일 동일하게",
                                       font=self.font)
        self.btn_same.pack(side="right")
        return
    
    def cmd_Click_to_Same(self):
        # 제일 앞 요일의 시간으로 통일
        
        attend_hour = 0
        attend_min = 0
        leave_hour = 0
        leave_min = 0
        rest = 0
        
        for idx, (key, value) in enumerate(self.chk_days_var.items()):
            # 제일 앞 요일의 내용 저장
            state = value.get()
            if state == 1:
                attend_hour = self.cmb_attend_hour[idx].get()
                attend_min = self.cmb_attend_min[idx].get()
                leave_hour = self.cmb_leave_hour[idx].get()
                leave_min = self.cmb_leave_min[idx].get()
                rest = self.cmb_rest[idx].get()
                break
            
        for idx, (key, value) in enumerate(self.chk_days_var.items()):
            # 저장한 제일 앞 요일의 내용으로 입력
            state = value.get()
            if state == 1:
                self.cmb_attend_hour[idx].set(attend_hour)
                self.cmb_attend_min[idx].set(attend_min)
                self.cmb_leave_hour[idx].set(leave_hour)
                self.cmb_leave_min[idx].set(leave_min)
                self.cmb_rest[idx].set(rest)
                self.cmd_Time_Select(event=None, idx=idx)
        return
    
    def set_Check_Day_Frame(self, parent):
        self.frame_chkbox_days = UI_setting.set_frame(parent, padx=5, pady=5)
        
        self.chk_days = []
        
        self.chk_days_var = {}
        for idx in range(7):
            self.chk_days_var[self.day_list[idx]] = IntVar()
# =============================================================================
#             temp_chk = Checkbutton(self.frame_chkbox_days, text=self.day_list[idx], variable=self.chk_days_var[self.day_list[idx]],
#                                    command=self.cmd_Check_Days, font=self.font)
# =============================================================================
            temp_chk = Checkbutton(self.frame_chkbox_days, text=self.day_list[idx], variable=self.chk_days_var[self.day_list[idx]],
                                   font=self.font)
            self.chk_days.append(temp_chk)
        
        for chk_day in reversed(self.chk_days):
            chk_day.pack(side="right")
    
    def cmd_Check_Days(self):
        for idx, (key, value) in enumerate(self.chk_days_var.items()):
            state = value.get()
            if state == 1:
                print(key)
                self.btn_days[idx].config(state="normal", font=self.font_selected)
            else:
                self.btn_days[idx].config(state="disabled", font=self.font)
        return
    
    def set_Button_Day_Frame(self, parent):
        self.frame_btn_days = UI_setting.set_frame(parent, pady=5, side="left")
        
        self.btn_days = []
        for idx in range(7):
# =============================================================================
#             temp_btn = Button(self.frame_btn_days, text=self.day_list[idx], font=self.font, 
#                               command=lambda : self.cmd_Change_Days(idx))
#             temp_btn.pack()
#             self.btn_days.append(temp_btn)
# =============================================================================
            self.btn_days.append(Button(self.frame_btn_days, text=self.day_list[idx],
                                        font=self.font, state="disabled"))
            self.btn_days[idx].pack()
        
# =============================================================================
#         for idx, btn in enumerate(self.btn_days):
#             btn.config(command=lambda x=idx : self.cmd_Change_Days(x))
# =============================================================================
            
# =============================================================================
#         self.btn_days[0].config(command=lambda : self.cmd_Change_Days(0))
#         self.btn_days[1].config(command=lambda : self.cmd_Change_Days(1))
#         self.btn_days[2].config(command=lambda : self.cmd_Change_Days(2))
#         self.btn_days[3].config(command=lambda : self.cmd_Change_Days(3))
#         self.btn_days[4].config(command=lambda : self.cmd_Change_Days(4))
#         self.btn_days[5].config(command=lambda : self.cmd_Change_Days(5))
#         self.btn_days[6].config(command=lambda : self.cmd_Change_Days(6))
# =============================================================================
        print(self.btn_days)
        return
    
    def cmd_Change_Days(self, day):
        print("day :", day)
        self.frame_day[day].tkraise()
        return
    
    def set_Day_Frame(self, parent, idx):
        day = self.day_list[idx]
        font = UI_setting.get_font(f_size=15, weight="bold")
        
        self.cmb_attend_hour.append(UI_setting.get_Hour_Combobox(parent, f_size=10))
        self.cmb_attend_min.append(UI_setting.get_Minute_Combobox(parent, f_size=10))
        self.cmb_leave_hour.append(UI_setting.get_Hour_Combobox(parent, f_size=10))
        self.cmb_leave_min.append(UI_setting.get_Minute_Combobox(parent, f_size=10))
        self.cmb_rest.append(UI_setting.get_Rest_Combobox(parent, f_size=10))
        
        col = 0
        Label(parent, text=day, font=font, width=5, height=3).grid(row=0, rowspan = 5, column=col, sticky="news")
        
        col += 1
        Label(parent, text="출근", font=self.font).grid(row=0, column=col, padx=3, pady=3)
        Label(parent, text="퇴근", font=self.font).grid(row=1, column=col, padx=3, pady=3)
        Label(parent, text="휴게", font=self.font).grid(row=2, column=col, padx=3, pady=3)
        #Label(parent, text="근무시간", font=self.font).grid(row=3, rowspan=2, column=col, padx=3, pady=3)
# =============================================================================
#         Label(parent, text="시간, 분", font=self.font).grid(row=3, column=2)
#         Label(parent, text="분", font=self.font).grid(row=4, column=2)
# =============================================================================
        
        col = col + 1
        self.cmb_attend_hour[idx].grid(row=0, column=col, padx=3, pady=3)
        self.cmb_leave_hour[idx].grid(row=1, column=col)
        #self.lbl_work_hour.append(Label(parent, text="-"))
        #self.lbl_work_hour[idx].grid(row=3, column=col)
        
        col = col + 1
        for i in range(2):
            Label(parent, text="시", font=self.font).grid(row=i, column=col)
        #Label(parent, text="시", font=self.font).grid(row=3, column=col)
        
        col = col + 1
        self.cmb_attend_min[idx].grid(row=0, column=col, padx=3, pady=3)
        self.cmb_leave_min[idx].grid(row=1, column=col, padx=3, pady=3)
        self.cmb_rest[idx].grid(row=2, column=col, padx=3, pady=3)
        #self.lbl_work_min.append(Label(parent, text="-"))
        #self.lbl_work_min[idx].grid(row=3, column=col, padx=3, pady=3)
        #self.lbl_work_time.append(Label(parent, text="-"))
        #self.lbl_work_time[idx].grid(row=4, column=col, padx=3, pady=3)
        
        col = col + 1
        #for i in range(5):
        for i in range(3):
            Label(parent, text="분", font=self.font).grid(row=i, column=col)
        
        frame_work_time = Frame(parent, relief="solid", bd=1)
        frame_work_time.grid(row=3, column=1, columnspan=5, sticky="news", pady=5)
        Label(frame_work_time, text="근무시간", font=self.font).grid(row=0, rowspan=2, column=0, padx=3, pady=3)
        self.lbl_work_hour.append(Label(frame_work_time, text="-", width=5))
        self.lbl_work_hour[idx].grid(row=0, column=1)
        Label(frame_work_time, text="시", font=self.font).grid(row=0, column=2)
        
        self.lbl_work_min.append(Label(frame_work_time, text="-", width=8))
        self.lbl_work_min[idx].grid(row=0, column=3, padx=3, pady=3)
        self.lbl_work_time.append(Label(frame_work_time, text="-", width=8))
        self.lbl_work_time[idx].grid(row=1, column=3, padx=3, pady=3)
        
        Label(frame_work_time, text="분", font=self.font).grid(row=0, column=4)
        Label(frame_work_time, text="분", font=self.font).grid(row=1, column=4)
        
        return
    def cmd_Time_Select(self, event, idx):
        try:
            start = self.cmb_attend_hour[idx].get() + self.cmb_attend_min[idx].get()
            print("start :", start)
            end = self.cmb_leave_hour[idx].get() + self.cmb_leave_min[idx].get()
            print("end :", end)
            rest = self.cmb_rest[idx].get()
            print("rest :", rest)
            
            work_h, work_m = compute.compute_time(start, end, rest)
            print("compute_work_time :", work_h, work_m)
            work_t = work_m + (work_h * 60)
            
            self.lbl_work_hour[idx].config(text=work_h)
            self.lbl_work_min[idx].config(text=work_m)
            self.lbl_work_time[idx].config(text=work_t)
        except:
            print("ERROR")
        return
    
    def set_Bottom_Frame(self):
        self.frame_bottom = UI_setting.set_frame(self.window, side="bottom", padx=5, pady=5)
        
        self.set_Input_Button(self.frame_bottom)
        
        return
    
    def set_Input_Button(self, parent):
        #self.btn_input = Button(parent, text="저장", font=self.font, command=self.cmd_Input_Button)
        self.btn_input = Button(parent, text="저장", font=self.font)
        self.btn_input.pack(side="right")
        return
    
    def cmd_Input_Button(self):
# =============================================================================
#         for item, content in self.text_dic.items():
#             if content.get() == "":
#                 msgbox.showerror("error", "입력되지 않은 항목이 있습니다.\n" + item)
#                 break
# =============================================================================
        days = 0
        for day in self.chk_days_var.values():
            days += day.get()
        if days == 0:
            msgbox.showinfo("입력하지 않은 내용", "입력된 근무시간이 없습니다")
            return
        
        for idx, day in enumerate(self.chk_days_var.values()):
            if day.get() == 1:
                if self.cmb_attend_hour[idx].get() == "" or self.cmb_attend_min[idx].get() == "" or self.cmb_leave_hour[idx].get() == "" or self.cmb_leave_min[idx].get() == "" or self.cmb_rest[idx].get() == "":
                    self.show_Error_MSG(idx)
                    return
                
        
        if not functions.check_Data_Integrity(self.text_dic):
            return
        
        # 기본정보 중복검사
        flag, duplicated_data = functions.check_Duplication(self.text_dic)
        
        if flag:
            msgbox.showinfo("중복 확인", "중복된 내용이 있습니다.\n" + duplicated_data[0] + "\n" + duplicated_data[1])
        else:
            response = msgbox.askokcancel("new Staff", "저장하시겠습니까?")
            if response == 1:
                print("저장")
                end_flag = functions.add_Staff(self.text_dic,
                                               self.chk_insurances,
                                               self.chk_days_var, self.cmb_attend_hour, self.cmb_attend_min, self.cmb_leave_hour, self.cmb_leave_min, self.cmb_rest)
                if end_flag:
                    self.parent.grab_set()
                    self.window.destroy()
            else:
                print("취소")
        
        print("cmd_Input_Button_Clicked")
    
    def show_Error_MSG(self, idx):
        msgbox.showerror("error", "입력되지 않은 항목이 있습니다.\n" + "근무시간\n" + self.btn_days[idx]["text"] + "요일")
        return
        
    def set_Commands(self):
        self.btn_same.config(command=self.cmd_Click_to_Same)
        for chk_day in self.chk_days:
            chk_day.config(command=self.cmd_Check_Days)
        
        for idx, btn in enumerate(self.btn_days):
            btn.config(command=lambda x=idx : self.cmd_Change_Days(x))
        
        for times_cmb in [self.cmb_attend_hour, self.cmb_attend_min, self.cmb_leave_hour, self.cmb_leave_min, self.cmb_rest]:
            for idx, cmb in enumerate(times_cmb):
                cmb.bind("<<ComboboxSelected>>", lambda event, x = idx : self.cmd_Time_Select(event, x))
                
                
        self.btn_input.config(command=self.cmd_Input_Button)
        return
    