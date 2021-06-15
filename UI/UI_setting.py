
from tkinter import *
import tkinter.ttk as ttk
import tkinter.font as tkFont

import datetime

from Functions import functions as f

def get_font(font="consolas", f_size=12, weight="normal"):
    fontStyle = tkFont.Font(family=font, size=f_size, weight=weight)
# =============================================================================
#      fontStyle = tkFont.Font(family="Lucida Grande", size=12)
#      fontStyle = tkFont.Font(family="consolas", size=12)
#      fontStyle = tkFont.Font(size=12)
#      fontStyle = None
# =============================================================================
    return fontStyle

def set_frame( parent, side=None, padx=None, pady=None, relief=None, bd=None, width=None, height=None):
    frame = Frame(parent, relief=relief, bd=bd, width=width, height=height)
    frame.pack(side=side, fill="both", expand=True, padx=padx, pady=pady)
    return frame

def set_LabelFrame(parent, text, font=None, side=None, padx=None, pady=None):
    lf = LabelFrame(parent, text=text, font=font)
    lf.pack(side=side, fill="both", expand=True, padx=padx, pady=pady)
    return lf

def new_Window(parent=None, title=None, frame_size=None):
    new_window = Toplevel(parent)
    new_window.geometry(frame_size)
    new_window.title(title)
    return new_window

# 여백 주기 위한 빈 라벨
def space_area(parent, side, length=1):
    string = ' ' * length
    Label(parent, text=string).pack(side=side)
    return


def get_Date_Spinbox(parent):
    current_date = datetime.datetime.today()
        
    sb_year = ttk.Spinbox(parent, from_=0, to=9999, width=6, validate="key")
    sb_month = ttk.Spinbox(parent, from_=1, to=12, width=3, validate="key")
    sb_day = ttk.Spinbox(parent, from_=1, to=f.get_last_day(current_date), width=3, validate="key")
    
    return sb_year, sb_month, sb_day


    
def get_Hour_Combobox(parent, f_size=12, width=5, state="readonly"):
    hours = [str(x) if x > 9 else "0" + str(x) for x in range(25)]
    cmb_hour = ttk.Combobox(parent, value=hours, width=width, state=state, font=get_font(f_size=f_size))
    return cmb_hour

def get_Minute_Combobox(parent, f_size=12, width=5, state="readonly"):
    mins = [str(x) if x > 9 else "0"+str(x) for x in range(0, 60, 5)]
    cmb_mins = ttk.Combobox(parent, value=mins, width=width, state=state, font=get_font(f_size=f_size))
    return cmb_mins

def get_Rest_Combobox(parent, f_size=12, width=5, state="readonly"):
    rest = [0, 30, 35, 40, 45, 50, 55, 60]
    cmb_rest = ttk.Combobox(parent, value=rest, width=width, state=state, font=get_font(f_size=f_size))
    return cmb_rest