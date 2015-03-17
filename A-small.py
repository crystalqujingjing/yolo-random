#!/usr/bin/python2.7

import fileinput
n = c = i = t = 0
ans = []

for line in fileinput.input():
    if t==0:
        n = int(line)
    if t==1:
        c = int(line)
    if t==2:
        i = int(line)
    if t==3:
        flag = 0
        out = line
        out = out.splitlines()[0]
        out = out.split(" ")
        out1 = []
        for j in range(0,i):
            in1 = int(out[j])
            out1.append(in1)
        for j in range(0,i-1):
            if out1[j] <= c:
                for k in range(j+1,i):
                    if out1[k]<=c:
                        s = out1[j]+out1[k]
                        if s == c:
                            ans.append((j+1,k+1))
                            flag = 1
                            break
            if flag==1:
                break
        t = 0
    t = t + 1
fileinput.close()

for i in range(0,n):
    print "Case #"+str(i+1)+": "+str(ans[i][0])+" "+str(ans[i][1])
        
    
