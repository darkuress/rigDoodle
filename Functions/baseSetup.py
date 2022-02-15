import controller
import partDict
import util

reload(partDict)
reload(controller)
reload(util)

import maya.cmds as cmds

class BaseSetup(object):
    def __init__(self):
        """
        create base of rigs
        """
        self.globalCtl = partDict.globalCtl
        self.localCtl = partDict.localCtl
        
        self.util = util.Util()
    
    def createMainCtl(self):
        """
        creating global and local controller
        """
        controller.circleController(self.globalCtl, 'zx', 10, color = 13, lockAttr = [])
        controller.circleController(self.localCtl, 'zx', 8, color = 14, lockAttr = ['sc'])
        self.util.parent(self.localCtl + '_grp', self.globalCtl)
        
    def createContainers(self):
        """
        creating empty containers or joint, mesh, ctl and misc
        """
        cmds.createNode('transform', n = 'geo')
        cmds.createNode('transform', n = 'joints')
        cmds.createNode('transform', n = 'controller')
        cmds.createNode('transform', n = 'misc')
        
        self.util.parent(['geo', 'joints', 'controller', 'misc'], self.localCtl)
        