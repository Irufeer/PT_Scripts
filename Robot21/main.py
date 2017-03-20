#! /usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import time
import re
tik = [1,1,2,2,4,4,6,6,8,8,10,10,20,20,30,30,60,60,300,300,1800,1800,3600,3600]

main_url  = 'http://npupt.com'
user_agent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) "
              "AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/36.0.1985.143 Safari/537.36")

def signIn(username, password):
    login_url = main_url + '/login.php'
    takelogin_url = main_url + '/takelogin.php'
    npupt_session.get(main_url)
    npupt_session.get(login_url)
    login_data = {
        'username': username,
        'password': password,
    }
    login_headers = {
        'User-Agent': user_agent,
        'Referer': main_url,
    }

    # Sign in
    npupt_session.post(takelogin_url, data=login_data, headers=login_headers)
    npupt_session.get(main_url + '/index.php')

def get_coins(html):
    pos = html.find('+/-')
    return int(re.findall('[-]?\d+', html[pos:pos+40])[0])
def getPoints(html):
    # 记得用正则重写匹配
    pos = html.find('点数')
    return int(html[pos + 9:pos + 11].strip('<'))

def need(html):
    sum = 0
    p = re.compile(r'cards/[0-9]*[a-z]+.bmp')
    num1 = re.compile(r'cards/t[pckb].bmp')
    num2_10 = re.compile(r'cards/[0-9]+[pckb].bmp')
    numJQK = re.compile(r'cards/[vdk][pckb].bmp')
    cards = p.findall(html)
    for card in cards:
        if num1.findall(card):
            sum += 1
        elif num2_10.findall(card):
            sum += int(re.findall('\d+', card)[0])
        elif numJQK.findall(card):
            sum += 10
    return sum < 15




def play():
    blackjack_url = main_url + '/blackjack.php'
    begin_data = {
        'game': 'hit',
        'start': 'yes',
    }
    again_data = {
        'game': 'hit',
    }
    stop_data  = {
        'game': 'stop',
    }

    # 记录初始值
    bj = npupt_session.get(blackjack_url).content
    coins1 = get_coins(bj)
    if coins1 < -40000 or coins1 > -20000:
        return
    # 开始新一局
    f = open('data.dat', 'a+')
    bj = npupt_session.post(blackjack_url, data=begin_data).content
    po = getPoints(bj)
    f.write(str(po) + ' ')
    # 2到14的牌面一定要牌 15 16 17看情况要牌
    while po < 15 or (15 <= po and po <= 16 and need(bj)):
        bj = npupt_session.post(blackjack_url, data=again_data).content
        po = getPoints(bj)
        f.write(str(po) + ' ')

    # (15,16,17) 18 19 20的牌面主动结束
    if po < 21:
        npupt_session.post(blackjack_url, data=stop_data)

    bj = npupt_session.get(blackjack_url).content
    # 等待上局结束
    t = 0
    while bj.find('请等待上局结束') != -1:
        print 'waiting for %d seconds' % tik[t]
        time.sleep(tik[t])
        t = (t + 1) % 24
        bj = npupt_session.get(blackjack_url).content
    coins2 = get_coins(bj)
    if coins1 < coins2:
        f.write('1\n')
        print '赢\n'
    elif coins1 > coins2:
        f.write('-1\n')
        print '输\n'
    else:
        f.write('0\n')
        print '平\n'
    f.close()


def analyse(startID, endID):
    # 弃用函数
    message_url = main_url + '/messages.php?action=viewmessage&id='
    f = open('smaller_than_16.dat', 'a+')
    for i in range(startID, endID):
        cont = npupt_session.get(message_url + str(i)).content
        soup = BeautifulSoup(cont, 'html.parser')
        reg1 = re.compile("<[^>]*>")
        content = reg1.sub('', soup.prettify())
        # print content
        start = content.find(u'BlackJack 结果')
        end   = content.find(u'沙粒。') + 10
        if start != -1:
            f.writelines(content[start:end].encode('utf8').split())
            f.write('\n')
    f.close()
def deletehang():
    # 弃用函数
    f = open('smaller_than_16.dat', 'r')
    g = open('data.dat', 'a+')
    for line in f.readlines():
        if len(line.strip()) == 0:
            continue
        g.write(line)
    f.close()
    g.close()


if __name__ == "__main__":
    npupt_session = requests.Session()
    signIn('', '')
    for i in range(10000):
        print '第%d局' % i
        play()
