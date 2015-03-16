#!/usr/bin/python2.7
import pcapy
from pcapy import open_live, findalldevs
import impacket
from impacket import ImpactPacket, ImpactDecoder
from impacket.ImpactDecoder import EthDecoder, UDPDecoder

import sys
import string
from threading import Thread
import socket

ETH_MY_MAC = 0x40,0x16,0x7e,0x9d,0xb5,0x78 #mac 40:16:7E:9D:B5:78

def main():
 
  
  print "Server.... Port: 62001"
  print "--------------------------------------------"
  p=open_live(findalldevs()[0],46,False,100)
  print "Listening...."
  
  p.setfilter("udp")
  p.setfilter("src port 62000")
  
  ethDecoded = p.loop(1,EthDecoder1)
  
def EthDecoder1(hdr,data):
  eth = EthDecoder().decode(data)
  ip = eth.child()
  udp = ip.child()  
  
  nonce=udp.get_data_as_string()
  print "Received: "+nonce
  
  nonceMod = hex(int(nonce.encode("hex"), 16) + 1)[2:].decode("hex")  #nonce incremented
  
  sendReply(nonceMod)
  
def sendReply(nonce):
  #build ethernet frame
  eth=ImpactPacket.Ethernet()
  eth.set_ether_type(0x88b5)
  eth.set_ether_shost(ETH_MY_MAC)
  eth.set_ether_dhost(ETH_MY_MAC)
  
  #build ip packet
  ip=ImpactPacket.IP()
  ip.set_ip_v(4)
  ip.set_ip_len(32)
  ip.set_ip_src("127.0.0.1")
  ip.set_ip_dst("127.0.0.1")
  
  #build UDP packet
  udp=ImpactPacket.UDP()
  udp.set_uh_sport(62001)
  udp.set_uh_dport(62000)
  udp.set_uh_ulen(12)
  payload=nonce
  udp.contains(ImpactPacket.Data(payload))
  
  ip.contains(udp)
  eth.contains(ip)
  
  device=findalldevs()[0]
  
  s=socket.socket(socket.AF_PACKET,socket.SOCK_RAW,socket.IPPROTO_RAW)  #socket initialized
  s.bind((findalldevs()[0],0))
  
  s.send(eth.get_packet())
  print "Sent: "+nonce
    
if __name__ == "__main__":
  main()  
