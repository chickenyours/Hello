
#文件操作建议使用二进制编码形式
from classO import *
import os
import struct
import time

class ComputerManager(AppManager):
    def __init__(self) -> None:
        super().__init__()
    def FileOpen(self,*args,**kwargs):
        '''
        用来打开文件，返回文件对象，如果文件不存在，则报错，如果参数new为Yes，则生成一个新的文件对象，名称为绝对路径的最后一项
        path=文件绝对路径,defult=文件打开处理操作
        '''
        path = kwargs.get('path',None)
        defult = kwargs.get('defult','r')
        pass
    def GetPath(self,*args,**kwargs):
        '''
        获取目录下的所有路径
        '''
        pass
    def WriteFlie(self,*args,**kwargs):
        '''
        将数据写入文件当中
        '''
    def GetFile(self,*args,**kwargs):
        '''
        请求服务器发送文件
        connSocket=conn,pathName=服务器计算机中的文件的绝对路径
        return 文件名，文件数据
        '''
        try:
            conn = kwargs.get('connSocket',self.s)
            #读取文件，生存头文件字节信息
            path = kwargs.get('pathName',None)
            
            fheadLength = 128
            #fhead = struct.pack('{:s}sl'.format(str(fheadLength)),fileName.encode('utf-8'),os.stat(path).st_size)
            #发送处理文件的请求（计算机执行SendFile命令，接受函数等待接受函数传递的文件地址
            self.InputCommand('Send SendFile fheadLength-{:s} isSendMessage-0 filePath-{:s}'.format(str(fheadLength),path))

            #出差
            fhead = self.GetMessage(**{'connSocket':conn,'length':kwargs.get('fheadLength','1024'),'isDecode':False}) 
            fileName,fileSize = struct.unpack('128sl',fhead)
            fileName = fileName.decode().strip('\x00')
            if fhead:
                print('接受到头文件:{:s},大小:{:s}'.format(fileName,str(fileSize)+'B'))
                self.Send(*['OK'],**{'isSendCommand':0,'connSocket':conn})
            receive = 0
            data = bytes()
            while receive < fileSize:
                singleData = self.GetMessage(**{'connSocket':conn,'length':kwargs.get('fheadLength',1024 * 100),'isDecode':False})
                receive += len(singleData)
                data += singleData
            self.Send(*['OK'],**{'isSendCommand':0,'connSocket':conn})
            print('成功接收到文件')
            return fileName,data
               # self.SendByte(*[fhead],**{'connSocket':conn})
            #等待接受远程计算机发来的头文件信息
            #接受计算机发来的文件数据
        except:
            assert False
            return '系统找不到文件'
    def SendFileTo(self,*args,**kwargs):
        '''
        向链接对象主动传输文件
        filePath=本地有效文件路径，
        '''
        try:
            conn = kwargs.get('connSocket',self.s)
            #获取文件信息并打包
            fheadLength = 128
            filePath = kwargs.get('filePath',None)
            destnation = kwargs.get('destnation',None)
            fileName = os.path.basename(filePath)
            fileSize = os.stat(filePath).st_size
            fhead = struct.pack('128sl',fileName.encode('utf-8'),fileSize)
            #链接对象文件地址
            self.InputCommand('Send ToGetFile  fheadLength-{:s} isSendMessage-0 filePath-{:s}'.format(str(fheadLength),destnation))
            #判断对方的请求状况
            flag = self.GetMessage(**{'connSocket':conn,'length':kwargs.get('fheadLength','1024'),'isDecode':True})
            if flag  == 'OK//s' :
                self.SendByte(*[fhead],**{'connSocket':conn})
            elif flag == 'NO//s':
                print('地址不存在')
                return None
            else:
                print('处理错误')
                return None
            if self.GetMessage(**{'connSocket':conn,'length':kwargs.get('fheadLength','1024'),'isDecode':True}) == 'OK//s' :
                print('传输中。。。')
                with open(filePath,'rb')  as f:
                    singleData = 1024 * 100
                    for i in range(fileSize // singleData):
                        self.SendByte(*[f.read(singleData)],**{'connSocket':conn})
                    self.SendByte(*[f.read(fileSize % singleData)],**{'connSocket':conn})
                    if self.GetMessage(**{'connSocket':conn,'length':kwargs.get('fheadLength','1024'),'isDecode':True}) == 'OK//s' :
                        print('连接对象接受到文件，文件传输成功')
                        return True
            else:
                print('链接对象拒绝文件的发送')
                return False
        except:
            assert False
    def ToGetFile(self,*args,**kwargs):
        '''
        接受文件的信息
        '''
        conn = kwargs.get('connSocket',self.s)
        Path = kwargs.get('filePath',None)
        if os.path.exists(Path):
            self.Send(*['OK'],**{'isSendCommand':0,'connSocket':conn})
        else:
            self.Send(*['NO'],**{'isSendCommand':0,'connSocket':conn})
            print('无效的路径')
            return None
        fhead = self.GetMessage(**{'connSocket':conn,'length':kwargs.get('fheadLength','1024'),'isDecode':False}) 
        fileName,fileSize = struct.unpack('128sl',fhead)
        filePath = os.path.join(Path,fileName)
        receive = 0
        with open(filePath,'wb') as f:
            while receive < fileSize:
                singleData = self.GetMessage(**{'connSocket':conn,'length':kwargs.get('fheadLength',1024 * 100),'isDecode':False})
                receive += len(singleData)
                f.write(singleData)
            self.Send(*['OK'],**{'isSendCommand':0,'connSocket':conn})
        print('成功接收到文件')

    def SendFile(self,*args,**kwargs):
        '''
        发送文件,执行函数后会等待接受头文件名
        connSocket=conn,fheadLength=接受到头文件的大小
        '''
        fileinfo_size = struct.calcsize('128sl')

        try:
            filePath = kwargs.get('filePath',None)
            conn = kwargs.get('connSocket',None)
            #出错
            #self.Send(*['OK'],**{'isSendCommand':0,'connSocket':conn})
            #path = self.GetMessage(**{'connSocket':conn,'length':kwargs.get('fheadLength','1024'),'isDecode':False})
            if filePath:
                fileName = os.path.basename(filePath)
                fileSize = os.stat(filePath).st_size
                fhead = struct.pack('128sl',fileName.encode('utf-8'),fileSize)
                self.SendByte(*[fhead],**{'connSocket':conn})
                if self.GetMessage(**{'connSocket':conn,'length':kwargs.get('fheadLength','1024'),'isDecode':True}) == 'OK//s' :
                    print('传输中。。。')
                    with open(filePath,'rb')  as f:
                        singleData = 1024 * 100
                        for i in range(fileSize // singleData):
                            self.SendByte(*[f.read(singleData)],**{'connSocket':conn})
                        self.SendByte(*[f.read(fileSize % singleData)],**{'connSocket':conn})
                else:
                    pass
                if self.GetMessage(**{'connSocket':conn,'length':kwargs.get('fheadLength','1024'),'isDecode':True}) == 'OK//s' :
                    print('连接对象接受到文件，文件传输成功')
                    return True
                else:
                    pass
                #filename,filesize = struct.unpack('136sl',fhead)
                #fn = filename.strip(b'\x00')
                #fn = filename.decode()
                #print(fn)

            return None
            
            
        except:
            assert False
            return False
        
if __name__ == '__main__':
    a = ComputerManager()
    print(a.SendFileTo(**{'pathName':r'E:\Python\project\Internet\test.png'}))
