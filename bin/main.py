#!/usr/bin/env python
#_*_ coding:utf-8 _*_
# Author:bear

import os,sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from core import teacher_func,student_func

def main():
    while True:
        print("欢迎来到学员管理系统！\n1.讲师窗口\n2.学员窗口\n3.退出")
        user_choice = input("请输入您要进行的操作：")
        if user_choice.isdigit():
            if user_choice == "1":
                teacher_func.run()
            elif user_choice == "2":
                student_func.run()
            elif user_choice == "3":
                exit()
            else:
                print("您输入的ID不存在请重新输入！")
        else:
            print("输入错误，请重新输入！")

if __name__ == "__main__":
    main()