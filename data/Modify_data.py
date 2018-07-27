#!/usr/bin/env python
#_*_ coding:utf-8 _*_
# Author:bear

import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import Initialization_data
from sqlalchemy.orm import sessionmaker,relationship

Session_class = sessionmaker(bind=Initialization_data.engine)  # 创建与数据库的会话session class ,注意,这里返回给session的是个class,不是实例
session = Session_class()

def Basic_Data():
    """初始化数据，这个手动添加,讲师信息、学生信息、课程信息"""
    t1 = Initialization_data.Teacher(name="Alex")
    t2 = Initialization_data.Teacher(name="Jack")
    t3 = Initialization_data.Teacher(name="Rain")
    session.add_all([t1,t2,t3])

    s1 = Initialization_data.Student(name="laoan",qq="111111")
    s2 = Initialization_data.Student(name="wangke",qq="222222")
    s3 = Initialization_data.Student(name="mengbi",qq="333333")
    s4 = Initialization_data.Student(name="alex", qq="444444")
    s5 = Initialization_data.Student(name="jack", qq="555555")
    s6 = Initialization_data.Student(name="rain", qq="666666")
    session.add_all([s1,s2,s3,s4,s5,s6])

    g1 = Initialization_data.Grade(name="Python")
    g2 = Initialization_data.Grade(name="Linux")
    session.add_all([g1,g2])

    grade_record1 = Initialization_data.GradeRecord(grade=g1,student=s1,date="2018-07-01",grade_status="YES",score=0)
    grade_record2 = Initialization_data.GradeRecord(grade=g1,student=s2,date="2018-07-01",grade_status="YES",score=0)
    grade_record3 = Initialization_data.GradeRecord(grade=g1,student=s3,date="2018-07-01",grade_status="YES",score=0)
    grade_record4 = Initialization_data.GradeRecord(grade=g2,student=s3,date="2018-07-02",grade_status="YES",score=0)
    session.add_all([grade_record1,grade_record2,grade_record3,grade_record4])

    #这里是做关联，Python课程对应关联学生，Linux关联一个学生
    g1.student = [s1,s2,s3]
    g2.student = [s3,]

    session.commit()

Basic_Data()
session.close()

# def select_test():
#     grade_obj = session.query(Initialization_data.Grade).filter(Initialization_data.Grade.name == "Python").first()
#     print(grade_obj.student)
#
# select_test()