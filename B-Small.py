#!/usr/bin/python2.7
import fileinput

out = []
i = 0
for line in fileinput.input():
  if i!=0:
    stri = line.splitlines()[0]
    strc = stri.split(" ")
    str1 = ""
    while len(strc)!=0:
      str1 = str1+strc.pop()+" "
    out.append(str1.strip())
  i = i + 1

fileinput.close()

for i in range(0,len(out)):
  print "Case #"+str(i+1)+": "+out[i]
