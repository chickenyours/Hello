import wx
# 主窗口类
class MainFrame(wx.Frame):
  def __init__(self, p, t):
    """ p: 父亲窗口
    t:  窗口标题
    """       
    wx.Frame.__init__(self, id=wx.NewId(), parent=p, title=t, size=
         (420, 320))
    # 该panel的父亲就是该窗口， id=-1就表示任意id
    panel_top = wx.Panel(self, -1, size=(420, 110), pos=(0, 0))
    panel_top.SetBackgroundColour("#DB7093")                # 红色
    panel_left_down = wx.Panel(self, -1, size=(210, 210), pos=(0, 116))
    panel_left_down.SetBackgroundColour("#007FFF")       # 蓝色
    panel_right_down = wx.Panel(self, -1, size=(210, 210), pos=(220, 116))
    panel_right_down.SetBackgroundColour("#00FF7F")     # 绿色
if __name__ == "__main__":                # 如果运行该脚本
    # 创建应用程序
    app = wx.App(False)
    # Frame就是应用程序的主窗口，不是子窗口
    frame = MainFrame(None, "计算器-演示版")
    frame.Show(True)                     # 显示主窗口
    app.MainLoop()
