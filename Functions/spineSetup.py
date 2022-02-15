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

class SpineSetup(object):
    def __init__(self):
        """
        partDict.spinePlaceLocs 
        """
        
        #- this might be combined into partDict
        self.locatorSetup = locatorSetup.LocatorSetup()
        self.util         = util.Util()
        self.spineElement = partDict.spineElement
    
    def createLocator(self):
        """
        create locators
        """
        self.spineParts   = self.locatorSetup.createLocator(partDict.spinePlaceLocs)
    
    def confirmJoints(self):
        """
        confirm joints
        """
        cmds.select(cl = True)
        print 'Spine Parts : ' , self.spineParts
        self.spinePosList = []
        for elem in self.spineElement :
            jointPos = cmds.xform(elem + '_adjust_ctl', t = True, q = True, ws = True)
            cmds.joint(n = '%s_jnt' %elem, p = jointPos)
            self.spinePosList.append(jointPos)

        #- delete position locators
        cmds.delete(self.spineParts)        

    def fkSpineSetup(self):
        """
        fk Spine setup
        """
        #- Spine ctls
        for i in range(len(self.spineElement)):
            controller.circleController(self.spineElement[i] + '_ctl', 'zx', 4, color = 14, lockAttr = ['sc', 'vi'])
            #cmds.move(self.spinePosList[i][0], self.spinePosList[i][1], self.spinePosList[i][2])                     
            cmds.select(self.spineElement[i] + '_jnt', r = True)
            cmds.select('%s_ctl_grp' %self.spineElement[i], tgl = True)
            pConstraint = cmds.pointConstraint(offset = [0, 0, 0], weight = 1)
            cmds.delete(pConstraint)
        for i in range(len(self.spineElement)-1):
            cmds.select('%s_ctl_grp' %self.spineElement[i+1], r = True)
            cmds.select('%s_ctl' %self.spineElement[i], tgl = True)
            cmds.parent()
        for elem in self.spineElement:
            cmds.select('%s_ctl' %elem, r = True)
            cmds.select('%s_jnt' %elem, tgl = True)
            cmds.pointConstraint(mo = False, weight = 1)
            cmds.orientConstraint(mo = False, weight = 1)
            
    def spineCleanup(self):
        """
        cleaning up hierarchy
        """
        
        self.util.group(['spine1_jnt'], 'spine_jnt_grp')
        