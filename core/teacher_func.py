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

class Teachers(object):
    def __init__(self, name):
        self.name = name

    def shwo_vive_students(self):
        """查看所有的学生信息"""
        select_data = session.query(Initialization_data.Student.id,Initialization_data.Student.name,Initialization_data.Student.qq).all()
        print(select_data)

    def shwo_vive_grade(self):
        """教师可以查看所有的课程"""
        select_data = session.query(Initialization_data.Grade.id,Initialization_data.Grade.name).all()
        print(select_data)

    def creat_grade(self):
        """教师可以创建班级"""
        grade_name = input("请输入要创建的课程名称").strip()
        grade = Initialization_data.Grade(name=grade_name)
        session.add(grade)
        session.commit()

    def add_grade_record(self):
        """添加上课记录，添加一条上课记录，所有报名这个课程的学员都增加一条上课记录"""
        pass

    def show_class(self):
        """查看班级信息,这里应该连表查把学生姓名和课程名字替换进行显示，sql是这样的：
        select gr.id,g.name,s.name,gr.date,gr.grade_status,gr.score from grade_record gr
            left join grades g
            on gr.grade_id = g.id
            left join students s
            on gr.stu_id = s.id
            """
        grade_record_count = session.query(Initialization_data.GradeRecord).count()
        grade_record_obj = session.query(Initialization_data.GradeRecord).all()
        for i in range(grade_record_count):
            print(grade_record_obj[i].student, grade_record_obj[i].grade, "上课日期：" + str(grade_record_obj[i].date),
                  "上课状态：" + grade_record_obj[i].grade_status, "上课成绩：" + str(grade_record_obj[i].score))

    def management_grade(self):
        """管理班级，创建班级，根据学员qq号把学员加入班级"""
        while True:
            stu_qq = input("请输入学员的qq号(返回上级菜单请输入B)：").strip()
            if stu_qq == "B":break
            stu_qq = (stu_qq,)
            select_stu_qq = session.query(Initialization_data.Student.qq).all()
            # print(select_stu_qq,stu_qq)
            if stu_qq in select_stu_qq:
                while True:
                    chois = input("1.为学员添加班级。\n2.为学员批改成绩,请输入要操作的ID：\n3.退出请输入B\n>>>>:").strip()
                    if chois == "1":
                        select_stu_id = session.query(Initialization_data.Student.id).filter(Initialization_data.Student.qq == stu_qq).first()
                        select_grade_name = session.query(Initialization_data.Grade.id,Initialization_data.Grade.name).all()

                        print(select_grade_name)
                        grade_choise = int(input("请输入为学员添加课程名称的编号：").strip())
                        grade_date = input("请输入添加上课记录的日期(格式：2018-07-01)：").strip()
                        insert_data = Initialization_data.GradeRecord(grade_id=grade_choise,stu_id=select_stu_id[0],date=grade_date)
                        session.add(insert_data)
                        session.commit()
                        break
                    elif chois == "2":
                        stu_name = session.query(Initialization_data.Student.name).filter(Initialization_data.Student.qq == stu_qq).first()
                        print("您要批改%s学员的成绩" %stu_name)
                        #先查出学员的id在students表根据学生的qq号
                        select_stu_id = session.query(Initialization_data.Student.id).filter(Initialization_data.Student.qq == stu_qq).first()
                        #在根据gread_record表里的stu_id字段查出对应的grade_id
                        select_grade_id = session.query(Initialization_data.GradeRecord.grade_id).filter(Initialization_data.GradeRecord.stu_id == select_stu_id[0]).all()
                        #根据学员id查询出学员修了几门课程的信息,这里需要循环两次，第一次是把select_grade_id的返回结果类似于[(1,),(2),]这个格式的列表元素都循环出来是一个元组
                        for index, item in enumerate(select_grade_id):  # [(1),(2)]
                            #然后进行第二次循环是把元组的元素取出来，这时候肯定元组只有一个元素
                            #print(index,item)
                            for i in item:
                                # print(i)
                                stu_obj = session.query(Initialization_data.GradeRecord).filter(Initialization_data.GradeRecord.stu_id == select_stu_id[0],Initialization_data.GradeRecord.grade_id == i).first()
                                print("%s %s 课程ID：%s 上课日期：%s 上课状态：%s 上课分数：%s" %(stu_obj.student,stu_obj.grade,stu_obj.grade_id,stu_obj.date,stu_obj.grade_status,stu_obj.score))
                        grade_choise = int(input("请输入您要修改成绩的课程ID：").strip())
                        grade_date = input("请输入需要修改成绩课程的上课日期").strip()
                        grade_score = int(input("请输入课程的成绩：").strip())
                        update_score = session.query(Initialization_data.GradeRecord).filter(Initialization_data.GradeRecord.grade_id == grade_choise,Initialization_data.GradeRecord.stu_id == select_stu_id[0],Initialization_data.GradeRecord.date == grade_date).first()
                        update_score.score = grade_score
                        session.commit()
                    elif chois == "B":
                        break
                    else:
                        print("您输入的ID不正确")
            else:
                print("您输入的学员qq号码不正确，请重新输入！")

    def modify_score(self):
        """讲师修改学生成绩分数"""
        pass

def teacher_list():
    """取出老师的列表"""
    select_data = session.query(Initialization_data.Teacher).filter().all()
    for index, item in enumerate(select_data):
        print(index, item)
    return select_data
# teacher_list()

def logout():
    # sys.exit("欢迎下次光临")
    pass

def run():
    """学校管理接口菜单打印"""
    while True:
        t_list = teacher_list()
        teacher_choise = input("欢迎来到讲师管理系统,请输入ID号，选择身份：(退出请输入B)").strip()
        if teacher_choise == "B":break
        teacher_choise = int(teacher_choise)
        print("您当前登录的用户为：", t_list[teacher_choise])
        teacher = Teachers(t_list[teacher_choise])
        menu = '''
        -------The lecturer system ---------
        \033[32;1m 1.  查看课程信息
        2.  查看学员信息
        3.  创建课程
        4.  管理班级
        5.  查看班级信息
        6.  退出
        \033[0m'''
        menu_dic = {
            "1": teacher.shwo_vive_grade,
            "2": teacher.shwo_vive_students,
            "3": teacher.creat_grade,
            "4": teacher.management_grade,
            "5": teacher.show_class,
            "6":logout
        }
        menu_flag = True
        while menu_flag:
            print(menu)
            user_choice = input("请输入您要操作的ID：").strip()
            if user_choice == "6":
                menu_flag = False
                print("程序安全退出！")
            elif user_choice in menu_dic:
                menu_dic[user_choice]()
            else:
                print("\033[31;1m您输入的ID不存在，请重新输入!\033[0m")

if __name__ == "__main__":
    run()