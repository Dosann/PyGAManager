<<<<<<< HEAD
# -*- coding: utf-8 -*-
=======
﻿# -*- coding: utf-8 -*-
>>>>>>> 6da510890b30b3bda1c2b7af8b04466846c58ff8
"""
Created on Fri Mar 31 14:01:25 2017

@author: duxin
"""


from sys import path
path.append("../")
from core import Tools
'''
<<<<<<< HEAD
GithubAccountManagement.ImportRawEmailAccounts(u'163邮箱3.txt')
=======
>>>>>>> 6da510890b30b3bda1c2b7af8b04466846c58ff8
GithubAccountManagement.ImportRawEmailAccounts(u'github_accounts.txt',split_char='\t')
GithubAccountManagement.ImportRawEmailAccounts(u'github_accounts2.txt')
GithubAccountManagement.ImportRawEmailAccounts(u'github_accounts3.txt')
'''
conn=Tools.DatabaseSupport.GenerateConn(dbname="grabgithub",host='10.2.1.26')
<<<<<<< HEAD
Tools.GithubAccountManagement.ImportRawEmailAccounts(conn,u'github_accounts4.txt')
=======
Tools.GithubAccountManagement.ImportRawEmailAccounts(conn,u'..//files//emails-20170417.txt')
>>>>>>> 6da510890b30b3bda1c2b7af8b04466846c58ff8
conn.close()