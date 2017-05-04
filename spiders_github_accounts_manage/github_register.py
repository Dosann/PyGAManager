# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 14:24:55 2017
@author: duxin
Email: duxin_be@outlook.com

"""

from sys import path
path.append("../")
from core import Tools
from core import Spider
import time
import Queue
import github
import traceback
from string import zfill
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def crawl_userdetails(threadname,taskque,crawlerbody,errortasks):
    #从队列中获取任务，编写与该任务相关的信息提取代码

    webdriver=crawlerbody.driver
    conn=crawlerbody.conn
    if taskque.empty():
        print "taskqueue is empty. program ends"
        return
    accountid,accountname,nickname=taskque.get()
    
    try:
        try:
            #根据accountname,nickname注册github账号
            webdriver.get("https://www.github.com/")
        except:
            pass
        
        Tools.SeleniumSupport.WaitUntilPresence(webdriver,"""//*[@id="user[login]"]""")
        tb1=webdriver.find_element_by_xpath("""//*[@id="user[login]"]""")
        tb1.clear()
        tb1.send_keys(nickname)
        Tools.SeleniumSupport.WaitUntilPresence(webdriver,"""//*[@id="user[email]"]""")
        tb2=webdriver.find_element_by_xpath("""//*[@id="user[email]"]""")
        tb2.clear()
        tb2.send_keys(accountname)
        Tools.SeleniumSupport.WaitUntilPresence(webdriver,"""//*[@id="user[password]"]""")
        tb3=webdriver.find_element_by_xpath("""//*[@id="user[password]"]""")
        tb3.clear()
        tb3.send_keys("a123456")
        Tools.SeleniumSupport.PushButtonByXpath(webdriver,"""/html/body/div[4]/div[1]/div/div/div[2]/form/button""")

        
        try:
            Tools.SeleniumSupport.PushButtonByXpath(webdriver,"""//*[@id="js-pjax-container"]/div/div[2]/div/form/button""")
        except Exception,e:
            print e
            print "this email has been used"
            Tools.SaveData.UpdateData(conn,['unusable'],"github_accounts",['status'],"github_account='%s'"%(accountname))
            return
        
        Tools.SeleniumSupport.WaitUntilPresence(webdriver,"""//*[@id="answers_98_choice_476"]""")
        webdriver.find_element_by_xpath("""//*[@id="answers_98_choice_476"]""").click()
        webdriver.find_element_by_xpath("""//*[@id="answers_99_choice_464"]""").click()
        webdriver.find_element_by_xpath("""//*[@id="answers_99_choice_467"]""").click()
        webdriver.find_element_by_xpath("""//*[@id="answers_100_choice_471"]""").click()
        webdriver.find_element_by_xpath("""//*[@id="js-pjax-container"]/div/div[2]/div/form/fieldset[4]/div/div/div[1]/input[1]""").send_keys('programming\n')
        Tools.SeleniumSupport.PushButtonByXpath(webdriver,"""//*[@id="js-pjax-container"]/div/div[2]/div/form/input""")
        Tools.SeleniumSupport.PushButtonByXpath(webdriver,"""//*[@id="user-links"]/li[3]/a/span""")
        Tools.SeleniumSupport.PushButtonByXpath(webdriver,"""//*[@id="user-links"]/li[3]/div/div/form/button""")
        print "account %s has been successfully registered"%(accountid)
        Tools.SaveData.UpdateData(conn,("unverified",time.strftime("%Y%m%d-%H%M%S")),"github_accounts",["status","update_time"],"id=%s"%(accountid))
        time.sleep(5)
    except Exception,e:
        webdriver.quit()
        traceback.print_exc()
        print e
        print "error while registering. current account:",accountid
    '''
    #检测该账号是否可用，若可用，则更新数据库
    g=github.Github(accountname,"a123456")
    if g.rate_limiting[1]>=5000:
        print "account %s is available"%(accountid)
        Tools.SaveData.UpdateData(conn,("available",time.strftime("%Y%m%d-%H%M%S")),"github_accounts",["status","update_time"],"id=%s"%(accountid))
    else:
        print "account %s is not available"%(accountid)
        Tools.SaveData.UpdateData(conn,("flagged",time.strftime("%Y%m%d-%H%M%S")),"github_accounts",["status","update_time"],"id=%s"%(accountid))
    '''

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
    paras["webdriver"]="Chrome"
    #使用的github账号列表
    paras["accountlist"]=None
    
    
    return paras


def create_queue():
    global limit_number,configs
    #读取任务信息
    conn=Tools.DatabaseSupport.GenerateConn(dbname=configs['dbname'],host=configs['host'],port=configs['port'],user=configs['user'],passwd=configs['passwd'],charset=configs['charset'])
    accounts=Tools.GithubAccountManagement.GetGithubAccounts(conn,select_condition="status='unregistered'",number_limit=limit_number)
    conn.close()
    #构建任务队列
    que=Queue.Queue()
    

    for i in range(len(accounts)):
        nickname=Tools.OtherSupport.GenerateRandomString(10)+zfill(accounts[i][0],5)
        que.put((accounts[i][0],accounts[i][1],nickname))
    return que

def main(configs1,limit_number1,threadnumber1):
    global threadnumber,limit_number,configs
    configs=configs1
    threadnumber=threadnumber1
    limit_number=limit_number1
    print threadnumber,limit_number
    Spider.main(get_paras(),create_queue,crawl_userdetails,mode=1)