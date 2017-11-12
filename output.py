# -*- coding: utf-8 -*-
'''
Author: Jimmy Chen
PN: Leetcode crawler (output), Created Nov. 2017
Ver: 1.2 (Add secret path)
Link: 
'''
# --------------------------------------------------- libs import
import sys
import sqlite3
# --------------------------------------------------- function
def get_one(diff):
    conn = sqlite3.connect('{}leetcode.sqlite'.format(PATH))
    cur = conn.cursor()
    if diff == 'easy' or diff == 'medium' or diff == 'hard':
        sqlstr = ("SELECT * FROM leetcode WHERE (difficult == '{}' AND lock == 0) ORDER BY RANDOM() LIMIT 1".format(diff))
    else:
        sqlstr = ("SELECT * FROM leetcode WHERE (lock == 0) ORDER BY RANDOM() LIMIT 1".format(diff))
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
        difficult = each[7]
        print("========================================")
        print("This is Question {}: {} ({})".format(id_, title, difficult.capitalize()))
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
    with open('/Users/jimmyweicc/PATH/leetcode-crawler/path.txt', 'r') as f:
        PATH = f.readline()
    diff = 'empty'
    if len(sys.argv) >= 2:
        diff = str(sys.argv[1])
    get_one(diff.lower())
    break