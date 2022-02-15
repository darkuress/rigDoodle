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

class LegSetup(object):
    def __init__(self):
        """
        partDict.legPlaceLocs 
        """
        
        #- this might be combined into partDict
        self.left         = partDict.lrPrefix[0]
        self.extraCtl     = 'leg_extra_ctl'
        
        self.locatorSetup = locatorSetup.LocatorSetup()
        self.util         = util.Util()
        self.legElement   = partDict.legElement
        self.lHipJnt      = self.left + partDict.legElement[0] + '_jnt'
        self.lrPrefix     = partDict.lrPrefix
    
    def createLocator(self):
        """
        create locators
        """
        self.legParts   = self.locatorSetup.createLocator(partDict.legPlaceLocs)
        self.pivotParts = self.locatorSetup.createLocator(partDict.legPivotLocs)

    def confirmJoints(self):
        """   
        draw joints in locator position
        """

        #- Getting Ball and Toe Location
        self.leftHipPos = cmds.xform('l_hip_adjust_ctl', q = True, ws = True, t = True)
        self.leftKneePos = cmds.xform('l_knee_adjust_ctl', q = True, ws = True, t = True)
        self.leftAnklePos = cmds.xform('l_ankle_adjust_ctl', q = True, ws = True, t = True)
        self.leftBallPos = cmds.xform('l_ball_adjust_ctl', q = True, ws = True, t = True)
        self.leftToePos = cmds.xform('l_toe_adjust_ctl', q = True, ws = True, t = True)
        self.leftHeelPos = cmds.xform('l_heel_PivotPosition', q = True, ws = True, t = True)
        self.leftSideInPos = cmds.xform('l_sidein_PivotPosition', q = True, ws = True, t = True)
        self.leftSideOutPos = cmds.xform('l_sideout_PivotPosition', q = True, ws = True, t = True)
        
        #duplicate pivots
        cmds.duplicate('l_heel_PivotPosition', n = 'r_heel_PivotPosition', rr =  True)
        cmds.xform('r_heel_PivotPosition', t = [-self.leftHeelPos[0], self.leftHeelPos[1], self.leftHeelPos[2]])
        cmds.duplicate('l_sidein_PivotPosition', n = 'r_sidein_PivotPosition', rr =  True)
        cmds.xform('r_sidein_PivotPosition', t = [-self.leftSideInPos[0], self.leftSideInPos[1], self.leftSideInPos[2]])
        cmds.duplicate('l_sideout_PivotPosition', n = 'r_sideout_PivotPosition', rr =  True)
        cmds.xform('r_sideout_PivotPosition', t = [-self.leftSideOutPos[0], self.leftSideOutPos[1], self.leftSideOutPos[2]])
        
        cmds.select(cl = True)
        print 'leg Parts : ' , self.legParts
        for elem in self.legElement :
            jointPos = cmds.xform(self.left + elem + '_adjust_ctl', t = True, q = True, ws = True)
            cmds.joint(n = '%s%s_jnt' %(self.left, elem), p = jointPos)
            
        #- orient joint
        cmds.joint(self.lHipJnt, e = True, oj = 'xzy', secondaryAxisOrient = 'yup', ch = True, zso = True)

        #- delete position locators
        cmds.delete(self.legParts)
    
    def mirrorJoints(self):
        """
        mirroring joints
        """
        
        self.util.mirrorJoints(self.lHipJnt)
        try:
            cmds.rename('r_balr_jnt', 'r_ball_jnt')
        except:
            pass

    def ikLegSetup(self):
        """
        setiing up ik leg
        """
        
        cmds.select(cl = True)
        for lr in self.lrPrefix:
            # creating Controllers
            if lr == self.left:
                    ctlColor = 6
            else:
                    ctlColor = 12
            #- making controller
            #- foot controller
            controller.circleController('%sleg_ctl' %lr, 'zx', 2, color = ctlColor, lockAttr = ['sc'])
            footAttr = ['1Rolls','0Heel_Roll','0Ball_Roll','0Toe_Roll','1Twists','0Heel_Twist','0Ball_Twist','0BallToe_Twist','0Toe_Twist','1Extras','0Side','0Tip']           
            for attr in footAttr:
                cmds.addAttr('%sleg_ctl' %lr, ln = "%s" %attr[1:], at = 'double')
                if attr[0] == '1':
                    cmds.setAttr('%sleg_ctl.%s' %(lr, attr[1:]), e = True, channelBox  = True)
                else:
                    cmds.setAttr('%sleg_ctl.%s' %(lr, attr[1:]), e = True, keyable = True )            
    
            #- polevector controller
            controller.arrowController('%sleg_pv_ctl' %lr, color = ctlColor, lockAttr = ['sc'])
            cmds.select('%sleg_pv_ctl.cv[0:10]' %lr, r = True)
            cmds.scale(0.2, 0.2, 0.2, r = True)
            cmds.select('%sleg_pv_ctl_grp' %lr, r = True)
            
            if lr == self.left:
                    cmds.move(self.leftToePos[0], self.leftKneePos[1], self.leftToePos[2]+2)
            else:
                    cmds.move(-self.leftToePos[0], self.leftKneePos[1], self.leftToePos[2]+2)   

            #- creating extra controller
            cmds.createNode('transform', n =  '%sleg_extra_ctl_grp' %lr)
            cmds.curve(n = '%sleg_extra_ctl' %lr, d = 1, p =[(-4, 0, -3),(-1, 0, -3),(-1, 0, -2),(-3, 0, -2),(-3, 0, -1), (-1, 0, -1),(-1, 0, 0),(-3, 0, 0),(-3, 0, 1),(-1, 0, 1),(-1, 0, 2),(-4, 0, 2),(-4, 0, -3),(3, 0, -3),(2, 0, -1),(2, 0, 0),(3, 0, 2),(2, 0, 2),(1, 0, 0),(0, 0, 2),(-1, 0, 2),(0, 0, 0),(0, 0, -1),(-1, 0, -3),(0, 0, -3),(1, 0, -1),(2, 0, -3),(3, 0, -3),(3, 0, 2),(-4, 0, 2)], k= [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29])
            cmds.scale(0.2,0.2,0.2)
            cmds.select('%sleg_extra_ctl_grp' %lr, tgl = True)
            cmds.parent()
            cmds.select('%sleg_extra_ctl_grp' %lr, r = True)
            if lr == 'l_':
                cmds.move(self.leftAnklePos[0]+4, self.leftAnklePos[1], self.leftAnklePos[2])
                cmds.rotate(90, 0, 0)
            else:   
                cmds.move(-self.leftAnklePos[0]-4, self.leftAnklePos[1], self.leftAnklePos[2])
                cmds.rotate(90, 0, 0)

            #adding color
            cmds.rename(cmds.listRelatives('%sleg_extra_ctl' %lr)[0], '%sleg_extra_ctlShape' %lr)
            cmds.setAttr('%sleg_extra_ctlShape.overrideEnabled' %lr, 1)
            cmds.setAttr('%sleg_extra_ctlShape.overrideColor' %lr, ctlColor)	
            
            #- setting up ik
            cmds.select('%ship_jnt' %lr, r = True)
            cmds.duplicate(rr = True, n = '%sik_hip_jnt' %lr)          
            legChild = cmds.listRelatives('%sik_hip_jnt' %lr, ad = True, f = True)
            cmds.rename(legChild[0], '%sik_toe_jnt' %lr )
            cmds.rename(legChild[1], '%sik_ball_jnt' %lr )
            cmds.rename(legChild[2], '%sik_ankle_jnt' %lr )
            cmds.rename(legChild[3], '%sik_knee_jnt' %lr )
                       
            legJoints         = [lr + 'ik_' + x + '_jnt' for x in partDict.legElement]
            legJointsIkNaming = [lr + x for x in partDict.legElement]
            print 'IK leg Joints : %s' %legJoints

            ikInstallJoints = legJoints
            del ikInstallJoints[1]
            for i in range(len(ikInstallJoints)-1):
                    
                cmds.select('%s.rotatePivot' %ikInstallJoints[i], r = True)
                cmds.select('%s.rotatePivot' %ikInstallJoints[i+1], add = True)
                cmds.ikHandle(n = '%s_IKHandle' %legJointsIkNaming[i+2], sol = 'ikRPsolver')
                 
            #-Making Group Nod
            cmds.createNode( 'transform', n='%sball_ik_grp' %lr )
            cmds.createNode( 'transform', n='%stoe_ik_grp' %lr )
            cmds.createNode('transform', n = '%sball_grp' %lr )
            cmds.createNode( 'transform', n='%sheel_grp' %lr )
            cmds.createNode( 'transform', n='%stoe_grp' %lr )
            cmds.createNode( 'transform', n='%ssidein_grp' %lr )
            
            #-Grouping IKs
            if lr == self.left:               
                cmds.select('%sball_ik_grp' %lr, r = True)
                cmds.select('%stoe_ik_grp' %lr, add = True)
                cmds.select('%sball_grp' %lr, tgl = True)
                cmds.move(self.leftBallPos[0], self.leftBallPos[1], self.leftBallPos[2])
                cmds.select('%stoe_grp' %lr, r = True)
                cmds.move(self.leftToePos[0], self.leftToePos[1], self.leftToePos[2])
                cmds.select('%sleg_ctl_grp' %lr, r = True)
                cmds.move(self.leftAnklePos[0], self.leftAnklePos[1], self.leftAnklePos[2])
                cmds.select('%sheel_grp' %lr, r = True)
                cmds.move(self.leftHeelPos[0], self.leftHeelPos[1], self.leftHeelPos[2])
                cmds.select('%ssidein_grp' %lr, r = True)
                cmds.move(self.leftSideInPos[0], self.leftSideInPos[1], self.leftSideInPos[2])
            else:
                cmds.select('%sball_ik_grp' %lr, r = True)
                cmds.select('%stoe_ik_grp' %lr, add = True)
                cmds.select('%sball_grp' %lr, tgl = True)
                cmds.move(-self.leftBallPos[0], self.leftBallPos[1], self.leftBallPos[2])
                cmds.select('%stoe_grp' %lr, r = True)
                cmds.move(-self.leftToePos[0], self.leftToePos[1], self.leftToePos[2])
                cmds.select('%sleg_ctl_grp' %lr, r = True)
                cmds.move(-self.leftAnklePos[0], self.leftAnklePos[1], self.leftAnklePos[2])
                cmds.select('%sheel_grp' %lr, r = True)
                cmds.move(-self.leftHeelPos[0], self.leftHeelPos[1], self.leftHeelPos[2])
                cmds.select('%ssidein_grp' %lr, r = True)
                cmds.move(-self.leftSideInPos[0], self.leftSideInPos[1], self.leftSideInPos[2])
            
            ####adjust Foot ctls
            cmds.select('%sleg_ctl.cv[0]' %lr, r = True)
            for i in range(7):
                    cmds.select('%sleg_ctl.cv[%s]' %(lr, i+1), tgl = True)
            cmds.move(0, -self.leftAnklePos[1], 0, r = True)
            cmds.select('%sleg_ctl.cv[3]' %lr, r = True)
            for i in range(4):
                    cmds.select('%sleg_ctl.cv[%s]' %(lr, i+4), tgl = True)
            cmds.move(0,0, abs(self.leftToePos[2]+1), r = True)
                    
                   
            #####Final Grouping#####
            cmds.select('%sankle_IKHandle' %lr, r = True)
            cmds.select('%sball_IKHandle'%lr, add = True)
            cmds.select('%sball_ik_grp' %lr, tgl = True)
            cmds.parent()
            cmds.select('%stoe_IKHandle' %lr, r = True)
            cmds.select('%stoe_ik_grp' %lr, tgl = True)
            cmds.parent()
            cmds.select('%sball_ik_grp' %lr, r = True)
            cmds.select('%stoe_ik_grp' %lr, add = True)
            cmds.select('%sball_grp' %lr, tgl = True)
            cmds.parent()
            cmds.select('%sball_grp' %lr, r = True)
            cmds.select('%ssideout_PivotPosition' %lr, tgl = True)
            cmds.parent()
            cmds.select('%ssideout_PivotPosition' %lr, r = True)
            cmds.select('%ssidein_PivotPosition' %lr, tgl = True)
            cmds.parent()
            cmds.select('%ssidein_PivotPosition' %lr, r = True)
            cmds.select('%ssidein_grp' %lr, tgl = True)
            cmds.parent()
            cmds.select('%ssidein_grp' %lr, r = True)
            cmds.select('%stoe_grp' %lr, tgl = True)
            cmds.parent()
            cmds.select('%stoe_grp' %lr, r = True)
            cmds.select('%sheel_grp' %lr, tgl = True)
            cmds.parent()
            cmds.select('%sheel_grp' %lr, r = True)
            cmds.select('%sleg_ctl' %lr, tgl = True)
            cmds.parent()
            cmds.setAttr('%sheel_grp.visibility' %lr, 0)

            ####leg Polevector Follow#########
            cmds.spaceLocator(n = '%spv_follow_loc' %lr)
            if lr == self.left:
                cmds.move(self.leftToePos[0], self.leftToePos[1], self.leftToePos[2])
            else:
                cmds.move(-self.leftToePos[0], self.leftToePos[1], self.leftToePos[2])
            cmds.setAttr('%spv_follow_loc.visibility' %lr, 0)
            cmds.select('%spv_follow_loc' %lr, r = True)
            cmds.select('%sleg_ctl' %lr, tgl = True)
            cmds.parent()
            cmds.select('%spv_follow_loc' %lr, r = True)
            cmds.select('%sleg_pv_ctl_grp' %lr, tgl = True)
            cmds.pointConstraint(offset = [0, 0, 0],mo = True, o = [0, 0, 0], weight = 1) 
                    

            #############Connect Attr###############
            #cmds.connectAttr('r_leg_ctl.Heel_Roll', 'r_heel_grp.rotateX') ,f = True) 
            ###Rolls###
            cmds.shadingNode('multiplyDivide', n = '%smulDiv_Roll' %lr, asUtility = True)
            cmds.setAttr ('%smulDiv_Roll.input2X' %lr, -1)
            cmds.setAttr ('%smulDiv_Roll.input2Y' %lr, -1)
            cmds.setAttr ('%smulDiv_Roll.input2Z' %lr, -1)
            cmds.connectAttr('%sleg_ctl.Heel_Roll' %lr, '%smulDiv_Roll.input1X' %lr, f = True)
            cmds.connectAttr('%smulDiv_Roll.outputX' %lr, '%sheel_grp.rotateX' %lr, f = True)
            cmds.connectAttr('%sleg_ctl.Ball_Roll' %lr, '%smulDiv_Roll.input1Y' %lr, f = True)
            cmds.connectAttr('%smulDiv_Roll.outputY' %lr, '%sball_ik_grp.rotateX' %lr, f = True)
            cmds.connectAttr('%sleg_ctl.Toe_Roll' %lr, '%smulDiv_Roll.input1Z' %lr, f = True)
            cmds.connectAttr('%smulDiv_Roll.outputZ' %lr, '%stoe_grp.rotateX' %lr, f = True)
            ###Twists###    
            #cmds.shadingNode('multiplyDivide', n = '%smulDiv_Twist' %lr, asUtility = True)
            cmds.shadingNode('multiplyDivide', n = '%smulDiv_Twist' %lr, asUtility = True)
            cmds.shadingNode('multiplyDivide', n = '%smulDiv_Twist1' %lr, asUtility = True)
            cmds.setAttr ('%smulDiv_Twist.input2X' %lr, -1)
            cmds.setAttr ('%smulDiv_Twist.input2Y' %lr, -1)
            cmds.setAttr ('%smulDiv_Twist.input2Z' %lr, -1)
            cmds.setAttr ('%smulDiv_Twist1.input2X' %lr, -1)
            if lr == self.left:
                    cmds.connectAttr('%sleg_ctl.Heel_Twist' %lr, '%sheel_grp.rotateY' %lr, f = True)
                    cmds.connectAttr('%sleg_ctl.Ball_Twist' %lr, '%sball_ik_grp.rotateY' %lr, f = True)
                    cmds.connectAttr('%sleg_ctl.Toe_Twist' %lr, '%stoe_grp.rotateY' %lr, f = True)
                    cmds.connectAttr('%sleg_ctl.BallToe_Twist' %lr, '%sball_grp.rotateY' %lr, f = True)
            else:
                    cmds.connectAttr('%sleg_ctl.Heel_Twist' %lr, '%smulDiv_Twist.input1X' %lr, f = True)
                    cmds.connectAttr('%smulDiv_Twist.outputX' %lr, '%sheel_grp.rotateY' %lr, f = True)
                    cmds.connectAttr('%sleg_ctl.Ball_Twist' %lr, '%smulDiv_Twist.input1Y' %lr, f = True)
                    cmds.connectAttr('%smulDiv_Twist.outputY' %lr, '%sball_ik_grp.rotateY' %lr, f = True)
                    cmds.connectAttr('%sleg_ctl.Toe_Twist' %lr, '%smulDiv_Twist.input1Z' %lr, f = True)
                    cmds.connectAttr('%smulDiv_Twist.outputZ' %lr, '%stoe_grp.rotateY' %lr, f = True)
                    cmds.connectAttr('%sleg_ctl.BallToe_Twist' %lr, '%smulDiv_Twist1.input1X' %lr, f = True)
                    cmds.connectAttr('%smulDiv_Twist1.outputX' %lr, '%sball_grp.rotateY' %lr, f = True)                             
            ###Extras###
            cmds.shadingNode('multiplyDivide', n = '%smulDiv_Extra' %lr, asUtility = True)
            cmds.setAttr ('%smulDiv_Extra.input2X' %lr, -1)
            cmds.connectAttr('%sleg_ctl.Tip' %lr, '%smulDiv_Extra.input1X' %lr, f = True)
            cmds.connectAttr('%smulDiv_Extra.outputX' %lr, '%stoe_ik_grp.rotateX' %lr, f = True)
            
            ####Side It's hard one...!!!###
            cmds.shadingNode('condition', n = '%ssidein' %lr, asUtility = True)
            cmds.shadingNode('condition', n = '%sSideOut' %lr, asUtility = True)
            cmds.shadingNode('multiplyDivide', n = 'mulDiv_Extra_side', asUtility = True)
            
            cmds.setAttr('%ssidein.operation' %lr, 2)
            cmds.setAttr('%sSideOut.operation' %lr, 4)
            
            cmds.connectAttr('%sleg_ctl.Side' %lr, '%ssidein.firstTerm' %lr, f = True)
            cmds.connectAttr('%ssidein.outColorR' %lr, '%smulDiv_Extra.input2Y' %lr, f = True)
            cmds.connectAttr('%sleg_ctl.Side' %lr, '%smulDiv_Extra.input1Y' %lr, f = True)
            cmds.setAttr ('mulDiv_Extra_side.input2X', -1)
            if lr == self.left:
                    cmds.connectAttr('%smulDiv_Extra.outputY' %lr, 'mulDiv_Extra_side.input1X', f = True)
                    cmds.connectAttr('mulDiv_Extra_side.outputX', '%ssidein_PivotPosition.rotateZ' %lr, f = True)
            else:
                    cmds.connectAttr('%smulDiv_Extra.outputY' %lr, '%ssidein_PivotPosition.rotateZ' %lr, f = True)
    
            cmds.connectAttr('%sleg_ctl.Side' %lr, '%sSideOut.firstTerm' %lr, f = True)
            cmds.connectAttr('%sSideOut.outColorR' %lr, '%smulDiv_Extra.input2Z' %lr, f = True)
            cmds.connectAttr('%sleg_ctl.Side' %lr, '%smulDiv_Extra.input1Z' %lr, f = True)
            cmds.setAttr ('mulDiv_Extra_side.input2Y', -1)
            if lr == self.left:
                    cmds.connectAttr('%smulDiv_Extra.outputZ' %lr, 'mulDiv_Extra_side.input1Y', f = True)
                    cmds.connectAttr('mulDiv_Extra_side.outputY', '%ssideout_PivotPosition.rotateZ' %lr, f = True)
            else:
                    cmds.connectAttr('%smulDiv_Extra.outputZ' %lr, '%ssideout_PivotPosition.rotateZ' %lr, f = True)
            
            #############Polevector##################
            cmds.select('%sleg_pv_ctl' %lr, r = True)
            cmds.select('%sankle_IKHandle' %lr, tgl = True)
            cmds.poleVectorConstraint(weight = 1)
                        
    def fkLegSetup(self):
        """
        fk leg setup
        """
        ####fk ctls###         
        fkLegJoints = ['fk_hip', 'fk_knee', 'fk_ankle','fk_ball']
        
        #- Making fk joints
        for lr in self.lrPrefix:
            cmds.select('%ship_jnt' %lr, r = True)
            cmds.duplicate(rr = True, n = '%sfk_hip_jnt' %lr)          
            legChild = cmds.listRelatives('%sfk_hip_jnt' %lr, ad = True, f = True)
            cmds.rename(legChild[0], '%sfk_toe_jnt' %lr )
            cmds.rename(legChild[1], '%sfk_ball_jnt' %lr )
            cmds.rename(legChild[2], '%sfk_ankle_jnt' %lr )
            cmds.rename(legChild[3], '%sfk_knee_jnt' %lr )
        
            # creating Controllers
            if lr == self.left:
                    ctlColor = 6
            else:
                    ctlColor = 12
            controller.circleController('%sfk_hip_ctl' %lr, 'yz', 2, color = ctlColor, lockAttr = ['tr', 'sc', 'vi'], lock = False)
            controller.circleController('%sfk_knee_ctl' %lr, 'yz', 2, color = ctlColor, lockAttr = ['tr', 'sc', 'vi'], lock = False)
            controller.circleController('%sfk_ankle_ctl' %lr, 'yz', 2, color = ctlColor, lockAttr = ['tr', 'sc', 'vi'], lock = False)
            controller.circleController('%sfk_ball_ctl' %lr, 'yz', 2, color = ctlColor, lockAttr = ['tr', 'sc', 'vi'], lock = False)
            
            
            for joints in fkLegJoints:
                cmds.select('%s%s_jnt' %(lr, joints), r = True)
                cmds.select('%s%s_ctl_grp' %(lr, joints), tgl = True)
                cmds.pointConstraint(weight = 1)
                cmds.orientConstraint(weight = 1)
                cmds.delete('%s%s_ctl_grp_pointConstraint1' %(lr, joints))
                cmds.delete('%s%s_ctl_grp_orientConstraint1' %(lr, joints))
                
                cmds.select('%s%s_ctl' %(lr, joints), r = True)
                cmds.select('%s%s_jnt' %(lr, joints), tgl = True)
                cmds.orientConstraint(weight = 1)
            
            cmds.select('%sfk_ball_ctl_grp' %lr, r = True)
            cmds.select('%sfk_ankle_ctl' %lr, tgl = True)  
            cmds.parent()
            cmds.select('%sfk_ankle_ctl_grp' %lr, r = True)
            cmds.select('%sfk_knee_ctl' %lr, tgl = True)   
            cmds.parent()
            cmds.select('%sfk_knee_ctl_grp' %lr, r = True)
            cmds.select('%sfk_hip_ctl' %lr, tgl = True)    
            cmds.parent()
       
        ###########FKIK Setting###############
            cmds.select('%sleg_extra_ctl' %lr)
            cmds.setAttr('%sleg_extra_ctl.tx' %lr, lock = True, keyable  = False, channelBox = False)
            cmds.setAttr('%sleg_extra_ctl.ty' %lr, lock = True, keyable  = False, channelBox = False)
            cmds.setAttr('%sleg_extra_ctl.tz' %lr, lock = True, keyable  = False, channelBox = False)
            cmds.setAttr('%sleg_extra_ctl.rx' %lr, lock = True, keyable  = False, channelBox = False)
            cmds.setAttr('%sleg_extra_ctl.ry' %lr, lock = True, keyable  = False, channelBox = False)
            cmds.setAttr('%sleg_extra_ctl.rz' %lr, lock = True, keyable  = False, channelBox = False)
            cmds.setAttr('%sleg_extra_ctl.sx' %lr, lock = True, keyable  = False, channelBox = False)
            cmds.setAttr('%sleg_extra_ctl.sy' %lr, lock = True, keyable  = False, channelBox = False)
            cmds.setAttr('%sleg_extra_ctl.sz' %lr, lock = True, keyable  = False, channelBox = False)
            cmds.setAttr('%sleg_extra_ctl.v' %lr, lock = True, keyable  = False, channelBox = False)
            ##############add Extra attributes####################
            cmds.addAttr(ln = 'FKIK', at = 'long', min = 0, max = 1)
            cmds.setAttr('%sleg_extra_ctl.FKIK' %lr, e = True, keyable = True)
            cmds.setAttr('%sleg_extra_ctl.FKIK' %lr, 1)
        
        #########FKIK Switch Node#############
            cmds.shadingNode('blendColors', n = '%sfkik_hip_Mux' %lr, asUtility = True)
            cmds.connectAttr('%sleg_extra_ctl.FKIK' %lr, '%sfkik_hip_Mux.blender' %lr, f = True)

            cmds.connectAttr('%sfk_hip_jnt.rotateX' %lr, '%sfkik_hip_Mux.color2R' %lr, f = True)
            cmds.connectAttr('%sfk_hip_jnt.rotateY' %lr, '%sfkik_hip_Mux.color2G' %lr, f = True)
            cmds.connectAttr('%sfk_hip_jnt.rotateZ' %lr, '%sfkik_hip_Mux.color2B' %lr, f = True)
            cmds.connectAttr('%sik_hip_jnt.rotateX' %lr, '%sfkik_hip_Mux.color1R' %lr, f = True)
            cmds.connectAttr('%sik_hip_jnt.rotateY' %lr, '%sfkik_hip_Mux.color1G' %lr, f = True)
            cmds.connectAttr('%sik_hip_jnt.rotateZ' %lr, '%sfkik_hip_Mux.color1B' %lr, f = True)
            cmds.connectAttr('%sfkik_hip_Mux.outputR' %lr, '%ship_jnt.rotateX' %lr, f = True)
            cmds.connectAttr('%sfkik_hip_Mux.outputG' %lr, '%ship_jnt.rotateY' %lr, f = True)
            cmds.connectAttr('%sfkik_hip_Mux.outputB' %lr, '%ship_jnt.rotateZ' %lr, f = True)
            
            cmds.shadingNode('blendColors', n = '%sfkik_knee_Mux' %lr, asUtility = True)
            cmds.connectAttr('%sleg_extra_ctl.FKIK' %lr, '%sfkik_knee_Mux.blender' %lr, f = True)
            cmds.connectAttr('%sfk_knee_jnt.rotateX' %lr, '%sfkik_knee_Mux.color2R' %lr, f = True)
            cmds.connectAttr('%sfk_knee_jnt.rotateY' %lr, '%sfkik_knee_Mux.color2G' %lr, f = True)
            cmds.connectAttr('%sfk_knee_jnt.rotateZ' %lr, '%sfkik_knee_Mux.color2B' %lr, f = True)
            cmds.connectAttr('%sik_knee_jnt.rotateX' %lr, '%sfkik_knee_Mux.color1R' %lr, f = True)
            cmds.connectAttr('%sik_knee_jnt.rotateY' %lr, '%sfkik_knee_Mux.color1G' %lr, f = True)
            cmds.connectAttr('%sik_knee_jnt.rotateZ' %lr, '%sfkik_knee_Mux.color1B' %lr, f = True)
            cmds.connectAttr('%sfkik_knee_Mux.outputR' %lr, '%sknee_jnt.rotateX' %lr, f = True)
            cmds.connectAttr('%sfkik_knee_Mux.outputG' %lr, '%sknee_jnt.rotateY' %lr, f = True)
            cmds.connectAttr('%sfkik_knee_Mux.outputB' %lr, '%sknee_jnt.rotateZ' %lr, f = True)
            
            cmds.shadingNode('blendColors', n = '%sfkik_ankle_Mux' %lr, asUtility = True)
            cmds.connectAttr('%sleg_extra_ctl.FKIK' %lr, '%sfkik_ankle_Mux.blender' %lr, f = True)
            cmds.connectAttr('%sfk_ankle_jnt.rotateX' %lr, '%sfkik_ankle_Mux.color2R' %lr, f = True)
            cmds.connectAttr('%sfk_ankle_jnt.rotateY' %lr, '%sfkik_ankle_Mux.color2G' %lr, f = True)
            cmds.connectAttr('%sfk_ankle_jnt.rotateZ' %lr, '%sfkik_ankle_Mux.color2B' %lr, f = True)
            cmds.connectAttr('%sik_ankle_jnt.rotateX' %lr, '%sfkik_ankle_Mux.color1R' %lr, f = True)
            cmds.connectAttr('%sik_ankle_jnt.rotateY' %lr, '%sfkik_ankle_Mux.color1G' %lr, f = True)
            cmds.connectAttr('%sik_ankle_jnt.rotateZ' %lr, '%sfkik_ankle_Mux.color1B' %lr, f = True)
            cmds.connectAttr('%sfkik_ankle_Mux.outputR' %lr, '%sankle_jnt.rotateX' %lr, f = True)
            cmds.connectAttr('%sfkik_ankle_Mux.outputG' %lr, '%sankle_jnt.rotateY' %lr, f = True)
            cmds.connectAttr('%sfkik_ankle_Mux.outputB' %lr, '%sankle_jnt.rotateZ' %lr, f = True)
            
            cmds.shadingNode('blendColors', n = '%sfkik_ball_Mux' %lr, asUtility = True)
            cmds.connectAttr('%sleg_extra_ctl.FKIK' %lr, '%sfkik_ball_Mux.blender' %lr, f = True)
            cmds.connectAttr('%sfk_ball_jnt.rotateX' %lr, '%sfkik_ball_Mux.color2R' %lr, f = True)
            cmds.connectAttr('%sfk_ball_jnt.rotateY' %lr, '%sfkik_ball_Mux.color2G' %lr, f = True)
            cmds.connectAttr('%sfk_ball_jnt.rotateZ' %lr, '%sfkik_ball_Mux.color2B' %lr, f = True)
            cmds.connectAttr('%sik_ball_jnt.rotateX' %lr, '%sfkik_ball_Mux.color1R' %lr, f = True)
            cmds.connectAttr('%sik_ball_jnt.rotateY' %lr, '%sfkik_ball_Mux.color1G' %lr, f = True)
            cmds.connectAttr('%sik_ball_jnt.rotateZ' %lr, '%sfkik_ball_Mux.color1B' %lr, f = True)
            cmds.connectAttr('%sfkik_ball_Mux.outputR' %lr, '%sball_jnt.rotateX' %lr, f = True)
            cmds.connectAttr('%sfkik_ball_Mux.outputG' %lr, '%sball_jnt.rotateY' %lr, f = True)
            cmds.connectAttr('%sfkik_ball_Mux.outputB' %lr, '%sball_jnt.rotateZ' %lr, f = True)
            
            ###Translate###
            cmds.shadingNode('blendColors', n = '%sfkik_knee_Translate_Mux' %lr, asUtility = True)
            cmds.connectAttr('%sleg_extra_ctl.FKIK' %lr, '%sfkik_knee_Translate_Mux.blender' %lr, f = True)
            cmds.connectAttr('%sfk_knee_jnt.translateX' %lr, '%sfkik_knee_Translate_Mux.color2R' %lr, f = True)
            cmds.connectAttr('%sfk_knee_jnt.translateY' %lr, '%sfkik_knee_Translate_Mux.color2G' %lr, f = True)
            cmds.connectAttr('%sfk_knee_jnt.translateZ' %lr, '%sfkik_knee_Translate_Mux.color2B' %lr, f = True)
            cmds.connectAttr('%sik_knee_jnt.translateX' %lr, '%sfkik_knee_Translate_Mux.color1R' %lr, f = True)
            cmds.connectAttr('%sik_knee_jnt.translateY' %lr, '%sfkik_knee_Translate_Mux.color1G' %lr, f = True)
            cmds.connectAttr('%sik_knee_jnt.translateZ' %lr, '%sfkik_knee_Translate_Mux.color1B' %lr, f = True)
            cmds.connectAttr('%sfkik_knee_Translate_Mux.outputR' %lr, '%sknee_jnt.translateX' %lr, f = True)
            cmds.connectAttr('%sfkik_knee_Translate_Mux.outputG' %lr, '%sknee_jnt.translateY' %lr, f = True)
            cmds.connectAttr('%sfkik_knee_Translate_Mux.outputB' %lr, '%sknee_jnt.translateZ' %lr, f = True)
            
            cmds.shadingNode('blendColors', n = '%sfkik_ankle_Translate_Mux' %lr, asUtility = True)
            cmds.connectAttr('%sleg_extra_ctl.FKIK' %lr, '%sfkik_ankle_Translate_Mux.blender' %lr, f = True)
            cmds.connectAttr('%sfk_ankle_jnt.translateX' %lr, '%sfkik_ankle_Translate_Mux.color2R' %lr, f = True)
            cmds.connectAttr('%sfk_ankle_jnt.translateY' %lr, '%sfkik_ankle_Translate_Mux.color2G' %lr, f = True)
            cmds.connectAttr('%sfk_ankle_jnt.translateZ' %lr, '%sfkik_ankle_Translate_Mux.color2B' %lr, f = True)
            cmds.connectAttr('%sik_ankle_jnt.translateX' %lr, '%sfkik_ankle_Translate_Mux.color1R' %lr, f = True)
            cmds.connectAttr('%sik_ankle_jnt.translateY' %lr, '%sfkik_ankle_Translate_Mux.color1G' %lr, f = True)
            cmds.connectAttr('%sik_ankle_jnt.translateZ' %lr, '%sfkik_ankle_Translate_Mux.color1B' %lr, f = True)
            cmds.connectAttr('%sfkik_ankle_Translate_Mux.outputR' %lr, '%sankle_jnt.translateX' %lr, f = True)
            cmds.connectAttr('%sfkik_ankle_Translate_Mux.outputG' %lr, '%sankle_jnt.translateY' %lr, f = True)
            cmds.connectAttr('%sfkik_ankle_Translate_Mux.outputB' %lr, '%sankle_jnt.translateZ' %lr, f = True)
            ####FKIK ctl Hide                      
            cmds.connectAttr('%sleg_extra_ctl.FKIK' %lr, '%sleg_ctl.visibility' %lr , f = True)
            cmds.connectAttr('%sleg_extra_ctl.FKIK' %lr, '%sleg_pv_ctl.visibility' %lr , f = True)
            cmds.shadingNode('condition', n = '%sfkik_leg_ctl_Mux' %lr, asUtility = True)
            cmds.setAttr('%sfkik_leg_ctl_Mux.secondTerm' %lr, 0)
            cmds.setAttr('%sfkik_leg_ctl_Mux.operation' %lr, 0)
            cmds.setAttr('%sfkik_leg_ctl_Mux.colorIfTrueR' %lr, 1)
            cmds.setAttr('%sfkik_leg_ctl_Mux.colorIfFalseR' %lr, 0)
            
            cmds.connectAttr('%sleg_extra_ctl.FKIK' %lr, '%sfkik_leg_ctl_Mux.firstTerm' %lr, f = True)
            cmds.connectAttr('%sfkik_leg_ctl_Mux.outColorR' %lr, '%sfk_hip_ctl.visibility' %lr, f = True)
            cmds.connectAttr('%sfkik_leg_ctl_Mux.outColorR' %lr, '%sfk_knee_ctl.visibility' %lr, f = True)
            cmds.connectAttr('%sfkik_leg_ctl_Mux.outColorR' %lr, '%sfk_ankle_ctl.visibility' %lr, f = True)
            
            #########Hiding Leg###########
            cmds.setAttr('%sfk_hip_jnt.visibility' %lr, 0)
            cmds.setAttr('%sik_hip_jnt.visibility' %lr, 0)

    def stretchIkLeg(self):
        """
        stretch IK Leg
        """
        
        for lr in self.lrPrefix:
            cmds.select('%sleg_extra_ctl' %lr)
            cmds.addAttr(ln = 'Stretch_IK', at = 'long', min = 0, max = 1)
            cmds.setAttr('%sleg_extra_ctl.Stretch_IK' %lr, e = True, keyable = True)

            #- Applies when both L, R leg's lengths are same. 
                    
            #- Installing Locator
            cmds.spaceLocator(n = '%ship_stretch_loc' %lr)
            if lr == self.left:
                    cmds.move(self.leftHipPos[0], self.leftHipPos[1], self.leftHipPos[2])
            else:
                    cmds.move(-self.leftHipPos[0], self.leftHipPos[1], self.leftHipPos[2])
            cmds.select('%ship_jnt' %lr, r = True)
            cmds.select('%ship_stretch_loc' %lr, tgl = True)
            cmds.pointConstraint(offset = [0, 0, 0], weight = 1)
                 
            cmds.spaceLocator(n = '%sankle_stretch_loc' %lr)
            if lr == self.left:
                    cmds.move(self.leftAnklePos[0], self.leftAnklePos[1], self.leftAnklePos[2])
            else:
                    cmds.move(-self.leftAnklePos[0], self.leftAnklePos[1], self.leftAnklePos[2])
            cmds.select('%sleg_ctl' %lr, r = True)
            cmds.select('%sankle_stretch_loc' %lr, tgl = True)
            cmds.pointConstraint(offset = [0, 0, 0], weight = 1)
           
            self.util.group(['%ship_stretch_loc' %lr, '%sankle_stretch_loc' %lr], '%sstretch_leg_grp' %lr)
            #cmds.select('%sstretch_leg_grp' %lr, r = True)
            #cmds.select('Puck', tgl = True)
            #cmds.parent()
                                            
            upperLegLength = [self.leftKneePos[0] - self.leftHipPos[0], self.leftKneePos[1] - self.leftHipPos[1], self.leftKneePos[2] - self.leftHipPos[2]]
            lowerLegLength = [self.leftAnklePos[0] - self.leftKneePos[0], self.leftAnklePos[1] - self.leftKneePos[1], self.leftAnklePos[2] - self.leftKneePos[2]]
            legLength = math.sqrt(upperLegLength[0]*upperLegLength[0]+upperLegLength[1]*upperLegLength[1]+upperLegLength[2]*upperLegLength[2])+math.sqrt(lowerLegLength[0]*lowerLegLength[0]+lowerLegLength[1]*lowerLegLength[1]+lowerLegLength[2]*lowerLegLength[2])
 
            #- Divided value by the scale of Puck.... distance between hip and ankle
            cmds.shadingNode('multiplyDivide', n = '%sstretch_legIK_Length_MulDiv' %lr, asUtility = True)
            cmds.setAttr('%sstretch_legIK_Length_MulDiv.operation' %lr, 1)
            cmds.setAttr('%sstretch_legIK_Length_MulDiv.input1X' %lr, legLength)
            cmds.connectAttr('%s.scaleX' %partDict.globalCtl, '%sstretch_legIK_Length_MulDiv.input2X' %lr)
           
            #- Distance between hip and ankle CTRL
            cmds.shadingNode('distanceBetween', n = '%sstretch_legIK_Distance' %lr, asUtility = True)
            cmds.connectAttr('%ship_stretch_loc.translateX' %lr, '%sstretch_legIK_Distance.point1X' %lr)
            cmds.connectAttr('%ship_stretch_loc.translateY' %lr, '%sstretch_legIK_Distance.point1Y' %lr)
            cmds.connectAttr('%ship_stretch_loc.translateZ' %lr, '%sstretch_legIK_Distance.point1Z' %lr)
            cmds.connectAttr('%sankle_stretch_loc.translateX' %lr, '%sstretch_legIK_Distance.point2X' %lr)
            cmds.connectAttr('%sankle_stretch_loc.translateY' %lr, '%sstretch_legIK_Distance.point2Y' %lr)
            cmds.connectAttr('%sankle_stretch_loc.translateZ' %lr, '%sstretch_legIK_Distance.point2Z' %lr)
            cmds.connectAttr('%sstretch_legIK_Distance.distance' %lr, '%sstretch_legIK_Length_MulDiv.input1Y' %lr)
            cmds.connectAttr('%s.scaleX' %partDict.globalCtl, '%sstretch_legIK_Length_MulDiv.input2Y' %lr)
            
            #- condition node calculate length and compare and do shit
            cmds.shadingNode('condition', n = '%sstretch_legIK_Con' %lr, asUtility = True)
            cmds.connectAttr('%sstretch_legIK_Length_MulDiv.outputY' %lr, '%sstretch_legIK_Con.firstTerm' %lr)
            cmds.connectAttr('%sstretch_legIK_Length_MulDiv.outputX' %lr, '%sstretch_legIK_Con.secondTerm' %lr)
            cmds.setAttr('%sstretch_legIK_Con.operation' %lr, 2)
            
            #- Stretch Ratio
            cmds.shadingNode('multiplyDivide', n = '%sstretch_legIK_ratio_MulDiv' %lr, asUtility = True)
            cmds.connectAttr('%sstretch_legIK_Length_MulDiv.outputY' %lr, '%sstretch_legIK_ratio_MulDiv.input1X' %lr)
            cmds.connectAttr('%sstretch_legIK_Length_MulDiv.outputX' %lr, '%sstretch_legIK_ratio_MulDiv.input2X' %lr)
            cmds.setAttr('%sstretch_legIK_ratio_MulDiv.operation' %lr, 2)
            
            #- Last Mux
            cmds.shadingNode('blendColors', n = '%sLeg_Stretch_Mux' %lr, asUtility = True)
            cmds.connectAttr('%sstretch_legIK_Con.outColorR' %lr, '%sLeg_Stretch_Mux.blender' %lr)
            cmds.setAttr('%sLeg_Stretch_Mux.color1R' %lr, 1)
            cmds.connectAttr('%sstretch_legIK_ratio_MulDiv.outputX' %lr,'%sLeg_Stretch_Mux.color2R' %lr)
            
            #- stretch MUX
            cmds.shadingNode('blendColors', n = '%sleg_stretchYesNo_mux' %lr, asUtility = True)
            cmds.connectAttr('%s%s.Stretch_IK' %(lr, self.extraCtl), '%sleg_stretchYesNo_mux.blender' %lr)
            cmds.setAttr('%sleg_stretchYesNo_mux.color2R' %lr, 1)
            cmds.connectAttr('%sLeg_Stretch_Mux.outputR' %lr, '%sleg_stretchYesNo_mux.color1R' %lr)
            
            cmds.connectAttr('%sleg_stretchYesNo_mux.outputR' %lr, '%ship_jnt.scaleX' %lr)
            cmds.connectAttr('%sleg_stretchYesNo_mux.outputR' %lr, '%sknee_jnt.scaleX' %lr)
            
    def legCleanup(self):
        for lr in self.lrPrefix:
            #- hide heel pivot
            cmds.setAttr('%sheel_PivotPosition.visibility' %lr, 0)

            #- placing extra control
            cmds.select('%sleg_extra_ctl_grp' %lr, r = True)
            cmds.select('%sankle_jnt' %lr, tgl = True)
            cmds.parent()
            
            #- hide attribute
            cmds.setAttr('%sleg_pv_ctl.visibility' %lr, keyable = False, channelBox = False)
            cmds.setAttr('%sleg_ctl.visibility' %lr, keyable = False, channelBox = False)
            
            #- clean up hierarchy
            self.util.group(['%sik_hip_jnt' %lr, '%sfk_hip_jnt' %lr], '%sfkik_leg_jnt_grp' %lr)
            self.util.group(['%ship_jnt' %lr, '%sfkik_leg_jnt_grp' %lr], '%sleg_jnt_grp' %lr)
            
            #- hide stretchIK locator
            cmds.setAttr('%sstretch_leg_grp.visibility' %lr, 0)
                        
        self.util.group(['l_leg_jnt_grp', 'r_leg_jnt_grp'], 'leg_jnt_grp')    
        children = ['l_leg_pv_ctl_grp', 'r_leg_pv_ctl_grp',
                    'l_fk_hip_ctl_grp', 'r_fk_hip_ctl_grp',
                    'l_leg_ctl_grp', 'r_leg_ctl_grp']
        self.util.group(children, 'leg_ctl_grp')
        self.util.group(['l_stretch_leg_grp', 'r_stretch_leg_grp'], 'stretch_leg_grp')
        self.util.group(['l_heel_PivotPosition', 'r_heel_PivotPosition', 'stretch_leg_grp'], 'leg_misc_grp')    
        
        
            