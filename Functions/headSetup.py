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

class HeadSetup(object):
    def __init__(self):
        """
        partDict.headPlaceLocs 
        """
        
        #- this might be combined into partDict
        self.locatorSetup = locatorSetup.LocatorSetup()
        self.util         = util.Util()
        self.headElement = partDict.headElement

    def createLocator(self):
        """
        create locators
        """
        self.headParts   = self.locatorSetup.createLocator(partDict.headPlaceLocs)

    def confirmJoints(self):
        """
        confirm joints
        """
        cmds.select(cl = True)
        print 'Head Parts : ' , self.headParts
        self.headPosList = []
        for elem in self.headElement :
            jointPos = cmds.xform(elem + '_adjust_ctl', t = True, q = True, ws = True)
            cmds.joint(n = '%s_jnt' %elem, p = jointPos)
            self.headPosList.append(jointPos)

        #- delete position locators
        cmds.delete(self.headParts)       
    

    def fkHeadSetup(self):
        """
        fk head setup
        """
        #- head ctls
        self.headElement = self.headElement[0:-1]
        for i in range(len(self.headElement)):
            controller.circleController(self.headElement[i] + '_ctl', 'zx', 3, color = 14, lockAttr = ['sc', 'vi'])
            cmds.select(self.headElement[i] + '_jnt', r = True)
            cmds.select('%s_ctl_grp' %self.headElement[i], tgl = True)
            pConstraint = cmds.pointConstraint(offset = [0, 0, 0], weight = 1)
            cmds.delete(pConstraint)
        for i in range(len(self.headElement)-1):
            cmds.select('%s_ctl_grp' %self.headElement[i+1], r = True)
            cmds.select('%s_ctl' %self.headElement[i], tgl = True)
            cmds.parent()
        for elem in self.headElement:
            cmds.select('%s_ctl' %elem, r = True)
            cmds.select('%s_jnt' %elem, tgl = True)
            cmds.pointConstraint(mo = False, weight = 1)
            cmds.orientConstraint(mo = False, weight = 1)
        
    def headCleanup(self):
        """
        cleaning up hierarch
        """
        
        self.util.group('neckbase_jnt', 'neckbase_jnt_grp')