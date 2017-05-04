# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 13:54:27 2017

@author: duxin
"""

from Tkinter import *
import tkFileDialog
import tkMessageBox
from core import Tools
import time
import os
import traceback
from sys import path
from spiders_github_accounts_manage import AccountsStatusCheck_available as Aa,AccountsStatusCheck_occupied as Ao,AccountsStatusCheck_unverified as Au,github_register as gr



def RefreshAccountsStatus():
    global configs,strvars
    conn=Tools.DatabaseSupport.GenerateConn(dbname=configs['dbname'],host=configs['host'],
                                            user=configs['user'],passwd=configs['passwd'],
                                            port=configs['port'],charset=configs['charset'])
    nums=[]
    nums.append(Tools.LoadData.LoadDataByCmd(conn,"select count(*) from github_accounts where status='available'"))
    nums.append(Tools.LoadData.LoadDataByCmd(conn,"select count(*) from github_accounts where status='occupied'"))
    nums.append(Tools.LoadData.LoadDataByCmd(conn,"select count(*) from github_accounts where status='unverified'"))
    nums.append(Tools.LoadData.LoadDataByCmd(conn,"select count(*) from github_accounts where status='unregistered'"))
    nums.append(Tools.LoadData.LoadDataByCmd(conn,"select count(*) from github_accounts"))
    
    values=map(lambda x:int(strvars[x].get().split('\t')[0]),range(5))
    diffes=map(lambda x:nums[x][0][0]-values[x],range(5))
    
    map(lambda x:strvars[x].set(str(nums[x][0][0])+'\t'+(diffes[x]>=0 and '+' or '')+'%s'%(diffes[x])),range(5))
    strvars[5].set('更新完毕！更新时间：%s'%(time.ctime()))
    conn.close()

def ReleaseAccounts():
    global configs,strvars
    conn=Tools.DatabaseSupport.GenerateConn(dbname=configs['dbname'],host=configs['host'],
                                            user=configs['user'],passwd=configs['passwd'],
                                            port=configs['port'],charset=configs['charset'])
    Tools.SaveData.UpdateData(conn,["available"],"github_accounts",["status"],"status='occupied'")
    RefreshAccountsStatus()
    strvars[5].set('已释放所有占用账号！')
    conn.close()

def CheckAccounts():
    global configs,strvars
    
    strvars[6].set("正在检查'可用'账号")
    time.sleep(0.5)
    Aa.main(configs,configs['线程数'])
    strvars[6].set("正在检查'占用'账号")
    time.sleep(0.5)
    Ao.main(configs,configs['线程数'])
    strvars[6].set('已检查完毕')
    RefreshAccountsStatus()

def CheckAccounts_unverified():
    global configs,strvars
    
    strvars[6].set("正在检查'未检验'账号")
    time.sleep(0.5)
    Au.main(configs,configs['线程数'])
    RefreshAccountsStatus()
    strvars[6].set('已检查完毕')

def SelectDirectory():
    global configs,strvars
    
    filename=tkFileDialog.askopenfilename()
    print filename
    strvars[7].set(filename)
    conn=Tools.DatabaseSupport.GenerateConn(dbname=configs['dbname'],host=configs['host'],
                                            user=configs['user'],passwd=configs['passwd'],
                                            port=configs['port'],charset=configs['charset'])
    new_account_count,repeat_account_count=Tools.GithubAccountManagement.ImportRawEmailAccounts(conn,filename)
    RefreshAccountsStatus()
    strvars[8].set('已经完成文件导入！导入新邮箱数: %s. 重复邮箱数: %s.'%(new_account_count,repeat_account_count))
    conn.close()

def ConfigChange():
    global configs
    config=Toplevel()
    config.title('设置')
    config.geometry('600x400+500+300')
    ori_config=__LoadConfig()
    
    f_COL1=Frame(config)
    f_COL2=Frame(config)
    
    #数据库连接设置Frame
    f_conn=Frame(f_COL1)
    Label(f_conn,text='数据库连接设置').pack(padx=10,pady=10,anchor=NW)
    f_conn_items=[]
    e_conn_items=[]
    item_names_conn=['dbname','host','port','user','passwd','charset']
    entry_values=[ori_config['dbname'],ori_config['host'],ori_config['port'],
                  ori_config['user'],ori_config['passwd'],ori_config['charset']]
    entry_textvaris=[]
    for i in range(6):
        entry_textvaris.append(StringVar())
        f_conn_items.append(Frame(f_conn))
        Label(f_conn_items[i],text=item_names_conn[i]).pack(anchor=NW)
        e_conn_items.append(Entry(f_conn_items[i],textvariable=entry_textvaris[i]))
        entry_textvaris[i].set(entry_values[i])
        e_conn_items[i].pack(padx=10,anchor=NE)
        f_conn_items[i].pack(padx=10,anchor=NW)
    
    #程序参数设置Frame
    f_paras=Frame(f_COL2)
    Label(f_paras,text='程序参数设置').pack(padx=10,pady=10,anchor=NW)
    f_paras_items=[]
    e_paras_items=[]
    item_names_paras=['线程数']
    entry_values=[ori_config['线程数']]
    entry_textvaris_paras=[]
    for i in range(1):
        entry_textvaris_paras.append(StringVar())
        f_paras_items.append(Frame(f_paras))
        Label(f_paras_items[i],text=item_names_paras[i]).pack(anchor=NW)
        e_paras_items.append(Entry(f_paras_items[i],textvariable=entry_textvaris_paras[i]))
        entry_textvaris_paras[i].set(entry_values[i])
        e_paras_items[i].pack(padx=10,anchor=NE)
        f_paras_items[i].pack(padx=10,anchor=NW)
        
    
    
    Button(config,text='保存设置',command=lambda:__SaveConfig(item_names_conn+item_names_paras,e_conn_items+e_paras_items)).pack(padx=10,side=BOTTOM)
    f_conn.pack(padx=20,anchor=NW)
    f_paras.pack(padx=20,anchor=NW)
    
    f_COL1.place(x=30,y=30)
    f_COL2.place(x=280,y=30)
    
    

def __SaveConfig(item_names,e_items):
    global configs
    new_config=map(lambda x:item_names[x]+'='+e_items[x].get(),range(len(e_items)))
    f=open('config.txt','w')
    for i in new_config:
        f.write(i+'\n')
    f.close()
    configs=__LoadConfig()
    tkMessageBox.askokcancel(title='保存成功',message='已保存配置成功！')
    

def __LoadConfig():
    f=open('config.txt','r')
    configtxt=map(lambda x:[x.split('=')[0],len(x.split('='))>=2 and x.split('=')[1].replace('\n','').replace(' ','') or ''],f.readlines())
    f.close()
    config=dict()
    for i in configtxt:
        if i=='':
            continue
        config[i[0]]=i[1]
    config['port']=int(config['port'])
    config['线程数']=int(config['线程数'])
    return config

def RegisterNewAccounts():
    global configs
    gr.main(configs,int(strvars[9].get()),configs['线程数'])
    strvars[10].set('注册完毕！ %s'%(time.ctime()))
    RefreshAccountsStatus()
    
def __LoadRecord():
    f=open('record.dat','r')
    recordtxt=map(lambda x:[x.split('=')[0],len(x.split('='))>=2 and x.split('=')[1].replace('\n','').replace(' ','') or ''],f.readlines())
    f.close()
    record=dict()
    for i in recordtxt:
        if i=='':
            continue
        record[i[0]]=i[1]
    return record



# 主程序入口
try:
    
    configs=__LoadConfig()
    
    root=Tk()
    root.wm_title('GAmanager')
    root.geometry('800x600+300+130')
    root.iconbitmap(bitmap='GAmanager.ico')
    
    
    
    menubar=Menu(root)
    menu_file=Menu(menubar)
    #menu_file.add_command(label='统计')
    #menu_file.add_command(label='导入账号')
    menu_file.add_command(label='设置',command=ConfigChange)
    menubar.add_cascade(label='文件',menu=menu_file)
    #menubar.add_command(label='账号状态')
    root['menu']=menubar
    
    Label(root,text='欢迎使用 Github Accounts Manager V1.0',font=('Courier New',)).pack()
    Label(root,text='----------------'*20).pack(anchor=NW,pady=10)
    
    strvars=[]
    for i in range(11):
        strvars.append(StringVar(root,value=''))
    for i in range(5):
        strvars[i].set(0)
    
    
    Label(root,text='当前账号状态').pack(padx=40,pady=10,anchor=NW)
    fs=[]
    texts=[u'当前可用账号数量：',u'当前占用账号数量：',u'未验证账号数量：',u'可注册账号数量：',u'账号总数量：']
    for i in range(len(texts)):
        f=Frame(root)
        Label(f,text=texts[i]).pack(padx=10,side=LEFT)
        Label(f,textvariable=strvars[i]).pack(side=LEFT)
        fs.append(f)
        f.pack(anchor=NW,padx=30)
    
    f_refresh_info=Frame(root)
    strvars[5].set('请刷新状态')
    Label(f_refresh_info,textvariable=strvars[5]).pack(padx=10,anchor=NW)
    Button(f_refresh_info,text='刷新状态',command=RefreshAccountsStatus).pack(padx=10,side=LEFT)
    Button(f_refresh_info,text='解除账号占用',command=ReleaseAccounts).pack(padx=10,side=LEFT)
    Button(f_refresh_info,text='检查账号：可用、占用账号',command=CheckAccounts).pack(padx=10,side=LEFT)
    Button(f_refresh_info,text='检查账号：未验证账号',command=CheckAccounts_unverified).pack(padx=10,side=LEFT)
    Label(f_refresh_info,textvariable=strvars[6]).pack(padx=10,side=LEFT)
    f_refresh_info.pack(anchor=NW,padx=30,pady=10)
    
    Label(root,text='----------------'*20).pack(anchor=NW,pady=5)
    f_import_account=Frame(root)
    Label(f_import_account,text='导入新邮箱').pack(padx=10,anchor=NW)
    entrys=Entry(f_import_account,textvariable=strvars[7]).pack(padx=10,side=LEFT)
    Button(f_import_account,text='选择文件并导入',command=SelectDirectory).pack(side=LEFT)
    Label(f_import_account,textvariable=strvars[8]).pack(padx=10,side=LEFT)
    f_import_account.pack(anchor=NW,padx=30,pady=10)
    
    Label(root,text='----------------'*20).pack(anchor=NW,pady=5)
    f_import_account=Frame(root)
    Label(f_import_account,text='注册新账号（需安装Chrome浏览器)').pack(padx=10,anchor=NW)
    Label(f_import_account,text='注册账号数量：').pack(padx=10,side=LEFT)
    entrys=Entry(f_import_account,textvariable=strvars[9]).pack(padx=10,side=LEFT)
    strvars[9].set(40)
    Button(f_import_account,text='开始注册',command=RegisterNewAccounts).pack(side=LEFT)
    Label(f_import_account,textvariable=strvars[10]).pack(padx=10,side=LEFT)
    f_import_account.pack(anchor=NW,padx=30,pady=10)
        
        
        
    root.mainloop()
except Exception,e:
    print e
    traceback.print_exc()

os.system("pause")