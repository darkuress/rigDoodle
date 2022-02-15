import locatorSetup
import controller
import poleVector
import partDict
import util
import math

reload(locatorSetup)
reload(partDict)
reload(controller)
reload(util)
reload(poleVector)

import maya.cmds as cmds

class ArmSetup(object):
    def __init__(self):
        """
        partDict.armPlaceLocs 
        """
        
        #- this might be combined into partDict
        self.left         = partDict.lrPrefix[0]
        self.extraCtl     = 'arm_extra_ctl'
        
        self.locatorSetup = locatorSetup.LocatorSetup()
        self.util         = util.Util()
        self.armElement   = partDict.armElement
        self.lClavicleJnt = self.left + partDict.armElement[0] + '_jnt'
        self.lShoulderJnt = self.left + partDict.armElement[1] + '_jnt'
        self.lWristJnt = self.left + partDict.armElement[3] + '_jnt'
        self.lrPrefix     = partDict.lrPrefix
    
    def createLocator(self):
        """
        create locators
        """
        self.armParts = self.locatorSetup.createLocator(partDict.armPlaceLocs)

    def confirmJoints(self):
        """   
        draw joints in locator position
        """

        #- Getting Ball and Toe Location
        self.leftShoulderPos = cmds.xform('l_shoulder_adjust_ctl', q = True, ws = True, t = True)
        self.leftElbowPos    = cmds.xform('l_elbow_adjust_ctl', q = True, ws = True, t = True)
        self.leftWristPos    = cmds.xform('l_wrist_adjust_ctl', q = True, ws = True, t = True)
                
        cmds.select(cl = True)
        print 'Arm Parts : ' , self.armParts
        for elem in self.armElement :
            jointPos = cmds.xform(self.left + elem + '_adjust_ctl', t = True, q = True, ws = True)
            cmds.joint(n = '%s%s_jnt' %(self.left, elem), p = jointPos)
            
        #- orient joint
        cmds.joint(self.lShoulderJnt, e = True, oj = 'xzy', secondaryAxisOrient = 'yup', ch = True, zso = True)
        
        cmds.setAttr(self.lWristJnt + ".jointOrientX", 0)
        cmds.setAttr(self.lWristJnt + ".jointOrientY", 0)
        cmds.setAttr(self.lWristJnt + ".jointOrientZ", 0)
        
        cmds.delete(self.armParts)
    
    def mirrorJoints(self):
        """
        mirroring joints
        """
        
        self.util.mirrorJoints(self.lClavicleJnt)

    def fkArmSetup(self):
        """
        #- fk arm setup
        """
        
        cmds.select(cl = True)
        for lr in self.lrPrefix:
            cmds.select('%sshoulder_jnt' %lr, r = True)
            cmds.duplicate(rr = True, n = '%sfk_shoulder_jnt' %lr)          
            armChild = cmds.listRelatives('%sfk_shoulder_jnt' %lr, ad = True, f = True)
            
            cmds.rename(armChild[0], '%sfk_wrist_jnt' %lr )
            cmds.rename(armChild[1], '%sfk_elbow_jnt' %lr )                 
    
            for elem in self.armElement[1:]:
                if lr == self.left:
                        ctlColor = 6
                else:
                        ctlColor = 12
                ctl = controller.circleController('%sfk_%s_ctl' %(lr, elem), 'yz', 2, ctlColor, ['tr', 'sc', 'vi'])
                cmds.select('%s%s_jnt' %(lr, elem), r = True)
                cmds.select('%s_grp' %ctl, tgl = True)
                cmds.pointConstraint(mo = False, weight = 1)
                cmds.orientConstraint(mo = False, weight = 1)
                cmds.delete('%s_grp_pointConstraint1' %ctl)
                cmds.delete('%s_grp_orientConstraint1' %ctl)            
        
                #- constrain joints
                cmds.select(ctl, r = True)
                cmds.select('%sfk_%s_jnt' %(lr, elem), tgl = True)
                cmds.orientConstraint(mo = False, weight = 1)

            
            if lr == self.left:
                    ctlColor = 6
            else:
                    ctlColor = 12
            ctl = controller.circleController('%s%s_ctl' %(lr, self.armElement[0]), 'yz', 2, ctlColor, ['tr', 'sc', 'vi'])
            cmds.select('%s%s_jnt' %(lr, self.armElement[0]), r = True)
            cmds.select('%s_grp' %ctl, tgl = True)
            cmds.pointConstraint(mo = False, weight = 1)
            cmds.orientConstraint(mo = False, weight = 1)
            cmds.delete('%s_grp_pointConstraint1' %ctl)
            cmds.delete('%s_grp_orientConstraint1' %ctl)            
    
            #- constrain joints
            cmds.select(ctl, r = True)
            cmds.select('%s%s_jnt' %(lr, self.armElement[0]), tgl = True)
            cmds.orientConstraint(mo = False, weight = 1)

            #- parent controls
            self.util.parent('%sfk_wrist_ctl_grp' %lr, '%sfk_elbow_ctl' %lr)
            self.util.parent('%sfk_elbow_ctl_grp' %lr, '%sfk_shoulder_ctl' %lr)
            self.util.parent('%sfk_shoulder_ctl_grp' %lr, '%sclavicle_ctl' %lr)
            
    def ikArmSetup(self):
        """
        #- ik arm setup
        """
        
        cmds.select(cl = True)
        for lr in self.lrPrefix:
            cmds.select('%sshoulder_jnt' %lr, r = True)
            cmds.duplicate(rr = True, n = '%sik_shoulder_jnt' %lr)          
            armChild = cmds.listRelatives('%sik_shoulder_jnt' %lr, ad = True, f = True)
            
            cmds.rename(armChild[0], '%sik_wrist_jnt' %lr )
            cmds.rename(armChild[1], '%sik_elbow_jnt' %lr ) 
            
            if lr == self.left:
                    ctlColor = 6
            else:
                    ctlColor = 12
            controller.boxController('%sarm_ik_ctl' %lr, ctlColor, ['sc', 'vi'])
            controller.arrowController('%sarm_polevector_ctl' %lr, ctlColor, ['ro', 'sc', 'vi'])
    
            cmds.select('%sik_wrist_jnt' %lr, r = True)
            cmds.select('%sarm_ik_ctl_grp' %lr, tgl = True)
            cmds.pointConstraint(mo = False, weight = 1)
            cmds.orientConstraint(mo = False, weight = 1)
            cmds.delete('%sarm_ik_ctl_grp_pointConstraint1' %lr)
            cmds.delete('%sarm_ik_ctl_grp_orientConstraint1' %lr)
            
            cmds.select('%sarm_ik_ctl' %lr, r = True)
            cmds.select('%sik_wrist_jnt' %lr, tgl = True)
            cmds.orientConstraint(mo = False, weight = 1)
            
            cmds.select('%sik_shoulder_jnt.rotatePivot' %lr, r = True)
            cmds.select('%sik_wrist_jnt.rotatePivot' %lr, add = True)
            cmds.ikHandle(n = '%sarm_ikHandle' %lr, sol = 'ikRPsolver')             
            
            self.util.parent('%sarm_ikHandle' %lr, '%sarm_ik_ctl' %lr)
            
            #polVecPos = poleVector.getPolVectorPos('%sik_shoulder_jnt' %lr, '%sik_elbow_jnt' %lr, '%sik_wrist_jnt' %lr, 1)
            polVecPos = cmds.xform('%sik_elbow_jnt' %lr, t = True, q = True, ws = True)
            polVecPos = [polVecPos[0], polVecPos[1], polVecPos[2]*2]
            cmds.select('%sarm_polevector_ctl_grp' %lr, r = True)
            cmds.move(polVecPos[0], polVecPos[1], polVecPos[2])
            
            cmds.select('%sarm_polevector_ctl' %lr, r = True)
            cmds.select('%sarm_ikHandle' %lr, tgl = True)
            cmds.poleVectorConstraint(weight = 1)
            
    def fkikCombine(self):
        """
        #fkik arm combine
        """
        
        cmds.select(cl = True)
        
        for lr in self.lrPrefix:
            # creating extra Control
            if lr == self.left:
                    ctlColor = 6
            else:
                    ctlColor = 12
            controller.extraController('%s%s' %(lr, self.extraCtl), ctlColor, ['tr', 'ro', 'sc', 'vi'])
                       
            #- add Extra attributes
            cmds.addAttr('%s%s' %(lr, self.extraCtl), ln = 'FKIK', at = 'long', min = 0, max = 1)
            cmds.setAttr('%s%s.FKIK' %(lr, self.extraCtl), e = True, keyable = True)              
            
            cmds.select('%s%s_grp' %(lr, self.extraCtl), tgl = True)
            cmds.parent()
            cmds.select('%s%s_grp' %(lr, self.extraCtl), r = True)
            extraCtlPos = cmds.xform('%swrist_jnt' %lr, t = True, q = True, ws = True)
            cmds.move(extraCtlPos[0], extraCtlPos[1], extraCtlPos[2] -2)
    
            cmds.select('%swrist_jnt' %lr, r = True)
            cmds.select('%s%s_grp' %(lr, self.extraCtl), tgl = True)
            cmds.parentConstraint(mo = True, weight = 1)    
            
            #- rotate
            cmds.shadingNode('blendColors', n = '%sFKIK_Arm_Mux' %lr, asUtility = True)
            cmds.connectAttr('%s%s.FKIK' %(lr, self.extraCtl), '%sFKIK_Arm_Mux.blender' %lr, f = True)
    
            cmds.setAttr('%sFKIK_Arm_Mux.color1R' %lr, 1)
            cmds.setAttr('%sFKIK_Arm_Mux.color2R' %lr, 0)
            cmds.setAttr('%sFKIK_Arm_Mux.color1G' %lr, 0)
            cmds.setAttr('%sFKIK_Arm_Mux.color2G' %lr, 1)
    
            for elem in self.armElement[1:]:
                cmds.select('%sfk_%s_jnt' %(lr, elem), r = True)
                cmds.select('%s%s_jnt' %(lr, elem), tgl = True)
                cmds.orientConstraint(mo = False, weight =1)
                
                cmds.select('%sik_%s_jnt' %(lr, elem), r = True)
                cmds.select('%s%s_jnt' %(lr, elem), tgl = True)
                cmds.orientConstraint(mo = False, weight =1)
                
                cmds.connectAttr('%sFKIK_Arm_Mux.outputR' %lr, '%s%s_jnt_orientConstraint1.%sik_%s_jntW1' %(lr, elem, lr, elem))
                cmds.connectAttr('%sFKIK_Arm_Mux.outputG' %lr, '%s%s_jnt_orientConstraint1.%sfk_%s_jntW0' %(lr, elem, lr, elem))
                  
            cmds.connectAttr('%sFKIK_Arm_Mux.outputG' %lr, '%sfk_shoulder_ctl_grp.visibility' %lr)
            cmds.connectAttr('%sFKIK_Arm_Mux.outputR' %lr, '%sarm_ik_ctl_grp.visibility' %lr)
            cmds.connectAttr('%sFKIK_Arm_Mux.outputR' %lr, '%sarm_polevector_ctl_grp.visibility' %lr)       
            
            cmds.setAttr('%sfk_shoulder_jnt.visibility' %lr, 0)
            cmds.setAttr('%sik_shoulder_jnt.visibility' %lr, 0)             
            
            cmds.createNode('transform', n = '%sfkik_arm_jnt_grp' %lr)
            
            self.util.parent(['%sfk_shoulder_jnt' %lr, '%sik_shoulder_jnt' %lr,], '%sfkik_arm_jnt_grp' %lr)
            cmds.parent()

            #- creating hand connection locator
            handLoc = self.handConnector(lr)
            cmds.connectAttr('%sFKIK_Arm_Mux.outputG' %lr, '%s.%sfk_wrist_ctlW0' %(handLoc[0], lr))
            cmds.connectAttr('%sFKIK_Arm_Mux.outputR' %lr, '%s.%sarm_ik_ctlW1' %(handLoc[0], lr))

    def stretchIkArm(self):
        """
        stretch IK Arm
        """
        
        for lr in self.lrPrefix:
            cmds.select('%sarm_extra_ctl' %lr)
            cmds.addAttr(ln = 'Stretch_IK', at = 'long', min = 0, max = 1)
            cmds.setAttr('%sarm_extra_ctl.Stretch_IK' %lr, e = True, keyable = True)

            #- Applies when both L, R arm's lengths are same. 
                    
            #- Installing Locator
            cmds.spaceLocator(n = '%sshoulder_stretch_loc' %lr)
            if lr == self.left:
                    cmds.move(self.leftShoulderPos[0], self.leftShoulderPos[1], self.leftShoulderPos[2])
            else:
                    cmds.move(-self.leftShoulderPos[0], self.leftShoulderPos[1], self.leftShoulderPos[2])
            cmds.select('%sshoulder_jnt' %lr, r = True)
            cmds.select('%sshoulder_stretch_loc' %lr, tgl = True)
            cmds.pointConstraint(offset = [0, 0, 0], weight = 1)
                 
            cmds.spaceLocator(n = '%swrist_stretch_loc' %lr)
            if lr == self.left:
                    cmds.move(self.leftWristPos[0], self.leftWristPos[1], self.leftWristPos[2])
            else:
                    cmds.move(-self.leftWristPos[0], self.leftWristPos[1], self.leftWristPos[2])
            cmds.select('%sarm_ik_ctl' %lr, r = True)
            cmds.select('%swrist_stretch_loc' %lr, tgl = True)
            cmds.pointConstraint(offset = [0, 0, 0], weight = 1)
           
            self.util.group(['%sshoulder_stretch_loc' %lr, '%swrist_stretch_loc' %lr], '%sstretch_arm_grp' %lr)
            #cmds.select('%sstretch_arm_grp' %lr, r = True)
            #cmds.select('Puck', tgl = True)
            #cmds.parent()
                                            
            upperArmLength = [self.leftElbowPos[0] - self.leftShoulderPos[0], self.leftElbowPos[1] - self.leftShoulderPos[1], self.leftElbowPos[2] - self.leftShoulderPos[2]]
            lowerArmLength = [self.leftWristPos[0] - self.leftElbowPos[0], self.leftWristPos[1] - self.leftElbowPos[1], self.leftWristPos[2] - self.leftElbowPos[2]]
            armLength = math.sqrt(upperArmLength[0]*upperArmLength[0]+upperArmLength[1]*upperArmLength[1]+upperArmLength[2]*upperArmLength[2])+math.sqrt(lowerArmLength[0]*lowerArmLength[0]+lowerArmLength[1]*lowerArmLength[1]+lowerArmLength[2]*lowerArmLength[2])
 
            #- Divided value by the scale of Puck.... distance between shoulder and wrist
            cmds.shadingNode('multiplyDivide', n = '%sstretch_armIK_Length_MulDiv' %lr, asUtility = True)
            cmds.setAttr('%sstretch_armIK_Length_MulDiv.operation' %lr, 1)
            cmds.setAttr('%sstretch_armIK_Length_MulDiv.input1X' %lr, armLength)
            cmds.connectAttr('%s.scaleX' %partDict.globalCtl, '%sstretch_armIK_Length_MulDiv.input2X' %lr)
           
            #- Distance between shoulder and wrist CTRL
            cmds.shadingNode('distanceBetween', n = '%sstretch_armIK_Distance' %lr, asUtility = True)
            cmds.connectAttr('%sshoulder_stretch_loc.translateX' %lr, '%sstretch_armIK_Distance.point1X' %lr)
            cmds.connectAttr('%sshoulder_stretch_loc.translateY' %lr, '%sstretch_armIK_Distance.point1Y' %lr)
            cmds.connectAttr('%sshoulder_stretch_loc.translateZ' %lr, '%sstretch_armIK_Distance.point1Z' %lr)
            cmds.connectAttr('%swrist_stretch_loc.translateX' %lr, '%sstretch_armIK_Distance.point2X' %lr)
            cmds.connectAttr('%swrist_stretch_loc.translateY' %lr, '%sstretch_armIK_Distance.point2Y' %lr)
            cmds.connectAttr('%swrist_stretch_loc.translateZ' %lr, '%sstretch_armIK_Distance.point2Z' %lr)
            cmds.connectAttr('%sstretch_armIK_Distance.distance' %lr, '%sstretch_armIK_Length_MulDiv.input1Y' %lr)
            cmds.connectAttr('%s.scaleX' %partDict.globalCtl, '%sstretch_armIK_Length_MulDiv.input2Y' %lr)
            
            #- condition node calculate length and compare and do shit
            cmds.shadingNode('condition', n = '%sstretch_armIK_Con' %lr, asUtility = True)
            cmds.connectAttr('%sstretch_armIK_Length_MulDiv.outputY' %lr, '%sstretch_armIK_Con.firstTerm' %lr)
            cmds.connectAttr('%sstretch_armIK_Length_MulDiv.outputX' %lr, '%sstretch_armIK_Con.secondTerm' %lr)
            cmds.setAttr('%sstretch_armIK_Con.operation' %lr, 2)
            
            #- Stretch Ratio
            cmds.shadingNode('multiplyDivide', n = '%sstretch_armIK_ratio_MulDiv' %lr, asUtility = True)
            cmds.connectAttr('%sstretch_armIK_Length_MulDiv.outputY' %lr, '%sstretch_armIK_ratio_MulDiv.input1X' %lr)
            cmds.connectAttr('%sstretch_armIK_Length_MulDiv.outputX' %lr, '%sstretch_armIK_ratio_MulDiv.input2X' %lr)
            cmds.setAttr('%sstretch_armIK_ratio_MulDiv.operation' %lr, 2)
            
            #- Last Mux
            cmds.shadingNode('blendColors', n = '%sArm_Stretch_Mux' %lr, asUtility = True)
            cmds.connectAttr('%sstretch_armIK_Con.outColorR' %lr, '%sArm_Stretch_Mux.blender' %lr)
            cmds.setAttr('%sArm_Stretch_Mux.color1R' %lr, 1)
            cmds.connectAttr('%sstretch_armIK_ratio_MulDiv.outputX' %lr,'%sArm_Stretch_Mux.color2R' %lr)
            
            #- stretch MUX
            cmds.shadingNode('blendColors', n = '%sarm_stretchYesNo_mux' %lr, asUtility = True)
            cmds.connectAttr('%s%s.Stretch_IK' %(lr, self.extraCtl), '%sarm_stretchYesNo_mux.blender' %lr)
            cmds.setAttr('%sarm_stretchYesNo_mux.color2R' %lr, 1)
            cmds.connectAttr('%sArm_Stretch_Mux.outputR' %lr, '%sarm_stretchYesNo_mux.color1R' %lr)
            
            cmds.connectAttr('%sarm_stretchYesNo_mux.outputR' %lr, '%sshoulder_jnt.scaleX' %lr)
            cmds.connectAttr('%sarm_stretchYesNo_mux.outputR' %lr, '%selbow_jnt.scaleX' %lr)
            
    def upperLowerStretchArm(self): #- skipped
        for lr in self.lrPrefix:
            #- add Attribute
            cmds.select('%s%s' %(lr, self.extraCtl), r = True)
            cmds.addAttr(ln = 'UpperArmStretch', at = 'double', min = -5, max = 5)
            cmds.setAttr('%s%s.UpperArmStretch' %(lr, self.extraCtl), e = True, keyable = True)
            cmds.select('%s%s' %(lr, self.extraCtl))
            cmds.addAttr(ln = 'LowerArmStretch', at = 'double', min = -5, max = 5)
            cmds.setAttr('%s%s.LowerArmStretch' %(lr, self.extraCtl), e = True, keyable = True)
            
            #- Elbow Stretch Loc
            cmds.createNode('transform', n = '%selbowStretchLoc_grp' %lr)
            cmds.spaceLocator(n = '%selbowStretchLoc' %lr)
            cmds.select('%selbowStretchLoc_grp' %lr, tgl = True)
            cmds.parent()
            cmds.select('%selbowStretchLoc_grp' %lr, r = True)
            if lr == self.left:
                    cmds.move(self.leftElbowPos[0], self.leftElbowPos[1], self.leftElbowPos[2])
            else:   
                    cmds.move(-self.leftElbowPos[0], self.leftElbowPos[1], self.leftElbowPos[2])
            cmds.select('%sshoulder_jnt' %lr, r = True)
            cmds.select('%selbowStretchLoc_grp' %lr, tgl = True)
            cmds.orientConstraint(weight = 1)
            cmds.delete('%selbowStretchLoc_grp_orientConstraint1' %lr)
            
            self.util.parent('%selbowStretchLoc_grp' %lr, '%sshoulder_jnt' %lr)
            
            #- Wrist Stretch Loc
            cmds.createNode('transform', n = '%swristStretchLoc1_grp' %lr)
            cmds.spaceLocator(n = '%swristStretchLoc1' %lr)
            cmds.select('%swristStretchLoc1_grp' %lr, tgl = True)
            cmds.parent()
            cmds.select('%swristStretchLoc1_grp' %lr, r = True)                   
            if lr == self.left:
                    cmds.move(self.leftWristPos[0], self.leftWristPos[1], self.leftWristPos[2])
            else:   
                    cmds.move(-self.leftWristPos[0], self.leftWristPos[1], self.leftWristPos[2])                      
            cmds.select('%selbow_jnt' %lr, r = True)
            cmds.select('%swristStretchLoc1_grp' %lr, tgl = True)
            cmds.orientConstraint(weight = 1)
            cmds.delete('%swristStretchLoc1_grp_orientConstraint1' %lr)
            self.util.parent('%swristStretchLoc1_grp' %lr, '%selbow_jnt' %lr)
            
            ###########Connect Attr translate Stretch###########
            '''cmds.select('%sElbow_Stretch_Loc' %lr, r = True)
            cmds.select('%sElbow' %lr, tgl = True)
            cmds.pointConstraint(mo = True, weight = 1)
            cmds.connectAttr('%sElbow.translateX' %lr, '%sFK_elbow.translateX' %lr)
            cmds.connectAttr('%sElbow.translateX' %lr, '%sIK_elbow.translateX' %lr) 
            cmds.select('%sElbow_Stretch_Loc' %lr, r = True)
            cmds.select('%sElbow_FK_CTRL' %lr, tgl = True)
            cmds.pointConstraint(mo = True, weight = 1)'''
            
            cmds.select('%swristStretchLoc1' %lr, r = True)
            cmds.select('%swrist_jnt' %lr, tgl = True)
            cmds.pointConstraint(mo = True, weight = 1)
            cmds.connectAttr('%swrist_jnt.translateX' %lr, '%sfk_wrist_jnt.translateX' %lr)
            cmds.connectAttr('%swrist_jnt.translateX' %lr, '%sik_wrist_jnt.translateX' %lr) 
            cmds.select('%swristStretchLoc1' %lr, r = True)
            cmds.select('%sfk_wrist_ctl' %lr, tgl = True)
            cmds.pointConstraint(mo = True, weight = 1)
            #cmds.select('%sWrist' %lr, r = True)
            #cmds.select('%sArm_IK_CTRL_grp' %lr, tgl = True)
            #cmds.pointConstraint(mo = True, weight = 1)

    def bendyArmSetup(self):
        """
        creating bendy arm
        """
        #- duplicate Shoulder... Making Bendy Arm, (Shoulder, Elbow, Wrist)
        
        for lr in self.lrPrefix:
            cmds.select('%sshoulder_jnt' %lr, r = True)
            cmds.duplicate(rr = True)
            cmds.rename('%sbendy_shoulder_jnt' %lr)
            allDec = cmds.listRelatives('%sbendy_shoulder_jnt' %lr, ad = True, f = True)
            for x in allDec:
                if cmds.objectType(x) == 'orientConstraint':
                    cmds.delete(x)
                elif 'wrist' in x:
                    cmds.rename(x, '%sbendy_wrist_jnt' %lr)
                elif 'elbow' in x:
                    cmds.rename(x, '%sbendy_elbow_jnt' %lr)
                
            bendyArmjnts = ['%sbendy_shoulder_jnt' %lr, '%sbendy_elbow_jnt' %lr, '%sbendy_elbow_end_jnt' %lr]
            
            #- unparent the Bendy Arm
            cmds.select('%sbendy_shoulder_jnt' %lr, r =True)
            cmds.parent(w= True)
            
            #- Insert jnts
            numjntInBetween = 6
            
            for i in range(len(bendyArmjnts)-2):
                pos_1 = cmds.xform('%s' %bendyArmjnts[i], ws = True, t = True, q = True )
                pos_2 = cmds.xform('%s' %bendyArmjnts[i+1], ws = True, t = True, q = True )
                if lr == self.left:
                    pos_2 = [pos_2[0]-pos_1[0], pos_2[1]-pos_1[1], pos_2[2]-pos_1[2]]
                    cmds.insertJoint('%s' %bendyArmjnts[i])
                    cmds.joint('joint1', n = '%s_bendy1_jnt' %bendyArmjnts[i].split('_jnt')[0], e = True, co = True, p = [pos_1[0] + pos_2[0]/numjntInBetween, pos_1[1] + pos_2[1]/numjntInBetween, pos_1[2] + pos_2[2]/numjntInBetween])
                    for j in range(numjntInBetween-2):
                        cmds.insertJoint('%s_bendy%s_jnt' %(bendyArmjnts[i].split('_jnt')[0], j+1))
                        cmds.joint('joint1', n = '%s_bendy%s_jnt' %(bendyArmjnts[i].split('_jnt')[0], j+2), e = True, co = True, p = [pos_1[0] + (j+2)*pos_2[0]/numjntInBetween, pos_1[1] + (j+2)*pos_2[1]/numjntInBetween, pos_1[2] + (j+2)*pos_2[2]/numjntInBetween])             

                else:   
                    pos_2 = [-pos_2[0]+pos_1[0], pos_2[1]-pos_1[1], pos_2[2]-pos_1[2]]
                    cmds.insertJoint('%s' %bendyArmjnts[i])
                    cmds.joint('joint1', n = '%s_bendy1_jnt' %bendyArmjnts[i].split('_jnt')[0], e = True, co = True, p = [pos_1[0] - pos_2[0]/numjntInBetween, pos_1[1] + pos_2[1]/numjntInBetween, pos_1[2] + pos_2[2]/numjntInBetween])
                    for j in range(numjntInBetween-2):
                        cmds.insertJoint('%s_bendy%s_jnt' %(bendyArmjnts[i].split('_jnt')[0], j+1))
                        cmds.joint('joint1', n = '%s_bendy%s_jnt' %(bendyArmjnts[i].split('_jnt')[0], j+2), e = True, co = True, p = [pos_1[0] - (j+2)*pos_2[0]/numjntInBetween, pos_1[1] + (j+2)*pos_2[1]/numjntInBetween, pos_1[2] + (j+2)*pos_2[2]/numjntInBetween])
            
            #- Making Elbow=>Wrist jnt
            #- Duplicate and renaming
            cmds.select('%sbendy_elbow_jnt' %lr, r = True)
            cmds.rename('%sbendy_shoulder_end_jnt' %lr)
            cmds.duplicate(rr = True)
            cmds.parent(w = True)
            cmds.rename('%sbendy_elbow_jnt' %lr)
            cmds.select('%sbendy_elbow_jnt|%sbendy_wrist_jnt' %(lr, lr), r = True)
            cmds.rename('%sbendy_elbow_end_jnt' %lr)
            cmds.delete('%sbendy_wrist_jnt' %lr)
            
            #- Insert jnt
            for i in range(len(bendyArmjnts)-2):
                i = i+1
                pos_1 = cmds.xform('%s' %bendyArmjnts[i], ws = True, t = True, q = True )
                pos_2 = cmds.xform('%s' %bendyArmjnts[i+1], ws = True, t = True, q = True )
                if lr == self.left:
                    pos_2 = [pos_2[0]-pos_1[0], pos_2[1]-pos_1[1], pos_2[2]-pos_1[2]]
                    cmds.insertJoint('%s' %bendyArmjnts[i])
                    cmds.joint('joint1', n = '%s_bendy1_jnt' %bendyArmjnts[i].split('_jnt')[0], e = True, co = True, p = [pos_1[0] + pos_2[0]/numjntInBetween, pos_1[1] + pos_2[1]/numjntInBetween, pos_1[2] + pos_2[2]/numjntInBetween])
                    for j in range(numjntInBetween-2):
                        cmds.insertJoint('%s_bendy%s_jnt' %(bendyArmjnts[i].split('_jnt')[0], j+1))
                        cmds.joint('joint1', n = '%s_bendy%s_jnt' %(bendyArmjnts[i].split('_jnt')[0], j+2), e = True, co = True, p = [pos_1[0] + (j+2)*pos_2[0]/numjntInBetween, pos_1[1] + (j+2)*pos_2[1]/numjntInBetween, pos_1[2] + (j+2)*pos_2[2]/numjntInBetween])             

                else:   
                    pos_2 = [-pos_2[0]+pos_1[0], pos_2[1]-pos_1[1], pos_2[2]-pos_1[2]]
                    cmds.insertJoint('%s' %bendyArmjnts[i])
                    cmds.joint('joint1', n = '%s_bendy1_jnt' %bendyArmjnts[i].split('_jnt')[0], e = True, co = True, p = [pos_1[0] - pos_2[0]/numjntInBetween, pos_1[1] + pos_2[1]/numjntInBetween, pos_1[2] + pos_2[2]/numjntInBetween])
                    for j in range(numjntInBetween-2):
                        cmds.insertJoint('%s_bendy%s_jnt' %(bendyArmjnts[i].split('_jnt')[0], j+1))
                        cmds.joint('joint1', n = '%s_bendy%s_jnt' %(bendyArmjnts[i].split('_jnt')[0], j+2), e = True, co = True, p = [pos_1[0] - (j+2)*pos_2[0]/numjntInBetween, pos_1[1] + (j+2)*pos_2[1]/numjntInBetween, pos_1[2] + (j+2)*pos_2[2]/numjntInBetween])                     
            
            #- IK Spline Curve
            bendyShoulderPos = cmds.xform('%s' %bendyArmjnts[0], ws = True, t = True, q = True )
            bendyShoulderElbowMiddlePos = cmds.xform('%s_bendy%s_jnt' %(bendyArmjnts[0].split('_jnt')[0], numjntInBetween/2), ws = True, t = True, q = True )
            bendyElbowPos = cmds.xform('%s' %bendyArmjnts[1], ws = True, t = True, q = True )
            bendyElbowWristMiddlePos = cmds.xform('%s_bendy%s_jnt' %(bendyArmjnts[1].split('_jnt')[0], numjntInBetween/2), ws = True, t = True, q = True )
            bendyWristPos = cmds.xform('%s' %bendyArmjnts[2], ws = True, t = True, q = True )
            cmds.curve(n = '%sshoulder_elbow_ikSplineCV' %lr, d = 2, p = [(bendyShoulderPos[0], bendyShoulderPos[1], bendyShoulderPos[2]), (bendyShoulderElbowMiddlePos[0], bendyShoulderElbowMiddlePos[1], bendyShoulderElbowMiddlePos[2]), (bendyElbowPos[0], bendyElbowPos[1], bendyElbowPos[2])], k = [0,0,1,1])
            cmds.curve(n = '%selbow_wrist_ikSplineCV' %lr, d = 2, p = [(bendyElbowPos[0], bendyElbowPos[1], bendyElbowPos[2]), (bendyElbowWristMiddlePos[0], bendyElbowWristMiddlePos[1], bendyElbowWristMiddlePos[2]), (bendyWristPos[0], bendyWristPos[1], bendyWristPos[2])], k = [0,0,1,1])
            
            #- IK Spline Handle
            cmds.select('%sbendy_shoulder_jnt' %lr, r = True)
            cmds.select('%sbendy_shoulder_end_jnt' %lr, add = True)
            cmds.select('%sshoulder_elbow_ikSplineCV' %lr, add= True) 
            cmds.ikHandle(n = '%sshoulder_bendy_ikSpline_handle'%lr, sol = 'ikSplineSolver', ccv = False, roc = False, pcv = False)
            cmds.select('%sbendy_elbow_jnt' %lr, r = True)
            cmds.select('%sbendy_elbow_end_jnt' %lr, add = True)
            cmds.select('%selbow_wrist_ikSplineCV' %lr, add= True) 
            cmds.ikHandle(n = '%selbow_bendy_ikSpline_handle'%lr, sol = 'ikSplineSolver', ccv = False, roc = False, pcv = False)
            
            if lr == self.left:
                cmds.connectAttr('%swrist_jnt.rotateX' %lr, '%selbow_bendy_ikSpline_handle.twist' %lr, f = True)
                cmds.connectAttr('%sshoulder_jnt.rotateX' %lr, '%sshoulder_bendy_ikSpline_handle.twist'  %lr, f = True)
            else:
                rArmTwsitMul = cmds.shadingNode('multiplyDivide', n = 'r_arm_twsit_multiply', asUtility = True)
                cmds.setAttr(rArmTwsitMul + '.input2X', -1)
                cmds.setAttr(rArmTwsitMul + '.input2Y', -1)
                cmds.connectAttr('r_shoulder_jnt.rotateX', rArmTwsitMul + '.input1X')
                cmds.connectAttr(rArmTwsitMul + '.outputX', 'r_shoulder_bendy_ikSpline_handle.twist', f = True)
                cmds.connectAttr('r_wrist_jnt.rotateX', rArmTwsitMul + '.input1Y')
                cmds.connectAttr(rArmTwsitMul + '.outputY', 'r_elbow_bendy_ikSpline_handle.twist', f = True)
            
            #- Insert Clusters
            for i in range(3):
                cmds.select('%sshoulder_elbow_ikSplineCV.cv[%s]' %(lr, i), r = True)
                cmds.cluster(n = '%sshoulder_elbow_ikSplineCV_cluster%s' %(lr, i))
                cmds.select('%selbow_wrist_ikSplineCV.cv[%s]' %(lr, i), r = True)
                cmds.cluster(n = '%selbow_wrist_ikSplineCV%s' %(lr, i))
            
            #- Making CTRLs
            if lr == self.left:
                    ctlColor = 6
            else:
                    ctlColor = 12
            ctl = controller.circleController('%supperArm_bend_ctl' %lr, 'yz', 1, ctlColor, ['ro', 'sc', 'vi'])
            ctl = controller.circleController('%slowerArm_bend_ctl' %lr, 'yz', 1, ctlColor, ['ro', 'sc', 'vi'])
            
            cmds.select('%sbendy_shoulder_bendy%s_jnt' %(lr, numjntInBetween/2), r = True)
            cmds.select('%supperArm_bend_ctl_grp' %lr, tgl = True)
            cmds.pointConstraint(weight = 1)
            cmds.orientConstraint(weight = 1)
            cmds.select('%sbendy_elbow_bendy%s_jnt' %(lr, numjntInBetween/2), r = True)
            cmds.select('%slowerArm_bend_ctl_grp' %lr, tgl = True)
            cmds.pointConstraint(weight = 1)
            cmds.orientConstraint(weight = 1)
            cmds.delete('%supperArm_bend_ctl_grp_pointConstraint1' %lr)
            cmds.delete('%supperArm_bend_ctl_grp_orientConstraint1' %lr)
            cmds.delete('%slowerArm_bend_ctl_grp_pointConstraint1' %lr)
            cmds.delete('%slowerArm_bend_ctl_grp_orientConstraint1' %lr)
                       
            #- Curve Length
            cmds.createNode('curveInfo', n = '%supperArm_length' %lr)
            cmds.createNode('curveInfo', n = '%slowerArm_length' %lr)
            cmds.connectAttr('%sshoulder_elbow_ikSplineCV.worldSpace' %lr, '%supperArm_length.inputCurve' %lr)
            cmds.connectAttr('%selbow_wrist_ikSplineCV.worldSpace' %lr, '%slowerArm_length.inputCurve' %lr)
            
            #- Original Length
            #- Locators for measuring distance
            bendyLoc = ['shoulder', 'elbow', 'wrist']
            cmds.createNode('transform', n = '%sarm_bendy_loc_grp' %lr)
            cmds.setAttr('%sarm_bendy_loc_grp.visibility' %lr, 0)
            for loc in bendyLoc:
                cmds.spaceLocator(n = '%sbendy_%s_loc' %(lr, loc))
                cmds.select('%s%s_jnt' %(lr, loc), r = True)
                cmds.select('%sbendy_%s_loc' %(lr, loc), tgl = True)
                cmds.pointConstraint(weight = 1)
                self.util.parent('%sbendy_%s_loc' %(lr, loc), '%sarm_bendy_loc_grp' %lr)
            
            #- Distance, need to use global_ctl's scale
            cmds.shadingNode('distanceBetween', n = '%sbendyArm_upperLength' %lr, asUtility = True)
            cmds.shadingNode('distanceBetween', n = '%sbendyArm_lowerLength' %lr, asUtility = True)
            cmds.connectAttr('%sbendy_shoulder_loc.translate' %lr,'%sbendyArm_upperLength.point1' %lr )
            cmds.connectAttr('%sbendy_elbow_loc.translate' %lr, '%sbendyArm_upperLength.point2' %lr )
            cmds.connectAttr('%sbendy_elbow_loc.translate' %lr, '%sbendyArm_lowerLength.point1' %lr )
            cmds.connectAttr('%sbendy_wrist_loc.translate' %lr, '%sbendyArm_lowerLength.point2' %lr )

            cmds.shadingNode('multiplyDivide', n = '%sbendy_globalScale' %lr, asUtility = True)
            cmds.connectAttr('global_ctl.scaleX', '%sbendy_globalScale.input1X' %lr)
            cmds.connectAttr('global_ctl.scaleX', '%sbendy_globalScale.input1Y' %lr)
            cmds.connectAttr('%sbendyArm_upperLength.distance' %lr, '%sbendy_globalScale.input2X' %lr)
            cmds.connectAttr('%sbendyArm_lowerLength.distance' %lr, '%sbendy_globalScale.input2Y' %lr)
            
            #- Stretch Ratio
            cmds.shadingNode('multiplyDivide', n = '%sbendyArm_stretchRatio' %lr, asUtility = True)
            cmds.setAttr('%sbendyArm_stretchRatio.operation' %lr, 2)              
            cmds.connectAttr('%sbendy_globalScale.outputX' %lr, '%sbendyArm_stretchRatio.input2X' %lr)
            cmds.connectAttr('%sbendy_globalScale.outputY' %lr, '%sbendyArm_stretchRatio.input2Y' %lr)
            cmds.connectAttr('%supperArm_length.arcLength' %lr, '%sbendyArm_stretchRatio.input1X' %lr)
            cmds.connectAttr('%slowerArm_length.arcLength' %lr, '%sbendyArm_stretchRatio.input1Y' %lr)
            
            #-Bendy Stretch Condition
            cmds.shadingNode('condition', n = '%sbendyArm_upperCondition' %lr, asUtility = True)
            cmds.shadingNode('condition', n = '%sbendyArm_lowerCondition' %lr, asUtility = True)
            cmds.setAttr('%sbendyArm_upperCondition.secondTerm' %lr, 1)                     
            cmds.setAttr('%sbendyArm_lowerCondition.secondTerm' %lr, 1)
            cmds.setAttr('%sbendyArm_upperCondition.operation' %lr, 3)
            cmds.setAttr('%sbendyArm_lowerCondition.operation' %lr, 3)
            cmds.connectAttr('%supperArm_length.arcLength' %lr, '%sbendyArm_upperCondition.firstTerm' %lr)
            cmds.connectAttr('%slowerArm_length.arcLength' %lr, '%sbendyArm_lowerCondition.firstTerm' %lr)
            cmds.connectAttr('%sbendyArm_upperLength.distance' %lr, '%sbendyArm_upperCondition.secondTerm' %lr)
            cmds.connectAttr('%sbendyArm_lowerLength.distance' %lr, '%sbendyArm_lowerCondition.secondTerm' %lr)
            cmds.connectAttr('%sbendyArm_stretchRatio.outputX' %lr, '%sbendyArm_upperCondition.colorIfTrueR' %lr)
            cmds.connectAttr('%sbendyArm_stretchRatio.outputY' %lr, '%sbendyArm_lowerCondition.colorIfTrueR' %lr)
            
            
            #- Grouping
            self.util.group('%sbendy_shoulder_jnt' %lr, '%sbendy_shoulder_jnt_grp' %lr)
            cmds.createNode('transform', n = '%sbendy_elbow_jnt_grp' %lr)
            self.util.match('%sbendy_elbow_jnt_grp' %lr, '%selbow_jnt' %lr)
            self.util.parent('%sbendy_elbow_jnt' %lr, '%sbendy_elbow_jnt_grp' %lr)
            self.util.group(['%sbendy_elbow_jnt_grp' %lr, '%sbendy_shoulder_jnt_grp' %lr], '%sarm_bendy_jnt_grp' %lr)
            self.util.group(['%sshoulder_bendy_ikSpline_handle' %lr, '%selbow_bendy_ikSpline_handle' %lr], '%sarm_bendy_splineik_grp' %lr)
            self.util.parent('%sshoulder_elbow_ikSplineCV_cluster1Handle' %lr, '%supperArm_bend_ctl' %lr)
            self.util.parent('%selbow_wrist_ikSplineCV1Handle' %lr, '%slowerArm_bend_ctl' %lr)
            self.util.group(['%sshoulder_elbow_ikSplineCV' %lr, '%selbow_wrist_ikSplineCV' %lr], '%sarm_bendy_cv_grp' %lr)
            self.util.group(['%sarm_bendy_splineik_grp' %lr, '%sarm_bendy_cv_grp' %lr, '%sarm_bendy_loc_grp' %lr], '%sarm_bendy_grp' %lr)
            
            cmds.select('%sshoulder_jnt' %lr, r = True)
            cmds.select('%sbendy_shoulder_jnt_grp' %lr, tgl = True)
            cmds.pointConstraint(weight = 1, mo = True)
            cmds.select('%selbow_jnt' %lr, r = True)
            cmds.select('%sbendy_elbow_jnt_grp' %lr, tgl = True)
            cmds.pointConstraint(weight = 1, mo = True)
            cmds.orientConstraint(weight = 1, mo = True)
                
            #- Cluster Grouping
            self.util.parent('%sshoulder_elbow_ikSplineCV_cluster0Handle' %lr, '%sshoulder_jnt' %lr)
            self.util.parent('%supperArm_bend_ctl_grp' %lr, '%sshoulder_jnt' %lr)
            self.util.parent('%sshoulder_elbow_ikSplineCV_cluster2Handle' %lr, '%selbow_jnt' %lr)
            self.util.parent('%selbow_wrist_ikSplineCV0Handle' %lr, '%selbow_jnt' %lr)
            self.util.parent('%slowerArm_bend_ctl_grp' %lr, '%selbow_jnt' %lr)
            self.util.parent('%selbow_wrist_ikSplineCV2Handle' %lr, '%swrist_jnt' %lr)
            
            #cmds.select('%sshoulder_elbow_ikSplineCV' %lr, r = True)
            #cmds.select('%sShoulder' %lr, tgl = True)
            #cmds.parent()
            #cmds.parent('%selbow_wrist_ikSplineCV' %lr, r = True)
            #cmds.select('%sShoulder' %lr, tgl = True)
            #cmds.parent()
            
            
            bendyShoulderDest = cmds.listRelatives('%sbendy_shoulder_jnt_grp' %lr, ad = True)
            bendyShoulderDest = bendyShoulderDest[2:-1]
            bendyElbowDest = cmds.listRelatives('%sbendy_elbow_jnt_grp' %lr, ad = True)
            bendyElbowDest = bendyElbowDest[2:-1]

            for joint in bendyShoulderDest:
                cmds.connectAttr('%sbendyArm_upperCondition.outColorR' %lr, '%s.scaleX' %joint)
            for joint in bendyElbowDest:
                cmds.connectAttr('%sbendyArm_lowerCondition.outColorR' %lr, '%s.scaleX' %joint)                 
            
            cmds.setAttr('%sshoulder_bendy_ikSpline_handle.visibility' %lr, 0)
            cmds.setAttr('%selbow_bendy_ikSpline_handle.visibility' %lr, 0)
            cmds.setAttr('%sshoulder_elbow_ikSplineCV_cluster0Handle.visibility' %lr, 0)
            cmds.setAttr('%sshoulder_elbow_ikSplineCV_cluster1Handle.visibility' %lr, 0)
            cmds.setAttr('%sshoulder_elbow_ikSplineCV_cluster2Handle.visibility' %lr, 0)
            cmds.setAttr('%selbow_wrist_ikSplineCV0Handle.visibility' %lr, 0)       
            cmds.setAttr('%selbow_wrist_ikSplineCV1Handle.visibility' %lr, 0)                       
            cmds.setAttr('%selbow_wrist_ikSplineCV2Handle.visibility' %lr, 0)       
                    
            cmds.addAttr('%s%s' %(lr, self.extraCtl),  ln = 'Bend', at = 'long', min = 0, max = 1)
            cmds.setAttr('%s%s.Bend' %(lr, self.extraCtl), e = True, keyable = True)
            cmds.connectAttr('%s%s.Bend' %(lr, self.extraCtl), '%supperArm_bend_ctl_grp.visibility' %lr)
            cmds.connectAttr('%s%s.Bend' %(lr, self.extraCtl), '%slowerArm_bend_ctl_grp.visibility' %lr)
        
            #- Stretch and Bend
            cmds.shadingNode('multiplyDivide', n = '%sArm_StretchBend' %lr, asUtility = True)
            
            cmds.connectAttr('%sarm_stretchYesNo_mux.outputR' %lr, '%sArm_StretchBend.input1X' %lr)
            cmds.connectAttr('%sarm_stretchYesNo_mux.outputR' %lr, '%sArm_StretchBend.input1Y' %lr)
            
            bendyShoulderDest = cmds.listRelatives('%sbendy_shoulder_jnt_grp' %lr, ad = True)
            bendyShoulderDest = bendyShoulderDest[2:-1]
            bendyElbowDest = cmds.listRelatives('%sbendy_elbow_jnt_grp' %lr, ad = True)
            bendyElbowDest = bendyElbowDest[2:-1]
            #print bendyShoulderDest
            #print bendyElbowDest
            
            cmds.connectAttr('%sbendyArm_upperCondition.outColorR' %lr, '%sArm_StretchBend.input2X' %lr)
            cmds.connectAttr('%sbendyArm_lowerCondition.outColorR' %lr, '%sArm_StretchBend.input2Y' %lr)
            
            for joint in bendyShoulderDest:
                    cmds.connectAttr('%sArm_StretchBend.outputX' %lr, '%s.scaleX' %joint, f = True)
            for joint in bendyElbowDest:
                    cmds.connectAttr('%sArm_StretchBend.outputY' %lr, '%s.scaleX' %joint, f = True)                         
            
            cmds.select('%sstretch_arm_grp' %lr, r = True)
            cmds.setAttr('%sstretch_arm_grp.visibility' %lr, 0)
        
    def handConnector(self, lr):
        """
        creating part that will be connected to hand
        """
    
        cmds.spaceLocator(n = '%shandCon_loc' %lr)
        self.util.group('%shandCon_loc' %lr,'%shandCon_loc_grp' %lr)
        cmds.select('%swrist_jnt' %lr, r =  True)
        cmds.select('%shandCon_loc_grp' %lr, tgl =  True)
        pct = cmds.pointConstraint(weight = 1, mo = False)
        ort = cmds.orientConstraint(weight = 1, mo = False)
        cmds.delete(pct)
        cmds.delete(ort)

        cmds.select('%sfk_wrist_ctl' %lr, r =  True)
        cmds.select('%shandCon_loc_grp' %lr, tgl =  True)
        cmds.parentConstraint(weight = 1, mo = False)
        cmds.select('%sarm_ik_ctl' %lr, r =  True)
        cmds.select('%shandCon_loc_grp' %lr, tgl =  True)
        handConPct = cmds.parentConstraint(weight = 1, mo = False)
        return handConPct
    
    def armCleanup(self):
        """
        cleaning up hierarchy
        """
        
        for lr in self.lrPrefix:
            cmds.setAttr('%sarm_ikHandle.visibility' %lr, 0)
            
            self.util.group(['%sclavicle_jnt' %lr, '%sfkik_arm_jnt_grp' %lr], '%sarm_jnt_grp' %lr)
            children = ['%sclavicle_ctl_grp' %lr, '%sarm_polevector_ctl_grp' %lr, '%sarm_extra_ctl_grp' %lr, '%sarm_ik_ctl_grp' %lr]
            self.util.group(children, '%sarm_ctl_grp' %lr)
            
            cmds.setAttr('%sstretch_arm_grp.visibility' %lr, 0)
            cmds.setAttr('%sarm_bendy_cv_grp.inheritsTransform' %lr, 0)
        
        self.util.group(['l_arm_bendy_grp', 'r_arm_bendy_grp'], 'arm_bendy_grp')
        self.util.group(['l_stretch_arm_grp', 'r_stretch_arm_grp'], 'stretch_arm_grp')
        self.util.group(['l_arm_jnt_grp', 'r_arm_jnt_grp', 'l_arm_bendy_jnt_grp', 'r_arm_bendy_jnt_grp'], 'arm_jnt_grp')
        self.util.group(['l_arm_ctl_grp', 'r_arm_ctl_grp'], 'arm_ctl_grp')
        self.util.group(['stretch_arm_grp', 'arm_bendy_grp'], 'arm_misc_grp')

