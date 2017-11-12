# -*- coding: utf-8 -*-
'''
Author: Jimmy Chen
PN: Leetcode crawler (crawler), Created Nov. 2017
Ver: 1.0 (finish)
Link: 
'''
# --------------------------------------------------- libs import
import requests
import re
import json
import sqlite3
# --------------------------------------------------- Main panel
def disp_menu():
    print("--------------------")
    print("Leetcode Crawler")
    print("--------------------")
    print("1. Create table")
    print("2. Store problems")
    print("3. Clear table")
    print("0. End")
    print("--------------------")
# --------------------------------------------------- Leetcode crawl
class Crawler(object):
    """docstring for Crawler"""
    # def __init__(self, arg):
        # super(Crawler, self).__init__()
        # self.arg = arg
    def crawl():
        '''
        Crawl leetcode contents
        '''
        headers = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
        res = requests.get("https://leetcode.com/api/problems/all/", headers=headers)
        regex_str = r'{"ac_easy": 0, "category_slug": "all", (.*?), "frequency_high": 0, "ac_medium": 0, "is_paid": false, "frequency_mid": 0, "num_solved": 0, "ac_hard": 0, "user_name": "", "num_total": [\d]*}'
        m = re.search(regex_str, res.text)
        js = json.loads('{'+m.group(1)+'}')
        with open ('usr/leetcode.json', 'w') as f:
            f.write(json.dumps(js))
            f.close()
    def store():
        '''
        Trans json content into sql db
        '''
        # ===== Clear DB =====
        sqlstr = 'DELETE FROM leetcode'
        cursor = conn.execute(sqlstr)
        conn.execute(sqlstr)
        conn.commit()
        # ===== Load lateset contents =====
        filename = "usr/leetcode.json"
        temp = open(filename).read()
        leets = json.loads(temp)
        count = 0
        try:
            for leet in leets['stat_status_pairs']:
                listicle = []
                stat = leet['stat']
                diff = leet['difficulty']

                id_ = stat['question_id']
                title_ = stat['question__title']
                submit_ = stat['total_submitted']
                accept_ = stat['total_acs']
                acc_ratio_ = float(accept_/submit_)
                q_link_ = stat['question__title_slug']
                a_link_ = stat['question__article__slug']
                difficult_ = diff['level']
                if difficult_ == 1:
                    difficult_ = 'easy'
                elif difficult_ == 2:
                    difficult_ = 'medium'
                else:
                    difficult_ = 'hard'
                lock_ = leet['paid_only']
                listicle.append((id_, title_, submit_, accept_, acc_ratio_, q_link_, a_link_, difficult_, lock_))
                sqlstr = ("INSERT INTO leetcode (id, title, submit, accept, acc_ratio, q_link, a_link, difficult, lock) VALUES (?,?,?,?,?,?,?,?,?)")
                conn.executemany(sqlstr, listicle)
                conn.commit()
                count += 1
        except Exception as e:
            print(e)
        print("Total Qs: {}".format(count))

# --------------------------------------------------- Start
while True:
    disp_menu()
    choice = int(input("Choose function: "))
    print("-----------------------------------------")
    if choice == 0:
        break
    # -- 1. Create table --
    elif choice == 1:
        try:
            sqlstr = ('CREATE TABLE leetcode (id INT UNIQUE, title TEXT, submit INT, accept INT, acc_ratio NUMERIC, q_link TEXT, a_link TEXT, difficult TEXT, lock BOOLEAN)')
            conn = sqlite3.connect('usr/leetcode.sqlite')
            conn.execute(sqlstr)
            conn.commit()
            print('-- DB created --')
            print("-----------------------------------------")
        except Exception as e:
            print(e)
    # -- 2. Store problems --
    elif choice == 2:
        conn = sqlite3.connect('usr/leetcode.sqlite')
        Crawler.crawl()
        Crawler.store()
        print('-- LeetCode downloaded --')
        print("-----------------------------------------")
    # -- 3. Clear DB --
    elif choice == 3:
        choice = str(input("確定刪除資料庫? (Y/N) "))
        if choice == 'Y' or choice == 'y':
            conn = sqlite3.connect('usr/leetcode.sqlite')
            sqlstr = 'DELETE FROM leetcode'
            cursor = conn.execute(sqlstr)
            conn.execute(sqlstr)
            conn.commit()
            print('-- Database cleared --')
        else:
            print('-- Back to Main --')