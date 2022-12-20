import wx
import time
import threading 
class Myframe(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,size=(500,500))

        self.p = wx.Panel(self)
        
        self.im = wx.Image(r'test.png',wx.BITMAP_TYPE_ANY)
        self.per = 0.01
        self.bit = self.im.Scale(self.im.GetWidth() * self.per,self.im.GetHeight() * self.per ).ConvertToBitmap()
        
        self.i = wx.StaticBitmap(self.p,bitmap=self.bit)

        self.bt = wx.Button(self.p,pos=(400,400),label='hh')
        self.bt.Bind(wx.EVT_BUTTON,self.hh)
    def hh(self,evt):
        def jj():
            while self.per < 2 :
                time.sleep(0.01)
                self.i.SetBitmap(self.im.Scale(self.im.GetWidth() * self.per,self.im.GetHeight() * self.per ).ConvertToBitmap())
                self.per += 0.005
        a = threading.Thread(target=jj())
        a.start()


a=wx.App()
f = Myframe()
f.Show()
a.MainLoop()
