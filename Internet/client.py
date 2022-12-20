import socket
import time
import random
from computerManager import *

if __name__ == "__main__":
     #   ikun = ['蔡徐坤','唱','跳','rap','篮球','music']
   # li = []
  #  print(a.InputCommand('Send Get hhh isListen=1'))
  #  a.InputCommand('Send Set jjj 120398123.0//f isSendMessage-0')
 #   print(a.InputCommand('Send Get jjj isListen=1'))
   # starttime = time.time()
  #  for i in range(100):
  #      a.InputCommand('Send Set {:s} {:s} isSendMessage-0'.format('ggg'+str(i),(i+1)))
   # ikunmessage = ''
   # for i in range(100):
   #     ikunmessage = ikunmessage + ikun[random.randint(0,len(ikun)-1)]
   #     a.InputCommand('Send Set {:s} {:s} isSendMessage-0'.format('ggg'+str(i),ikunmessage))
   #     time.sleep(0.1)
   #     print(a.InputCommand('Send Get {:s} isListen=1'.format('ggg'+str(i))))
 #   endtime = time.time()
 #   print(endtime-starttime)
    ip = socket.gethostname()
  #  ip = '192.168.1.132'
    port = 12348
    path = r'C:\Users\qwe\Desktop\Internet\test.png'
    destnation = r'C:\Users\qwe\Desktop'
    a = ComputerManager()
    a.GetConnect((ip,port))
##    for i in range(1):
##        filename,filedata = a.GetFile(**{'pathName':path})
##        with open(r'C:\Users\Administrator\Desktop\{:s}.pptx'.format(str(i)),'wb') as f:
##          f.write(filedata)
##          f.close()
    a.SendFileTo(**{'filePath':path,'destnation':destnation})
    input()
