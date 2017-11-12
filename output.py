# -*- coding: utf-8 -*-
'''
Author: Jimmy Chen
PN: Leetcode crawler (output), Created Nov. 2017
Ver: 1.0 (finish)
Link: 
'''
# --------------------------------------------------- libs import
import requests
from bs4 import BeautifulSoup
import re
import json
import random
import sqlite3
# --------------------------------------------------- function
def get_one(diff):
    conn = sqlite3.connect('usr/leetcode.sqlite')
    cur = conn.cursor()
    sqlstr = ("SELECT * FROM leetcode WHERE (difficult == '{}' AND lock == 0) ORDER BY RANDOM() LIMIT 1".format(diff))
    cur.execute(sqlstr)
    count = 0
    for each in cur:
        id_ = each[0]
        title = each[1]
        submit = each[2]
        accept = each[3]
        acc_ratio = round(each[4]*100, 2)
        q_link = each[5]
        a_link = each[6]
        print("========================================")
        print("This is Question {}: {} ({})".format(id_, title, diff.capitalize()))
        print("Accept: {}".format(accept))
        print("Submit: {}".format(submit))
        print("Accept Rate: {}".format(str(acc_ratio)+'%'))
        print("Link: https://leetcode.com/problems/{}/description/".format(q_link))
        if a_link == None:
            print('No solution')
        else:
            print("Solution: https://leetcode.com/problems/{}/solution/".format(a_link))
        print("========================================")

# --------------------------------------------------- Start
while True:
    diff = input(str('Choose difficulty (Easy, Medium or Hard)> '))
    if diff == 'Q' or diff == 'q' or diff == '0':
        break
    get_one(diff.lower())