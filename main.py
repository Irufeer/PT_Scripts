# -*- coding: utf-8 -*-
import codecs
import sqlite3

import requests
from bs4 import BeautifulSoup

main_url = 'http://npupt.com/'

def sign_in(username, password):
    takelogin_url = main_url + 'takelogin.php'
    login_data = {
        'username': username,
        'password': password,
    }
    npupt_session.post(takelogin_url, data=login_data)

def get_content():
    for i in range(50001,100000):
        torrent_url = 'http://npupt.com/details.php?id=' + str(i)
        cont = npupt_session.get(torrent_url).content
        soup = BeautifulSoup(cont, 'html.parser')
        if soup.find_all('div', class_='jumbotron'):
            continue
        print i
        try:
            name = soup.find_all('title')[0].get_text().split('\'')[1].strip()
            size = soup.find_all('span', class_='label label-danger')[0].get_text()[3:].strip()
            up, down = soup.find_all('div', class_='btn-group')[0].get_text().split()
            time = soup.find_all('small')[0].span['title']
            data = '%-6d %-60s %-10s %-4s %-4s %-20s\n' % (i, name, size, up, down, time)
            with codecs.open('50000.txt', 'a', 'utf-8') as f:
                f.write(data)
        except:
            with codecs.open('Error.txt', 'a', 'utf-8') as f:
                f.write('%d Problem!\n' % i)
    print 'Mission Completed'

def store(data):
    conn = sqlite3.connect("torrents.db")
    print 'Opened database successfully'
    conn.execute('''
    CREATE TABLE t20170320(
        ID    INT  PRIMARY KEY NOT NULL,
        NAME  TEXT             NOT NULL, 
        SIZE  TEXT             NOT NULL,
        UP    INT              NOT NULL,
        DOWN  INT              NOT NULL,
        TIME  TEXT             NOT NULL);
        ''')
    print 'Table created successfully' 
    sql = "insert into t20170320(id,name,age)values(%d,'%s',%d)" % (1, 'haha', 8)
    conn.execute(sql)  
    conn.commit()   
    conn.close()  
if __name__ == '__main__':
    npupt_session = requests.session()
    # need change
    sign_in('username', 'password')
    get_content()