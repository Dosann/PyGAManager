# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 16:34:22 2017
@author: duxin
Email: duxin_be@outlook.com

"""

def db_construction(cur,tables):
    
    #若表单不存在，则添加
    
    if "github_accounts" not in tables:
        CreateUserdetails(cur)

#添加表单

def CreateUserdetails(cur):
    cmd="""create table github_accounts(
            id int auto_increment primary key,
            github_account varchar(100),
            github_passwd varchar(20),
            mail_type varchar(20),
            mail_passwd varchar(20),
            status varchar(20),
            update_time varchar(15),
            occupation tinyint(4))
            """
    cur.execute(cmd)

