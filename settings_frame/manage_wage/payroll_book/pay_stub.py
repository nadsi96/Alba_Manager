from tkinter import *
import tkinter.ttk as ttk

from UI import UI_setting


class Pay_Stub:
    def __init__(self, parent, data, year, month):
        self.data = data
        self.year = year
        self.month = month
        self.window = UI_setting.new_Window(parent, "Pay_Stub")
        
        self.font = UI_setting.get_font(f_size=10)
        self.set_Window()
    
    def set_Window(self):
        frame_payment_statement = UI_setting.set_frame(self.window, padx=10, pady=10)
        lbl_title = Label(frame_payment_statement, text="{}.{} 급여명세서".format(self.year, self.month),
                          font=UI_setting.get_font(f_size=12, weight="bold"))
        lbl_title.pack()
        
        total_payment = self.set_Frame_Payment_Detail(frame_payment_statement)
        total_deduction = self.set_Frame_Deduction_Detial(frame_payment_statement)
        
        Label(frame_payment_statement, text="급여총액", font=self.font, padx=5, pady=5).pack(side="left")
        Label(frame_payment_statement, text=self.set_Comma((total_payment - total_deduction)),
              padx=5, pady=5).pack(side="right")
        
        return
    
    def set_Frame_Payment_Detail(self, parent):
        lblframe_payment_detail = UI_setting.set_LabelFrame(parent, text="지급내역", font=self.font, padx=5, pady=5)
        
        key_data = {"basic_pay" : "기본급",
                    "weekly_holiday_allowance" : "주휴수당",
                    "additional_work" : "추가근로수당",
                    "night_work" : "야간근로수당"}
        frame = []
        total_payment = 0
        for idx, (key, value) in enumerate(self.data["payment_details"].items()):
            frame.append(UI_setting.set_frame(lblframe_payment_detail, padx=5))
            Label(frame[idx], text=key_data[key], font=self.font).pack(side="left")
            try:
                Label(frame[idx], text=self.set_Comma(value), font=self.font).pack(side="right")
                total_payment += value
            except:
                Label(frame[idx], text=self.set_Comma(value[0]), font=self.font).pack(side="right")
                total_payment += value[0]
        
        ttk.Separator(lblframe_payment_detail, orient="horizon").pack(fill="x")
        
        total_payment = int(total_payment)
        frame.append(UI_setting.set_frame(lblframe_payment_detail, padx=5, pady=3))
        Label(frame[-1], text="지급총액", font=self.font).pack(side="left")
        Label(frame[-1], text=self.set_Comma(total_payment)).pack(side="right")
        return total_payment
    
    def set_Frame_Deduction_Detial(self, parent):
        lblframe_deduction_detail = UI_setting.set_LabelFrame(parent, text="공제내역", font=self.font, padx=5, pady=5)
        
        frame = []
        total_deduction = 0
        for idx, (key, value) in enumerate(self.data["deduction_details"].items()):
            frame.append(UI_setting.set_frame(lblframe_deduction_detail, padx=5))
            Label(frame[idx], text=key, font=self.font).pack(side="left")
            Label(frame[idx], text=self.set_Comma(value), font=self.font).pack(side="right")
            total_deduction += value
        
        ttk.Separator(lblframe_deduction_detail, orient="horizon").pack(fill="x")
        
        total_deduction = int(total_deduction)
        frame.append(UI_setting.set_frame(lblframe_deduction_detail, padx=5, pady=3))
        Label(frame[-1], text="공제총액", font=self.font).pack(side="left")
        Label(frame[-1], text=self.set_Comma(total_deduction), font=self.font).pack(side="right")
        return total_deduction
    
    def set_Comma(self, string):
        print(string)
        return "{0:,}".format(string)
    