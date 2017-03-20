#! /usr/bin/env python
# -*- coding: utf-8 -*-
import re
win   = [0 for i in range(25)]
equal = [0 for i in range(25)]
lose  = [0 for i in range(25)]
f = open('data.dat', 'r')
for line in f.readlines():
    s = re.findall('[-]?\d+', line)
    if int(s[-1]) == 1:
        win[int(s[-2])] += 1
    elif int(s[-1]) == -1:
        lose[int(s[-2])] += 1
    else:
        equal[int(s[-2])] += 1

print [0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5]
print win
print equal
print lose
f.close()
