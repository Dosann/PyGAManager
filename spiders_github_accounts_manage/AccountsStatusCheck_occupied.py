# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 14:24:55 2017
@author: duxin
Email: duxin_be@outlook.com

"""

from sys import path
import os
path.append("../")
path.append(os.getcwd())
from core import Tools
from core import Spider
import Queue



def run(threadname,taskque,crawlerbody,errortasks):
    #从队列中获取任务，编写与该任务相关的信息提取代码
    
    accounts=[]
    for i in range(5):
        if not taskque.empty():
            account=taskque.get()
            accounts.append(account)
        else:
            print "taskque is empty."
            break
    if len(accounts)!=0:
        Tools.GithubAccountManagement.GetGithubAccountStatus(crawlerbody.conn,accounts)

def get_paras():
    global threadnumber,configs
    #设置参数
    paras={}
    #数据库访问设置
    paras["conn_settings"]={"dbname":configs['dbname'],
                             'host':configs['host'],
                             'port':configs['port'],
                             'user':configs['user'],
                             'passwd':configs['passwd'],
                             'charset':configs['charset']}
    #paras["conn_settings"]=None
    #线程数
    paras["threadnumber"]=threadnumber
    #不开启webdriver
    paras["webdriver"]=None
    #使用的github账号列表
    paras["accountlist"]=None
    #是否创建自动表单
    paras["db_construction"]=True
    
    
    return paras


def create_queue():
    global configs
    #创建队列
    taskque=Queue.Queue()
    #读取任务信息
    conn=Tools.DatabaseSupport.GenerateConn(dbname=configs['dbname'],host=configs['host'],port=configs['port'],user=configs['user'],passwd=configs['passwd'],charset=configs['charset'])
    accounts=Tools.GithubAccountManagement.GetGithubAccounts(conn,select_condition="status='occupied'")
    conn.close()
    print "%s accounts loaded"%(len(accounts))
    for account in accounts:
        taskque.put(account)
    
    
    return taskque

def main(configs1,threadnumber1):
    global threadnumber,configs
    configs=configs1
    threadnumber=threadnumber1
    Spider.main(get_paras(),create_queue,run,mode=1)