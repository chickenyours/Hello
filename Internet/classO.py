import socket
from threading import Thread

class AppManager():
    idValue =1
    value = 0
    returnValue = 3
    retutnId = 4
    def __init__(self) -> None:
        self.num_int = '//i'
        self.num_float = '//f'
        self.num_bool = '//b'
        self.string = '//s'
        self.command = '//c'
        self.id = '//d'
        self.q = '//q'
        self.pool = dict()
        self.threadPool = []
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        self.ip = socket.gethostname()
        self.port = None

        self.conn = None
        self.addr = None
        
    def Get(self,*args,**kwargs):
        '''
        key,defult = 0
        '''
        conn = kwargs.get('connSocket')
        try :
            key = args[0]
            defult = kwargs.get('defult',0)
        except:
            assert False , "参数过少或不对"
        if defult == 0 or defult == '0':
            return self.pool.get(key,None)
        elif defult == 1 or defult == '1':
            return id(self.pool.get(key,None))
    def Set(self,*args,**kwargs):
        '''
        key,value
        '''
        try :
            
            key = args[0]
            value = args[1]
        except:
            assert False , "参数过少或不对"
        isKeyInDict = False
        if key in self.pool:
            isKeyInDict = True
        self.pool[key] = value
        
        return isKeyInDict
    def Format(self,*args,**kwargs):
        '''
        args
        '''
        messageArgs = []
        messageKwargs = {}
        try:
            for i in args:
                
                    if isinstance(i,str):
                        messageArgs.append(i + self.string) 
                    elif isinstance(i,int):
                        messageArgs.append(str(i) + self.num_int)  
                    elif isinstance(i,float):
                        messageArgs.append(str(i) + self.num_float)  
                    elif isinstance(i,bool):
                        messageArgs.append( str(i) + self.num_bool)  
                    else:
                        messageArgs.append(i + self.string)  
            for key,value in kwargs :
                messageArgs.append('='.join(key,self.Format(value)))
        except:
           assert False,"值输入出现问题"
        return messageArgs,messageKwargs
    def InFormat(self,*args,**kwargs):
        '''
        去格式化数据：
        args 如：[hh//s,1//i,k=1//f] -> (['hh',1],{'k':1})

        '''        
        messageArgs = []
        messagekwargs = {}
        for i in args:
            try:
                tp = i[-3:]
                if '=' in i and i.count('=') < 2:
                    key,value = i.split('=')
                    value = self.InFormat(*(value,))[0][0]
                    messagekwargs[key] = value
                elif tp == self.num_int:
                   messageArgs.append(int(i[:-3])) 
                elif tp == self.num_float:
                    messageArgs.append(float(i[:-3]))
                elif tp == self.string:
                    messageArgs.append(i[:-3])
                elif tp == self.num_bool:
                    messageArgs.append(bool(i[:-3]))
                else:
                    messageArgs.append(i)
            except:
                print(value)
        #print(messageArgs)
        return messageArgs,messagekwargs
    def SetTCPService(self,hostAndPort,listen=1):
        try:
            self.s.bind(hostAndPort)
            self.s.listen(listen)
            self.ip = hostAndPort[0]
            self.port = hostAndPort[1]
            print(str(self.ip)+'(Service)','绑定端口：'+str(self.port))
            return None
        except:
            assert False,"地址输入错误"
    def GetConnect(self,hostandport):
        try:
            print('链接中')
            self.s.connect(hostandport)
            conn = self.s
            print('服务器链接成功')
            return None
        except:
            assert False,"地址输入错误或者没有链接对象"
    def TCPLaunchConnect(self):
        try:
            print(str(self.ip)+'(Service)','：'+str(self.port)+'：\n发起链接')
            while True:
                conn,addr = self.s.accept()
                print('接受到'+ str(self.addr)+'的链接,等待客户端请求')
                #使用多线程执行 TCPBehaviTCPour
                try:
                    tr = Thread(target=self.TCPBehaviTCPour,kwargs={'connSocket':conn})
                    self.threadPool.append(tr)
                    tr.start()
                except:
                    print('函数无法运行或不存在')
                    assert 'error'
            return None
        except:
            assert False ,"套接字出错"
    def TCPBehaviTCPour(self,*args,**kwargs):
        'conn'
        conn = kwargs.get('connSocket')
        while True:
            self.UnderStandMessage(*(self.GetMessage(**{'connSocket':conn}),),**{'connSocket':conn})
            
    def InputCommand(self,message=''):  
        '''
        isListen=0:当isListen为1时则接受请求
        '''
        conn = self.s
        try :
            if message == '':
                message =  input('>>>')
            MessageList =  message.split(' ')

            commandArgs,commandkwargs = self.InFormat(*MessageList)
            commandkwargs['connSocket'] = conn
            isListen = commandkwargs.get('isListen',0)

            f = getattr(self,commandArgs[0])
            data = f(*commandArgs[1:],**commandkwargs)
            if isListen == 1 or isListen == '1':
                data = self.GetMessage(**{'connSocket':conn},)
                return self.InFormat(*(data,))[0][0] 
            return data
        except :
            assert False
            print("无此命令")
        return None
    def GetMessage(self,*args,**kwargs):
        '''
        接受链接对象返回的二进制数据
        kwargs: conn=connSocket,isDecode=True:当值为False表示返回二进制数据，否则进行解码
        '''
        conn = kwargs.get('connSocket',self.s)
        length = int(kwargs.get('length',1024))
        isDecode = kwargs.get('isDecode',True)
        return conn.recv(length).decode() if isDecode else conn.recv(length)
       
            
    def TCPClose(self,*args,**kwargs):
        conn = kwargs.get('connSocket')
        self.conn.send(('\n'+str(self.ip)+':'+str(self.port)+'(serivous):\n关闭链接').encode())
        self.conn.close()
        self.conn = None
        print(str(self.addr)+'：断开链接')
        return '//closed//'
    def Send(self,*args,**kwargs):
        '''
        isSendCommand(1 or 0),message();conn = connSocket
        向远程计算机传递信息
        '''
        
        try :
            messageList = self.Format(*args)[0]
            isSendCommand = kwargs.get('isSendCommand',1)
            conn = kwargs.get('connSocket')
            if conn == None:
                assert False,'没有conn链接对象'
            if isSendCommand == 1:
                message = ' '.join(messageList) + '//c'
            else:
                message = ' '.join(messageList)
            message = message.replace('-','=')
            conn.send(message.encode())
            
            return None
        except:
            assert False
            print("Send:找不到链接(conn)对象或参数输入错误")
            return None
    def SendByte(self,*args,**kwargs):
            '''
            args:message;kwargs:conn = connSocket
            向链接对象传递单一的二进制数据
            '''
            byteMessage = args[0]
            conn = kwargs.get('connSocket')
            if conn == None:
                assert False,'没有conn链接对象'
            conn.send(byteMessage)
    def GetInformation(self,*args):
        '''
        使用Get函数返回一个未解码的字符
        '''
        key = args[0]
        defult = 0
        if len(args) >= 2:
            defult = args[1]
        if defult == 0:
            self.Send((self.SendCommand(('Get',key,AppManager.returnValue)),))
        elif defult == 1:
            self.Send((self.SendCommand(('Get',key,AppManager.retutnId)) ,))
        return None   
        
    def UnderStandMessage(self,*args,**kwargs):
        '''
        conn,message,isSendCommand=1:当值设定不为1时，则不向连接对象发送消息
        接收者理解句子的意思并执行
        '''
        message = args[0]
        conn = kwargs.get('connSocket')
        tp = message[-3:]
        #接到命令信息，执行相应方法
        if tp == self.command:
            try:
                messageList = message[:-3].split(' ')
                commandArgs,commandKwargs = self.InFormat(*messageList)
                commandKwargs['connSocket'] = conn
                isSendMessage = commandKwargs.get('isSendMessage',1)
                f = getattr(self,commandArgs[0])
                data = f(*commandArgs[1:],**commandKwargs)
                if isSendMessage == 1:
                    self.Send(*(data,),**{'connSocket':conn,'isSendCommand':0})
                return data
            except:
                assert False
                conn.send(('\n'+str(self.ip)+':'+str(self.port)+"(serivous):函数运算错误或者函数不存在").encode())
                return 0
        else:
            conn.send(('\n'+str(self.ip)+':'+str(self.port)+'(serivous):\n接受到信息').encode())
            messageList = message[:-3].split(' ')
            Text = []
            print(str(self.addr)+'：\n')
            for i in messageList:
                Text.append(self.InFormat(i))
            for i in Text:
                print(i)
