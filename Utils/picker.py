#- initialize window
if cmds.window('rigDoodlePicker', ex = True):
    cmds.deleteUI('rigDoodlePicker')    

class UI:
    def __init__(self):
        window = cmds.window('rigDoodlePicker', title="Picker", widthHeight=(200, 120))
        cmds.columnLayout( adjustableColumn=True )
        cmds.button(label='Select All Controllers', command = self.selectAllCtl)
        cmds.button(label='Select Visible Controllers', command = self.selectAllVisibleCtl)
        cmds.rowLayout(nc = 2)
        cmds.button(label='Set key', w = 100, command = self.setKey)
        cmds.button(label='Reset Selected', w = 100, command = self.reset)
        cmds.setParent("..")
        cmds.setParent("..")
        cmds.showWindow( window )

    def selectAllCtl(self, *args):
        allCtl = cmds.ls('*ctl') 
        cmds.select(allCtl, r = True)
    
    def selectAllVisibleCtl(self, *args):
        allVisibleCtl = cmds.ls('*ctl', v = True)
        cmds.select(allVisibleCtl, r = True)
    
    def setKey(self, *args):
        cmds.setKeyframe()
    
    def reset(self, *args):
        tAttrs = ['.tx', '.ty', '.tx']
        rAttrs = ['.rx', '.ry', '.rz']
        sAttrs = ['.sx', '.sy', '.sz']
        
        for x in cmds.ls(sl = True):
            try:
                for attr in tAttrs:
                    cmds.setAttr(x + attr, 0)
            except:
                pass
            try:
                for attr in rAttrs:
                    cmds.setAttr(x + attr, 0)
            except:
                pass
            try:
                for attr in sAttrs:
                    cmds.setAttr(x + attr, 1)
            except:
                pass

x = UI()
               