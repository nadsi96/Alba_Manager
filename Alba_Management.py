



# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 19:20:12 2021

Alba_Management Program
Main_UI

@author: Owner
"""

from tkinter import *
import main_frame.main_frame as main_frame

main_window = Tk()

# 타이틀 이름 설정
main_window.title("Alba_Management")

# 크기 지정
# 가로 x 세로
#root.geometry("640x480")

# 프로그램 등장 위치 지정
# 가로 x 세로 + x좌표 + y좌표
# main_window.geometry("640x480+300+100")


# 창 크기 조정 설정
# (x, y)
main_window.resizable(False, False)
##############################################



mf = main_frame.Frame_Main(main_window)



##############################################

main_window.mainloop()

# =============================================================================
# from tkinter import *
# from settings_frame.work_record.lookup_record.search_type import by_month
# 
# root = Tk()
# a = by_month.By_Month(root)
# #a = analysis_wage.Analysis_Wage(root)
# 
# root.mainloop()
# =============================================================================

