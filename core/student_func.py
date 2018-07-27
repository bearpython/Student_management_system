#!/usr/bin/env python
#_*_ coding:utf-8 _*_
# Author:bear

import sys,os,json,pickle,re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from data import Initialization_data
from sqlalchemy.orm import sessionmaker,relationship

Session_class = sessionmaker(bind=Initialization_data.engine)
session = Session_class()

class Student(object):
    def __init__(self, name,qq):
        self.name = name
        self.qq = qq

    def sub_homewrok(self):
        """学生提交作业，需要输入学生自己的qq号，选择自己的课程，通过日期把上课状态改了，就等于交作业了，应该在添加一个字段，就这样吧"""
        select_stu_id = session.query(Initialization_data.Student.id).filter(Initialization_data.Student.qq == self.qq).first()
        select_stu_grade = session.query(Initialization_data.GradeRecord.grade_id).filter(Initialization_data.GradeRecord.stu_id == select_stu_id[0]).all()
        for index in select_stu_grade:
            for i in index:
                stu_obj = session.query(Initialization_data.GradeRecord).filter(Initialization_data.GradeRecord.stu_id == select_stu_id[0],Initialization_data.GradeRecord.grade_id == i).first()
                print("%s 课程ID：%s" %(stu_obj.grade,stu_obj.grade_id))
        grade_id_input = int(input("请输入你要提交课程作业的ID：").strip())
        grade_date_input = input("请输入提交课程的学习日期：").strip()
        update_grade_status = session.query(Initialization_data.GradeRecord).filter(
            Initialization_data.GradeRecord.grade_id == grade_id_input,
            Initialization_data.GradeRecord.stu_id == select_stu_id[0],
            Initialization_data.GradeRecord.date == grade_date_input).first()
        update_grade_status.grade_status = "Finish"
        session.commit()

    def show_score(self):
        """通过qq好查询自己的上课成绩，要选择哪个课程，通过日期选择哪节课"""
        select_stu_id = session.query(Initialization_data.Student.id).filter(Initialization_data.Student.qq == self.qq).first()
        select_stu_grade = session.query(Initialization_data.GradeRecord.grade_id).filter(Initialization_data.GradeRecord.stu_id == select_stu_id[0]).all()
        for index in select_stu_grade:
            for i in index:
                stu_obj = session.query(Initialization_data.GradeRecord).filter(Initialization_data.GradeRecord.stu_id == select_stu_id[0],Initialization_data.GradeRecord.grade_id == i).first()
                print("%s %s 上课时间%s 课程状态：%s 课程成绩：%s" %(stu_obj.student,stu_obj.grade,stu_obj.date,stu_obj.grade_status,stu_obj.score))

def student_list():
    """这里通过学员qq来查询出学员的信息，就类似登录吧，后边实例化类的时候带名字和qq号参数进去"""
    while True:
        stu_qq_input = input("请输入学员的QQ号码：").strip()
        select_stu = session.query(Initialization_data.Student).filter(Initialization_data.Student.qq == stu_qq_input).first()
        if select_stu:
            #print(select_stu.name,select_stu.qq)
            return select_stu.name,select_stu.qq
        else:
            print("您输入的qq号码不正确，请重新输入！")
# student_list()

def logout():
    # sys.exit("欢迎下次光临")
    pass

def run():
    """学员视图入口"""
    stu_namne,stu_qq = student_list()
    student = Student(stu_namne,stu_qq)
    menu = '''
    -------学员查询入口---------
    \033[32;1m 1.  提交作业
    2.  查看作业成绩
    3.  退出
    \033[0m'''
    menu_dic = {
        "1": student.sub_homewrok,
        "2": student.show_score,
        "3":logout
    }
    menu_flag = True
    while menu_flag:
        print(menu)
        user_choice = input("请输入您要操作的ID：").strip()
        if user_choice == "3":
            menu_flag = False
            print("程序安全退出！")
        elif user_choice in menu_dic:
            menu_dic[user_choice]()
        else:
            print("\033[31;1m您输入的ID不存在，请重新输入!\033[0m")

if __name__ == "__main__":
    run()