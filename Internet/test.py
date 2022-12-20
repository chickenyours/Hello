import wx
import time
import threading
class Frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,title='hhh',size=(800,600))
        font = wx.Font(10,wx.ROMAN,wx.ITALIC,wx.NORMAL)
        self.pos=[0,100]
        self.panel = wx.Panel(self,pos=self.pos,size=(1000,1000))
      
        
        lb1 = wx.StaticText(self.panel,-1,style=wx.ALIGN_CENTER)
        lb1.SetFont(font)
        txt = 'hello world\nhhh'
        lb1.SetLabel(txt)

##        lb2 = wx.StaticText(self,-1,style=wx.ALIGN_CENTER)
##        lb2.SetFont(font)
##        txt = 'wxpython'
##        lb2.SetLabel(txt)

        self.text1 = wx.TextCtrl(self.panel,-1,pos=(100,100),size=(100,100))
        self.b1 = wx.Button(self.panel,-1,label='hh',pos=(300,200))
        self.b1.Bind(wx.EVT_BUTTON,self.B1_OnClick)
    def B1_OnClick(self,evt):
##        f = wx.Frame(self,size=(500,300))
##        p = wx.Panel(f)
##        l = wx.StaticText(p,label='You press a button',pos=(100,20))
##        f.Show()
        def hh():
            x = 300
            y = 300
            v_x = 1
            v_y = 1
            while True:
                time.sleep(0.011)   
                if  self.pos[0] + v_x >= x or  self.pos[0] + v_x <= 0:
                    v_x = -v_x
                if  self.pos[1] + v_x >= x or  self.pos[1] + v_x <= 0:
                    v_y = -v_y
                self.pos[0] += v_x
                self.pos[1] += v_y
                
                self.SetPosition(self.pos)
                evt.Skip()
        t = threading.Thread(target=hh)
        t.start()  
        print('You press a button')
if __name__ == '__main__':
    app = wx.App()
    a = Frame()
    a.Show()
    app.MainLoop()
