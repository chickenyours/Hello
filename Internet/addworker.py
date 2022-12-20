import classO

class addworker(classO.AppManager):
    def __init__(self) -> None:
        super().__init__()
    def Add(self,*args,**kwargs):
        '''
        a,b
        '''
        a = args[0]
        b = args[1]
        try:
            return a+b
        except:
            return '输入错误'