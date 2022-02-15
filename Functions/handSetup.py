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

class HandSetup(object):
    def __init__(self, isThumb = True, numFingers = 4):
        """
        partDict.handPlaceLocs 
        """
        
        #- this might be combined into partDict
        self.locatorSetup   = locatorSetup.LocatorSetup()
        self.util           = util.Util()
        self.handElement    = partDict.handElement
        self.isThumb        = isThumb
        self.numFingers     = numFingers
        
        self.left         = partDict.lrPrefix[0]
        self.lrPrefix     = partDict.lrPrefix
        
        self.util = util.Util()
    
        if self.isThumb:
            self.thumbElement   = partDict.thumbElement
        if self.numFingers >= 1:
            self.indexElement   = partDict.indexElement
        if self.numFingers >= 2:
            self.middleElement = partDict.middleElement
        if self.numFingers >= 3:
            self.ringElement    = partDict.ringElement
        if self.numFingers == 4:
            self.pinkyElement   = partDict.pinkyElement
        
    def createLocator(self):
        """
        create locators
        """
        self.handParts   = self.locatorSetup.createLocator(partDict.handPlaceLocs)
        if self.isThumb:
            self.thumbParts   = self.locatorSetup.createLocator(partDict.thumbPlaceLocs)
        if self.numFingers >= 1:
            self.indexParts   = self.locatorSetup.createLocator(partDict.indexPlaceLocs)
        if self.numFingers >= 2:
            self.middleParts   = self.locatorSetup.createLocator(partDict.middlePlaceLocs)
        if self.numFingers >= 3:
            self.ringParts   = self.locatorSetup.createLocator(partDict.ringPlaceLocs)
        if self.numFingers == 4:
            self.pinkyParts   = self.locatorSetup.createLocator(partDict.pinkyPlaceLocs)
        
    def confirmJoints(self):
        """
        confirm joints
        """
        cmds.select(cl = True)
        print 'hand Parts : ' , self.handParts
        self.handPosList = []
        self.thumbPosList = []
        self.indexPosList = []
        self.middlePosList = []
        self.ringPosList = []
        self.pinkyPosList = []
        self.fingerBase = []
        self.allfingers = []
        
        for elem in self.handElement :
            jointPos = cmds.xform(self.left + elem + '_adjust_ctl', t = True, q = True, ws = True)
            cmds.joint(n = '%s%s_jnt' %(self.left, elem), p = jointPos)
            self.handPosList = jointPos
        #- delete position locators
        cmds.delete(self.handParts)   
        cmds.select(cl = True)
            
        if self.isThumb:
            for elem in self.thumbElement :
                jointPos = cmds.xform(self.left + elem + '_adjust_ctl', t = True, q = True, ws = True)
                cmds.joint(n = '%s%s_jnt' %(self.left, elem), p = jointPos)
                self.thumbPosList.append(jointPos)
            cmds.delete(self.thumbParts)
            cmds.select(cl = True)
            self.fingerBase.append('%sthumb1_jnt' %self.left)
            cmds.joint('%sthumb1_jnt' %self.left, e = True, oj = 'xzy', secondaryAxisOrient = 'yup', ch = True, zso = True)
            self.allfingers.append(self.thumbElement)
        
        if self.numFingers >= 1:
            for elem in self.indexElement :
                jointPos = cmds.xform(self.left + elem + '_adjust_ctl', t = True, q = True, ws = True)
                cmds.joint(n = '%s%s_jnt' %(self.left, elem), p = jointPos)
                self.indexPosList.append(jointPos)
            cmds.delete(self.indexParts)
            cmds.select(cl = True)
            self.fingerBase.append('%sindex1_jnt' %self.left)
            cmds.joint('%sindex1_jnt' %self.left, e = True, oj = 'xzy', secondaryAxisOrient = 'yup', ch = True, zso = True)
            self.allfingers.append(self.indexElement)
            
        if self.numFingers >= 2:
            for elem in self.middleElement :
                jointPos = cmds.xform(self.left + elem + '_adjust_ctl', t = True, q = True, ws = True)
                cmds.joint(n = '%s%s_jnt' %(self.left, elem), p = jointPos)
                self.middlePosList.append(jointPos)
            cmds.delete(self.middleParts)
            cmds.select(cl = True)
            self.fingerBase.append('%smiddle1_jnt' %self.left)
            cmds.joint('%smiddle1_jnt' %self.left, e = True, oj = 'xzy', secondaryAxisOrient = 'yup', ch = True, zso = True)
            self.allfingers.append(self.middleElement)
            
        if self.numFingers >= 3:
            for elem in self.ringElement :
                jointPos = cmds.xform(self.left + elem + '_adjust_ctl', t = True, q = True, ws = True)
                cmds.joint(n = '%s%s_jnt' %(self.left, elem), p = jointPos)
                self.ringPosList.append(jointPos)
            cmds.delete(self.ringParts)
            cmds.select(cl = True)
            self.fingerBase.append('%sring1_jnt' %self.left)
            cmds.joint('%sring1_jnt' %self.left, e = True, oj = 'xzy', secondaryAxisOrient = 'yup', ch = True, zso = True)
            self.allfingers.append(self.ringElement)
            
        if self.numFingers == 4:
            for elem in self.pinkyElement :
                jointPos = cmds.xform(self.left + elem + '_adjust_ctl', t = True, q = True, ws = True)
                cmds.joint(n = '%s%s_jnt' %(self.left, elem), p = jointPos)
                self.pinkyPosList.append(jointPos)
            cmds.delete(self.pinkyParts)
            cmds.select(cl = True)
            self.fingerBase.append('%spinky1_jnt' %self.left)
            cmds.joint('%spinky1_jnt' %self.left, e = True, oj = 'xzy', secondaryAxisOrient = 'yup', ch = True, zso = True)
            self.allfingers.append(self.pinkyElement)
            
        self.util.parent(self.fingerBase, self.left + 'palm_jnt')
        
        
    def mirrorJoints(self):
        """
        mirroring joints
        """
        
        self.util.mirrorJoints(self.left + partDict.handElement[0] + '_jnt')
        

    def fkFingerSetup(self):
        """
        #- fk finger setup
        """
        
        cmds.select(cl = True)
        for fingerElement in self.allfingers:
            for lr in self.lrPrefix:
                for elem in fingerElement[0:-1]:
                    if lr == self.left:
                            ctlColor = 6
                    else:
                            ctlColor = 12
                    ctl = controller.circleController('%s%s_ctl' %(lr, elem), 'yz', 0.5, ctlColor, ['tr', 'sc', 'vi'], doublePadding = True)
                    cmds.select('%s%s_jnt' %(lr, elem), r = True)
                    cmds.select('%s_grp' %ctl, tgl = True)
                    cmds.pointConstraint(mo = False, weight = 1)
                    cmds.orientConstraint(mo = False, weight = 1)
                    cmds.delete('%s_grp_pointConstraint1' %ctl)
                    cmds.delete('%s_grp_orientConstraint1' %ctl)            
            
                    #- constrain joints
                    cmds.select(ctl, r = True)
                    cmds.select('%s%s_jnt' %(lr, elem), tgl = True)
                    cmds.orientConstraint(mo = False, weight = 1)
                
                fingerElementTmp = fingerElement[:-1]
                fingerElementTmp.reverse()
                for i in range(len(fingerElementTmp)-1):
                    self.util.parent('%s%s_ctl_grp' %(lr, fingerElementTmp[i]), '%s%s_ctl' %(lr, fingerElementTmp[i+1]))

    def fingerCtlSetup(self):
        """
        finger all ctl setup
        """
        for lr in self.lrPrefix:
            if lr == self.left:
                    ctlColor = 6
            else:
                    ctlColor = 12
            controller.lollipopController('%spalmFinger_ctl' %lr, color = ctlColor)            
            cmds.select('%spalmFinger_ctl_grp' %lr, r = True)
            cmds.scale(0.5,0.5,0.5)
            if lr == self.left:
                    cmds.move(self.handPosList[0], self.handPosList[1], self.handPosList[2])
            else:   
                    cmds.move(-self.handPosList[0], self.handPosList[1], self.handPosList[2])

    def palmFingerCtlSetup(self):
        """
        palm lollipop control setup
        """
        allFingerName = ['index', 'middle', 'ring', 'pinky']
        if self.numFingers == 3:
            fingerName = allFingerName[:2]    
        elif self.numFingers == 2:
            fingerName = allFingerName[:1]
        elif self.numFingers == 1:
            fingerName = [allFingerName[0]]
        
        attrFingerName = []
        fingerAttr = ['Base', 'Mid', 'Tip', 'Spread', 'Twist']
        for finger in allFingerName:
                attrFingerName.append('%sOOOOOOOOO' %finger)
                
        #- Thumb
        for lr in self.lrPrefix:
            if self.isThumb == True:
                thumbAttr = ['Base', 'Mid', 'Tip', 'Spread', 'Twist']
                cmds.addAttr('%spalmFinger_ctl' %lr, ln = 'ThumbOOOOOOOOO', at = 'double')
                cmds.setAttr('%spalmFinger_ctl.ThumbOOOOOOOOO' %lr, e = True, keyable = False, channelBox = True)
        
                for attr in thumbAttr:
                        cmds.addAttr('%spalmFinger_ctl' %lr, ln = 'T%s' %attr, at = 'double')
                        cmds.setAttr('%spalmFinger_ctl.T%s' %(lr, attr), e = True, keyable = True)
    
            for finger in attrFingerName:
                cmds.addAttr('%spalmFinger_ctl' %lr, ln = '%s' %finger, at = 'double')
                cmds.setAttr('%spalmFinger_ctl.%s' %(lr, finger), e = True, keyable = False, channelBox = True)
                for attr in fingerAttr:
                    cmds.addAttr('%spalmFinger_ctl' %lr, ln = '%s%s' %(finger[0], attr), at = 'double')
                    cmds.setAttr('%spalmFinger_ctl.%s%s' %(lr, finger[0], attr), e = True, keyable = True)
            
            if self.isThumb == True and self.numFingers == 4:               
                cmds.addAttr('%spalmFinger_ctl' %lr, ln = 'PalmOOOOOOOOOO', at = 'double')
                cmds.setAttr('%spalmFinger_ctl.PalmOOOOOOOOOO' %lr, e = True, keyable = False, channelBox = True)
                cmds.addAttr('%spalmFinger_ctl' %lr, ln = 'Cup', at = 'double', min = 0, max = 30)
                cmds.setAttr('%spalmFinger_ctl.Cup' %lr, e = True, keyable = True)
            
            #- connect Attributes

            #fingerConnectName = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
            fingerConnectName = allFingerName
            if 'thumb' not in fingerConnectName:
                fingerConnectName.insert(0, 'thumb')
            
            XYZ = ['X', 'Y', 'Z']
            if self.isThumb:
                for connect in [fingerConnectName[0]]:
                    cmds.shadingNode('multiplyDivide',n = '%s%s_connect_0' %(lr, connect), asUtility = True)
                    cmds.shadingNode('multiplyDivide',n = '%s%s_connect_1' %(lr, connect), asUtility = True)
                    for i in range(2):
                        cmds.setAttr('%s%s_connect_%s.input2X' %(lr, connect,str(i)),-1)
                        cmds.setAttr('%s%s_connect_%s.input2Y' %(lr, connect,str(i)), -1)
                        cmds.setAttr('%s%s_connect_%s.input2Z' %(lr, connect,str(i)), -1)
                    if connect =='thumb':
                        for j in range(5):
                            if j<3:
                                cmds.connectAttr('%spalmFinger_ctl.T%s' %(lr, thumbAttr[j]), '%s%s_connect_0.input1%s' %(lr, connect, XYZ[j]), f = True)
                                cmds.connectAttr('%s%s_connect_0.output%s' %(lr, connect, XYZ[j]), '%s%s%s_ctl_ofs.rotateY' %(lr, connect, str(j+1)), f = True)
                            else:
                                cmds.connectAttr('%spalmFinger_ctl.T%s' %(lr, thumbAttr[j]), '%s%s_connect_1.input1%s' %(lr, connect, XYZ[j-2]), f = True)
                                if thumbAttr[j] == 'Spread':
                                    cmds.connectAttr('%s%s_connect_1.output%s' %(lr, connect, XYZ[j-2]), '%s%s1_ctl_ofs.rotateZ' %(lr, connect), f = True)
                                else:
                                    cmds.connectAttr('%s%s_connect_1.output%s' %(lr, connect, XYZ[j-2]), '%s%s1_ctl_ofs.rotateX' %(lr, connect), f = True)
            

            for connect in fingerConnectName[1:]:
                cmds.shadingNode('multiplyDivide',n = '%s%s_connect_0' %(lr, connect), asUtility = True)
                cmds.shadingNode('multiplyDivide',n = '%s%s_connect_1' %(lr, connect), asUtility = True)
                for i in range(2):
                    cmds.setAttr('%s%s_connect_%s.input2X' %(lr, connect,str(i)),-1)
                    cmds.setAttr('%s%s_connect_%s.input2Y' %(lr, connect,str(i)), -1)
                    cmds.setAttr('%s%s_connect_%s.input2Z' %(lr, connect,str(i)), -1)
                for j in range(5):
                    if j<3:
                        cmds.connectAttr('%spalmFinger_ctl.%s%s' %(lr, connect[0] ,fingerAttr[j]), '%s%s_connect_0.input1%s' %(lr, connect, XYZ[j]), f = True)
                        cmds.connectAttr('%s%s_connect_0.output%s' %(lr, connect, XYZ[j]), '%s%s%s_ctl_ofs.rotateY' %(lr, connect, str(j+2)), f = True)
                    else:
                        cmds.connectAttr('%spalmFinger_ctl.%s%s' %(lr, connect[0] ,fingerAttr[j]), '%s%s_connect_1.input1%s' %(lr, connect, XYZ[j-2]), f = True)
                        if fingerAttr[j] == 'Spread':
                            cmds.connectAttr('%s%s_connect_1.output%s' %(lr, connect, XYZ[j-2]), '%s%s2_ctl_ofs.rotateZ' %(lr, connect), f = True)
                        else:
                            cmds.connectAttr('%s%s_connect_1.output%s' %(lr, connect, XYZ[j-2]), '%s%s2_ctl_ofs.rotateX' %(lr, connect), f = True)
            """
            if self.isThumb == True and self.numFingers == 4:
                cmds.shadingNode('multiplyDivide', n = '%sPalmCup_inverse' %lr, asUtility = True)
                cmds.setAttr('%sPalmCup_inverse.input2X' %lr, -1)
                cmds.connectAttr('%spalmFinger_ctl.Cup' %lr, '%sPalmCup_inverse.input1X' %lr)
                cmds.connectAttr('%spalmFinger_ctl.Cup' %lr, '%sThumb0.rotateX' %lr)
                cmds.connectAttr('%sPalmCup_inverse. outputX' %lr, '%sPinky0.rotateZ' %lr)
                #cmds.connectAttr('%sPalmCup_inverse. outputX' %lr, '%sRing0.rotateZ' %lr)
            
            """
    def fingerCleanup(self):
        """
        claening up finger ctl
        """
        self.fingerCtlSetup()
        self.palmFingerCtlSetup()
        
        for lr in self.lrPrefix:
            basefingerCtl = []
            for x in self.allfingers:
                basefingerCtl.append(lr + x[0] + '_ctl_grp')
            self.util.group(basefingerCtl, lr + 'finger_ctl_grp')
            
            cmds.createNode('transform', n = '%spalm_jnt_grp' %lr)
            self.util.match('%spalm_jnt_grp' %lr, '%spalm_jnt' %lr)
            self.util.parent('%spalm_jnt' %lr, '%spalm_jnt_grp' %lr)
            
            self.util.toggleSelect('%spalm_jnt' %lr, '%sfinger_ctl_grp' %lr)
            cmds.parentConstraint(mo = True, weight = 1)
            
            cmds.setAttr('%shandCon_loc_grp.visibility' %lr, 0)
            
            #- parenting palmFinger_ctl
            self.util.parent('%spalmFinger_ctl_grp' %lr, '%sfinger_ctl_grp' %lr)
        
        self.util.group(['l_handCon_loc_grp', 'r_handCon_loc_grp'], 'hand_misc_grp')
        self.util.group(['l_finger_ctl_grp', 'r_finger_ctl_grp'], 'hand_ctl_grp')
        self.util.group(['l_palm_jnt_grp', 'r_palm_jnt_grp'], 'hand_jnt_grp')