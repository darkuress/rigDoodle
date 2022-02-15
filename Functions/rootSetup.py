import locatorSetup
import controller
import poleVector
import partDict
import util

reload(locatorSetup)
reload(partDict)
reload(controller)
reload(util)
reload(poleVector)

import maya.cmds as cmds

class RootSetup(object):
    def __init__(self):
        """
        partDict.rootPlaceLocs 
        """
        
        #- this might be combined into partDict
        self.locatorSetup = locatorSetup.LocatorSetup()
        self.util         = util.Util()
        self.rootElement = partDict.rootElement

    def createLocator(self):
        """
        create locators
        """
        self.rootParts   = self.locatorSetup.createLocator(partDict.rootPlaceLocs)

    def confirmJoints(self):
        """
        confirm joints
        """
        cmds.select(cl = True)
        print 'Root Parts : ' , self.rootParts
        self.rootPosList = []
        for elem in self.rootElement :
            jointPos = cmds.xform(elem + '_adjust_ctl', t = True, q = True, ws = True)
            cmds.joint(n = '%s_jnt' %elem, p = jointPos)
            self.rootPosList.append(jointPos)

        #- delete position locators
        cmds.delete(self.rootParts)       
    

    def rootSetup(self):
        """
        fk root setup
        """
        #- root ctls
        for i in range(len(self.rootElement)):
            if i == 0:
                controller.circleController(self.rootElement[i] + '_ctl', 'zx', 6, color = 18, lockAttr = ['sc', 'vi'])
            else:
                controller.circleController(self.rootElement[i] + '_ctl', 'zx', 5, color = 16, lockAttr = ['sc', 'vi'])
            cmds.select(self.rootElement[i] + '_jnt', r = True)
            cmds.select('%s_ctl_grp' %self.rootElement[i], tgl = True)
            pConstraint = cmds.pointConstraint(mo = False, weight = 1)
            cmds.delete(pConstraint)
        for i in range(len(self.rootElement)-1):
            cmds.select('%s_ctl_grp' %self.rootElement[i+1], r = True)
            cmds.select('%s_ctl' %self.rootElement[i], tgl = True)
            cmds.parent()
        for elem in self.rootElement:
            cmds.select('%s_ctl' %elem, r = True)
            cmds.select('%s_jnt' %elem, tgl = True)
            cmds.pointConstraint(mo = False, weight = 1)
            cmds.orientConstraint(mo = False, weight = 1)
        
    def rootCleanup(self):
        """
        cleaning up hierarch
        """
        
        self.util.group('root_jnt', 'root_jnt_grp')
        
    def deleteAllCtl(self):
        """
        """
        cmds.delete('all_ctl')