packets.py:
Is used to define methods to set SID's, TID's, role, etc- inspired from Impacket.ImpactPacket module


sds1.py:
Is used to service directory_smp requests from sock_smp as well as sendto_smp calls. Receives SDS Request PDU's, responds with SDS Response PDU's
It is capable of servicing 50 requests. It's MAC No. is given as 10:10:10:10:10:10


smp1.py:
Is the SMP library present in every host. It has a tab_smp dictionary. tab_smp stores the file descriptor(smpfd) of every socket which is opened using the sock_smp call. This smpfd is associated with the service ID and role requested for. This serves as an abstraction for the Associate state. Whichever socket's file descriptor will be in the tab_smp dictionary will be allowed to send or receive SMP Packets.


EPM.py:
This is the end point mapper. It is capable of servicing 20 requests from the host it is running on. The number 20 is for testing purposes. EPM communicates with smp1(the SMP Library) totally through named pipes(FIFOs) 'EPMr' and 'EPMw'. First a choice is asked from the SMP Library:
1: for registering a server port,should give appropriate reply in case of duplication, 2: for knowing whether a port is engaged or not, 
3: for inserting a recently queried ServiceID, Role with Auth='NO', 
4: for fetching associated cached values with ep
SMP Library replies to each one with a suitable formatted string(as in comments of EPM). EPM then responds with the answer or '0'.
EPM also timestamps each new (serviceID, role) inserted in it to implement ttl(Time-To-Live)
