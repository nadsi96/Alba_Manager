from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox

import datetime

from UI import UI_setting
from Functions import functions as f
from Functions import mongoDB

class Check_Input_Sub:
    def __init__(self, parent, top, temp_data):
        print("top :", top)
        print("parent :", parent)
        print("temp_data :", temp_data)
        self.top = top
        self.parent = parent
        self.temp_data = temp_data
        
        #self.window = Toplevel(parent)
        self.window = UI_setting.new_Window(parent, title="check")
        #self.window.title("check")
        self.font = UI_setting.get_font(f_size=10)
        
        self.set_Window()
        
        self.window.grab_set()
        self.window.protocol("WM_DELETE_WINDOW", lambda : f.on_Closing(parent, self.window))
        
    def set_Window(self):
        self.set_Frame_Radio_Buttons(self.window)
        self.set_Frame_Content(self.window)
        self.set_Frame_Buttons(self.window)
        
        self.set_Command()
        return
    
    def set_Frame_Radio_Buttons(self, parent):
        self.frame_radio_buttons = UI_setting.set_frame(parent)
        
        self.option_var = IntVar()
        self.rb_substitution = Radiobutton(self.frame_radio_buttons, text="대타", value=1, variable=self.option_var, font=self.font)
        self.rb_change_time = Radiobutton(self.frame_radio_buttons, text="시간 변경", value=2, variable=self.option_var, font=self.font)
        
        self.rb_substitution.pack(side="left")
        self.rb_change_time.pack(side="left")
    
    def set_Frame_Content(self, parent):
        self.frame_content_master = UI_setting.set_frame(parent)
        
        self.frame_content_master.grid_rowconfigure(0, weight=1)
        self.frame_content_master.grid_columnconfigure(0, weight=1)
        
        self.frames = []
        for F in (Substitution, Change_Time):
            page_name = F.__name__
            print(page_name)
            frame = F(parent=self.frame_content_master, controller=self.window, top=self.top)
            self.frames.append(frame)
            frame.grid(row=0, column=0, sticky="nsew")

        print("\n\n")
        print(self.frames)
        print("\n\n")
        
    def show_frame(self):
        frame = self.frames[self.option_var.get()-1]
        print(frame)
        print()
        frame.tkraise()
        return
    
    def set_Frame_Buttons(self, parent):
        self.frame_btns = UI_setting.set_frame(parent)
        
        self.btn_back = Button(self.frame_btns, text="뒤로", font=self.font, padx=5)
        self.btn_back.pack(side="left")
        
        self.btn_input = Button(self.frame_btns, text="입력", font=self.font, padx=5)
        self.btn_input.pack(side="right")
    
    def set_Command(self):
        self.btn_back.config(command=self.cmd_btn_back)
        self.btn_input.config(command=self.cmd_btn_input)
        
        self.rb_substitution.config(command=self.show_frame)
        self.rb_change_time.config(command=self.show_frame)
        return
    
    def cmd_btn_back(self):
        self.parent.grab_set()
        self.window.destroy()
        return
    
    def cmd_btn_input(self):
        
        option_var = self.option_var.get()
        if option_var:
            content = self.frames[option_var-1].get_Content()
            if content == "" or content == None:
                msgbox.showwarning("", "내용을 입력하세요")
                return
            print("\n")
            print(content)
            print()
            msgbox.showinfo("addtional_content", "입력되었습니다")
            self.top.destroy_flag = True
            self.top.content = (option_var, content)
            
            self.top.check_and_save_Data(self.temp_data)
            self.window.destroy()
        else:
            msgbox.showwarning("", "항목을 선택하세요")
            return
        
        return


# == Frame
class Substitution(LabelFrame):
    def __init__(self, parent, controller, top):
        self.font = UI_setting.get_font(f_size=10)
        LabelFrame.__init__(self, parent, font=self.font, padx=5, pady=5)
        self.controller = controller
        self.top = top
        self.set_Frame()
    
    def set_Frame(self):
        Label(self, text="기존 근무자 :", font=self.font, padx=5, pady=5).pack(side="left")
        
        db = mongoDB.MongoDB.instance()
        cursors = db.collection_staff.find({"name" : {"$not" : {"$eq" : self.top.data["name"]}}}).sort("empno",1)
        staff_names = []
        
        for cursor in cursors:
            staff_names.append(cursor["name"])
        self.cmb_staff_lst = ttk.Combobox(self, font=self.font, value=staff_names,
                                          width=7, state="readonly")
        self.cmb_staff_lst.pack(side="right")
    
    def get_Content(self):
        return self.cmb_staff_lst.get()
    
class Change_Time(LabelFrame):
    def __init__(self, parent, controller, top):
        self.font = UI_setting.get_font(f_size=10)
        LabelFrame.__init__(self, parent, font=self.font, padx=5, pady=5)
        
        self.controller = controller
        self.top = top
        
        self.set_Frame()
        return
    
    def set_Frame(self):
        self.y_scroll = Scrollbar(self)
        self.y_scroll.pack(side="right")
        self.txt_box = Text(self, width=30, height=5, yscrollcommand=self.y_scroll.set, font = self.font)
        self.txt_box.pack(side="left")
        self.y_scroll.config(command=self.txt_box.yview)
        
        self.txt_box.insert(END, "시간 변경 이유 작성")
        
    def get_Content(self):
        return self.txt_box.get("1.0", END)