#!/usr/bin/env python
#_*_ coding:utf-8 _*_
# Author:bear

from sqlalchemy import Table, Column, Integer,String,DATE, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os,sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

engine = create_engine("mysql+pymysql://root:123456@172.18.1.106/stu_management?charset=utf8",  #要写入中文必须加上?charset=utf8
                       encoding='utf-8') #echo=True #echo的作用就是打印出执行的过程，所有的信息都打印出来

Base = declarative_base()

grade_m2m_student = Table('grade_m2m_student', Base.metadata,
                        Column('stu_id',Integer,ForeignKey('students.id')),
                        Column('grade_id',Integer,ForeignKey('grades.id')),
                        )

class Teacher(Base):
    """初始化创建的教师表，只有id与名字字段，不与其他表关联"""
    __tablename__ = 'teachers'
    id = Column(Integer,primary_key=True)
    name = Column(String(64),nullable=False)

    def __repr__(self):
        return self.name

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String(32),nullable=False)
    qq = Column(String(32), nullable=False)

    def __repr__(self):
        return "学员姓名：%s.学员QQ号码：%s"%(self.name,self.qq)

class GradeRecord(Base):
    """课程信息记录表，上课时间、学生状态、分数、课程,外键关联学生id和课程id"""
    __tablename__ = 'grade_record'
    id = Column(Integer, primary_key=True)
    grade_id = Column(Integer, ForeignKey("grades.id"))
    stu_id = Column(Integer, ForeignKey("students.id"))
    date = Column(DATE,nullable=False)
    grade_status = Column(String(32),default="NO")
    score = Column(Integer,default=0)

    grade = relationship("Grade", foreign_keys=[grade_id])
    student = relationship("Student",foreign_keys=[stu_id])

    def __repr__(self):
        return "上课日期：%s.\n上课状态：%s.\n上课学分：%s\n" %(self.date,self.grade_status,self.score)

class Grade(Base):
    """课程表，id，课程名，对grade_m2m_student，grade_record表进行关联，一个课程对应多个学生，一个学生也可以对应多个课程"""
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    name = Column(String(32),nullable=False)
    student = relationship('Student', secondary=grade_m2m_student, backref='grades')

    def __repr__(self):
        return "课程名称：%s" %self.name

Base.metadata.create_all(engine)