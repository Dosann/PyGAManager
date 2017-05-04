# -*- coding: utf-8 -*-
'''
create time: 2017/5/5 22:48
author: duxin
site: 
email: duxin_be@outlook.com
'''

import random

def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    rando = random.Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str

email_filename=raw_input("Please input emails output file's name: ")
email_count=int(raw_input("Please input emails count: "))
emails=['']*email_count
for i in range(email_count):
    emails[i]=random_str(12)+'@outlook.com'
print emails

f=open(email_filename,'w')
for email in emails:
    f.write(email+'----'+'fatalemails'+'\n')
f.close()




