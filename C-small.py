#!/usr/bin/python2.7

import fileinput
n = c = 0
out = []
t9 = {0: [' '],2:['a','b','c'],3:['d','e','f'],4:['g','h','i'],5:['j','k','l'],6:['m','n','o'],7:['p','q','r','s'],8:['t','u','v'],9:['w','x','y','z']}  
for line in fileinput.input():
    if c==0:
        n = int(line)
    else:
        ans = ''
        msg = line
        prev = 0
        for j in range(0,len(msg)):
            ind = 0
            ch = msg[j]
            for key in t9.keys():
                if ch in t9[key]:
                    if c!=1 and key == prev:
                        ans = ans+' '
                    ind = t9[key].index(ch)
                    for k in range(0,ind+1):
                        ans = ans+str(key)
                    prev = key
                    break
        out.append(ans)
    c = c + 1
fileinput.close()
for i in range(0,n):
    print "Case #"+str(i+1)+": "+out[i]
                    
            
    
