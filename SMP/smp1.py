#!/usr/bin/python2.7
import socket
import pcapy
import impacket
import sys
import string
import time
from impacket import ImpactDecoder, ImpactPacket
from impacket.ImpactDecoder import EthDecoder
import sds1
import random
import packets
from packets import SMP, SDSReq, SDSResponse
import re, os
from pcapy import open_live

#generate a random 32-but port no for non-server end points(sock_smp calls)


ETH_MY_MAC = 0x40,0x16,0x7e,0x9d,0xb5,0x78 #mac 40:16:7E:9D:B5:78 #host mac address
ETH_SMP_TYPE = 0x88b5
ETH_SDS_TYPE = 0x88b6
ETH_SDS = 0x10,0x10,0x10,0x10 ,0x10,0x10 #lan sds mac address
SPORT = 62003 #port of this host

class role:
    CLIENT = 0
    PEER = 1
    SERVER = 2
    TRACKER = 3
    PROXY = 4

class smp_ep:
    #r         #role
    #serviceID      #10 byte service IDs
    def __init__(self):
        self.serviceID = re.findall('..','zzzzz'+''.join(random.choice(string.ascii_lowercase) for _ in range(5))) #5-tupled field
        self.r = 'peer'
    

class smp_ep_eth:
    #eth_addr       #6 byte eth NIC addresses
    #port           #32 bit port nos- generate randomly for non-server EP's
    def __init__(self,eth_addr,port):
        self.eth_addr = ETH_MY_MAC
        self.port = port

tab_smp = {} #hashed with smpfd's to make closing faster; key=smpfd, fields= socketObject, serviceID, r, eth, port, ttl

def socket_smp(ep,addrlen):  #socket needed only for sending, for receiving pcapy is good; if role is server=2, then register with EPM(choice=1), else-generate random 32-bit port nos, check with EPM(choice='2'), try fetching corresponding eth, port, ttl, auth, from EPM(choice = '4'), if reply is '0', go to SDS, after receiving reply from SDS, insert into EMP(choice ='3')
#first send the request to SDS server- obtain eth
   """ try:
        s = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(ETH_SMP_TYPE))
        response = sds.directory_smp(ep, addrlen, ep_eth, ethlen)  #call only for r != 'client'
        if response == -1:
            return -2
        tab_smp[s.fileno]=(s,ep.serviceID,ep.r)
        return s.fileno
    except:
        return -1"""
   print os.path.exists('EPMr')
   pout = os.open('EPMr', os.O_WRONLY)
   pin = open('EPMw', 'r')
   os.write(pout, '1\n')
   port = int(''.join(random.choice('10') for _ in range(32)), 2) #least chance that ports will be repeated- randomized
   if ep.r == 2:
       os.write(pout, ep.serviceID+" "+"2"+" "+str(port)+"\n")
       print 'Written'
       res = pin.readline()[:-1]
       if res == '0':
           return -2
       try:
           s1 = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(ETH_SMP_TYPE))
           tab_smp[s1.fileno()]=(s1,ep.serviceID,ep.r)
           return s1.fileno()
       except:
           return -1
   

def close_smp(smpfd):
    if tab_smp.has_key(smpfd):
        tab_smp[smpfd][0].close()
        tab_smp.pop(smpfd)
        return 0
    return -1

#only those applications/end\ points? whose smpfd is in tab_smp will be allowed to make smp_send and smp_recvfrom calls- associate state abstraction
def sendto_smp(smpfd, buf, bytes1, to): #int sendto_smp(int smpfd,const void *buf,size_t bytes,const struct smp_ep *to,socklen_t addrlen);
    print tab_smp
    if tab_smp.has_key(smpfd):
        #construct a pdu to SDS
        sdsReq1 = SDSReq()
        tid = ''.join(random.choice(string.digits+'abcdef') for _ in range(8)) #highly random- can't repeat- supports 2^8 tid's
        tidb = tuple(int('0x'+i, 16) for i in re.findall('..',tid))
        sdsReq1.set_tid(tidb)
        sdsReq1.set_sid(tuple(ord(i) for i in re.findall('.',tab_smp[smpfd][1])))
        sdsReq1.set_role(tab_smp[smpfd][2])
        
        #ETH pdu
        eth = ImpactPacket.Ethernet()
        eth.set_ether_type(ETH_SDS_TYPE)
        eth.set_ether_shost(ETH_MY_MAC)
        eth.set_ether_dhost(ETH_SDS)

        eth.contains(sdsReq1)

        s = tab_smp[smpfd][0]
        print s
        s.bind(("eth0",0))
        s.send(eth.get_packet())

        p = open_live("eth0", 46+bytes1, False, 100)
        p.setfilter("ether src 10:10:10:10:10:10")
        p.loop(1,EthDecoder1)

def EthDecoder1(hdr,data):
    eth = EthDecoder().decode(data)
    sdsResp = eth.child()
    print "ETH Decoded "+str(eth)+" "+sdsResp.__str__()

    port = sdsResp.get_port()
    ttl = sdsResp.get_ttl()
    ethAddress = sdsResp.get_ethAddress()
    sid1 = sdsResp.get_sid()
    role1 = sdsResp.get_role()

    sock1 = 0
    for key in tab_smp.keys():
        if tab_smp[key] == (sid1, role1):
            sock1 = tab_smp[key][0]
            break

    smpPacket = SMP()
    smpPacket.set_plen(bytes1)
    smpPacket.set_dport(port)
    smpPacket.set_sport(SPORT)
    smpPacket.contains(ImpactPacket.Data(buf))

    ethsmp = ImpactPacket.Ethernet()

    ethsmp.set_ether_shost(ETH_MY_MAC)
    ethsmp.set_ether_dhost(ethAddress)
    ethsmp.set_ether_type(ETH_SMP_TYPE)
    ethsmp.contains(smpPacket)

    sock1.send(ethsmp.get_packet())


to = smp_ep()
to.r = 2
to.serviceID = 'ca4433b4ad'
s11 = socket_smp(to, 10)
print s11
sendto_smp(s11, 'abcd', 32, to)
    
    
    


            
        
        
    
    
    
    
    
    
