############################################################################
#                       Auto Rigging Scrpit 2010                           #
#                          by Jonghwan Hwang                               #
#                         All Rights Reserved                              #
############################################################################

import maya.cmds as cmds
import partDic
reload(partDic)
import math

#make libary
#make each part as class 
#use object

L_o_R = ['L_', 'R_']

class Auto_Rig:
        def __init__(self):
                self.adjustCtrls = []
                self.spineJoints = partDic.spineJoints
                self.legJoints = partDic.legJoints
                self.legJoints_R = partDic.legJointsR
                self.armJoints = partDic.armJoints
                self.armJoints_R = partDic.armJointsR
                self.handJoints = partDic.handJoints
                self.fingerJoints = partDic.fingerJoints
                self.tailJoints = partDic.tailJoints
                
                self.placeLocs = partDic.placeLocs
                
        def placeJoints(self):
                for oneLoc in self.placeLocs.keys():
                    print self.placeLocs[oneLoc]
                    cmds.spaceLocator( n = oneLoc) #Joint control
                    cmds.move(self.placeLocs[oneLoc][0][0], self.placeLocs[oneLoc][0][1], self.placeLocs[oneLoc][0][2], r = True)
                    cmds.scale(self.placeLocs[oneLoc][1], self.placeLocs[oneLoc][1], self.placeLocs[oneLoc][1]) 
                    if self.placeLocs[oneLoc][2]: 
                        cmds.setAttr(oneLoc + '.' + self.placeLocs[oneLoc][2] , lock = True)#CTRL Move
                    
                    self.adjustCtrls.append(oneLoc)
                
                cmds.select('Pelvis_Adjust_CTRL', r = True)
                cmds.select('Root_Adjust_CTRL', tgl = True)
                cmds.parent()
                
        def placeFingerJoints(self, No_Fingers, Thumb_YN):
    
                ###Fingers Count####
                #print No_Fingers
                #print Thumb_YN
                if No_Fingers == 4:
                        self.fingerJointsLocal = self.fingerJoints[0:]
                else:
                        self.fingerJointsLocal = self.fingerJoints[0:No_Fingers-4]
                if Thumb_YN == 'No':
                        self.fingerJointsLocal = self.fingerJointsLocal[1:]
                
                print self.fingerJointsLocal
                ##Palm##
                cmds.select(cl = True)
                cmds.spaceLocator( n = 'L_Palm_Adjust_CTRL') #Joint control
                cmds.move(9.7, 20, -0.3, r = True)
                self.adjustCtrls.append('L_Palm_Adjust_CTRL')
                
                ##Fingers##
                for i in range(len(self.fingerJointsLocal)):
                        for j in range(5):
                                cmds.select(cl = True)
                                cmds.spaceLocator( n = 'L_%s%s_Adjust_CTRL' %(self.fingerJointsLocal[i], j)) #Joint control
                                cmds.scale(0.3, 0.3, 0.3)
                                if Thumb_YN == 'Yes':
                                        if j == 0:
                                                cmds.move(10.5+j, 20, 0.5-0.3*i, r = True)
                                        elif j == 1:
                                                cmds.move(10.5+j, 20, 0.7-0.4*i, r = True)
                                        elif i == 0:
                                                cmds.move(11+0.8*j, 19.5, 0.7+0.7, r = True)
                                        elif i == 1:
                                                cmds.move(11+0.8*j, 20.2, 0.7-0.5*i, r = True)
                                        elif i == 2:
                                                cmds.move(11+0.85*j, 20.5, 0.7-0.5*i, r = True)
                                        elif i == 3:
                                                cmds.move(11+0.82*j, 20.3, 0.7-0.5*i, r = True)
                                        elif i == 4:
                                                cmds.move(11+0.65*j, 20, 0.7-0.5*i, r = True)
                                        else:
                                                cmds.move(11+0.7*j, 20, 0.7-0.5*i, r = True)

                                elif Thumb_YN == 'No':
                                        if j == 0:
                                                cmds.move(10.5+j, 20, 0.5-0.3*i, r = True)
                                        elif j == 1:
                                                cmds.move(10.5+j, 20, 0.7-0.4*i, r = True)
                                        elif i == 0:
                                                cmds.move(11+0.8*j, 20.2, 0.7-0.5*i, r = True)
                                        elif i == 1:
                                                cmds.move(11+0.85*j, 20.5, 0.7-0.5*i, r = True)
                                        elif i == 2:
                                                cmds.move(11+0.82*j, 20.3, 0.7-0.5*i, r = True)
                                        elif i == 3:
                                                cmds.move(11+0.65*j, 20, 0.7-0.5*i, r = True)
                                        else:
                                                cmds.move(11+0.7*j, 20, 0.7-0.5*i, r = True)
                                self.adjustCtrls.append('L_%s%s_Adjust_CTRL' %(self.fingerJointsLocal[i], j))                      

                #####parent finger joint adjust ctrl#############
                for i in range(len(self.fingerJointsLocal)):
                        for j in range(4):
                                cmds.select(cl = True)
                                cmds.select('L_%s%s_Adjust_CTRL' %(self.fingerJointsLocal[i], j+1), r = True) #Joint control
                                cmds.select('L_%s%s_Adjust_CTRL' %(self.fingerJointsLocal[i], j), tgl = True)
                                cmds.parent()
                        cmds.select('L_%s0_Adjust_CTRL' %self.fingerJointsLocal[i], r = True) #Joint control.
                        cmds.select('L_Palm_Adjust_CTRL', tgl = True)
                        cmds.parent()
                cmds.select('L_Palm_Adjust_CTRL', r = True)
                cmds.select('L_Wrist_Adjust_CTRL', tgl = True)
                cmds.parent()
                
                if Thumb_YN == 'Yes':
                        cmds.delete('L_Thumb4_Adjust_CTRL')
                        self.adjustCtrls.remove('L_Thumb4_Adjust_CTRL')
                
                cmds.select(cl = True)
                
        def placeTailJoints(self):
                #######Tail Position###########
                cmds.select(cl = True)
                cmds.spaceLocator( n = 'Tail0_Adjust_CTRL') #Joint control
                cmds.move(0, 12, -3, r = True)
                cmds.setAttr('Tail0_Adjust_CTRL.tx', lock = True)#CTRL Move
                
                cmds.spaceLocator( n = 'Tail1_Adjust_CTRL') #Joint control
                cmds.move(0, 12, -13, r = True)
                cmds.setAttr('Tail1_Adjust_CTRL.tx', lock = True)#CTRL Move
                
                cmds.select('Tail1_Adjust_CTRL', r = True)
                cmds.select('Tail0_Adjust_CTRL', tgl = True)
                cmds.parent()
                cmds.setAttr('Tail1_Adjust_CTRL.ty', lock = True)
        
        def confirmJoints(self, No_Fingers, Thumb_YN):
                                
                ####Root Location
                self.rootPos = cmds.xform('Root_Adjust_CTRL', q = True, t = True)
                
                        
                ####Getting Ball and Toe Location
                self.leftHipPos = cmds.xform('L_Hip_Adjust_CTRL', q = True, ws = True, t = True)
                self.leftKneePos = cmds.xform('L_Knee_Adjust_CTRL', q = True, ws = True, t = True)
                self.leftAnklePos = cmds.xform('L_Ankle_Adjust_CTRL', q = True, ws = True, t = True)
                self.leftBallPos = cmds.xform('L_Ball_Adjust_CTRL', q = True, ws = True, t = True)
                self.leftToePos = cmds.xform('L_Toe_Adjust_CTRL', q = True, ws = True, t = True)
                self.leftHeelPos = cmds.xform('L_Heel_PivotPosition', q = True, ws = True, t = True)
                self.leftSideInPos = cmds.xform('L_SideIn_PivotPosition', q = True, ws = True, t = True)
                self.leftSideOutPos = cmds.xform('L_SideOut_PivotPosition', q = True, ws = True, t = True)
                self.leftScapulaPos = cmds.xform('L_Scapula_Adjust_CTRL', q = True, ws = True, t = True)
                self.leftShoulderPos = cmds.xform('L_Shoulder_Adjust_CTRL', q = True, ws = True, t = True)
                self.leftElbowPos = cmds.xform('L_Elbow_Adjust_CTRL', q = True, ws = True, t = True)
                self.leftWristPos = cmds.xform('L_Wrist_Adjust_CTRL', q = True, ws = True, t = True)
                self.leftPalmPos = cmds.xform('L_Palm_Adjust_CTRL', q = True, ws = True, t = True)
                
                
                ##########getting location for spine
                self.spine1Pos = cmds.xform('Spine1_Adjust_CTRL', q = True, t = True)
                self.spine2Pos = cmds.xform('Spine2_Adjust_CTRL', q = True, t = True)
                self.spine3Pos = cmds.xform('Spine3_Adjust_CTRL', q = True, t = True)
                self.spine4Pos = cmds.xform('Spine4_Adjust_CTRL', q = True, t = True)
                self.neckBasePos = cmds.xform('NeckBase_Adjust_CTRL', q = True, t = True)
                self.headPos = cmds.xform('Head_Adjust_CTRL', q = True, t = True)
                self.jawPos = cmds.xform('Jaw_Adjust_CTRL', q = True, t = True)
                self.jawAimPos = cmds.xform('JawAim_Adjust_CTRL', q = True, t = True)
                self.spinePosList = [self.spine1Pos, self.spine2Pos, self.spine3Pos, self.spine4Pos, self.neckBasePos, self.headPos]
                
                
                ###R_Foot SideIN, OUT HEEL Locators#####
                cmds.spaceLocator(n = 'R_Heel_PivotPosition', p = (-self.leftHeelPos[0], self.leftHeelPos[1], self.leftHeelPos[2]))
                cmds.spaceLocator(n = 'R_SideIn_PivotPosition', p = (0,0,0))
                cmds.move(-self.leftSideInPos[0], self.leftSideInPos[1], self.leftSideInPos[2])
                cmds.spaceLocator(n = 'R_SideOut_PivotPosition', p = (0,0,0))
                cmds.move(-self.leftSideOutPos[0], self.leftSideOutPos[1], self.leftSideOutPos[2])
                
                cmds.select('Pelvis_Adjust_CTRL', r = True)
                cmds.parent(w = True)
                                
                ###Unparent Fingers
                cmds.select(cl = True)
                cmds.select('L_Palm_Adjust_CTRL', r = True)
                cmds.parent(w = True)
                
                if Thumb_YN == 'Yes':
                        for i in range(4):
                                cmds.select('L_Thumb%s_Adjust_CTRL' %i, r = True)
                                cmds.parent(w = True)
                
                        for i in range(len(self.fingerJointsLocal)-1):
                                for j in range(5):
                                        cmds.select(cl = True)
                                        cmds.select('L_%s%s_Adjust_CTRL' %(self.fingerJointsLocal[i+1], j), r = True)
                                        cmds.parent(w = True)
                else:
                        for i in range(len(self.fingerJointsLocal)):
                                for j in range(5):
                                        cmds.select(cl = True)
                                        cmds.select('L_%s%s_Adjust_CTRL' %(self.fingerJointsLocal[i], j), r = True)
                                        cmds.parent(w = True)                   
                
                locToSkip = ['L_Heel_PivotPosition', 'L_SideIn_PivotPosition', 'L_SideOut_PivotPosition']
                for Joint in self.adjustCtrls:
                    if Joint not in locToSkip:
                        cmds.select(cl = True)
                        Joint_Position = cmds.xform(Joint, q = True, t = True)
                        Joint_Name = Joint[0:-12]
                        cmds.createNode('transform', n = '%s_GRP' %Joint_Name)
                        cmds.move(Joint_Position[0], Joint_Position[1], Joint_Position[2])
                        cmds.joint(n = Joint_Name, p = Joint_Position) #Create Joint
                
                for oneCTRL in self.adjustCtrls:
                    if oneCTRL not in locToSkip:
                        cmds.delete(oneCTRL)
                
                ########Spine Joint Parent
                for i in range(len(self.spineJoints)-1):
                        cmds.select(cl = True)
                        print '...............', self.spineJoints[i+1]
                        cmds.select(self.spineJoints[i+1], r = True)
                        cmds.select(self.spineJoints[i], tgl = True)
                        cmds.parent()
                
                ########Leg Joint Parent
                for i in range(len(self.legJoints)-1):
                        cmds.select(cl = True)
                        cmds.select(self.legJoints[i+1], r = True)
                        cmds.select(self.legJoints[i], tgl = True)
                        cmds.parent()   
                
                ########Arm Joint Parent
                for i in range(len(self.armJoints)-1):
                        cmds.select(cl = True)
                        cmds.select(self.armJoints[i+1], r = True)
                        cmds.select(self.armJoints[i], tgl = True)
                        cmds.parent()   
                cmds.select('L_Palm', r = True)
                cmds.select('L_Wrist', tgl = True)
                cmds.parent()
                
                if Thumb_YN == 'Yes':
                        for i in range(3):
                                cmds.select(cl = True)
                                cmds.select('L_Thumb%s_GRP' %(i+1), r = True) #Joint control
                                cmds.select('L_Thumb%s' %i, tgl = True)
                                cmds.parent()
                        cmds.select('L_Thumb0', r = True) #Joint control.
                        cmds.select('L_Palm', tgl = True)
                        cmds.parent()
                
                        for i in range(len(self.fingerJointsLocal)-1):
                                for j in range(4):
                                        cmds.select(cl = True)
                                        cmds.select('L_%s%s_GRP' %(self.fingerJointsLocal[i+1], j+1), r = True) #Joint control
                                        cmds.select('L_%s%s' %(self.fingerJointsLocal[i+1], j), tgl = True)
                                        cmds.parent()
                                cmds.select('L_%s0' %self.fingerJointsLocal[i+1], r = True) #Joint control.
                                cmds.select('L_Palm', tgl = True)
                                cmds.parent()
                else:
                        for i in range(len(self.fingerJointsLocal)):
                                for j in range(4):
                                        cmds.select(cl = True)
                                        cmds.select('L_%s%s_GRP' %(self.fingerJointsLocal[i], j+1), r = True) #Joint control
                                        cmds.select('L_%s%s' %(self.fingerJointsLocal[i], j), tgl = True)
                                        cmds.parent()
                                cmds.select('L_%s0' %self.fingerJointsLocal[i], r = True) #Joint control.
                                cmds.select('L_Palm', tgl = True)
                                cmds.parent()           
                cmds.select('L_Hip', r = True)
                cmds.mirrorJoint(mirrorYZ = True, mirrorBehavior = True, searchReplace = ['L_', 'R_']);
                cmds.select('L_Scapula', r = True)
                cmds.mirrorJoint(mirrorYZ = True, mirrorBehavior = True, searchReplace = ['L_', 'R_']);
                
                cmds.delete('NeckBase_GRP', 'Spine1_GRP', 'Spine2_GRP', 'Spine3_GRP', 'Spine4_GRP', 'Head_GRP', 'Jaw_GRP', 'JawAim_GRP' )
                cmds.delete('Pelvis_GRP', 'L_Hip_GRP', 'L_Knee_GRP', 'L_Ankle_GRP', 'L_Ball_GRP', 'L_Toe_GRP', 'L_Scapula_GRP', 'L_Shoulder_GRP')
                cmds.delete('L_Elbow_GRP', 'L_Wrist_GRP', 'L_Palm_GRP', 'L_Thumb0_GRP', 'L_Index0_GRP', 'L_Middle0_GRP', 'L_Ring0_GRP', 'L_Pinky0_GRP')
                
                
        def tailConfirm(self):
                cmds.setAttr('Tail0_Adjust_CTRL.tx', lock = False)
                cmds.setAttr('Tail1_Adjust_CTRL.tx', lock = False)
                cmds.setAttr('Tail1_Adjust_CTRL.ty', lock = False)

                #####Unparent Tail Tip#####
                cmds.select('Tail1_Adjust_CTRL', r = True)
                cmds.parent(w = True)
                                
                ####deciding Tail Joint number########
                Tail0_Pos = cmds.xform('Tail0_Adjust_CTRL', ws = True, q = True, t =True)
                Tail1_Pos = cmds.xform('Tail1_Adjust_CTRL', ws = True, q = True, t =True)
                self.numTailJoints = int((Tail0_Pos[2]-Tail1_Pos[2])/(self.rootPos[1]/10))
                print self.rootPos[1]
                print self.numTailJoints
                Tail_Joint_Space = (Tail1_Pos[2]-Tail0_Pos[2])/self.numTailJoints
                
                cmds.select(cl = True)
                ####Create Joints#######
                space_Temp = 0
                for i in range(self.numTailJoints+1):
                        cmds.joint(n = 'Tail%s' %i, p =(Tail0_Pos[0], Tail0_Pos[1], Tail0_Pos[2]-space_Temp))
                        space_Temp = space_Temp - Tail_Joint_Space
                        cmds.rotate(0, 90, 0, 'Tail%s.rotateAxis' %i, r = True, os = True) 
                cmds.delete('Tail0_Adjust_CTRL')
                cmds.delete('Tail1_Adjust_CTRL')
                
        
        def fkTailSetup(self):
                cmds.select('Tail0', r = True)
                cmds.duplicate(rr = True)
                cmds.rename('FK_Tail0')
                FK_Tail_Joints_rest = cmds.listRelatives(ad = True)
                FK_Tail_Joints = ['FK_Tail0']
                Length_FK_Tail_Joints = len(FK_Tail_Joints_rest)
                for i in range(Length_FK_Tail_Joints):
                        FK_Tail_Joints.append(FK_Tail_Joints_rest[Length_FK_Tail_Joints-i-1])                   
                
                ########Renaming FK Tail Joints###########
                for i in range(len(FK_Tail_Joints)-1):
                        temp = cmds.listRelatives('%s' %FK_Tail_Joints[i], f = True, c = True)
                        cmds.select('%s' %temp[0])
                        cmds.rename('FK_%s' %FK_Tail_Joints[i+1])
                        temp = cmds.listRelatives('%s' %FK_Tail_Joints[i], c = True)
                        FK_Tail_Joints[i+1] = temp[0]
                
                ########Making Controllers################
                for i in range(len(FK_Tail_Joints)-1):
                        cmds.createNode('transform', n = '%s_CTRL_GRP' %FK_Tail_Joints[i])
                        cmds.circle( n = '%s_CTRL' %FK_Tail_Joints[i], nr=(1, 0, 0), c=(0, 0, 0), r = 2 )
                        cmds.select('%s_CTRL_GRP' %FK_Tail_Joints[i], tgl = True)
                        cmds.parent()
                        cmds.select('%s_CTRL_GRP' %FK_Tail_Joints[i], r = True )
                        Tail_CTRL_Pos = cmds.xform('%s' %FK_Tail_Joints[i], q = True, t = True, ws = True)
                        cmds.move(Tail_CTRL_Pos[0], Tail_CTRL_Pos[1], Tail_CTRL_Pos[2])
                        cmds.select('%s' %FK_Tail_Joints[i], r =True)
                        cmds.select('%s_CTRL_GRP' %FK_Tail_Joints[i], tgl = True )
                        cmds.orientConstraint(weight = True)
                        cmds.delete('%s_CTRL_GRP_orientConstraint1' %FK_Tail_Joints[i])
                        cmds.select('%s_CTRL' %FK_Tail_Joints[i], r = True)
                        cmds.select('%s' %FK_Tail_Joints[i], tgl = True)
                        cmds.orientConstraint(weight = True)
                
                ###########Parenting Controllers#########
                for i in range(len(FK_Tail_Joints)-2):
                        temp = len(FK_Tail_Joints)-2
                        cmds.select('%s_CTRL_GRP' %FK_Tail_Joints[i-temp-1], r = True)
                        cmds.select('%s_CTRL' %FK_Tail_Joints[i-temp-2], tgl = True)
                        cmds.parent()
                
                #for joint in FK_Tail_Joints:
                #       cmds.connectAttr('%s.rotate' %joint, '%s.rotate' %joint[3:])
                
                cmds.createNode('transform', n = 'Tail_Joint_GRP')
                cmds.select('Tail0', r = True)
                cmds.select('Tail_Joint_GRP', tgl = True)
                cmds.parent()
                
                cmds.createNode('transform', n = 'FK_Tail_Joint_GRP')
                cmds.select('FK_Tail0', r = True)
                cmds.select('FK_Tail_Joint_GRP', tgl = True)
                cmds.parent()
                cmds.createNode('transform', n = 'FK_Tail_GRP')
                
                cmds.select('FK_Tail_Joint_GRP', r = True)
                cmds.select('FK_Tail0_CTRL_GRP', add = True)
                cmds.select('FK_Tail_GRP', tgl = True)
                cmds.parent()
                
                cmds.createNode('transform', n = 'Tail_GRP')
                cmds.select('Tail_Joint_GRP', r = True)
                cmds.select('FK_Tail_GRP', add = True)
                cmds.select('Tail_GRP', tgl = True)
                cmds.parent()
                cmds.select('Tail_GRP', r = True)
                cmds.select('Puck', tgl = True)
                cmds.parent()
                
                cmds.select('Root', r = True)
                cmds.select('FK_Tail_GRP', tgl = True)
                cmds.parentConstraint(weight = 1, mo = True)
                
                cmds.select('Root', r = True)
                cmds.select('Tail_Joint_GRP', tgl = True)
                cmds.parentConstraint(weight = 1, mo = True)
                
                cmds.setAttr('FK_Tail0.visibility', 0)
                
        def ikTailSetup(self):
                cmds.select('Tail0', r = True)
                cmds.duplicate(rr = True)
                cmds.parent(w = True)
                cmds.rename('IK_Tail0')
                IK_Tail_Joints_rest = cmds.listRelatives(ad = True)
                IK_Tail_Joints = ['IK_Tail0']
                Length_IK_Tail_Joints = len(IK_Tail_Joints_rest)
                for i in range(Length_IK_Tail_Joints):
                        IK_Tail_Joints.append(IK_Tail_Joints_rest[Length_IK_Tail_Joints-i-1])                   
                
                ########Renaming IK Tail Joints###########
                for i in range(len(IK_Tail_Joints)-1):
                        temp = cmds.listRelatives('%s' %IK_Tail_Joints[i], f = True, c = True)
                        cmds.select('%s' %temp[0])
                        cmds.rename('IK_%s' %IK_Tail_Joints[i+1])
                        temp = cmds.listRelatives('%s' %IK_Tail_Joints[i], c = True)
                        IK_Tail_Joints[i+1] = temp[0]
                
                #####Install IK Handle##########                
                cmds.select('IK_Tail0.rotatePivot', r = True)
                cmds.select('IK_Tail%s.rotatePivot' %str(len(IK_Tail_Joints)-1), add= True)
                cmds.ikHandle(sol = 'ikSplineSolver', n = 'Tail_IK_Handle')
                cmds.rename('curve1', 'Tail_IK_Curve')
                cmds.select('Tail_IK_Curve.cv[0]', r = True)
                cluster0_Pos = cmds.xform('Tail_IK_Curve.cv[0]', q = True, t = True)
                cmds.select('Tail_IK_Curve.cv[1]', r = True)
                cluster1_Pos = cmds.xform('Tail_IK_Curve.cv[1]', q = True, t = True)
                cmds.select('Tail_IK_Curve.cv[2]', r = True)
                cluster2_Pos = cmds.xform('Tail_IK_Curve.cv[2]', q = True, t = True)
                cmds.select('Tail_IK_Curve.cv[3]', r = True)
                cluster3_Pos = cmds.xform('Tail_IK_Curve.cv[3]', q = True, t = True)
                
                ##########Tail IK CTRLs########
                for i in range(4):
                        cmds.createNode('transform', n = 'IK_Tail%s_CTRL_GRP' %i)
                        cmds.circle( n = 'IK_Tail%s_CTRL' %i, nr=(1, 0, 0), c=(0, 0, 0), r = 3 )
                        cmds.select('IK_Tail%s_CTRL_GRP' %i, tgl = True)
                        cmds.parent()
                        spaceTemp = int(self.numTailJoints/4)*i
                        print 'self.numTailJoints = %s'%self.numTailJoints
                        print 'spaceTemp = %s' %spaceTemp
                        cmds.select('IK_Tail%s' %spaceTemp, r = True)
                        cmds.select('IK_Tail%s_CTRL_GRP' %i, tgl = True )
                        cmds.pointConstraint(weight = 1)
                        cmds.orientConstraint(weight = 1)
                        cmds.delete('IK_Tail%s_CTRL_GRP_pointConstraint1' %i)
                        cmds.delete('IK_Tail%s_CTRL_GRP_orientConstraint1' %i)
                        #if i == 0:
                        #       cmds.move(cluster0_Pos[0], cluster0_Pos[1], cluster0_Pos[2])    
                        #elif i == 1:
                        #       cmds.move(cluster1_Pos[0], cluster1_Pos[1], cluster1_Pos[2])    
                        #elif i == 2:
                        #       cmds.move(cluster2_Pos[0], cluster2_Pos[1], cluster2_Pos[2])    
                        #elif i == 3:
                        #       cmds.move(cluster3_Pos[0], cluster3_Pos[1], cluster3_Pos[2])    
                        cmds.select('Tail_IK_Curve.cv[%i]' %i, r = True)                        
                        cmds.cluster(n = 'Tail_Cluster%s' %i)
                        cmds.select('IK_Tail%s_CTRL' %i, tgl = True)
                        cmds.parent()
                        cmds.setAttr('Tail_Cluster%sHandle.visibility' %i, 0)
                
                #########parenting##########
                #cmds.select('Tail_IK_Curve.cv[0]', r = True)
                #cmds.cluster(n = 'Tail_Cluster0')
                #cmds.select('IK_Tail0_CTRL_GRP', tgl = True)
                #cmds.parent()
                cmds.select('IK_Tail0_CTRL_GRP', r = True)
                cmds.select('Root_CTRL', tgl = True)
                cmds.parent()
                
                cmds.createNode('transform', n = 'IK_Tail_Joint_GRP')
                cmds.select('IK_Tail0', r = True)
                cmds.select('IK_Tail_Joint_GRP', tgl = True)
                cmds.parent()
                cmds.createNode('transform', n = 'IK_Tail_GRP')
                cmds.select('Tail_IK_Handle', r = True)
                cmds.select('IK_Tail_Joint_GRP', add = True)
                cmds.select('IK_Tail_GRP', tgl = True)
                cmds.parent()
                cmds.select('IK_Tail_GRP', r = True)
                cmds.select('Puck', tgl = True)
                cmds.parent()

                

                cmds.createNode('transform', n = 'IK_Tail3_CTRL_Pivot0_GRP')
                cmds.move(cluster0_Pos[0], cluster0_Pos[1], cluster0_Pos[2])
                cmds.createNode('transform', n = 'IK_Tail3_CTRL_Pivot1_GRP')
                cmds.move(cluster1_Pos[0], cluster1_Pos[1], cluster1_Pos[2])
                cmds.createNode('transform', n = 'IK_Tail3_CTRL_Pivot2_GRP')
                cmds.move(cluster2_Pos[0], cluster2_Pos[1], cluster2_Pos[2])
                cmds.select('IK_Tail3_CTRL_Pivot2_GRP', r= True)
                cmds.select('IK_Tail3_CTRL_Pivot1_GRP', tgl= True)
                cmds.parent()
                cmds.select('IK_Tail3_CTRL_Pivot1_GRP', r= True)
                cmds.select('IK_Tail3_CTRL_Pivot0_GRP', tgl= True)
                cmds.parent()
                cmds.select('IK_Tail3_CTRL_GRP', r = True)
                cmds.select('IK_Tail3_CTRL_Pivot1_GRP', tgl= True)
                cmds.parent()
                
                
                cmds.createNode('transform', n = 'IK_Tail2_CTRL_Pivot0_GRP')
                cmds.move(cluster0_Pos[0], cluster0_Pos[1], cluster0_Pos[2])
                cmds.createNode('transform', n = 'IK_Tail2_CTRL_Pivot1_GRP')
                cmds.move(cluster1_Pos[0], cluster1_Pos[1], cluster1_Pos[2])
                cmds.select('IK_Tail2_CTRL_Pivot1_GRP', r= True)
                cmds.select('IK_Tail2_CTRL_Pivot0_GRP', tgl= True)
                cmds.parent()
                cmds.select('IK_Tail2_CTRL_GRP', r = True)
                cmds.select('IK_Tail2_CTRL_Pivot1_GRP', tgl= True)
                cmds.parent()
                
                cmds.createNode('transform', n = 'IK_Tail1_CTRL_Pivot0_GRP')
                cmds.move(cluster0_Pos[0], cluster0_Pos[1], cluster0_Pos[2])
                cmds.select('IK_Tail1_CTRL_GRP', r = True)
                cmds.select('IK_Tail1_CTRL_Pivot0_GRP', tgl = True)
                cmds.parent()
                                
                cmds.select('IK_Tail2_CTRL', r = True)
                cmds.select('IK_Tail3_CTRL_Pivot1_GRP', tgl = True)
                cmds.orientConstraint(mo = True, weight = True)

                cmds.select('IK_Tail1_CTRL', r = True)
                cmds.select('IK_Tail2_CTRL_Pivot1_GRP', tgl = True)
                cmds.orientConstraint(mo = True, weight = True)
                
                cmds.select('IK_Tail1_CTRL', r = True)
                cmds.select('IK_Tail3_CTRL_Pivot1_GRP', tgl = True)
                cmds.orientConstraint(mo = True, weight = True)
                
                cmds.select('IK_Tail0_CTRL', r = True)
                cmds.select('IK_Tail1_CTRL_Pivot0_GRP', tgl = True)
                cmds.orientConstraint(mo = True, weight = True)
                
                cmds.select('IK_Tail0_CTRL', r = True)
                cmds.select('IK_Tail2_CTRL_Pivot0_GRP', tgl = True)
                cmds.orientConstraint(mo = True, weight = True)
                
                cmds.select('IK_Tail0_CTRL', r = True)
                cmds.select('IK_Tail3_CTRL_Pivot0_GRP', tgl = True)
                cmds.orientConstraint(mo = True, weight = True)         
        
                cmds.createNode('transform', n = 'IK_Tail_CTRL_GRP')
                cmds.select('IK_Tail1_CTRL_Pivot0_GRP', r = True)
                cmds.select('IK_Tail2_CTRL_Pivot0_GRP', add = True)
                cmds.select('IK_Tail3_CTRL_Pivot0_GRP', add = True)
                #cmds.select('Tail_IK_Curve', add = True)
                cmds.select('IK_Tail_CTRL_GRP', tgl = True)
                cmds.parent()
                cmds.select('IK_Tail_CTRL_GRP', r = True)
                cmds.select('Puck', tgl = True)
                cmds.parent()
                
                cmds.setAttr('IK_Tail_GRP.visibility', 0)
                cmds.setAttr('Tail_IK_Curve.visibility', 0)
        
######### Stretch #######       
                cmds.addAttr('Root_CTRL', ln = 'Stretch_Tail',  at = 'long', min = 0, max = 1)
                cmds.setAttr('Root_CTRL.Stretch_Tail', e = True, keyable = True)
                
                ####distance locator####
                cmds.spaceLocator(n = 'Tail0_Loc')
                cmds.move(cluster0_Pos[0], cluster0_Pos[1], cluster0_Pos[2])
                cmds.select('Tail0', r = True)
                cmds.select('Tail0_Loc', tgl = True)
                cmds.pointConstraint(offset = [0, 0, 0], weight = 1)
                cmds.spaceLocator(n = 'Tail1_Loc')
                cmds.move(cluster3_Pos[0], cluster3_Pos[1], cluster3_Pos[2])
                cmds.select('IK_Tail3_CTRL', r = True)
                cmds.select('Tail1_Loc', tgl = True)
                cmds.pointConstraint(offset = [0, 0, 0], weight = 1)
                
                cmds.createNode('transform', n = 'Stretch_Tail_Loc_GRP')
                cmds.select('Tail0_Loc', r = True)
                cmds.select('Tail1_Loc', add = True)
                cmds.select('Stretch_Tail_Loc_GRP', tgl = True)
                cmds.parent()
                
                cmds.select('Stretch_Tail_Loc_GRP', r = True)
                cmds.select('Puck', tgl = True)
                cmds.parent()
                
                
                Tail_Length = cmds.arclen('Tail_IK_Curve')
                print Tail_Length
                
                #######Loc Distance#####
                cmds.shadingNode('distanceBetween', n = 'Tail_Loc_Distance', asUtility = True)
                cmds.connectAttr('Tail0_Loc.translate', 'Tail_Loc_Distance.point1')
                cmds.connectAttr('Tail1_Loc.translate', 'Tail_Loc_Distance.point2')
                        
                
                #######multiplied spine length#########
                cmds.shadingNode('multiplyDivide', n = 'Tail_Length', asUtility = True)
                cmds.connectAttr('Puck.scaleX', 'Tail_Length.input1X')
                cmds.connectAttr('Puck.scaleX', 'Tail_Length.input1Y')
                cmds.connectAttr('Tail_Loc_Distance.distance', 'Tail_Length.input2Y')
                cmds.setAttr('Tail_Length.input2X', Tail_Length)
                                
                
                #####Stretch Ratio###########
                cmds.shadingNode('multiplyDivide', n = 'Tail_Stretch_ratio', asUtility = True)
                cmds.setAttr('Tail_Stretch_ratio.operation', 2)
                cmds.connectAttr('Tail_Length.outputX', 'Tail_Stretch_ratio.input2X')
                cmds.connectAttr('Tail_Length.outputY', 'Tail_Stretch_ratio.input1X')
                
                cmds.shadingNode('blendColors', n = 'Tail_Stretch_Mux', asUtility = True)
                cmds.connectAttr('Root_CTRL.Stretch_Tail', 'Tail_Stretch_Mux.blender')
                cmds.setAttr('Tail_Stretch_Mux.color2R', 1)
                cmds.connectAttr('Tail_Length.outputY', 'Tail_Stretch_Mux.color1R')
                
                ######condidition#############
                cmds.shadingNode('condition', n = 'Stretch_Tail_Condition', asUtility = True)
                cmds.connectAttr('Tail_Stretch_Mux.outputR', 'Stretch_Tail_Condition.firstTerm')
                cmds.connectAttr('Tail_Length.outputX', 'Stretch_Tail_Condition.secondTerm')
                cmds.setAttr('Stretch_Tail_Condition.operation', 2)
                cmds.connectAttr('Tail_Stretch_ratio.outputX', 'Stretch_Tail_Condition.colorIfTrueR')
                cmds.setAttr('Stretch_Tail_Condition.colorIfFalseR', 1)
                
                
                for joint in IK_Tail_Joints:
                        joint = joint[3:]
                        cmds.connectAttr('Stretch_Tail_Condition.outColorR', '%s.scaleZ' %joint)
                
        
        def fkikTailSetup(self):
                Tails = cmds.listRelatives('Tail_Joint_GRP', ad = True)
                Tails = Tails[0:-1]
                print Tails
                
                cmds.select('Root_CTRL', r = True)
                cmds.addAttr(ln = 'Tail', at = 'long', min = 0, max = 1)
                cmds.setAttr('Root_CTRL.Tail', e = True, keyable = True)
                
                ###########Root Attr => IK Tail CTRL visibility
                cmds.connectAttr('Root_CTRL.Tail', 'IK_Tail0_CTRL.visibility')
                cmds.connectAttr('Root_CTRL.Tail', 'IK_Tail1_CTRL.visibility')
                cmds.connectAttr('Root_CTRL.Tail', 'IK_Tail2_CTRL.visibility')
                cmds.connectAttr('Root_CTRL.Tail', 'IK_Tail3_CTRL.visibility')
                
                cmds.createNode('reverse', n = 'FKIK_Tail_Inverter')
                cmds.connectAttr('Root_CTRL.Tail', 'FKIK_Tail_Inverter.inputX')
                cmds.connectAttr('FKIK_Tail_Inverter.outputX', 'FK_Tail0_CTRL.visibility')
                
                ##########Tail Last Mux############
                for tail in Tails:
                        cmds.shadingNode('blendColors', n = '%s_Mux' %tail, asUtility = True)
                        cmds.connectAttr('Root_CTRL.Tail', '%s_Mux.blender' %tail, f = True)
                        cmds.connectAttr('IK_%s.rotateX' %tail, '%s_Mux.color1R' %tail, f = True)
                        cmds.connectAttr('IK_%s.rotateY' %tail, '%s_Mux.color1G' %tail, f = True)
                        cmds.connectAttr('IK_%s.rotateZ' %tail, '%s_Mux.color1B' %tail, f = True)
                        cmds.connectAttr('FK_%s.rotateX' %tail, '%s_Mux.color2R' %tail, f = True)
                        cmds.connectAttr('FK_%s.rotateY' %tail, '%s_Mux.color2G' %tail, f = True)
                        cmds.connectAttr('FK_%s.rotateZ' %tail, '%s_Mux.color2B' %tail, f = True)

                        cmds.connectAttr('%s_Mux.outputR' %tail, '%s.rotateX' %tail, f = True)
                        cmds.connectAttr('%s_Mux.outputG' %tail, '%s.rotateY' %tail, f = True)
                        cmds.connectAttr('%s_Mux.outputB' %tail, '%s.rotateZ' %tail, f = True)                  
                
        def orientJoints(self, No_Fingers, Thumb_YN):
        ################Orient Spine Joint################
                for i in range(len(self.spineJoints)-1):
                        Joint1 = cmds.xform(self.spineJoints[i], ws = True, q = True, t = True)
                        Joint2 = cmds.xform(self.spineJoints[i+1], ws = True, q = True, t = True)
                        Joint_Aim = [Joint2[0]-Joint1[0], Joint2[1]-Joint1[1], Joint2[2]-Joint1[2]]
                        Joint_Length = math.sqrt(Joint_Aim[0]*Joint_Aim[0]+Joint_Aim[1]*Joint_Aim[1]+Joint_Aim[2]*Joint_Aim[2])
                        
                        Orient_Angle = []
                        for j in range(3):
                                if Joint_Length == 0:
                                        Orient_Angle.append(0)
                                else:
                                        Orient_Angle.append(math.degrees(math.acos(Joint_Aim[j]/Joint_Length)))
                                        
                        #print '%s' %self.spineJoints[i]
                        #print Joint_Length
                        #print Joint_Aim
                        #print Orient_Angle
                        if self.spineJoints[i] == 'Root':
                                cmds.rotate(0, 90, 0, '%s.rotateAxis' %self.spineJoints[i], r = True, os = True) 
                        else:
                                cmds.rotate(0, Orient_Angle[0], 0, '%s.rotateAxis' %self.spineJoints[i], r = True, os = True) 
                                if Joint_Aim[2]<0:
                                        cmds.rotate(0, 0, -Orient_Angle[1], '%s.rotateAxis' %self.spineJoints[i], r = True, os = True) 
                                else:
                                        cmds.rotate(0, 0, Orient_Angle[1], '%s.rotateAxis' %self.spineJoints[i], r = True, os = True) 
                        #cmds.rotate(Orient_Angle[2],0, 0, '%s.rotateAxis' %Joint, r = True, os = True) 
                cmds.rotate(0, 0, 0, 'NeckBase.rotateAxis', r = True, os = True, a = True)              
                cmds.rotate(0, 0, 0, 'Head.rotateAxis', r = True, os = True, a = True)          
        #########################################################

        ################Orient L_Leg Joint################
                self.legJoints_temp = self.legJoints[2:]
                cmds.rotate(0, 90, 0, 'Pelvis.rotateAxis', r = True, os = True) 
                for Joint in self.legJoints_temp:

                        cmds.joint('%s' %Joint, e = True, oj = 'yzx', secondaryAxisOrient =  'xup', ch = True, zso = True)
                        cmds.rotate(0, 180, 0, '%s.rotateAxis' %Joint, r = True, os = True) 
                
        
        ################Orient R_Leg Joint################
                for Joint in self.legJoints_R:
                        
                        cmds.joint('%s' %Joint, e = True, oj = 'yzx', secondaryAxisOrient =  'xup', ch = True, zso = True)
                        cmds.rotate(0, 180, 0, '%s.rotateAxis' %Joint, r = True, os = True) 
                        cmds.rotate(0, 0, 180, '%s.rotateAxis' %Joint, r = True, os = True) 
        
        #################Orient L_Arm_Joint##################
                cmds.joint('L_Scapula', e = True, oj = 'xyz', secondaryAxisOrient =  'yup', ch = True, zso = True)
                cmds.joint('L_Palm', e = True, oj = 'none', secondaryAxisOrient =  'yup', zso = True)
                
                
        #################Orient R_Arm_Joint##################
                cmds.joint('R_Scapula' , e = True, oj = 'xyz', secondaryAxisOrient =  'ydown', ch = True, zso = True)
                cmds.joint('R_Palm', e = True, oj = 'none', secondaryAxisOrient =  'ydown', zso = True)
                R_Arm_Orient_Joint = cmds.listRelatives('R_Scapula', ad = True)
                cmds.rotate(0, 180, 0, 'R_Scapula.rotateAxis', r = True, os = True) 
                for Joint in R_Arm_Orient_Joint:
                        cmds.rotate(0, 180, 0, '%s.rotateAxis' %Joint, r = True, os = True) 
                        #cmds.rotate(180, 0, 0, '%s.rotateAxis' %Joint, r = True, os = True)                    
        ####Finger orient##########
                print 'Nu O Fin = %s' %No_Fingers
                if Thumb_YN == 'Yes':
                        for i in range(4):
                                cmds.rotate(-45, 0, 0, 'L_Thumb%s.rotateAxis' %str(i), r = True, os = True) 
                        for i in range(4):
                                cmds.rotate(315, 0, 0, 'R_Thumb%s.rotateAxis' %str(i), r = True, os = True)     
                ####Varies by the NO. Fingers
                if No_Fingers == 4:
                        for i in range(5):
                                cmds.rotate(10, 0, 0, 'L_Pinky%s.rotateAxis' %str(i), r = True, os = True) 
                        for i in range(5):
                                cmds.rotate(-10, 0, 0, 'R_Pinky%s.rotateAxis' %str(i), r = True, os = True) 
                        for i in range(5):
                                cmds.rotate(5, 0, 0, 'L_Ring%s.rotateAxis' %str(i), r = True, os = True) 
                        for i in range(5):
                                cmds.rotate(-5, 0, 0, 'R_Ring%s.rotateAxis' %str(i), r = True, os = True)
                        for i in range(5):
                                cmds.rotate(5, 0, 0, 'L_Index%s.rotateAxis' %str(i), r = True, os = True)
                        for i in range(5):
                                cmds.rotate(-5, 0, 0, 'R_Index%s.rotateAxis' %str(i), r = True, os = True)
                elif No_Fingers == 3:
                        for i in range(5):
                                cmds.rotate(5, 0, 0, 'L_Ring%s.rotateAxis' %str(i), r = True, os = True) 
                        for i in range(5):
                                cmds.rotate(-5, 0, 0, 'R_Ring%s.rotateAxis' %str(i), r = True, os = True)
                        for i in range(5):
                                cmds.rotate(5, 0, 0, 'L_Index%s.rotateAxis' %str(i), r = True, os = True)
                        for i in range(5):
                                cmds.rotate(-5, 0, 0, 'R_Index%s.rotateAxis' %str(i), r = True, os = True)
                else:
                        for i in range(5):
                                cmds.rotate(5, 0, 0, 'L_Index%s.rotateAxis' %str(i), r = True, os = True)
                        for i in range(5):
                                cmds.rotate(-5, 0, 0, 'R_Index%s.rotateAxis' %str(i), r = True, os = True)
        
        def makeControllers(self):
        ##############Puck CTRL######################################
                cmds.circle( n = 'Puck', nr=(0, 1, 0), c=(0, 0, 0), r = 12 )
        ##############Leg CTRLs#######################################
                cmds.circle( n = 'L_Leg_CTRL', nr=(0, 1, 0), c=(0, 0, 0) )
                cmds.circle( n = 'R_Leg_CTRL', nr=(0, 1, 0), c=(0, 0, 0) )
                ###Attributes###
                Foot_attr = ['1Rolls','0Heel_Roll','0Ball_Roll','0Toe_Roll','1Twists','0Heel_Twist','0Ball_Twist','0BallToe_Twist','0Toe_Twist','1Extras','0Side','0Tip']

                for attr in Foot_attr:
                        for LR in L_o_R:
                                #print '%sLeg_CTRL' %LR
                                cmds.addAttr('%sLeg_CTRL' %LR, ln = "%s" %attr[1:], at = 'double')
                                if attr[0] == '1':
                                        cmds.setAttr('%sLeg_CTRL.%s' %(LR, attr[1:]), e = True, channelBox  = True)
                                else:
                                        cmds.setAttr('%sLeg_CTRL.%s' %(LR, attr[1:]), e = True, keyable = True )
                for LR in L_o_R:
                        cmds.setAttr('%sLeg_CTRL.scaleX' %LR, lock = True, keyable = False, channelBox = False)
                        cmds.setAttr('%sLeg_CTRL.scaleY' %LR, lock = True, keyable = False, channelBox = False)
                        cmds.setAttr('%sLeg_CTRL.scaleZ' %LR, lock = True, keyable = False, channelBox = False)
                        #cmds.setAttr('%sLeg_CTRL.v' %LR, lock = True, keyable = False, channelBox = False)
                        
                        ########Polevector###########
                        cmds.curve(n = '%sPolevector' %LR, d =  1, p = [(0, 2, 1),(0, 3, 1),(0, 0, 3), (0, -3, 1), (0, -2, 1), (0, -2, -2), (0, 2, -2), (0, 2, 1), (0, -2, -2), (0, 2, -2), (0, -2, 1)], k = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
                        cmds.scale(0.25, 0.25, 0.25, r = True)
                        cmds.createNode('transform', n = '%sPolevector_GRP' %LR)
                        cmds.select('%sPolevector' %LR, r = True)
                        cmds.select('%sPolevector_GRP' %LR, tgl = True)
                        cmds.parent()
                        cmds.select('%sPolevector_GRP' %LR, r = True)
                        if LR == 'L_':
                                cmds.move(self.leftToePos[0], self.leftKneePos[1], self.leftToePos[2]+2)
                        else:
                                cmds.move(-self.leftToePos[0], self.leftKneePos[1], self.leftToePos[2]+2)
                        cmds.setAttr('%sPolevector.scaleX' %LR, lock = True, keyable = False, channelBox = False)
                        cmds.setAttr('%sPolevector.scaleY' %LR, lock = True, keyable = False, channelBox = False)
                        cmds.setAttr('%sPolevector.scaleZ' %LR, lock = True, keyable = False, channelBox = False)
                
                ############FK Leg CTRls################
                for LR in L_o_R:
                        cmds.circle( n = '%sFK_Hip_CTRL' %LR, nr=(0, 1, 0), c=(0, 0, 0) )
                        cmds.createNode('transform', n = '%sFK_Hip_CTRL_GRP' %LR)
                        cmds.select('%sFK_Hip_CTRL' %LR, r = True)
                        cmds.select('%sFK_Hip_CTRL_GRP' %LR, tgl = True)
                        cmds.parent()
                        cmds.circle( n = '%sFK_Knee_CTRL' %LR, nr=(0, 1, 0), c=(0, 0, 0) )
                        cmds.createNode('transform', n = '%sFK_Knee_CTRL_GRP' %LR)
                        cmds.select('%sFK_Knee_CTRL' %LR, r = True)
                        cmds.select('%sFK_Knee_CTRL_GRP' %LR, tgl = True)
                        cmds.parent()
                        cmds.circle( n = '%sFK_Ankle_CTRL' %LR, nr=(0, 1, 0), c=(0, 0, 0) )
                        cmds.createNode('transform', n = '%sFK_Ankle_CTRL_GRP' %LR)
                        cmds.select('%sFK_Ankle_CTRL' %LR, r = True)
                        cmds.select('%sFK_Ankle_CTRL_GRP' %LR, tgl = True)
                        cmds.parent()
                        cmds.circle( n = '%sFK_Ball_CTRL' %LR, nr=(0, 1, 0), c=(0, 0, 0) )
                        cmds.createNode('transform', n = '%sFK_Ball_CTRL_GRP' %LR)
                        cmds.select('%sFK_Ball_CTRL' %LR, r = True)
                        cmds.select('%sFK_Ball_CTRL_GRP' %LR, tgl = True)
                        cmds.parent()

                for LR in L_o_R:
                        cmds.createNode('transform', n =  '%sLeg_Extra_CTRL_GRP' %LR)
                        cmds.curve(n = '%sLeg_Extra_CTRL' %LR, d = 1, p =[(-4, 0, -3),(-1, 0, -3),(-1, 0, -2),(-3, 0, -2),(-3, 0, -1), (-1, 0, -1),(-1, 0, 0),(-3, 0, 0),(-3, 0, 1),(-1, 0, 1),(-1, 0, 2),(-4, 0, 2),(-4, 0, -3),(3, 0, -3),(2, 0, -1),(2, 0, 0),(3, 0, 2),(2, 0, 2),(1, 0, 0),(0, 0, 2),(-1, 0, 2),(0, 0, 0),(0, 0, -1),(-1, 0, -3),(0, 0, -3),(1, 0, -1),(2, 0, -3),(3, 0, -3),(3, 0, 2),(-4, 0, 2)], k= [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29])
                        cmds.scale(0.2,0.2,0.2)
                        cmds.select('%sLeg_Extra_CTRL_GRP' %LR, tgl = True)
                        cmds.parent()
                        cmds.select('%sLeg_Extra_CTRL_GRP' %LR, r = True)
                        if LR == 'L_':
                                cmds.move(self.leftAnklePos[0]+4, self.leftAnklePos[1], self.leftAnklePos[2])
                                cmds.rotate(90, 0, 0)
                        else:   
                                cmds.move(-self.leftAnklePos[0]-4, self.leftAnklePos[1], self.leftAnklePos[2])
                                cmds.rotate(90, 0, 0)
        ##############################################################
        
        ###############Root CTRL######################################
                cmds.createNode('transform', n = 'Root_CTRL_GRP')
                #cmds.circle(n = 'Root_CTRL',  nr=(0, 1, 0), c=(0, 0, 0),  r=5 , s = 16)
                #cmds.select('Root_CTRL.cv[0]', r = True)
                #for i in range (7):
                #       cmds.select('Root_CTRL.cv[%s]' %(2*(i+1)), tgl = True)
                #cmds.scale(0.7, 0.7, 0.7, r = True)
                #cmds.move(0, 1, 0, r =True)
                cmds.curve(n = 'Root_CTRL', d =  1, p =[(-1, 1, 1),(1, 1, 1), (1, -1, 1), (-1, -1, 1), (-1, 1, 1), (-1, 1, -1), (-1, -1, -1), (-1, -1, 1), (1, -1, 1), (1, -1, -1),(-1, -1, -1), (-1, 1, -1), (1, 1, -1), (1, -1, -1), (1, 1, -1), (1, 1, 1) ], k = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15, 16]) 
                
                cmds.select('Root_CTRL', r = True)
                cmds.select('Root_CTRL_GRP', tgl = True)
                cmds.parent()
                cmds.select('Root_CTRL_GRP', r = True)
                cmds.move(self.rootPos[0], self.rootPos[1], self.rootPos[2])
                cmds.select('Root', r = True)
                cmds.select('Root_CTRL_GRP', tgl = True)
                cmds.orientConstraint(offset = [0, 0, 0], weight = 1)
                cmds.delete('Root_CTRL_GRP_orientConstraint1')

        ##############################################################

        ##############Pelvis CTRL#####################################
                cmds.createNode('transform', n = 'Pelvis_CTRL_GRP')
                cmds.circle(n = 'Pelvis_CTRL',  nr=(0, 1, 0), c=(0, 0, 0),  r=4 , s = 16)
                                
                cmds.select('Pelvis_CTRL', r = True)
                cmds.select('Pelvis_CTRL_GRP', tgl = True)
                cmds.parent()
                cmds.select('Pelvis_CTRL_GRP', r = True)
                cmds.move(self.rootPos[0], self.rootPos[1], self.rootPos[2])
                cmds.select('Root', r = True)
                cmds.select('Pelvis_CTRL_GRP', tgl = True)
                cmds.orientConstraint(offset = [0, 0, 0], weight = 1)
                cmds.delete('Pelvis_CTRL_GRP_orientConstraint1')
                
        ##############################################################
        
        ###############Spine CTRLs####################################
                spine_CTRLs = self.spineJoints[1:7]
                for i in range(len(spine_CTRLs)):       
                        cmds.createNode('transform', n = '%s_CTRL_GRP' %spine_CTRLs[i])
                        cmds.move(self.spinePosList[i][0], self.spinePosList[i][1], self.spinePosList[i][2])
                        #cmds.curve(n = '%s_CTRL' %spine_CTRLs[i], d = 1, p =[ (0, 0, 0), (-3, 0, 0), (-3.5, 0.5, 0), (-4, 0, 0), (-3.5, -0.5, 0), (-3, 0, 0), (-3.5, 0.5, 0), (-3.5, -0.5, 0), (-3, 0, 0), (-4, 0, 0)], k = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
                        cmds.circle(n = '%s_CTRL' %spine_CTRLs[i], nr=(0, 1, 0), c=(0, 0, 0),  r=3 , s = 8)
                        cmds.move(self.spinePosList[i][0], self.spinePosList[i][1], self.spinePosList[i][2])                     
                        cmds.select('%s_CTRL_GRP' %spine_CTRLs[i], tgl = True)
                        cmds.parent()
                        cmds.select('%s' %spine_CTRLs[i], r = True)
                        cmds.select('%s_CTRL_GRP' %spine_CTRLs[i], tgl = True)
                        cmds.orientConstraint(offset = [0, 0, 0], weight = 1)
                        cmds.delete('%s_CTRL_GRP_orientConstraint1' %spine_CTRLs[i])
                for i in range(len(spine_CTRLs)-1):
                        cmds.select('%s_CTRL_GRP' %spine_CTRLs[i+1], r = True)
                        cmds.select('%s_CTRL' %spine_CTRLs[i], tgl = True)
                        cmds.parent()
                        
        ##############################################################
        
        #################Jaw CTRL####################################
                cmds.createNode('transform', n = 'Jaw_CTRL_GRP')
                cmds.circle(n = 'Jaw_CTRL',  nr=(0, 1, 0), c=(0, 0, 0),  r=3 , s = 8)
                cmds.scale(0.2, 1, 1, r = True)
                cmds.select('Jaw_CTRL', r = True)
                cmds.select('Jaw_CTRL_GRP', tgl = True)
                cmds.parent()
                cmds.select('Jaw_CTRL_GRP', r = True)
                cmds.move(self.jawPos[0], self.jawPos[1], self.jawPos[2])   
                cmds.select('Jaw', r = True)
                cmds.select('Jaw_CTRL_GRP', tgl = True)
                cmds.orientConstraint(offset = [0, 0, 0], weight = 1)
                cmds.delete('Jaw_CTRL_GRP_orientConstraint1')
                
        ##############################################################
                
        #####parent root, spine, pelvis 
                cmds.select('Spine1_CTRL_GRP', r = True)
                cmds.select('Root_CTRL', tgl = True)
                cmds.parent()
                cmds.select('Pelvis_CTRL_GRP', r = True)
                cmds.select('Root_CTRL', tgl = True)
                cmds.parent()
                cmds.select('Jaw_CTRL_GRP', r = True)
                cmds.select('Head_CTRL', tgl = True)
                cmds.parent()
                
        ###############################################################
        #############Arm Controlers####################################
        ##########Scapula CTRL
                for LR in L_o_R:
                        cmds.createNode('transform', n = '%sScapula_CTRL_GRP' %LR)
                        cmds.circle(n = '%sScapula_CTRL' %LR, c = (0, 0, 0), nr =(0, 1, 0), sw = 360, r = 2)
                        cmds.select('%sScapula_CTRL_GRP' %LR, add = True)
                        cmds.parent()
                        cmds.select('%sScapula_CTRL_GRP' %LR, r = True)
                        if LR == 'L_':
                                cmds.move(self.leftScapulaPos[0], self.leftScapulaPos[1], self.leftScapulaPos[2] )
                        else:   
                                cmds.move(-self.leftScapulaPos[0], self.leftScapulaPos[1], self.leftScapulaPos[2] )
        
        ##########IK Arm CTRL
                for LR in L_o_R:
                        cmds.createNode('transform', n = '%sArm_IK_CTRL_GRP' %LR)
                        cmds.curve(n = '%sArm_IK_CTRL' %LR, d =  1, p =[(-1, 1, 1),(1, 1, 1), (1, -1, 1), (-1, -1, 1), (-1, 1, 1), (-1, 1, -1), (-1, -1, -1), (-1, -1, 1), (1, -1, 1), (1, -1, -1),(-1, -1, -1), (-1, 1, -1), (1, 1, -1), (1, -1, -1), (1, 1, -1), (1, 1, 1) ], k = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15, 16]) 
                        cmds.select('%sArm_IK_CTRL_GRP' %LR, add= True)
                        cmds.parent()
                        cmds.select('%sArm_IK_CTRL_GRP' %LR)
                        if LR == 'L_':
                                cmds.move(self.leftWristPos[0], self.leftWristPos[1], self.leftWristPos[2] )
                        else:   
                                cmds.move(-self.leftWristPos[0], self.leftWristPos[1], self.leftWristPos[2] )
                
                        cmds.createNode('transform', n = '%sArm_Polevector_GRP' %LR)
                        cmds.curve(n = '%sArm_Polevector' %LR, d =  1, p = [(0, 2, 1),(0, 3, 1),(0, 0, 3), (0, -3, 1), (0, -2, 1), (0, -2, -2), (0, 2, -2), (0, 2, 1), (0, -2, -2), (0, 2, -2), (0, -2, 1)], k = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
                        cmds.select('%sArm_Polevector_GRP' %LR, add = True)
                        cmds.parent()
                        cmds.select('%sArm_Polevector_GRP' %LR, r = True)
                        cmds.scale(0.2, 0.2, 0.2)
                        if LR == 'L_':
                                cmds.move(self.leftElbowPos[0], self.leftElbowPos[1], self.leftElbowPos[2]-2.5 )
                        else:   
                                cmds.move(-self.leftElbowPos[0], self.leftElbowPos[1], self.leftElbowPos[2]-2.5 )
        ############FK Arm CTRL
                Arm_FK_CTRL_List = ['Shoulder', 'Elbow', 'Wrist']
                for LR in L_o_R:
                        for CTRL in Arm_FK_CTRL_List:
                                cmds.createNode('transform', n = '%s%s_FK_CTRL_GRP' %(LR, CTRL))
                                cmds.circle(n = '%s%s_FK_CTRL' %(LR, CTRL), s = 32, c = (0, 0, 0), nr =(1, 0, 0), sw = 360, r = 1.5)
                                '''cmds.select('%s%s_FK_CTRL.cv[0]'%(LR, CTRL), r = True)
                                for i in range(15):
                                        i = 2*(i+1)
                                        cmds.select('%s%s_FK_CTRL.cv[%i]' %(LR, CTRL, i), tgl = True)
                                cmds.scale(2, 2, 2)'''

                                ##Shoulder
                        cmds.select('%sShoulder_FK_CTRL' %LR, r = True)
                        cmds.select('%sShoulder_FK_CTRL_GRP' %LR, tgl = True)
                        cmds.parent()
                        cmds.select('%sShoulder_FK_CTRL_GRP' %LR, r = True)
                        if LR == 'L_':
                                cmds.move(self.leftShoulderPos[0], self.leftShoulderPos[1], self.leftShoulderPos[2] )
                        else:   
                                cmds.move(-self.leftShoulderPos[0], self.leftShoulderPos[1], self.leftShoulderPos[2] )
                        ##Elbow
                        cmds.select('%sElbow_FK_CTRL' %LR, r = True)
                        cmds.select('%sElbow_FK_CTRL_GRP' %LR, tgl = True)
                        cmds.parent()
                        cmds.select('%sElbow_FK_CTRL_GRP' %LR, r = True)
                        if LR == 'L_':
                                cmds.move(self.leftElbowPos[0], self.leftElbowPos[1], self.leftElbowPos[2] )
                        else:   
                                cmds.move(-self.leftElbowPos[0], self.leftElbowPos[1], self.leftElbowPos[2] )
                        ##Wrist
                        cmds.select('%sWrist_FK_CTRL' %LR, r = True)
                        cmds.select('%sWrist_FK_CTRL_GRP' %LR, tgl = True)
                        cmds.parent()
                        cmds.select('%sWrist_FK_CTRL_GRP' %LR, r = True)
                        if LR == 'L_':
                                cmds.move(self.leftWristPos[0], self.leftWristPos[1], self.leftWristPos[2] )
                        else:   
                                cmds.move(-self.leftWristPos[0], self.leftWristPos[1], self.leftWristPos[2] )
        ############Arm EX CTRL
                for LR in L_o_R:
                        cmds.createNode('transform', n =  '%sArm_Extra_CTRL_GRP' %LR)
                        cmds.curve(n = '%sArm_Extra_CTRL' %LR, d = 1, p =[(-4, 0, -3),(-1, 0, -3),(-1, 0, -2),(-3, 0, -2),(-3, 0, -1), (-1, 0, -1),(-1, 0, 0),(-3, 0, 0),(-3, 0, 1),(-1, 0, 1),(-1, 0, 2),(-4, 0, 2),(-4, 0, -3),(3, 0, -3),(2, 0, -1),(2, 0, 0),(3, 0, 2),(2, 0, 2),(1, 0, 0),(0, 0, 2),(-1, 0, 2),(0, 0, 0),(0, 0, -1),(-1, 0, -3),(0, 0, -3),(1, 0, -1),(2, 0, -3),(3, 0, -3),(3, 0, 2),(-4, 0, 2)], k= [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29])
                        cmds.scale(0.2,0.2,0.2)
                        cmds.select('%sArm_Extra_CTRL_GRP' %LR, tgl = True)
                        cmds.parent()
                        cmds.select('%sArm_Extra_CTRL_GRP' %LR, r = True)
                        if LR == 'L_':
                                cmds.move(self.leftWristPos[0], self.leftWristPos[1], self.leftWristPos[2] -2)
                        else:   
                                cmds.move(-self.leftWristPos[0], self.leftWristPos[1], self.leftWristPos[2] -2)
                #############Palm and Finger
                        cmds.createNode('transform', n = '%sPalmFinger_CTRL_GRP' %LR)
                        cmds.curve(n = '%sPalmFinger_CTRL' %LR, d = 1, p = [ (0, 0, 0), (0, 3, 0),(0, 4, 1),(0, 5, 0), (0, 4, -1),(0, 3, 0),(0, 4, 1),(0, 4, -1)], k = [1,2,3,4,5,6,7,8])
                        cmds.select('%sPalmFinger_CTRL_GRP' %LR, tgl = True)
                        cmds.parent()
                        cmds.select('%sPalmFinger_CTRL_GRP' %LR, r = True)
                        cmds.scale(0.5,0.5,0.5)
                        if LR == 'L_':
                                cmds.move(self.leftPalmPos[0], self.leftPalmPos[1], self.leftPalmPos[2])
                        else:   
                                cmds.move(-self.leftPalmPos[0], self.leftPalmPos[1], self.leftPalmPos[2])
#################################################################################       
        def legSetting(self):
                leftLegJoints = self.legJoints[2:7]
                rightLegJoints = self.legJoints_R
                del leftLegJoints[1]
                del rightLegJoints[1]
                for i in range(len(leftLegJoints)-1):
                        
                        cmds.select('%s.rotatePivot' %leftLegJoints[i], r = True)
                        cmds.select('%s.rotatePivot' %leftLegJoints[i+1], add = True)
                        cmds.ikHandle(n = '%s_IKHandle' %leftLegJoints[i+1], sol = 'ikRPsolver')
                        cmds.select('%s.rotatePivot' %rightLegJoints[i], r = True)
                        cmds.select('%s.rotatePivot' %rightLegJoints[i+1], add = True)
                        cmds.ikHandle(n = '%s_IKHandle' %rightLegJoints[i+1], sol = 'ikRPsolver')

                for LR in L_o_R:
                        #####Making Group Node######
                        cmds.createNode( 'transform', n='%sBall_Ik_GRP' %LR )
                        cmds.createNode( 'transform', n='%sToe_Ik_GRP' %LR )
                        cmds.createNode('transform', n = '%sBall_GRP' %LR )
                        cmds.createNode( 'transform', n='%sLeg_CTRL_GRP' %LR )
                        cmds.createNode( 'transform', n='%sHeel_GRP' %LR )
                        cmds.delete('%sHeel_PivotPosition' %LR)
                        cmds.createNode( 'transform', n='%sToe_GRP' %LR )
                        cmds.createNode( 'transform', n='%sSideIn_GRP' %LR )
                        cmds.select('%sLeg_CTRL' %LR, r = True)
                        cmds.select('%sLeg_CTRL_GRP' %LR, tgl = True)
                        cmds.parent()
                        ####Grouping IKs#####
                        if LR == 'L_':
                                cmds.select('%sBall_Ik_GRP' %LR, r = True)
                                cmds.select('%sToe_Ik_GRP' %LR, add = True)
                                cmds.select('%sBall_GRP' %LR, tgl = True)
                                cmds.move(self.leftBallPos[0], self.leftBallPos[1], self.leftBallPos[2])
                                cmds.select('%sToe_GRP' %LR, r = True)
                                cmds.move(self.leftToePos[0], self.leftToePos[1], self.leftToePos[2])
                                cmds.select('%sLeg_CTRL_GRP' %LR, r = True)
                                cmds.move(self.leftAnklePos[0], self.leftAnklePos[1], self.leftAnklePos[2])
                                cmds.select('%sHeel_GRP' %LR, r = True)
                                cmds.move(self.leftHeelPos[0], self.leftHeelPos[1], self.leftHeelPos[2])
                                cmds.select('%sSideIn_GRP' %LR, r = True)
                                cmds.move(self.leftSideInPos[0], self.leftSideInPos[1], self.leftSideInPos[2])
                        else:
                                cmds.select('%sBall_Ik_GRP' %LR, r = True)
                                cmds.select('%sToe_Ik_GRP' %LR, add = True)
                                cmds.select('%sBall_GRP' %LR, tgl = True)
                                cmds.move(-self.leftBallPos[0], self.leftBallPos[1], self.leftBallPos[2])
                                cmds.select('%sToe_GRP' %LR, r = True)
                                cmds.move(-self.leftToePos[0], self.leftToePos[1], self.leftToePos[2])
                                cmds.select('%sLeg_CTRL_GRP' %LR, r = True)
                                cmds.move(-self.leftAnklePos[0], self.leftAnklePos[1], self.leftAnklePos[2])
                                cmds.select('%sHeel_GRP' %LR, r = True)
                                cmds.move(-self.leftHeelPos[0], self.leftHeelPos[1], self.leftHeelPos[2])
                                cmds.select('%sSideIn_GRP' %LR, r = True)
                                cmds.move(-self.leftSideInPos[0], self.leftSideInPos[1], self.leftSideInPos[2])
                        
                        ####Adjust Foot CTRLs
                        cmds.select('%sLeg_CTRL.cv[0]' %LR, r = True)
                        for i in range(7):
                                cmds.select('%sLeg_CTRL.cv[%s]' %(LR, i+1), tgl = True)
                        cmds.move(0, -self.leftAnklePos[1], 0, r = True)
                        cmds.select('%sLeg_CTRL.cv[3]' %LR, r = True)
                        for i in range(4):
                                cmds.select('%sLeg_CTRL.cv[%s]' %(LR, i+4), tgl = True)
                        cmds.move(0,0, abs(self.leftToePos[2]+1), r = True)
                        
                        
                        #####Final Grouping#####
                        cmds.select('%sAnkle_IKHandle' %LR, r = True)
                        cmds.select('%sBall_IKHandle'%LR, add = True)
                        cmds.select('%sBall_Ik_GRP' %LR, tgl = True)
                        cmds.parent()
                        cmds.select('%sToe_IKHandle' %LR, r = True)
                        cmds.select('%sToe_Ik_GRP' %LR, tgl = True)
                        cmds.parent()
                        cmds.select('%sBall_Ik_GRP' %LR, r = True)
                        cmds.select('%sToe_Ik_GRP' %LR, add = True)
                        cmds.select('%sBall_GRP' %LR, tgl = True)
                        cmds.parent()
                        cmds.select('%sBall_GRP' %LR, r = True)
                        cmds.select('%sSideOut_PivotPosition' %LR, tgl = True)
                        cmds.parent()
                        cmds.select('%sSideOut_PivotPosition' %LR, r = True)
                        cmds.select('%sSideIn_PivotPosition' %LR, tgl = True)
                        cmds.parent()
                        cmds.select('%sSideIn_PivotPosition' %LR, r = True)
                        cmds.select('%sSideIn_GRP' %LR, tgl = True)
                        cmds.parent()
                        cmds.select('%sSideIn_GRP' %LR, r = True)
                        cmds.select('%sToe_GRP' %LR, tgl = True)
                        cmds.parent()
                        cmds.select('%sToe_GRP' %LR, r = True)
                        cmds.select('%sHeel_GRP' %LR, tgl = True)
                        cmds.parent()
                        cmds.select('%sHeel_GRP' %LR, r = True)
                        cmds.select('%sLeg_CTRL' %LR, tgl = True)
                        cmds.parent()
                        cmds.setAttr('%sHeel_GRP.visibility' %LR, 0)
                        
                        ####Leg Polevector Follow#########
                        cmds.select('%sLeg_CTRL' %LR, r = True)
                        cmds.select('%sPolevector_GRP' %LR, tgl = True)
                        cmds.pointConstraint(offset = [0, 0, 0],mo = True, o = [0, 0, 0], weight = 1) 
                        
                        
                #############Connect Attr###############
                #cmds.connectAttr('R_Leg_CTRL.Heel_Roll', 'R_Heel_GRP.rotateX') ,f = True) 
                for LR in L_o_R:
                ###Rolls###
                        cmds.shadingNode('multiplyDivide', n = '%smulDiv_Roll' %LR, asUtility = True)
                        cmds.setAttr ('%smulDiv_Roll.input2X' %LR, -1)
                        cmds.setAttr ('%smulDiv_Roll.input2Y' %LR, -1)
                        cmds.setAttr ('%smulDiv_Roll.input2Z' %LR, -1)
                        cmds.connectAttr('%sLeg_CTRL.Heel_Roll' %LR, '%smulDiv_Roll.input1X' %LR, f = True)
                        cmds.connectAttr('%smulDiv_Roll.outputX' %LR, '%sHeel_GRP.rotateX' %LR, f = True)
                        cmds.connectAttr('%sLeg_CTRL.Ball_Roll' %LR, '%smulDiv_Roll.input1Y' %LR, f = True)
                        cmds.connectAttr('%smulDiv_Roll.outputY' %LR, '%sBall_Ik_GRP.rotateX' %LR, f = True)
                        cmds.connectAttr('%sLeg_CTRL.Toe_Roll' %LR, '%smulDiv_Roll.input1Z' %LR, f = True)
                        cmds.connectAttr('%smulDiv_Roll.outputZ' %LR, '%sToe_GRP.rotateX' %LR, f = True)
                ###Twists###    
                        #cmds.shadingNode('multiplyDivide', n = '%smulDiv_Twist' %LR, asUtility = True)
                        cmds.shadingNode('multiplyDivide', n = '%smulDiv_Twist' %LR, asUtility = True)
                        cmds.shadingNode('multiplyDivide', n = '%smulDiv_Twist1' %LR, asUtility = True)
                        cmds.setAttr ('%smulDiv_Twist.input2X' %LR, -1)
                        cmds.setAttr ('%smulDiv_Twist.input2Y' %LR, -1)
                        cmds.setAttr ('%smulDiv_Twist.input2Z' %LR, -1)
                        cmds.setAttr ('%smulDiv_Twist1.input2X' %LR, -1)
                        if LR == 'L_':
                                cmds.connectAttr('%sLeg_CTRL.Heel_Twist' %LR, '%sHeel_GRP.rotateY' %LR, f = True)
                                cmds.connectAttr('%sLeg_CTRL.Ball_Twist' %LR, '%sBall_Ik_GRP.rotateY' %LR, f = True)
                                cmds.connectAttr('%sLeg_CTRL.Toe_Twist' %LR, '%sToe_GRP.rotateY' %LR, f = True)
                                cmds.connectAttr('%sLeg_CTRL.BallToe_Twist' %LR, '%sBall_GRP.rotateY' %LR, f = True)
                        else:
                                cmds.connectAttr('%sLeg_CTRL.Heel_Twist' %LR, '%smulDiv_Twist.input1X' %LR, f = True)
                                cmds.connectAttr('%smulDiv_Twist.outputX' %LR, '%sHeel_GRP.rotateY' %LR, f = True)
                                cmds.connectAttr('%sLeg_CTRL.Ball_Twist' %LR, '%smulDiv_Twist.input1Y' %LR, f = True)
                                cmds.connectAttr('%smulDiv_Twist.outputY' %LR, '%sBall_Ik_GRP.rotateY' %LR, f = True)
                                cmds.connectAttr('%sLeg_CTRL.Toe_Twist' %LR, '%smulDiv_Twist.input1Z' %LR, f = True)
                                cmds.connectAttr('%smulDiv_Twist.outputZ' %LR, '%sToe_GRP.rotateY' %LR, f = True)
                                cmds.connectAttr('%sLeg_CTRL.BallToe_Twist' %LR, '%smulDiv_Twist1.input1X' %LR, f = True)
                                cmds.connectAttr('%smulDiv_Twist1.outputX' %LR, '%sBall_GRP.rotateY' %LR, f = True)                             
                ###Extras###
                        cmds.shadingNode('multiplyDivide', n = '%smulDiv_Extra' %LR, asUtility = True)
                        cmds.setAttr ('%smulDiv_Extra.input2X' %LR, -1)
                        cmds.connectAttr('%sLeg_CTRL.Tip' %LR, '%smulDiv_Extra.input1X' %LR, f = True)
                        cmds.connectAttr('%smulDiv_Extra.outputX' %LR, '%sToe_Ik_GRP.rotateX' %LR, f = True)
                        
                        ####Side It's hard one...!!!###
                        cmds.shadingNode('condition', n = '%sSideIn' %LR, asUtility = True)
                        cmds.shadingNode('condition', n = '%sSideOut' %LR, asUtility = True)
                        cmds.shadingNode('multiplyDivide', n = 'mulDiv_Extra_side', asUtility = True)
                        
                        cmds.setAttr('%sSideIn.operation' %LR, 2)
                        cmds.setAttr('%sSideOut.operation' %LR, 4)
                        
                        cmds.connectAttr('%sLeg_CTRL.Side' %LR, '%sSideIn.firstTerm' %LR, f = True)
                        cmds.connectAttr('%sSideIn.outColorR' %LR, '%smulDiv_Extra.input2Y' %LR, f = True)
                        cmds.connectAttr('%sLeg_CTRL.Side' %LR, '%smulDiv_Extra.input1Y' %LR, f = True)
                        cmds.setAttr ('mulDiv_Extra_side.input2X', -1)
                        if LR == 'L_':
                                cmds.connectAttr('%smulDiv_Extra.outputY' %LR, 'mulDiv_Extra_side.input1X', f = True)
                                cmds.connectAttr('mulDiv_Extra_side.outputX', '%sSideIn_PivotPosition.rotateZ' %LR, f = True)
                        else:
                                cmds.connectAttr('%smulDiv_Extra.outputY' %LR, '%sSideIn_PivotPosition.rotateZ' %LR, f = True)
                
                        cmds.connectAttr('%sLeg_CTRL.Side' %LR, '%sSideOut.firstTerm' %LR, f = True)
                        cmds.connectAttr('%sSideOut.outColorR' %LR, '%smulDiv_Extra.input2Z' %LR, f = True)
                        cmds.connectAttr('%sLeg_CTRL.Side' %LR, '%smulDiv_Extra.input1Z' %LR, f = True)
                        cmds.setAttr ('mulDiv_Extra_side.input2Y', -1)
                        if LR == 'L_':
                                cmds.connectAttr('%smulDiv_Extra.outputZ' %LR, 'mulDiv_Extra_side.input1Y', f = True)
                                cmds.connectAttr('mulDiv_Extra_side.outputY', '%sSideOut_PivotPosition.rotateZ' %LR, f = True)
                        else:
                                cmds.connectAttr('%smulDiv_Extra.outputZ' %LR, '%sSideOut_PivotPosition.rotateZ' %LR, f = True)
                        
                        #############Polevector##################
                        cmds.select('%sPolevector' %LR, r = True)
                        cmds.select('%sAnkle_IKHandle' %LR, tgl = True)
                        cmds.poleVectorConstraint(weight = 1)
                        
        ########################################################################                
        def fkLegSetting(self):
                
                ########Making FK, Bind, bones##############
                for LR in L_o_R:
                        cmds.select('%sHip' %LR, r = True)
                        cmds.duplicate()
                        cmds.rename('%sHip' %LR, '%sIK_Hip' %LR)
                        cmds.rename('%sIK_Hip|%sKnee' %(LR, LR), '%sIK_Knee' %LR)
                        cmds.rename('%sIK_Hip|%sIK_Knee|%sAnkle' %(LR, LR, LR), '%sIK_Ankle' %LR)
                        cmds.rename('%sIK_Hip|%sIK_Knee|%sIK_Ankle|%sBall' %(LR, LR, LR, LR), '%sIK_Ball' %LR)
                        cmds.rename('%sIK_Hip|%sIK_Knee|%sIK_Ankle|%sIK_Ball|%sToe' %(LR, LR, LR, LR, LR), '%sIK_Toe' %LR)
                        ###Bind Joint
                        cmds.rename('%sHip1' %LR, '%sHip' %LR)
                        cmds.select('%sHip' %LR, r = True)
                        cmds.duplicate()
                        ###FK_Joint
                        cmds.rename('%sHip1' %LR, '%sFK_Hip' %LR)
                        cmds.rename('%sFK_Hip|%sKnee' %(LR, LR), '%sFK_Knee' %LR)
                        cmds.rename('%sFK_Hip|%sFK_Knee|%sAnkle' %(LR, LR, LR), '%sFK_Ankle' %LR)       
                        cmds.rename('%sFK_Hip|%sFK_Knee|%sFK_Ankle|%sBall' %(LR, LR, LR, LR), '%sFK_Ball' %LR)
                        cmds.rename('%sFK_Hip|%sFK_Knee|%sFK_Ankle|%sFK_Ball|%sToe' %(LR, LR, LR, LR, LR), '%sFK_Toe' %LR)
                
                ####FK CTRLs###         
                FKLegJoints = ['FK_Hip', 'FK_Knee', 'FK_Ankle','FK_Ball']
                for LR in L_o_R:                        
                        for joints in FKLegJoints:
                                cmds.select('%s%s' %(LR, joints), r = True)
                                cmds.select('%s%s_CTRL_GRP' %(LR, joints), tgl = True)
                                cmds.pointConstraint(weight = 1)
                                cmds.orientConstraint(weight = 1)
                                cmds.delete('%s%s_CTRL_GRP_pointConstraint1' %(LR, joints))
                                cmds.delete('%s%s_CTRL_GRP_orientConstraint1' %(LR, joints))
                                
                                cmds.select('%s%s_CTRL' %(LR, joints), r = True)
                                cmds.select('%s%s' %(LR, joints), tgl = True)
                                cmds.orientConstraint(weight = 1)
                        cmds.select('%sFK_Ball_CTRL_GRP' %LR, r = True)
                        cmds.select('%sFK_Ankle_CTRL' %LR, tgl = True)  
                        cmds.parent()
                        cmds.select('%sFK_Ankle_CTRL_GRP' %LR, r = True)
                        cmds.select('%sFK_Knee_CTRL' %LR, tgl = True)   
                        cmds.parent()
                        cmds.select('%sFK_Knee_CTRL_GRP' %LR, r = True)
                        cmds.select('%sFK_Hip_CTRL' %LR, tgl = True)    
                        cmds.parent()

                        cmds.select('%sLeg_Extra_CTRL_GRP' %LR, r = True)
                        cmds.select('%sAnkle' %LR, tgl = True)
                        cmds.parent()
                
                ###########FKIK Setting###############
                        cmds.select('%sLeg_Extra_CTRL' %LR)
                        cmds.setAttr('%sLeg_Extra_CTRL.tx' %LR, lock = True, keyable  = False, channelBox = False)
                        cmds.setAttr('%sLeg_Extra_CTRL.ty' %LR, lock = True, keyable  = False, channelBox = False)
                        cmds.setAttr('%sLeg_Extra_CTRL.tz' %LR, lock = True, keyable  = False, channelBox = False)
                        cmds.setAttr('%sLeg_Extra_CTRL.rx' %LR, lock = True, keyable  = False, channelBox = False)
                        cmds.setAttr('%sLeg_Extra_CTRL.ry' %LR, lock = True, keyable  = False, channelBox = False)
                        cmds.setAttr('%sLeg_Extra_CTRL.rz' %LR, lock = True, keyable  = False, channelBox = False)
                        cmds.setAttr('%sLeg_Extra_CTRL.sx' %LR, lock = True, keyable  = False, channelBox = False)
                        cmds.setAttr('%sLeg_Extra_CTRL.sy' %LR, lock = True, keyable  = False, channelBox = False)
                        cmds.setAttr('%sLeg_Extra_CTRL.sz' %LR, lock = True, keyable  = False, channelBox = False)
                        cmds.setAttr('%sLeg_Extra_CTRL.v' %LR, lock = True, keyable  = False, channelBox = False)
                        ##############add Extra attributes####################
                        cmds.addAttr(ln = 'FKIK', at = 'long', min = 0, max = 1)
                        cmds.setAttr('%sLeg_Extra_CTRL.FKIK' %LR, e = True, keyable = True)
                        cmds.setAttr('%sLeg_Extra_CTRL.FKIK' %LR, 1)
                
                #########FKIK Switch Node#############
                        cmds.shadingNode('blendColors', n = '%sFKIK_Hip_Mux' %LR, asUtility = True)
                        cmds.connectAttr('%sLeg_Extra_CTRL.FKIK' %LR, '%sFKIK_Hip_Mux.blender' %LR, f = True)

                        cmds.connectAttr('%sFK_Hip.rotateX' %LR, '%sFKIK_Hip_Mux.color2R' %LR, f = True)
                        cmds.connectAttr('%sFK_Hip.rotateY' %LR, '%sFKIK_Hip_Mux.color2G' %LR, f = True)
                        cmds.connectAttr('%sFK_Hip.rotateZ' %LR, '%sFKIK_Hip_Mux.color2B' %LR, f = True)
                        cmds.connectAttr('%sIK_Hip.rotateX' %LR, '%sFKIK_Hip_Mux.color1R' %LR, f = True)
                        cmds.connectAttr('%sIK_Hip.rotateY' %LR, '%sFKIK_Hip_Mux.color1G' %LR, f = True)
                        cmds.connectAttr('%sIK_Hip.rotateZ' %LR, '%sFKIK_Hip_Mux.color1B' %LR, f = True)
                        cmds.connectAttr('%sFKIK_Hip_Mux.outputR' %LR, '%sHip.rotateX' %LR, f = True)
                        cmds.connectAttr('%sFKIK_Hip_Mux.outputG' %LR, '%sHip.rotateY' %LR, f = True)
                        cmds.connectAttr('%sFKIK_Hip_Mux.outputB' %LR, '%sHip.rotateZ' %LR, f = True)
                        
                        cmds.shadingNode('blendColors', n = '%sFKIK_Knee_Mux' %LR, asUtility = True)
                        cmds.connectAttr('%sLeg_Extra_CTRL.FKIK' %LR, '%sFKIK_Knee_Mux.blender' %LR, f = True)
                        cmds.connectAttr('%sFK_Knee.rotateX' %LR, '%sFKIK_Knee_Mux.color2R' %LR, f = True)
                        cmds.connectAttr('%sFK_Knee.rotateY' %LR, '%sFKIK_Knee_Mux.color2G' %LR, f = True)
                        cmds.connectAttr('%sFK_Knee.rotateZ' %LR, '%sFKIK_Knee_Mux.color2B' %LR, f = True)
                        cmds.connectAttr('%sIK_Knee.rotateX' %LR, '%sFKIK_Knee_Mux.color1R' %LR, f = True)
                        cmds.connectAttr('%sIK_Knee.rotateY' %LR, '%sFKIK_Knee_Mux.color1G' %LR, f = True)
                        cmds.connectAttr('%sIK_Knee.rotateZ' %LR, '%sFKIK_Knee_Mux.color1B' %LR, f = True)
                        cmds.connectAttr('%sFKIK_Knee_Mux.outputR' %LR, '%sKnee.rotateX' %LR, f = True)
                        cmds.connectAttr('%sFKIK_Knee_Mux.outputG' %LR, '%sKnee.rotateY' %LR, f = True)
                        cmds.connectAttr('%sFKIK_Knee_Mux.outputB' %LR, '%sKnee.rotateZ' %LR, f = True)
                        
                        cmds.shadingNode('blendColors', n = '%sFKIK_Ankle_Mux' %LR, asUtility = True)
                        cmds.connectAttr('%sLeg_Extra_CTRL.FKIK' %LR, '%sFKIK_Ankle_Mux.blender' %LR, f = True)
                        cmds.connectAttr('%sFK_Ankle.rotateX' %LR, '%sFKIK_Ankle_Mux.color2R' %LR, f = True)
                        cmds.connectAttr('%sFK_Ankle.rotateY' %LR, '%sFKIK_Ankle_Mux.color2G' %LR, f = True)
                        cmds.connectAttr('%sFK_Ankle.rotateZ' %LR, '%sFKIK_Ankle_Mux.color2B' %LR, f = True)
                        cmds.connectAttr('%sIK_Ankle.rotateX' %LR, '%sFKIK_Ankle_Mux.color1R' %LR, f = True)
                        cmds.connectAttr('%sIK_Ankle.rotateY' %LR, '%sFKIK_Ankle_Mux.color1G' %LR, f = True)
                        cmds.connectAttr('%sIK_Ankle.rotateZ' %LR, '%sFKIK_Ankle_Mux.color1B' %LR, f = True)
                        cmds.connectAttr('%sFKIK_Ankle_Mux.outputR' %LR, '%sAnkle.rotateX' %LR, f = True)
                        cmds.connectAttr('%sFKIK_Ankle_Mux.outputG' %LR, '%sAnkle.rotateY' %LR, f = True)
                        cmds.connectAttr('%sFKIK_Ankle_Mux.outputB' %LR, '%sAnkle.rotateZ' %LR, f = True)
                        
                        cmds.shadingNode('blendColors', n = '%sFKIK_Ball_Mux' %LR, asUtility = True)
                        cmds.connectAttr('%sLeg_Extra_CTRL.FKIK' %LR, '%sFKIK_Ball_Mux.blender' %LR, f = True)
                        cmds.connectAttr('%sFK_Ball.rotateX' %LR, '%sFKIK_Ball_Mux.color2R' %LR, f = True)
                        cmds.connectAttr('%sFK_Ball.rotateY' %LR, '%sFKIK_Ball_Mux.color2G' %LR, f = True)
                        cmds.connectAttr('%sFK_Ball.rotateZ' %LR, '%sFKIK_Ball_Mux.color2B' %LR, f = True)
                        cmds.connectAttr('%sIK_Ball.rotateX' %LR, '%sFKIK_Ball_Mux.color1R' %LR, f = True)
                        cmds.connectAttr('%sIK_Ball.rotateY' %LR, '%sFKIK_Ball_Mux.color1G' %LR, f = True)
                        cmds.connectAttr('%sIK_Ball.rotateZ' %LR, '%sFKIK_Ball_Mux.color1B' %LR, f = True)
                        cmds.connectAttr('%sFKIK_Ball_Mux.outputR' %LR, '%sBall.rotateX' %LR, f = True)
                        cmds.connectAttr('%sFKIK_Ball_Mux.outputG' %LR, '%sBall.rotateY' %LR, f = True)
                        cmds.connectAttr('%sFKIK_Ball_Mux.outputB' %LR, '%sBall.rotateZ' %LR, f = True)
                        
                        ###Translate###
                        cmds.shadingNode('blendColors', n = '%sFKIK_Knee_Translate_Mux' %LR, asUtility = True)
                        cmds.connectAttr('%sLeg_Extra_CTRL.FKIK' %LR, '%sFKIK_Knee_Translate_Mux.blender' %LR, f = True)
                        cmds.connectAttr('%sFK_Knee.translateX' %LR, '%sFKIK_Knee_Translate_Mux.color2R' %LR, f = True)
                        cmds.connectAttr('%sFK_Knee.translateY' %LR, '%sFKIK_Knee_Translate_Mux.color2G' %LR, f = True)
                        cmds.connectAttr('%sFK_Knee.translateZ' %LR, '%sFKIK_Knee_Translate_Mux.color2B' %LR, f = True)
                        cmds.connectAttr('%sIK_Knee.translateX' %LR, '%sFKIK_Knee_Translate_Mux.color1R' %LR, f = True)
                        cmds.connectAttr('%sIK_Knee.translateY' %LR, '%sFKIK_Knee_Translate_Mux.color1G' %LR, f = True)
                        cmds.connectAttr('%sIK_Knee.translateZ' %LR, '%sFKIK_Knee_Translate_Mux.color1B' %LR, f = True)
                        cmds.connectAttr('%sFKIK_Knee_Translate_Mux.outputR' %LR, '%sKnee.translateX' %LR, f = True)
                        cmds.connectAttr('%sFKIK_Knee_Translate_Mux.outputG' %LR, '%sKnee.translateY' %LR, f = True)
                        cmds.connectAttr('%sFKIK_Knee_Translate_Mux.outputB' %LR, '%sKnee.translateZ' %LR, f = True)
                        
                        cmds.shadingNode('blendColors', n = '%sFKIK_Ankle_Translate_Mux' %LR, asUtility = True)
                        cmds.connectAttr('%sLeg_Extra_CTRL.FKIK' %LR, '%sFKIK_Ankle_Translate_Mux.blender' %LR, f = True)
                        cmds.connectAttr('%sFK_Ankle.translateX' %LR, '%sFKIK_Ankle_Translate_Mux.color2R' %LR, f = True)
                        cmds.connectAttr('%sFK_Ankle.translateY' %LR, '%sFKIK_Ankle_Translate_Mux.color2G' %LR, f = True)
                        cmds.connectAttr('%sFK_Ankle.translateZ' %LR, '%sFKIK_Ankle_Translate_Mux.color2B' %LR, f = True)
                        cmds.connectAttr('%sIK_Ankle.translateX' %LR, '%sFKIK_Ankle_Translate_Mux.color1R' %LR, f = True)
                        cmds.connectAttr('%sIK_Ankle.translateY' %LR, '%sFKIK_Ankle_Translate_Mux.color1G' %LR, f = True)
                        cmds.connectAttr('%sIK_Ankle.translateZ' %LR, '%sFKIK_Ankle_Translate_Mux.color1B' %LR, f = True)
                        cmds.connectAttr('%sFKIK_Ankle_Translate_Mux.outputR' %LR, '%sAnkle.translateX' %LR, f = True)
                        cmds.connectAttr('%sFKIK_Ankle_Translate_Mux.outputG' %LR, '%sAnkle.translateY' %LR, f = True)
                        cmds.connectAttr('%sFKIK_Ankle_Translate_Mux.outputB' %LR, '%sAnkle.translateZ' %LR, f = True)
                        ####FKIK CTRL Hide                      
                        cmds.connectAttr('%sLeg_Extra_CTRL.FKIK' %LR, '%sLeg_CTRL.visibility' %LR , f = True)
                        cmds.connectAttr('%sLeg_Extra_CTRL.FKIK' %LR, '%sPolevector.visibility' %LR , f = True)
                        cmds.shadingNode('condition', n = '%sFKIK_Leg_CTRL_Mux' %LR, asUtility = True)
                        cmds.setAttr('%sFKIK_Leg_CTRL_Mux.secondTerm' %LR, 0)
                        cmds.setAttr('%sFKIK_Leg_CTRL_Mux.operation' %LR, 0)
                        cmds.setAttr('%sFKIK_Leg_CTRL_Mux.colorIfTrueR' %LR, 1)
                        cmds.setAttr('%sFKIK_Leg_CTRL_Mux.colorIfFalseR' %LR, 0)
                        
                        cmds.connectAttr('%sLeg_Extra_CTRL.FKIK' %LR, '%sFKIK_Leg_CTRL_Mux.firstTerm' %LR, f = True)
                        cmds.connectAttr('%sFKIK_Leg_CTRL_Mux.outColorR' %LR, '%sFK_Hip_CTRL.visibility' %LR, f = True)
                        cmds.connectAttr('%sFKIK_Leg_CTRL_Mux.outColorR' %LR, '%sFK_Knee_CTRL.visibility' %LR, f = True)
                        cmds.connectAttr('%sFKIK_Leg_CTRL_Mux.outColorR' %LR, '%sFK_Ankle_CTRL.visibility' %LR, f = True)
                        
                        #########Hiding Leg###########
                        cmds.setAttr('L_FK_Hip.visibility', 0)
                        cmds.setAttr('L_IK_Hip.visibility', 0)
                        cmds.setAttr('R_FK_Hip.visibility', 0)
                        cmds.setAttr('R_IK_Hip.visibility', 0)
                        
                ########Upper Lower Stretch######
                self.leftKneePos_Nw = cmds.xform('L_Knee', q = True, t = True)
                self.leftAnklePos_Nw = cmds.xform('L_Ankle', q = True, t = True)
                for LR in L_o_R:
                        cmds.addAttr('%sLeg_Extra_CTRL' %LR, ln = 'UpperStretch', at  = 'double', min = -10, max = 10)
                        cmds.setAttr('%sLeg_Extra_CTRL.UpperStretch' %LR, e =True, keyable = True)
                        cmds.addAttr('%sLeg_Extra_CTRL' %LR, ln = 'LowerStretch', at  = 'double', min = -10, max = 10)
                        cmds.setAttr('%sLeg_Extra_CTRL.LowerStretch' %LR, e =True, keyable = True)
                        cmds.createNode('setRange', n = '%sLeg_UpperLowerStretch_SetRange' %LR)
                        
                        ######Joint select Mux########
                
                        cmds.connectAttr('%sLeg_Extra_CTRL.UpperStretch' %LR, '%sLeg_UpperLowerStretch_SetRange.valueX' %LR, f = True)
                        cmds.connectAttr('%sLeg_Extra_CTRL.LowerStretch' %LR, '%sLeg_UpperLowerStretch_SetRange.valueY' %LR, f = True)
                        
                        cmds.shadingNode('multiplyDivide', n = '%sLeg_UpperLowerStretch_Mul'%LR ,asUtility = True)
                        cmds.setAttr('%sLeg_UpperLowerStretch_Mul.input1X' %LR, self.leftKneePos_Nw[1])
                        cmds.setAttr('%sLeg_UpperLowerStretch_Mul.input2X' %LR, 2)
                        cmds.setAttr('%sLeg_UpperLowerStretch_Mul.input1Y' %LR, self.leftAnklePos_Nw[1])
                        cmds.setAttr('%sLeg_UpperLowerStretch_Mul.input2Y' %LR, 2)
                        
                        cmds.setAttr('%sLeg_UpperLowerStretch_SetRange.oldMinX' %LR, -10)
                        cmds.setAttr('%sLeg_UpperLowerStretch_SetRange.oldMaxX' %LR, 10)
                        cmds.setAttr('%sLeg_UpperLowerStretch_SetRange.oldMinY' %LR, -10)
                        cmds.setAttr('%sLeg_UpperLowerStretch_SetRange.oldMaxY' %LR, 10)
                        
                        cmds.setAttr('%sLeg_UpperLowerStretch_SetRange.minX' %LR, 0)
                        cmds.connectAttr('%sLeg_UpperLowerStretch_Mul.outputX' %LR, '%sLeg_UpperLowerStretch_SetRange.maxX' %LR)
                        cmds.setAttr('%sLeg_UpperLowerStretch_SetRange.minY' %LR, 0)
                        cmds.connectAttr('%sLeg_UpperLowerStretch_Mul.outputY' %LR, '%sLeg_UpperLowerStretch_SetRange.maxY' %LR)
                        
                        cmds.connectAttr('%sLeg_UpperLowerStretch_SetRange.outValueX' %LR, '%sFK_Knee.translateY' %LR)
                        cmds.connectAttr('%sLeg_UpperLowerStretch_SetRange.outValueX' %LR, '%sIK_Knee.translateY' %LR)
                        cmds.connectAttr('%sLeg_UpperLowerStretch_SetRange.outValueY' %LR, '%sFK_Ankle.translateY' %LR)
                        cmds.connectAttr('%sLeg_UpperLowerStretch_SetRange.outValueY' %LR, '%sIK_Ankle.translateY' %LR)
                        
                        cmds.select('%sKnee' %LR, r = True)
                        cmds.select('%sFK_Knee_CTRL_GRP' %LR, tgl = True)
                        cmds.pointConstraint(weight = 1)
                        cmds.select('%sAnkle' %LR, r = True)
                        cmds.select('%sFK_Ankle_CTRL_GRP' %LR, tgl = True)
                        cmds.pointConstraint(weight = 1)
                        
                        cmds.select('%sFK_Hip_CTRL_GRP' %LR, r = True)
                        cmds.select('Pelvis_CTRL', tgl = True)
                        cmds.parent()
                
                ######FK Leg Joint Seperate#######              
                cmds.createNode('transform', n = 'FK_Leg_Joint_GRP')
                cmds.select('Puck', tgl = True)
                cmds.parent()
                cmds.select('Pelvis', r = True)
                cmds.select('FK_Leg_Joint_GRP', tgl = True)
                cmds.parentConstraint(weight = 1)
                
                for LR in L_o_R:
                        cmds.select('%sFK_Hip' %LR, r = True)
                        cmds.select('FK_Leg_Joint_GRP', tgl = True)
                        cmds.parent()           
                
                ######IK Leg Joint Seperate#######
                cmds.createNode('transform', n = 'IK_Leg_Joint_GRP')
                cmds.select('Puck', tgl = True)
                cmds.parent()
                cmds.select('Pelvis', r = True)
                cmds.select('IK_Leg_Joint_GRP', tgl = True)
                cmds.parentConstraint(weight = 1)
                
                for LR in L_o_R:
                        cmds.select('%sIK_Hip' %LR, r = True)
                        cmds.select('IK_Leg_Joint_GRP', tgl = True)
                        cmds.parent()
                        
        def spineSetting(self):                
                ######Root Constraint##############
                cmds.select('Root_CTRL', r = True)
                cmds.select('Root', tgl = True)
                cmds.orientConstraint(offset = [0, 0, 0], weight = 1)
                cmds.pointConstraint(offset = [0, 0, 0], weight = 1)
                
                ######Pelvis Constratint############
                
                cmds.select('Pelvis_CTRL', r = True)
                cmds.select('Pelvis', tgl = True)
                cmds.orientConstraint(offset = [0, 0, 0], weight = 1)
                cmds.pointConstraint(offset = [0, 0, 0], weight = 1)
                
                ######FK Spine Constraint###########
                spine_CTRLs = self.spineJoints[1:7]
                for i in range(len(spine_CTRLs)):
                        cmds.select('%s_CTRL' %spine_CTRLs[i], r = True)
                        cmds.select('%s' %spine_CTRLs[i], tgl = True)
                        cmds.orientConstraint(offset = [0, 0, 0], weight = 1) 
                
                #######Jaw Constraint###############
                cmds.select('Jaw_CTRL', r = True)
                cmds.select('Jaw', tgl = True)
                cmds.orientConstraint(offset = [0, 0, 0], weight = 1) 
                cmds.pointConstraint(offset = [0, 0, 0], weight = 1)
                
                cmds.select(cl = True)
                cmds.select('Jaw_CTRL.cv[1]', r = True)
                cmds.select('Jaw_CTRL.cv[5]', tgl = True)
                cmds.move(0, 0, -5.5, r = True) 
                cmds.select('Jaw_CTRL.cv[0]', r = True)
                for i in range(7):
                        cmds.select('Jaw_CTRL.cv[%i]' %(i+1), tgl = True)
                cmds.rotate(0, 0, -45, r = True)
                cmds.move(0, -self.jawAimPos[1]/5, self.jawAimPos[2]*2/3, r = True)
                cmds.select(cl = True)
                self.spineJoints_attr = self.spineJoints[0:-2]
                for Attr in self.spineJoints_attr:
                        cmds.setAttr('%s_CTRL.scaleX' %Attr, lock  = True, keyable = False, channelBox = False)
                        cmds.setAttr('%s_CTRL.scaleY' %Attr, lock  = True, keyable = False, channelBox = False)
                        cmds.setAttr('%s_CTRL.scaleZ' %Attr, lock  = True, keyable = False, channelBox = False)
                        cmds.setAttr('%s_CTRL.visibility' %Attr, lock  = True, keyable = False, channelBox = False)
                        
        def armSetting(self, TwistArm):
                ######################Controllers#######################
                for LR in L_o_R:
                        #############Scapula Setting############
                        
                        cmds.select('%sScapula' %LR, r = True)
                        cmds.select('%sScapula_CTRL_GRP' %LR, tgl = True)
                        cmds.orientConstraint(offset = [0, 0, 0], weight = 1) 
                        cmds.delete('%sScapula_CTRL_GRP_orientConstraint1' %LR)
                        cmds.select('%sScapula_CTRL_GRP' %LR, r = True)
                        cmds.select('Spine4_CTRL', add = True)
                        cmds.parent()
                        cmds.select('%sScapula_CTRL' %LR, r = True)
                        cmds.select('%sScapula' %LR, tgl = True)
                        cmds.orientConstraint(offset = [0, 0, 0], weight = 1) 
                        cmds.pointConstraint(offset = [0, 0, 0], weight = 1) 

                        cmds.select('%sShoulder' %LR, r = True)
                        cmds.duplicate(rr = True)
                        cmds.parent(w = True)
                        cmds.rename('%sShoulder1' %LR, '%sFK_Shoulder' %LR )
                        cmds.rename('%sFK_Shoulder|%sElbow' %(LR, LR), '%sFK_Elbow' %LR )
                        cmds.rename('%sFK_Shoulder|%sFK_Elbow|%sWrist' %(LR, LR, LR), '%sFK_Wrist' %LR )
                        cmds.delete('%sFK_Shoulder|%sFK_Elbow|%sFK_Wrist|%sPalm' %(LR, LR, LR, LR))
                        
                ############Create FK Arm###################
                FK_Joints = ['Shoulder', 'Elbow', 'Wrist']
                for LR in L_o_R:
                        for Joint in FK_Joints:
                                cmds.select('%sFK_%s' %(LR, Joint), r = True)
                                cmds.select('%s%s_FK_CTRL_GRP' %(LR, Joint), tgl = True)
                                cmds.orientConstraint(offset = [0, 0, 0], weight = 1) 
                                cmds.delete('%s%s_FK_CTRL_GRP_orientConstraint1' %(LR, Joint))
                                cmds.select('%s%s_FK_CTRL' %(LR, Joint), r = True)
                                cmds.select('%sFK_%s' %(LR, Joint), tgl = True)
                                cmds.orientConstraint(offset = [0, 0, 0], weight = 1) 
                                #cmds.connectAttr('%s%s_FK_CTRL.rotate' %(LR, Joint), '%sFK_%s.rotate' %(LR, Joint))
                        
                        ############Create IK Arm###################
                        cmds.select('%sShoulder' %LR, r = True)
                        cmds.duplicate(rr = True)
                        cmds.parent(w = True)
                        cmds.rename('%sShoulder1' %LR, '%sIK_Shoulder' %LR )
                        cmds.rename('%sIK_Shoulder|%sElbow' %(LR, LR), '%sIK_Elbow' %LR )
                        cmds.rename('%sIK_Shoulder|%sIK_Elbow|%sWrist' %(LR, LR, LR), '%sIK_Wrist' %LR )
                        cmds.delete('%sIK_Shoulder|%sIK_Elbow|%sIK_Wrist|%sPalm' %(LR, LR, LR, LR))
                        cmds.select('%sIK_Shoulder.rotatePivot' %LR, r = True) 
                        cmds.select('%sIK_Wrist.rotatePivot' %LR, add = True)
                        cmds.ikHandle(n = '%sArm_IKHandle' %LR, sol = 'ikRPsolver')
                        cmds.select('%sWrist.rotatePivot' %LR, r = True) 
                        cmds.select('%sPalm.rotatePivot' %LR, add = True)
                        cmds.ikHandle(n = '%sIKWrist_IKHandle' %LR, sol = 'ikSCsolver')
                        cmds.createNode('transform', n = '%sWrist_IKSC_Zero_GRP' %LR )
                        cmds.createNode('transform', n = '%sWrist_IKSC_GRP' %LR )
                        cmds.select('%sWrist_IKSC_Zero_GRP' %LR, tgl = True )
                        cmds.parent()
                        
                        cmds.select('%sWrist' %LR, r = True)
                        cmds.select('%sWrist_IKSC_Zero_GRP' %LR, tgl = True)
                        cmds.orientConstraint(offset = [0, 0, 0], weight = 1)
                        cmds.pointConstraint(offset = [0, 0, 0], weight = 1)
                        cmds.delete('%sWrist_IKSC_Zero_GRP_orientConstraint1' %LR)
                        cmds.delete('%sWrist_IKSC_Zero_GRP_pointConstraint1' %LR)
                        
                        cmds.select('%sIKWrist_IKHandle' %LR, r = True)
                        cmds.select('%sWrist_IKSC_GRP' %LR, tgl = True)
                        cmds.parent()
                        cmds.select('%sWrist_IKSC_Zero_GRP' %LR, r = True)
                        cmds.select('Puck', tgl = True)
                        cmds.parent()
                        
                        #####FK Wrist Connect############
                        cmds.delete('%sFK_Wrist_orientConstraint1' %LR)
                        cmds.select('%sWrist_FK_CTRL' %LR, r = True)
                        cmds.select('%sWrist_IKSC_GRP' %LR, tgl = True)
                        cmds.orientConstraint(offset = [0, 0, 0], weight = 1)
                        
                        #####IK Connect#############
                        cmds.select('%sIK_Wrist' %LR, r = True)
                        cmds.select('%sArm_IK_CTRL_GRP' %LR, tgl = True)
                        cmds.orientConstraint(offset = [0, 0, 0], weight = 1)
                        cmds.delete('%sArm_IK_CTRL_GRP_orientConstraint1' %LR)
                        
                        cmds.select('%sWrist' %LR, r = True)
                        cmds.select('%sWrist_IKSC_GRP' %LR, tgl = True)
                        cmds.pointConstraint(offset = [0, 0, 0], weight = 1)
                        
                        cmds.select('%sArm_IK_CTRL' %LR, r = True)
                        cmds.select('%sArm_IKHandle' %LR, tgl = True)
                        cmds.pointConstraint(offset = [0, 0, 0], weight = 1)
                        #cmds.connectAttr('%sArm_IK_CTRL.translate' %LR, '%sArm_IKHandle.translate' %LR)
                        
                        cmds.select('%sArm_IK_CTRL' %LR, r = True)
                        cmds.select('%sWrist_IKSC_GRP' %LR, tgl = True)
                        cmds.orientConstraint(offset = [0, 0, 0], weight = 1)
                        #cmds.connectAttr('%sArm_IK_CTRL.rotate' %LR, '%sIK_Wrist.rotate' %LR)
                                                
                        ########Polevector################
                        cmds.select('%sArm_Polevector' %LR, r = True)
                        cmds.select('%sArm_IKHandle' %LR, tgl = True)
                        cmds.poleVectorConstraint(weight = 1)
                                        
                ############Arm CTRL parenting###############
                for LR in L_o_R:
                        cmds.select('%sWrist_FK_CTRL_GRP' %LR, r = True)
                        cmds.select('%sElbow_FK_CTRL' %LR, tgl = True)
                        cmds.parent()
                        cmds.select('%sElbow_FK_CTRL_GRP' %LR, r = True)
                        cmds.select('%sShoulder_FK_CTRL' %LR, tgl = True)
                        cmds.parent()
                        cmds.select('%sShoulder_FK_CTRL_GRP' %LR, r = True)
                        cmds.select('%sScapula_CTRL' %LR, tgl = True)
                        cmds.parent()
                        cmds.select('%sArm_Extra_CTRL_GRP' %LR, r = True)
                        cmds.select('%sWrist' %LR, tgl = True)
                        cmds.parent()
                
                ###########FKIK Setting###############
                        cmds.select('%sArm_Extra_CTRL' %LR)
                        cmds.setAttr('%sArm_Extra_CTRL.tx' %LR, lock = True, keyable  = False, channelBox = False)
                        cmds.setAttr('%sArm_Extra_CTRL.ty' %LR, lock = True, keyable  = False, channelBox = False)
                        cmds.setAttr('%sArm_Extra_CTRL.tz' %LR, lock = True, keyable  = False, channelBox = False)
                        cmds.setAttr('%sArm_Extra_CTRL.rx' %LR, lock = True, keyable  = False, channelBox = False)
                        cmds.setAttr('%sArm_Extra_CTRL.ry' %LR, lock = True, keyable  = False, channelBox = False)
                        cmds.setAttr('%sArm_Extra_CTRL.rz' %LR, lock = True, keyable  = False, channelBox = False)
                        cmds.setAttr('%sArm_Extra_CTRL.sx' %LR, lock = True, keyable  = False, channelBox = False)
                        cmds.setAttr('%sArm_Extra_CTRL.sy' %LR, lock = True, keyable  = False, channelBox = False)
                        cmds.setAttr('%sArm_Extra_CTRL.sz' %LR, lock = True, keyable  = False, channelBox = False)
                        cmds.setAttr('%sArm_Extra_CTRL.v' %LR, lock = True, keyable  = False, channelBox = False)
                        ##############add Extra attributes####################
                        cmds.addAttr(ln = 'FKIK', at = 'long', min = 0, max = 1)
                        cmds.setAttr('%sArm_Extra_CTRL.FKIK' %LR, e = True, keyable = True)
                        #cmds.addAttr(ln = 'Stretch_IK', at = 'long', min = 0, max = 1)
                        #cmds.setAttr('%sArm_Extra_CTRL.Stretch_IK' %LR, e = True, keyable = True)
                        
                #########FKIK Switch Node#############
                        ###rotate###
                        cmds.shadingNode('blendColors', n = '%sFKIK_Shoulder_Mux' %LR, asUtility = True)
                        cmds.connectAttr('%sArm_Extra_CTRL.FKIK' %LR, '%sFKIK_Shoulder_Mux.blender' %LR, f = True)
                        print 'TwistArm = %s' %TwistArm
                        if TwistArm == False:
                                cmds.connectAttr('%sFK_Shoulder.rotateX' %LR, '%sFKIK_Shoulder_Mux.color2R' %LR, f = True)
                        cmds.connectAttr('%sFK_Shoulder.rotateY' %LR, '%sFKIK_Shoulder_Mux.color2G' %LR, f = True)
                        cmds.connectAttr('%sFK_Shoulder.rotateZ' %LR, '%sFKIK_Shoulder_Mux.color2B' %LR, f = True)
                        cmds.connectAttr('%sIK_Shoulder.rotateX' %LR, '%sFKIK_Shoulder_Mux.color1R' %LR, f = True)
                        cmds.connectAttr('%sIK_Shoulder.rotateY' %LR, '%sFKIK_Shoulder_Mux.color1G' %LR, f = True)
                        cmds.connectAttr('%sIK_Shoulder.rotateZ' %LR, '%sFKIK_Shoulder_Mux.color1B' %LR, f = True)
                        cmds.connectAttr('%sFKIK_Shoulder_Mux.outputR' %LR, '%sShoulder.rotateX' %LR, f = True)
                        cmds.connectAttr('%sFKIK_Shoulder_Mux.outputG' %LR, '%sShoulder.rotateY' %LR, f = True)
                        cmds.connectAttr('%sFKIK_Shoulder_Mux.outputB' %LR, '%sShoulder.rotateZ' %LR, f = True)
                        
                        cmds.select('%sFK_Elbow' %LR, r = True)
                        cmds.select('%sElbow' %LR, tgl = True)
                        cmds.orientConstraint(weight = 1, mo = True)
                        cmds.select('%sIK_Elbow' %LR, r = True)
                        cmds.select('%sElbow' %LR, tgl = True)
                        cmds.orientConstraint(weight = 1, mo = True)
                        
                        cmds.createNode('reverse', n = '%sElbow_FKIK' %LR)
                        cmds.connectAttr('%sArm_Extra_CTRL.FKIK' %LR, '%sElbow_FKIK.inputX' %LR)
                        cmds.connectAttr('%sArm_Extra_CTRL.FKIK' %LR, '%sElbow_orientConstraint1.%sIK_ElbowW1' %(LR, LR))
                        cmds.connectAttr('%sElbow_FKIK.outputX' %LR, '%sElbow_orientConstraint1.%sFK_ElbowW0' %(LR, LR))
                        
                        #cmds.shadingNode('blendColors', n = '%sFKIK_Elbow_Mux' %LR, asUtility = True)
                        #cmds.connectAttr('%sArm_Extra_CTRL.FKIK' %LR, '%sFKIK_Elbow_Mux.blender' %LR, f = True)
                        #cmds.connectAttr('%sFK_Elbow.rotateX' %LR, '%sFKIK_Elbow_Mux.color2R' %LR, f = True)
                        #cmds.connectAttr('%sFK_Elbow.rotateY' %LR, '%sFKIK_Elbow_Mux.color2G' %LR, f = True)
                        #cmds.connectAttr('%sFK_Elbow.rotateZ' %LR, '%sFKIK_Elbow_Mux.color2B' %LR, f = True)
                        #cmds.connectAttr('%sIK_Elbow.rotateX' %LR, '%sFKIK_Elbow_Mux.color1R' %LR, f = True)
                        #cmds.connectAttr('%sIK_Elbow.rotateY' %LR, '%sFKIK_Elbow_Mux.color1G' %LR, f = True)
                        #cmds.connectAttr('%sIK_Elbow.rotateZ' %LR, '%sFKIK_Elbow_Mux.color1B' %LR, f = True)
                        #cmds.connectAttr('%sFKIK_Elbow_Mux.outputR' %LR, '%sElbow.rotateX' %LR, f = True)
                        #cmds.connectAttr('%sFKIK_Elbow_Mux.outputG' %LR, '%sElbow.rotateY' %LR, f = True)
                        #cmds.connectAttr('%sFKIK_Elbow_Mux.outputB' %LR, '%sElbow.rotateZ' %LR, f = True)
                        
                        cmds.shadingNode('blendColors', n = '%sFKIK_Wrist_Mux' %LR, asUtility = True)
                        cmds.connectAttr('%sArm_Extra_CTRL.FKIK' %LR, '%sFKIK_Wrist_Mux.blender' %LR, f = True)
                        cmds.connectAttr('%sFK_Wrist.rotateX' %LR, '%sFKIK_Wrist_Mux.color2R' %LR, f = True)
                        cmds.connectAttr('%sFK_Wrist.rotateY' %LR, '%sFKIK_Wrist_Mux.color2G' %LR, f = True)
                        cmds.connectAttr('%sFK_Wrist.rotateZ' %LR, '%sFKIK_Wrist_Mux.color2B' %LR, f = True)
                        cmds.connectAttr('%sIK_Wrist.rotateX' %LR, '%sFKIK_Wrist_Mux.color1R' %LR, f = True)
                        cmds.connectAttr('%sIK_Wrist.rotateY' %LR, '%sFKIK_Wrist_Mux.color1G' %LR, f = True)
                        cmds.connectAttr('%sIK_Wrist.rotateZ' %LR, '%sFKIK_Wrist_Mux.color1B' %LR, f = True)
                        cmds.connectAttr('%sFKIK_Wrist_Mux.outputR' %LR, '%sWrist.rotateX' %LR, f = True)
                        cmds.connectAttr('%sFKIK_Wrist_Mux.outputG' %LR, '%sWrist.rotateY' %LR, f = True)
                        cmds.connectAttr('%sFKIK_Wrist_Mux.outputB' %LR, '%sWrist.rotateZ' %LR, f = True)
                        ####translate###                        
                        cmds.shadingNode('blendColors', n = '%sFKIK_Elbow_Translate_Mux' %LR, asUtility = True)
                        cmds.connectAttr('%sArm_Extra_CTRL.FKIK' %LR, '%sFKIK_Elbow_Translate_Mux.blender' %LR, f = True)
                        cmds.connectAttr('%sFK_Elbow.translateX' %LR, '%sFKIK_Elbow_Translate_Mux.color2R' %LR, f = True)
                        cmds.connectAttr('%sFK_Elbow.translateY' %LR, '%sFKIK_Elbow_Translate_Mux.color2G' %LR, f = True)
                        cmds.connectAttr('%sFK_Elbow.translateZ' %LR, '%sFKIK_Elbow_Translate_Mux.color2B' %LR, f = True)
                        cmds.connectAttr('%sIK_Elbow.translateX' %LR, '%sFKIK_Elbow_Translate_Mux.color1R' %LR, f = True)
                        cmds.connectAttr('%sIK_Elbow.translateY' %LR, '%sFKIK_Elbow_Translate_Mux.color1G' %LR, f = True)
                        cmds.connectAttr('%sIK_Elbow.translateZ' %LR, '%sFKIK_Elbow_Translate_Mux.color1B' %LR, f = True)
                        cmds.connectAttr('%sFKIK_Elbow_Translate_Mux.outputR' %LR, '%sElbow.translateX' %LR, f = True)
                        cmds.connectAttr('%sFKIK_Elbow_Translate_Mux.outputG' %LR, '%sElbow.translateY' %LR, f = True)
                        cmds.connectAttr('%sFKIK_Elbow_Translate_Mux.outputB' %LR, '%sElbow.translateZ' %LR, f = True)
                        
                        cmds.shadingNode('blendColors', n = '%sFKIK_Wrist_Translate_Mux' %LR, asUtility = True)
                        cmds.connectAttr('%sArm_Extra_CTRL.FKIK' %LR, '%sFKIK_Wrist_Translate_Mux.blender' %LR, f = True)
                        cmds.connectAttr('%sFK_Wrist.translateX' %LR, '%sFKIK_Wrist_Translate_Mux.color2R' %LR, f = True)
                        cmds.connectAttr('%sFK_Wrist.translateY' %LR, '%sFKIK_Wrist_Translate_Mux.color2G' %LR, f = True)
                        cmds.connectAttr('%sFK_Wrist.translateZ' %LR, '%sFKIK_Wrist_Translate_Mux.color2B' %LR, f = True)
                        cmds.connectAttr('%sIK_Wrist.translateX' %LR, '%sFKIK_Wrist_Translate_Mux.color1R' %LR, f = True)
                        cmds.connectAttr('%sIK_Wrist.translateY' %LR, '%sFKIK_Wrist_Translate_Mux.color1G' %LR, f = True)
                        cmds.connectAttr('%sIK_Wrist.translateZ' %LR, '%sFKIK_Wrist_Translate_Mux.color1B' %LR, f = True)
                        cmds.connectAttr('%sFKIK_Wrist_Translate_Mux.outputR' %LR, '%sWrist.translateX' %LR, f = True)
                        cmds.connectAttr('%sFKIK_Wrist_Translate_Mux.outputG' %LR, '%sWrist.translateY' %LR, f = True)
                        cmds.connectAttr('%sFKIK_Wrist_Translate_Mux.outputB' %LR, '%sWrist.translateZ' %LR, f = True)
                        ####FKIK CTRL Hide                      
                        cmds.connectAttr('%sArm_Extra_CTRL.FKIK' %LR, '%sArm_IK_CTRL.visibility' %LR , f = True)
                        cmds.connectAttr('%sArm_Extra_CTRL.FKIK' %LR, '%sArm_Polevector.visibility' %LR , f = True)
                        cmds.shadingNode('condition', n = '%sFKIK_CTRL_Mux' %LR, asUtility = True)
                        cmds.setAttr('%sFKIK_CTRL_Mux.secondTerm' %LR, 0)
                        cmds.setAttr('%sFKIK_CTRL_Mux.operation' %LR, 0)
                        cmds.setAttr('%sFKIK_CTRL_Mux.colorIfTrueR' %LR, 1)
                        cmds.setAttr('%sFKIK_CTRL_Mux.colorIfFalseR' %LR, 0)
                        
                        cmds.connectAttr('%sArm_Extra_CTRL.FKIK' %LR, '%sFKIK_CTRL_Mux.firstTerm' %LR, f = True)
                        cmds.connectAttr('%sFKIK_CTRL_Mux.outColorR' %LR, '%sShoulder_FK_CTRL.visibility' %LR, f = True)
                        cmds.connectAttr('%sFKIK_CTRL_Mux.outColorR' %LR, '%sElbow_FK_CTRL.visibility' %LR, f = True)
                        cmds.connectAttr('%sFKIK_CTRL_Mux.outColorR' %LR, '%sWrist_FK_CTRL.visibility' %LR, f = True)
                        
                        ###########Arm Parenting##################
                        cmds.createNode('transform', n = '%sFK_Arm_Joint_GRP' %LR)
                        cmds.select('%sFK_Shoulder' %LR, r = True)
                        cmds.select('%sFK_Arm_Joint_GRP' %LR, tgl = True)
                        cmds.parent()
                        cmds.createNode('transform', n = '%sIK_Arm_Joint_GRP' %LR)
                        cmds.select('%sIK_Shoulder' %LR, r = True)
                        cmds.select('%sIK_Arm_Joint_GRP' %LR, tgl = True)
                        cmds.parent()
                        cmds.createNode('transform', n = '%sArm_FKIK_GRP' %LR)
                        cmds.select('%sFK_Arm_Joint_GRP' %LR, r = True)
                        cmds.select('%sIK_Arm_Joint_GRP' %LR, tgl = True)
                        cmds.select('%sArm_IKHandle' %LR, tgl = True)
                        cmds.select('%sArm_FKIK_GRP' %LR, tgl = True)
                        cmds.parent()
                        cmds.setAttr('%sArm_FKIK_GRP.visibility' %LR,0)
                        cmds.select('%sScapula' %LR, r = True)
                        cmds.select('%sFK_Arm_Joint_GRP' %LR, tgl = True)
                        cmds.parentConstraint(mo = True, weight = 1)
                        cmds.select('%sScapula' %LR, r = True)
                        cmds.select('%sIK_Arm_Joint_GRP' %LR, tgl = True)                       
                        cmds.parentConstraint(mo = True, weight = 1)
                        
                        ###########FKIK Match Locator##########
                        cmds.spaceLocator(n = '%sWrist_Match' %LR, p = [0, 0, 0])
                        cmds.createNode('transform', n = '%sWrist_Match_GRP' %LR)
                        cmds.select('%sWrist_Match' %LR, r = True)
                        cmds.select('%sWrist_Match_GRP' %LR, tgl = True)
                        cmds.parent()
                        if LR == 'L_':
                                cmds.xform('%sWrist_Match_GRP' %LR, t = [self.leftWristPos[0], self.leftWristPos[1], self.leftWristPos[2]] )
                        else: 
                                cmds.xform('%sWrist_Match_GRP' %LR, t = [-self.leftWristPos[0], self.leftWristPos[1], self.leftWristPos[2]] )     
                        cmds.select('%sWrist_IKSC_GRP' %LR, r = True)
                        cmds.select('%sWrist_Match_GRP' %LR, tgl = True)
                        cmds.orientConstraint(weight = 1)
                        cmds.delete('%sWrist_Match_GRP_orientConstraint1' %LR)
                        
                        cmds.select('%sWrist_Match_GRP' %LR, r = True)
                        cmds.select('Puck', tgl = True)
                        cmds.parent()
                        
                        cmds.select('%sWrist' %LR, r = True)
                        cmds.select('%sWrist_Match' %LR, tgl = True)
                        cmds.orientConstraint(mo = True, weight = 1)
                        cmds.pointConstraint(mo =True, weight = 1)
                        cmds.setAttr('%sWrist_Match.visibility' %LR, 0)
                        
                        ########FKIK Wrist Selection########
                        #cmds.connectAttr('%sArm_Extra_CTRL.FKIK' %LR, '%sWrist_IKSC_GRP_orientConstraint1.%sWrist_FK_CTRLW0' %(LR, LR))
                        cmds.connectAttr('%sArm_Extra_CTRL.FKIK' %LR, '%sWrist_IKSC_GRP_orientConstraint1.%sArm_IK_CTRLW1' %(LR, LR))
                        cmds.createNode('reverse', n = '%sFKIK_WristSelect' %LR)
                        cmds.connectAttr('%sArm_Extra_CTRL.FKIK' %LR, '%sFKIK_WristSelect.inputX' %LR)
                        cmds.connectAttr('%sFKIK_WristSelect.outputX' %LR, '%sWrist_IKSC_GRP_orientConstraint1.%sWrist_FK_CTRLW0' %(LR, LR))                    
                        
                        cmds.setAttr('%sIKWrist_IKHandle.visibility' %LR, 0)
                
                ########Upper Lower Stretch######
                self.leftElbowPos_Nw = cmds.xform('L_Elbow', q = True, t = True)
                self.leftWristPos_Nw = cmds.xform('L_Wrist', q = True, t = True)
                for LR in L_o_R:
                        cmds.addAttr('%sArm_Extra_CTRL' %LR, ln = 'UpperStretch', at  = 'double', min = -10, max = 10)
                        cmds.setAttr('%sArm_Extra_CTRL.UpperStretch' %LR, e =True, keyable = True)
                        cmds.addAttr('%sArm_Extra_CTRL' %LR, ln = 'LowerStretch', at  = 'double', min = -10, max = 10)
                        cmds.setAttr('%sArm_Extra_CTRL.LowerStretch' %LR, e =True, keyable = True)
                        cmds.createNode('setRange', n = '%sArm_UpperLowerStretch_SetRange' %LR)
                        
                        ######Joint select Mux########
                
                        cmds.connectAttr('%sArm_Extra_CTRL.UpperStretch' %LR, '%sArm_UpperLowerStretch_SetRange.valueX' %LR, f = True)
                        cmds.connectAttr('%sArm_Extra_CTRL.LowerStretch' %LR, '%sArm_UpperLowerStretch_SetRange.valueY' %LR, f = True)
                        
                        cmds.shadingNode('multiplyDivide', n = '%sArm_UpperLowerStretch_Mul'%LR ,asUtility = True)
                        print self.leftElbowPos_Nw[0]
                        cmds.setAttr('%sArm_UpperLowerStretch_Mul.input1X' %LR, self.leftElbowPos_Nw[0])
                        cmds.setAttr('%sArm_UpperLowerStretch_Mul.input2X' %LR, 2)
                        cmds.setAttr('%sArm_UpperLowerStretch_Mul.input1Y' %LR, self.leftWristPos_Nw[0])
                        cmds.setAttr('%sArm_UpperLowerStretch_Mul.input2Y' %LR, 2)
                        
                        cmds.setAttr('%sArm_UpperLowerStretch_SetRange.oldMinX' %LR, -10)
                        cmds.setAttr('%sArm_UpperLowerStretch_SetRange.oldMaxX' %LR, 10)
                        cmds.setAttr('%sArm_UpperLowerStretch_SetRange.oldMinY' %LR, -10)
                        cmds.setAttr('%sArm_UpperLowerStretch_SetRange.oldMaxY' %LR, 10)
                        
                        cmds.setAttr('%sArm_UpperLowerStretch_SetRange.minX' %LR, 0)
                        cmds.connectAttr('%sArm_UpperLowerStretch_Mul.outputX' %LR, '%sArm_UpperLowerStretch_SetRange.maxX' %LR)
                        cmds.setAttr('%sArm_UpperLowerStretch_SetRange.minY' %LR, 0)
                        cmds.connectAttr('%sArm_UpperLowerStretch_Mul.outputY' %LR, '%sArm_UpperLowerStretch_SetRange.maxY' %LR)
                        
                        cmds.connectAttr('%sArm_UpperLowerStretch_SetRange.outValueX' %LR, '%sFK_Elbow.translateX' %LR)
                        cmds.connectAttr('%sArm_UpperLowerStretch_SetRange.outValueX' %LR, '%sIK_Elbow.translateX' %LR)
                        cmds.connectAttr('%sArm_UpperLowerStretch_SetRange.outValueY' %LR, '%sFK_Wrist.translateX' %LR)
                        cmds.connectAttr('%sArm_UpperLowerStretch_SetRange.outValueY' %LR, '%sIK_Wrist.translateX' %LR)
                        
                        cmds.select('%sElbow' %LR, r = True)
                        cmds.select('%sElbow_FK_CTRL_GRP' %LR, tgl = True)
                        cmds.pointConstraint(weight = 1)
                        cmds.select('%sWrist' %LR, r = True)
                        cmds.select('%sWrist_FK_CTRL_GRP' %LR, tgl = True)
                        cmds.pointConstraint(weight = 1)
                        
        def fingerSetting(self, No_Fingers, Thumb_YN):
                print 'is thumb ? : ', Thumb_YN
                print 'how many fingers ? : ', No_Fingers
                #####FInger CTRL####
                for LR in L_o_R:
                        
                        '''Do this if the Arm is 45 degrees
                        cmds.select('%sPalm' %LR, r = True)
                        cmds.select('%sPalmFinger_CTRL_GRP' %LR, tgl = True)
                        cmds.orientConstraint(offset = [0, 0, 0], weight = 1)
                        cmds.delete('%sPalmFinger_CTRL_GRP_orientConstraint1' %LR)'''
                        
                        cmds.select('%sPalmFinger_CTRL_GRP' %LR, r = True)
                        cmds.select('%sPalm' %LR, tgl = True)
                        cmds.parent()
                        cmds.select('%sPalmFinger_CTRL' %LR, r = True)
                        cmds.setAttr('%sPalmFinger_CTRL.tx' %LR, lock = True, keyable  = False, channelBox = False)
                        cmds.setAttr('%sPalmFinger_CTRL.ty' %LR, lock = True, keyable  = False, channelBox = False)
                        cmds.setAttr('%sPalmFinger_CTRL.tz' %LR, lock = True, keyable  = False, channelBox = False)
                        cmds.setAttr('%sPalmFinger_CTRL.rx' %LR, lock = True, keyable  = False, channelBox = False)
                        cmds.setAttr('%sPalmFinger_CTRL.ry' %LR, lock = True, keyable  = False, channelBox = False)
                        cmds.setAttr('%sPalmFinger_CTRL.rz' %LR, lock = True, keyable  = False, channelBox = False)
                        cmds.setAttr('%sPalmFinger_CTRL.sx' %LR, lock = True, keyable  = False, channelBox = False)
                        cmds.setAttr('%sPalmFinger_CTRL.sy' %LR, lock = True, keyable  = False, channelBox = False)
                        cmds.setAttr('%sPalmFinger_CTRL.sz' %LR, lock = True, keyable  = False, channelBox = False)
                        cmds.setAttr('%sPalmFinger_CTRL.v' %LR, lock = True, keyable  = False, channelBox = False)
                        
                        print self.fingerJointsLocal
                        ####add attributes####
                        ##Fingers
                        self.fingerJointsLocalAttr = self.fingerJointsLocal

                        Finger_Name = []
                        for Attr in self.fingerJointsLocalAttr:
                                Finger_Name.append('%sOOOOOOOOO' %Attr)
                        Finger_Attr = ['Base', 'Mid', 'Tip', 'Spread', 'Twist']

                        ##Thumb
                        if Thumb_YN == 'Yes':
                                Thumb_Attr = ['Base', 'Mid', 'Tip', 'Spread', 'Twist']
                                cmds.addAttr(ln = 'ThumbOOOOOOOOO', at = 'double')
                                cmds.setAttr('%sPalmFinger_CTRL.ThumbOOOOOOOOO' %LR, e = True, keyable = False, channelBox = True)
                        
                                for Attr in Thumb_Attr:
                                        cmds.addAttr(ln = 'T%s' %Attr, at = 'double')
                                        cmds.setAttr('%sPalmFinger_CTRL.T%s' %(LR, Attr), e = True, keyable = True)
                                Finger_Name = Finger_Name[1:]
                                for Finger in Finger_Name: 

                                        cmds.addAttr(ln = '%s' %Finger, at = 'double')
                                        cmds.setAttr('%sPalmFinger_CTRL.%s' %(LR, Finger), e = True, keyable = False, channelBox = True)
                                        for Attr in Finger_Attr:
                                                #cmds.select('%sPalmFinger_CTRL' %LR, r = True)
                                                cmds.addAttr(ln = '%s%s' %(Finger[0], Attr), at = 'double')
                                                cmds.setAttr('%sPalmFinger_CTRL.%s%s' %(LR, Finger[0], Attr), e = True, keyable = True)
                        ####W/O Thumb#######
                        else:
                                for Finger in Finger_Name: 

                                        cmds.addAttr(ln = '%s' %Finger, at = 'double')
                                        cmds.setAttr('%sPalmFinger_CTRL.%s' %(LR, Finger), e = True, keyable = False, channelBox = True)
                                        for Attr in Finger_Attr:
                                                #cmds.select('%sPalmFinger_CTRL' %LR, r = True)
                                                cmds.addAttr(ln = '%s%s' %(Finger[0], Attr), at = 'double')
                                                cmds.setAttr('%sPalmFinger_CTRL.%s%s' %(LR, Finger[0], Attr), e = True, keyable = True)                 
                        
                        
                        if Thumb_YN == 'Yes' and No_Fingers == 4:               
                                cmds.addAttr(ln = 'PalmOOOOOOOOOO', at = 'double')
                                cmds.setAttr('%sPalmFinger_CTRL.PalmOOOOOOOOOO' %LR, e = True, keyable = False, channelBox = True)
                                cmds.addAttr(ln = 'Cup', at = 'double', min = 0, max = 30)
                                cmds.setAttr('%sPalmFinger_CTRL.Cup' %LR, e = True, keyable = True)
                        
                        #############Connect Attributes###########
                        
                        #Finger_Connect_Name = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
                        Finger_Connect_Name = self.fingerJointsLocalAttr
                        XYZ = ['X', 'Y', 'Z']
                        for Connect in Finger_Connect_Name:
                                cmds.shadingNode('multiplyDivide',n = '%s%s_Connect_0' %(LR, Connect), asUtility = True)
                                cmds.shadingNode('multiplyDivide',n = '%s%s_Connect_1' %(LR, Connect), asUtility = True)
                                for i in range(2):
                                        cmds.setAttr('%s%s_Connect_%s.input2X' %(LR, Connect,str(i)),-1)
                                        cmds.setAttr('%s%s_Connect_%s.input2Y' %(LR, Connect,str(i)), -1)
                                        cmds.setAttr('%s%s_Connect_%s.input2Z' %(LR, Connect,str(i)), -1)
                                if Connect =='Thumb':
                                        for j in range(5):
                                                if j<3:
                                                        cmds.connectAttr('%sPalmFinger_CTRL.T%s' %(LR, Thumb_Attr[j]), '%s%s_Connect_0.input1%s' %(LR, Connect, XYZ[j]), f = True)
                                                        cmds.connectAttr('%s%s_Connect_0.output%s' %(LR, Connect, XYZ[j]), '%s%s%s.rotateZ' %(LR, Connect, str(j)), f = True)
                                                else:
                                                        cmds.connectAttr('%sPalmFinger_CTRL.T%s' %(LR, Thumb_Attr[j]), '%s%s_Connect_1.input1%s' %(LR, Connect, XYZ[j-2]), f = True)
                                                        if Thumb_Attr[j] == 'Spread':
                                                                cmds.connectAttr('%s%s_Connect_1.output%s' %(LR, Connect, XYZ[j-2]), '%s%s1.rotateY' %(LR, Connect), f = True)
                                                        else:
                                                                cmds.connectAttr('%s%s_Connect_1.output%s' %(LR, Connect, XYZ[j-2]), '%s%s1.rotateX' %(LR, Connect), f = True)
                                else:
                                        for j in range(5):
                                                if j<3:
                                                        cmds.connectAttr('%sPalmFinger_CTRL.%s%s' %(LR, Connect[0] ,Finger_Attr[j]), '%s%s_Connect_0.input1%s' %(LR, Connect, XYZ[j]), f = True)
                                                        cmds.connectAttr('%s%s_Connect_0.output%s' %(LR, Connect, XYZ[j]), '%s%s%s.rotateZ' %(LR, Connect, str(j+1)), f = True)
                                                else:
                                                        cmds.connectAttr('%sPalmFinger_CTRL.%s%s' %(LR, Connect[0] ,Finger_Attr[j]), '%s%s_Connect_1.input1%s' %(LR, Connect, XYZ[j-2]), f = True)
                                                        if Finger_Attr[j] == 'Spread':
                                                                cmds.connectAttr('%s%s_Connect_1.output%s' %(LR, Connect, XYZ[j-2]), '%s%s1.rotateY' %(LR, Connect), f = True)
                                                        else:
                                                                cmds.connectAttr('%s%s_Connect_1.output%s' %(LR, Connect, XYZ[j-2]), '%s%s1.rotateX' %(LR, Connect), f = True)
                        
                        if Thumb_YN == 'Yes' and No_Fingers == 4:
                                cmds.shadingNode('multiplyDivide', n = '%sPalmCup_inverse' %LR, asUtility = True)
                                cmds.setAttr('%sPalmCup_inverse.input2X' %LR, -1)
                                cmds.connectAttr('%sPalmFinger_CTRL.Cup' %LR, '%sPalmCup_inverse.input1X' %LR)
                                cmds.connectAttr('%sPalmFinger_CTRL.Cup' %LR, '%sThumb0.rotateX' %LR)
                                cmds.connectAttr('%sPalmCup_inverse. outputX' %LR, '%sPinky0.rotateZ' %LR)
                                #cmds.connectAttr('%sPalmCup_inverse. outputX' %LR, '%sRing0.rotateZ' %LR)
        
        def parenting(self):
                cmds.select('Root', r = True)
                cmds.select('L_Polevector_GRP', tgl = True)
                cmds.select('R_Polevector_GRP', tgl = True)
                cmds.select('Root_CTRL_GRP', tgl = True)
                cmds.select('L_Arm_IK_CTRL_GRP', tgl = True)
                cmds.select('L_Arm_Polevector_GRP', tgl = True)
                cmds.select('R_Arm_IK_CTRL_GRP', tgl = True)
                cmds.select('R_Arm_Polevector_GRP', tgl = True)
                cmds.select('L_Leg_CTRL_GRP', tgl = True)
                cmds.select('R_Leg_CTRL_GRP', tgl = True)
                cmds.select('L_Arm_FKIK_GRP', tgl = True)
                cmds.select('R_Arm_FKIK_GRP', tgl = True)
                cmds.select('Puck', tgl = True)
                cmds.parent()
                cmds.select(cl = True)  
                
        def stretchIkArm(self):
                for LR in L_o_R:
                        cmds.select('%sArm_Extra_CTRL' %LR)
                        cmds.addAttr(ln = 'Stretch_IK', at = 'long', min = 0, max = 1)
                        cmds.setAttr('%sArm_Extra_CTRL.Stretch_IK' %LR, e = True, keyable = True)

                ###Applies when both L, R arm's lengths are same. 
                        
                        ###Installing Locator
                        cmds.spaceLocator(n = '%sShoulder_Stretch_Loc' %LR)
                        if LR == 'L_':
                                cmds.move(self.leftShoulderPos[0], self.leftShoulderPos[1], self.leftShoulderPos[2])
                        else:
                                cmds.move(-self.leftShoulderPos[0], self.leftShoulderPos[1], self.leftShoulderPos[2])
                        cmds.select('%sShoulder' %LR, r = True)
                        cmds.select('%sShoulder_Stretch_Loc' %LR, tgl = True)
                        cmds.pointConstraint(offset = [0, 0, 0], weight = 1)
                        
                        cmds.spaceLocator(n = '%sWrist_Stretch_Loc' %LR)
                        if LR == 'L_':
                                cmds.move(self.leftWristPos[0], self.leftWristPos[1], self.leftWristPos[2])
                        else:
                                cmds.move(-self.leftWristPos[0], self.leftWristPos[1], self.leftWristPos[2])
                        cmds.select('%sArm_IK_CTRL' %LR, r = True)
                        cmds.select('%sWrist_Stretch_Loc' %LR, tgl = True)
                        cmds.pointConstraint(offset = [0, 0, 0], weight = 1)
                        
                        cmds.createNode('transform', n = '%sStretch_Arm_GRP' %LR)
                        cmds.select('%sShoulder_Stretch_Loc' %LR, r = True)
                        cmds.select('%sWrist_Stretch_Loc' %LR, add = True)
                        cmds.select('%sStretch_Arm_GRP' %LR, tgl = True)
                        cmds.parent()
                        cmds.select('%sStretch_Arm_GRP' %LR, r = True)
                        cmds.select('Puck', tgl = True)
                        cmds.parent()
                                                
                        Upper_Arm_Length = [self.leftElbowPos[0] - self.leftShoulderPos[0], self.leftElbowPos[1] - self.leftShoulderPos[1], self.leftElbowPos[2] - self.leftShoulderPos[2]]
                        Lower_Arm_Length = [self.leftWristPos[0] - self.leftElbowPos[0], self.leftWristPos[1] - self.leftElbowPos[1], self.leftWristPos[2] - self.leftElbowPos[2]]
                        Arm_Length = math.sqrt(Upper_Arm_Length[0]*Upper_Arm_Length[0]+Upper_Arm_Length[1]*Upper_Arm_Length[1]+Upper_Arm_Length[2]*Upper_Arm_Length[2])+math.sqrt(Lower_Arm_Length[0]*Lower_Arm_Length[0]+Lower_Arm_Length[1]*Lower_Arm_Length[1]+Lower_Arm_Length[2]*Lower_Arm_Length[2])
                        
                        ####Divided value by the scale of Puck.... distance between shoulder and wrist
                        cmds.shadingNode('multiplyDivide', n = '%sStretch_ArmIK_Length_MulDiv' %LR, asUtility = True)
                        cmds.setAttr('%sStretch_ArmIK_Length_MulDiv.operation' %LR, 1)
                        cmds.setAttr('%sStretch_ArmIK_Length_MulDiv.input1X' %LR, Arm_Length)
                        cmds.connectAttr('Puck.scaleX', '%sStretch_ArmIK_Length_MulDiv.input2X' %LR)
                        
                        ####Distance between shoulder and wrist CTRL
                        cmds.shadingNode('distanceBetween', n = '%sStretch_ArmIK_Distance' %LR, asUtility = True)
                        cmds.connectAttr('%sShoulder_Stretch_Loc.translateX' %LR, '%sStretch_ArmIK_Distance.point1X' %LR)
                        cmds.connectAttr('%sShoulder_Stretch_Loc.translateY' %LR, '%sStretch_ArmIK_Distance.point1Y' %LR)
                        cmds.connectAttr('%sShoulder_Stretch_Loc.translateZ' %LR, '%sStretch_ArmIK_Distance.point1Z' %LR)
                        cmds.connectAttr('%sWrist_Stretch_Loc.translateX' %LR, '%sStretch_ArmIK_Distance.point2X' %LR)
                        cmds.connectAttr('%sWrist_Stretch_Loc.translateY' %LR, '%sStretch_ArmIK_Distance.point2Y' %LR)
                        cmds.connectAttr('%sWrist_Stretch_Loc.translateZ' %LR, '%sStretch_ArmIK_Distance.point2Z' %LR)
                        cmds.connectAttr('%sStretch_ArmIK_Distance.distance' %LR, '%sStretch_ArmIK_Length_MulDiv.input1Y' %LR)
                        cmds.connectAttr('Puck.scaleX', '%sStretch_ArmIK_Length_MulDiv.input2Y' %LR)
                        
                        ###condition node calculate length and compare and do shit
                        cmds.shadingNode('condition', n = '%sStretch_ArmIK_Con' %LR, asUtility = True)
                        cmds.connectAttr('%sStretch_ArmIK_Length_MulDiv.outputY' %LR, '%sStretch_ArmIK_Con.firstTerm' %LR)
                        cmds.connectAttr('%sStretch_ArmIK_Length_MulDiv.outputX' %LR, '%sStretch_ArmIK_Con.secondTerm' %LR)
                        cmds.setAttr('%sStretch_ArmIK_Con.operation' %LR, 2)
                        
                        ####Stretch Ratio
                        cmds.shadingNode('multiplyDivide', n = '%sStretch_ArmIK_ratio_MulDiv' %LR, asUtility = True)
                        cmds.connectAttr('%sStretch_ArmIK_Length_MulDiv.outputY' %LR, '%sStretch_ArmIK_ratio_MulDiv.input1X' %LR)
                        cmds.connectAttr('%sStretch_ArmIK_Length_MulDiv.outputX' %LR, '%sStretch_ArmIK_ratio_MulDiv.input2X' %LR)
                        cmds.setAttr('%sStretch_ArmIK_ratio_MulDiv.operation' %LR, 2)
                        ####Last Mux
                        cmds.shadingNode('blendColors', n = '%sArm_Stretch_Mux' %LR, asUtility = True)
                        cmds.connectAttr('%sStretch_ArmIK_Con.outColorR' %LR, '%sArm_Stretch_Mux.blender' %LR)
                        cmds.setAttr('%sArm_Stretch_Mux.color1R' %LR, 1)
                        cmds.connectAttr('%sStretch_ArmIK_ratio_MulDiv.outputX' %LR,'%sArm_Stretch_Mux.color2R' %LR)
                        
                        ####stretch MUX
                        cmds.shadingNode('blendColors', n = '%sArm_StretchYesNo_Mux' %LR, asUtility = True)
                        cmds.connectAttr('%sArm_Extra_CTRL.Stretch_IK' %LR, '%sArm_StretchYesNo_Mux.blender' %LR)
                        cmds.setAttr('%sArm_StretchYesNo_Mux.color2R' %LR, 1)
                        cmds.connectAttr('%sArm_Stretch_Mux.outputR' %LR, '%sArm_StretchYesNo_Mux.color1R' %LR)
                        
                        cmds.connectAttr('%sArm_StretchYesNo_Mux.outputR' %LR, '%sShoulder.scaleX' %LR)
                        cmds.connectAttr('%sArm_StretchYesNo_Mux.outputR' %LR, '%sElbow.scaleX' %LR)
                        
                        #######Stretch and Bend##########
                        cmds.shadingNode('multiplyDivide', n = '%sArm_StretchBend' %LR, asUtility = True)
                        
                        cmds.connectAttr('%sArm_StretchYesNo_Mux.outputR' %LR, '%sArm_StretchBend.input1X' %LR)
                        cmds.connectAttr('%sArm_StretchYesNo_Mux.outputR' %LR, '%sArm_StretchBend.input1Y' %LR)

                        Bendy_Shoulder_destination = cmds.listRelatives('%sBendy_Shoulder_Joint_GRP' %LR, ad = True)
                        Bendy_Shoulder_destination = Bendy_Shoulder_destination[2:-1]
                        Bendy_Elbow_destination = cmds.listRelatives('%sBendy_Elbow_Joint_GRP' %LR, ad = True)
                        Bendy_Elbow_destination = Bendy_Elbow_destination[2:-1]
                        #print Bendy_Shoulder_destination
                        #print Bendy_Elbow_destination
                        
                        cmds.connectAttr('%sBendyArm_UpperCondition.outColorR' %LR, '%sArm_StretchBend.input2X' %LR)
                        cmds.connectAttr('%sBendyArm_LowerCondition.outColorR' %LR, '%sArm_StretchBend.input2Y' %LR)
                        
                        for joint in Bendy_Shoulder_destination:
                                cmds.connectAttr('%sArm_StretchBend.outputX' %LR, '%s.scaleX' %joint, f = True)
                        for joint in Bendy_Elbow_destination:
                                cmds.connectAttr('%sArm_StretchBend.outputY' %LR, '%s.scaleX' %joint, f = True)                         
                        
                        cmds.select('%sStretch_Arm_GRP' %LR, r = True)
                        cmds.setAttr('%sStretch_Arm_GRP.visibility' %LR, 0)
        
        def individualStretchArm(self):#####postponed
                for LR in L_o_R:
                        ########add Attribute########
                        cmds.select('%sArm_Extra_CTRL' %LR)
                        cmds.addAttr(ln = 'UpperArmStretch', at = 'double', min = -5, max = 5)
                        cmds.setAttr('%sArm_Extra_CTRL.UpperArmStretch' %LR, e = True, keyable = True)
                        cmds.select('%sArm_Extra_CTRL' %LR)
                        cmds.addAttr(ln = 'LowerArmStretch', at = 'double', min = -5, max = 5)
                        cmds.setAttr('%sArm_Extra_CTRL.LowerArmStretch' %LR, e = True, keyable = True)
                        
                        ######Elbow Stretch Loc#######
                        cmds.createNode('transform', n = '%sElbow_Stretch_Loc_GRP' %LR)
                        cmds.spaceLocator(n = '%sElbow_Stretch_Loc' %LR)
                        cmds.select('%sElbow_Stretch_Loc_GRP' %LR, tgl = True)
                        cmds.parent()
                        cmds.select('%sElbow_Stretch_Loc_GRP' %LR, r = True)
                        if LR == 'L_':
                                cmds.move(self.leftElbowPos[0], self.leftElbowPos[1], self.leftElbowPos[2])
                        else:   
                                cmds.move(-self.leftElbowPos[0], self.leftElbowPos[1], self.leftElbowPos[2])
                        cmds.select('%sShoulder' %LR, r = True)
                        cmds.select('%sElbow_Stretch_Loc_GRP' %LR, tgl = True)
                        cmds.orientConstraint(weight = 1)
                        cmds.delete('%sElbow_Stretch_Loc_GRP_orientConstraint1' %LR)
                        #if LR == 'R_':
                        #       cmds.rotate(0, 180, 0, '%sElbow_Stretch_Loc_GRP' %LR)
                        #       cmds.setAttr('%sElbow_Stretch_Loc_GRP.rotateY' %LR, 0)
                        cmds.select('%sElbow_Stretch_Loc_GRP' %LR, r = True)
                        cmds.select('%sShoulder' %LR, tgl = True)
                        cmds.parent()
                        
                        
                        ######Wrist Stretch Loc#######
                        cmds.createNode('transform', n = '%sWrist_Stretch_Loc1_GRP' %LR)
                        cmds.spaceLocator(n = '%sWrist_Stretch_Loc1' %LR)
                        cmds.select('%sWrist_Stretch_Loc1_GRP' %LR, tgl = True)
                        cmds.parent()
                        cmds.select('%sWrist_Stretch_Loc1_GRP' %LR, r = True)                   
                        if LR == 'L_':
                                cmds.move(self.leftWristPos[0], self.leftWristPos[1], self.leftWristPos[2])
                        else:   
                                cmds.move(-self.leftWristPos[0], self.leftWristPos[1], self.leftWristPos[2])                      
                        cmds.select('%sElbow' %LR, r = True)
                        cmds.select('%sWrist_Stretch_Loc1_GRP' %LR, tgl = True)
                        cmds.orientConstraint(weight = 1)
                        cmds.delete('%sWrist_Stretch_Loc1_GRP_orientConstraint1' %LR)
                        cmds.select('%sWrist_Stretch_Loc1_GRP' %LR, r = True)
                        cmds.select('%sElbow' %LR, tgl = True)
                        cmds.parent()
                        
                        ###########Connect Attr translate Stretch###########
                        '''cmds.select('%sElbow_Stretch_Loc' %LR, r = True)
                        cmds.select('%sElbow' %LR, tgl = True)
                        cmds.pointConstraint(mo = True, weight = 1)
                        cmds.connectAttr('%sElbow.translateX' %LR, '%sFK_Elbow.translateX' %LR)
                        cmds.connectAttr('%sElbow.translateX' %LR, '%sIK_Elbow.translateX' %LR) 
                        cmds.select('%sElbow_Stretch_Loc' %LR, r = True)
                        cmds.select('%sElbow_FK_CTRL' %LR, tgl = True)
                        cmds.pointConstraint(mo = True, weight = 1)'''
                        
                        cmds.select('%sWrist_Stretch_Loc1' %LR, r = True)
                        cmds.select('%sWrist' %LR, tgl = True)
                        cmds.pointConstraint(mo = True, weight = 1)
                        cmds.connectAttr('%sWrist.translateX' %LR, '%sFK_Wrist.translateX' %LR)
                        cmds.connectAttr('%sWrist.translateX' %LR, '%sIK_Wrist.translateX' %LR) 
                        cmds.select('%sWrist_Stretch_Loc1' %LR, r = True)
                        cmds.select('%sWrist_FK_CTRL' %LR, tgl = True)
                        cmds.pointConstraint(mo = True, weight = 1)
                        #cmds.select('%sWrist' %LR, r = True)
                        #cmds.select('%sArm_IK_CTRL_GRP' %LR, tgl = True)
                        #cmds.pointConstraint(mo = True, weight = 1)
        
        def bendyArm(self):
                #######duplicate Shoulder... Making Bendy Arm, (Shoulder, Elbow, Wrist)##########
                for LR in L_o_R:
                        cmds.select('%sShoulder' %LR, r = True)
                        cmds.duplicate(rr = True)
                        cmds.rename('%sBendy_Shoulder' %LR)
                        cmds.select('%sBendy_Shoulder|%sElbow' %(LR, LR), r =True)
                        cmds.rename('%sBendy_Elbow' %LR)
                        cmds.select('%sBendy_Shoulder|%sBendy_Elbow|%sWrist' %(LR, LR, LR), r = True)                   
                        cmds.rename('%sBendy_Wrist' %LR)
                        cmds.select('%sBendy_Shoulder|%sBendy_Elbow|%sBendy_Wrist|%sPalm' %(LR, LR, LR, LR), r = True)
                        cmds.delete()
                        if LR == 'L_':
                                cmds.select('%sBendy_Shoulder|%sBendy_Elbow|%sBendy_Wrist|effector8' %(LR, LR, LR), r = True)
                                cmds.delete()
                        else:
                                cmds.select('%sBendy_Shoulder|%sBendy_Elbow|%sBendy_Wrist|effector10' %(LR, LR, LR), r = True)
                                cmds.delete()
                        cmds.select('%sBendy_Shoulder|%sBendy_Elbow|%sBendy_Wrist|%sArm_Extra_CTRL_GRP' %(LR, LR, LR, LR), r = True)
                        cmds.delete()
                        
                        bendyArmJoints = ['%sBendy_Shoulder' %LR, '%sBendy_Elbow' %LR, '%sBendy_Elbow_End' %LR]
                        
                        ####unparent the Bendy Arm####
                        cmds.select('%sBendy_Shoulder' %LR, r =True)
                        cmds.parent(w= True)
                        
                        ###Insert Joints#####
                        Number_Of_JointBetween = 6
                        
                        for i in range(len(bendyArmJoints)-2):
                                pos_1 = cmds.xform('%s' %bendyArmJoints[i], ws = True, t = True, q = True )
                                pos_2 = cmds.xform('%s' %bendyArmJoints[i+1], ws = True, t = True, q = True )
                                if LR == 'L_':
                                        pos_2 = [pos_2[0]-pos_1[0], pos_2[1]-pos_1[1], pos_2[2]-pos_1[2]]
                                        cmds.insertJoint('%s' %bendyArmJoints[i])
                                        cmds.joint('joint1', n = '%s_Bendy1' %bendyArmJoints[i], e = True, co = True, p = [pos_1[0] + pos_2[0]/Number_Of_JointBetween, pos_1[1] + pos_2[1]/Number_Of_JointBetween, pos_1[2] + pos_2[2]/Number_Of_JointBetween])
                                        for j in range(Number_Of_JointBetween-2):
                                                cmds.insertJoint('%s_Bendy%s' %(bendyArmJoints[i], j+1))
                                                cmds.joint('joint1', n = '%s_Bendy%s' %(bendyArmJoints[i], j+2), e = True, co = True, p = [pos_1[0] + (j+2)*pos_2[0]/Number_Of_JointBetween, pos_1[1] + (j+2)*pos_2[1]/Number_Of_JointBetween, pos_1[2] + (j+2)*pos_2[2]/Number_Of_JointBetween])             

                                else:   
                                        pos_2 = [-pos_2[0]+pos_1[0], pos_2[1]-pos_1[1], pos_2[2]-pos_1[2]]
                                        cmds.insertJoint('%s' %bendyArmJoints[i])
                                        cmds.joint('joint1', n = '%s_Bendy1' %bendyArmJoints[i], e = True, co = True, p = [pos_1[0] - pos_2[0]/Number_Of_JointBetween, pos_1[1] + pos_2[1]/Number_Of_JointBetween, pos_1[2] + pos_2[2]/Number_Of_JointBetween])
                                        for j in range(Number_Of_JointBetween-2):
                                                cmds.insertJoint('%s_Bendy%s' %(bendyArmJoints[i], j+1))
                                                cmds.joint('joint1', n = '%s_Bendy%s' %(bendyArmJoints[i], j+2), e = True, co = True, p = [pos_1[0] - (j+2)*pos_2[0]/Number_Of_JointBetween, pos_1[1] + (j+2)*pos_2[1]/Number_Of_JointBetween, pos_1[2] + (j+2)*pos_2[2]/Number_Of_JointBetween])
                                
                        #####Making Elbow=>Wrist Joint##########
                        #####Duplicate and renaming#############
                        cmds.select('%sBendy_Elbow' %LR, r = True)
                        cmds.rename('%sBendy_Shoulder_End' %LR)
                        cmds.duplicate(rr = True)
                        cmds.parent(w = True)
                        cmds.rename('%sBendy_Elbow' %LR)
                        cmds.select('%sBendy_Elbow|%sBendy_Wrist' %(LR, LR), r = True)
                        cmds.rename('%sBendy_Elbow_End' %LR)
                        cmds.delete('%sBendy_Wrist' %LR)
                        
                        ####Insert Joint########
                        for i in range(len(bendyArmJoints)-2):
                                i = i+1
                                pos_1 = cmds.xform('%s' %bendyArmJoints[i], ws = True, t = True, q = True )
                                pos_2 = cmds.xform('%s' %bendyArmJoints[i+1], ws = True, t = True, q = True )
                                if LR == 'L_':
                                        pos_2 = [pos_2[0]-pos_1[0], pos_2[1]-pos_1[1], pos_2[2]-pos_1[2]]
                                        cmds.insertJoint('%s' %bendyArmJoints[i])
                                        cmds.joint('joint1', n = '%s_Bendy1' %bendyArmJoints[i], e = True, co = True, p = [pos_1[0] + pos_2[0]/Number_Of_JointBetween, pos_1[1] + pos_2[1]/Number_Of_JointBetween, pos_1[2] + pos_2[2]/Number_Of_JointBetween])
                                        for j in range(Number_Of_JointBetween-2):
                                                cmds.insertJoint('%s_Bendy%s' %(bendyArmJoints[i], j+1))
                                                cmds.joint('joint1', n = '%s_Bendy%s' %(bendyArmJoints[i], j+2), e = True, co = True, p = [pos_1[0] + (j+2)*pos_2[0]/Number_Of_JointBetween, pos_1[1] + (j+2)*pos_2[1]/Number_Of_JointBetween, pos_1[2] + (j+2)*pos_2[2]/Number_Of_JointBetween])             

                                else:   
                                        pos_2 = [-pos_2[0]+pos_1[0], pos_2[1]-pos_1[1], pos_2[2]-pos_1[2]]
                                        cmds.insertJoint('%s' %bendyArmJoints[i])
                                        cmds.joint('joint1', n = '%s_Bendy1' %bendyArmJoints[i], e = True, co = True, p = [pos_1[0] - pos_2[0]/Number_Of_JointBetween, pos_1[1] + pos_2[1]/Number_Of_JointBetween, pos_1[2] + pos_2[2]/Number_Of_JointBetween])
                                        for j in range(Number_Of_JointBetween-2):
                                                cmds.insertJoint('%s_Bendy%s' %(bendyArmJoints[i], j+1))
                                                cmds.joint('joint1', n = '%s_Bendy%s' %(bendyArmJoints[i], j+2), e = True, co = True, p = [pos_1[0] - (j+2)*pos_2[0]/Number_Of_JointBetween, pos_1[1] + (j+2)*pos_2[1]/Number_Of_JointBetween, pos_1[2] + (j+2)*pos_2[2]/Number_Of_JointBetween])                     
                        
                        ######IK Spline Curve########
                        Bendy_Shoulder_Pos = cmds.xform('%s' %bendyArmJoints[0], ws = True, t = True, q = True )
                        Bendy_Shoulder_Elbow_Middle_Pos = cmds.xform('%s_Bendy%s' %(bendyArmJoints[0], Number_Of_JointBetween/2), ws = True, t = True, q = True )
                        Bendy_Elbow_Pos = cmds.xform('%s' %bendyArmJoints[1], ws = True, t = True, q = True )
                        Bendy_Elbow_Wrist_Middle_Pos = cmds.xform('%s_Bendy%s' %(bendyArmJoints[1], Number_Of_JointBetween/2), ws = True, t = True, q = True )
                        Bendy_Wrist_Pos = cmds.xform('%s' %bendyArmJoints[2], ws = True, t = True, q = True )
                        cmds.curve(n = '%sShoulder_Elbow_IKSplineCV' %LR, d = 2, p = [(Bendy_Shoulder_Pos[0], Bendy_Shoulder_Pos[1], Bendy_Shoulder_Pos[2]), (Bendy_Shoulder_Elbow_Middle_Pos[0], Bendy_Shoulder_Elbow_Middle_Pos[1], Bendy_Shoulder_Elbow_Middle_Pos[2]), (Bendy_Elbow_Pos[0], Bendy_Elbow_Pos[1], Bendy_Elbow_Pos[2])], k = [0,0,1,1])
                        cmds.curve(n = '%sElbow_Wrist_IKSplineCV' %LR, d = 2, p = [(Bendy_Elbow_Pos[0], Bendy_Elbow_Pos[1], Bendy_Elbow_Pos[2]), (Bendy_Elbow_Wrist_Middle_Pos[0], Bendy_Elbow_Wrist_Middle_Pos[1], Bendy_Elbow_Wrist_Middle_Pos[2]), (Bendy_Wrist_Pos[0], Bendy_Wrist_Pos[1], Bendy_Wrist_Pos[2])], k = [0,0,1,1])
                        
                        ######IK Spline Handle#######
                        cmds.select('%sBendy_Shoulder' %LR, r = True)
                        cmds.select('%sBendy_Shoulder_End' %LR, add = True)
                        cmds.select('%sShoulder_Elbow_IKSplineCV' %LR, add= True) 
                        cmds.ikHandle(n = '%sShoulder_Bendy_IKSpline_Handle'%LR, sol = 'ikSplineSolver', ccv = False, roc = False, pcv = False)
                        cmds.select('%sBendy_Elbow' %LR, r = True)
                        cmds.select('%sBendy_Elbow_End' %LR, add = True)
                        cmds.select('%sElbow_Wrist_IKSplineCV' %LR, add= True) 
                        cmds.ikHandle(n = '%sElbow_Bendy_IKSpline_Handle'%LR, sol = 'ikSplineSolver', ccv = False, roc = False, pcv = False)
                        
                        cmds.connectAttr('%sWrist.rotateX' %LR, '%sElbow_Bendy_IKSpline_Handle.twist' %LR, f = True)
                        cmds.connectAttr('%sShoulder.rotateX' %LR, '%sShoulder_Bendy_IKSpline_Handle.twist'  %LR, f = True)
                        
                        #######Insert Clusters########
                        for i in range(3):
                                cmds.select('%sShoulder_Elbow_IKSplineCV.cv[%s]' %(LR, i), r = True)
                                cmds.cluster(n = '%sShoulder_Elbow_IKSplineCV_Cluster%s' %(LR, i))
                                cmds.select('%sElbow_Wrist_IKSplineCV.cv[%s]' %(LR, i), r = True)
                                cmds.cluster(n = '%sElbow_Wrist_IKSplineCV%s' %(LR, i))
                        
                        #########Making CTRLs#########
                        cmds.createNode('transform', n = '%sUpperArm_Bend_GRP' %LR)
                        cmds.circle( n = '%sUpperArm_Bend' %LR, nr=(1, 0, 0), c=(0, 0, 0), r = 2)
                        cmds.select('%sUpperArm_Bend_GRP' %LR, tgl = True)
                        cmds.parent()
                        cmds.createNode('transform', n = '%sLowerArm_Bend_GRP' %LR)
                        cmds.circle( n = '%sLowerArm_Bend' %LR, nr=(1, 0, 0), c=(0, 0, 0), r = 2)
                        cmds.select('%sLowerArm_Bend_GRP' %LR, tgl = True)
                        cmds.parent()                   
                        
                        cmds.select('%sBendy_Shoulder_Bendy%s' %(LR, Number_Of_JointBetween/2), r = True)
                        cmds.select('%sUpperArm_Bend_GRP' %LR, tgl = True)
                        cmds.pointConstraint(weight = 1)
                        cmds.orientConstraint(weight = 1)
                        cmds.select('%sBendy_Elbow_Bendy%s' %(LR, Number_Of_JointBetween/2), r = True)
                        cmds.select('%sLowerArm_Bend_GRP' %LR, tgl = True)
                        cmds.pointConstraint(weight = 1)
                        cmds.orientConstraint(weight = 1)
                        cmds.delete('%sUpperArm_Bend_GRP_pointConstraint1' %LR)
                        cmds.delete('%sUpperArm_Bend_GRP_orientConstraint1' %LR)
                        cmds.delete('%sLowerArm_Bend_GRP_pointConstraint1' %LR)
                        cmds.delete('%sLowerArm_Bend_GRP_orientConstraint1' %LR)
                        
                        #######Curve Length########
                        cmds.createNode('curveInfo', n = '%sUpperArm_Length' %LR)
                        cmds.createNode('curveInfo', n = '%sLowerArm_Length' %LR)
                        cmds.connectAttr('%sShoulder_Elbow_IKSplineCV.worldSpace' %LR, '%sUpperArm_Length.inputCurve' %LR)
                        cmds.connectAttr('%sElbow_Wrist_IKSplineCV.worldSpace' %LR, '%sLowerArm_Length.inputCurve' %LR)
                        
                        #######Original Length#########
                        #####Locators for measuring distance#######
                        Bendy_Loc = ['Shoulder', 'Elbow', 'Wrist']
                        cmds.createNode('transform', n = '%sBendy_Loc_GRP' %LR)
                        cmds.select('%sBendy_Loc_GRP' %LR, r = True)
                        cmds.select('Puck', tgl = True)
                        cmds.parent()
                        cmds.setAttr('%sBendy_Loc_GRP.visibility' %LR, 0)
                        for loc in Bendy_Loc:
                                cmds.spaceLocator(n = '%sBendy_%s_Loc' %(LR, loc))

                                cmds.select('%s%s' %(LR, loc), r = True)
                                cmds.select('%sBendy_%s_Loc' %(LR, loc), tgl = True)
                                cmds.pointConstraint(weight = 1)
                                cmds.select('%sBendy_%s_Loc' %(LR, loc), r = True)
                                cmds.select('%sBendy_Loc_GRP' %LR, tgl = True)
                                cmds.parent()
                        
                        #######Distance#######
                        cmds.shadingNode('distanceBetween', n = '%sBendyArm_UpperLength' %LR, asUtility = True)
                        cmds.shadingNode('distanceBetween', n = '%sBendyArm_LowerLength' %LR, asUtility = True)
                        cmds.connectAttr('%sBendy_Shoulder_Loc.translate' %LR,'%sBendyArm_UpperLength.point1' %LR )
                        cmds.connectAttr('%sBendy_Elbow_Loc.translate' %LR, '%sBendyArm_UpperLength.point2' %LR )
                        cmds.connectAttr('%sBendy_Elbow_Loc.translate' %LR, '%sBendyArm_LowerLength.point1' %LR )
                        cmds.connectAttr('%sBendy_Wrist_Loc.translate' %LR, '%sBendyArm_LowerLength.point2' %LR )

                        cmds.shadingNode('multiplyDivide', n = '%sBendy_PuckScale' %LR, asUtility = True)
                        cmds.connectAttr('Puck.scaleX', '%sBendy_PuckScale.input1X' %LR)
                        cmds.connectAttr('Puck.scaleX', '%sBendy_PuckScale.input1Y' %LR)
                        cmds.connectAttr('%sBendyArm_UpperLength.distance' %LR, '%sBendy_PuckScale.input2X' %LR)
                        cmds.connectAttr('%sBendyArm_LowerLength.distance' %LR, '%sBendy_PuckScale.input2Y' %LR)
                        
                        #######Stretch Ratio######
                        cmds.shadingNode('multiplyDivide', n = '%sBendyArm_StretchRatio' %LR, asUtility = True)
                        cmds.setAttr('%sBendyArm_StretchRatio.operation' %LR, 2)
                                                
                        cmds.connectAttr('%sBendy_PuckScale.outputX' %LR, '%sBendyArm_StretchRatio.input2X' %LR)
                        cmds.connectAttr('%sBendy_PuckScale.outputY' %LR, '%sBendyArm_StretchRatio.input2Y' %LR)
                        cmds.connectAttr('%sUpperArm_Length.arcLength' %LR, '%sBendyArm_StretchRatio.input1X' %LR)
                        cmds.connectAttr('%sLowerArm_Length.arcLength' %LR, '%sBendyArm_StretchRatio.input1Y' %LR)
                        
                        #######Bendy Stretch Condition###########
                        cmds.shadingNode('condition', n = '%sBendyArm_UpperCondition' %LR, asUtility = True)
                        cmds.shadingNode('condition', n = '%sBendyArm_LowerCondition' %LR, asUtility = True)
                        cmds.setAttr('%sBendyArm_UpperCondition.secondTerm' %LR, 1)                     
                        cmds.setAttr('%sBendyArm_LowerCondition.secondTerm' %LR, 1)
                        cmds.setAttr('%sBendyArm_UpperCondition.operation' %LR, 3)
                        cmds.setAttr('%sBendyArm_LowerCondition.operation' %LR, 3)
                        cmds.connectAttr('%sUpperArm_Length.arcLength' %LR, '%sBendyArm_UpperCondition.firstTerm' %LR)
                        cmds.connectAttr('%sLowerArm_Length.arcLength' %LR, '%sBendyArm_LowerCondition.firstTerm' %LR)
                        cmds.connectAttr('%sBendyArm_UpperLength.distance' %LR, '%sBendyArm_UpperCondition.secondTerm' %LR)
                        cmds.connectAttr('%sBendyArm_LowerLength.distance' %LR, '%sBendyArm_LowerCondition.secondTerm' %LR)
                        cmds.connectAttr('%sBendyArm_StretchRatio.outputX' %LR, '%sBendyArm_UpperCondition.colorIfTrueR' %LR)
                        cmds.connectAttr('%sBendyArm_StretchRatio.outputY' %LR, '%sBendyArm_LowerCondition.colorIfTrueR' %LR)
                        
                        ########Grouping##########
                        cmds.createNode('transform', n = '%sBendy_Shoulder_Joint_GRP' %LR)
                        cmds.select('%sBendy_Shoulder' %LR, r = True)
                        cmds.select('%sBendy_Shoulder_Joint_GRP' %LR , tgl = True)
                        cmds.parent()
                        cmds.createNode('transform', n = '%sBendy_Elbow_Joint_GRP' %LR)
                        cmds.select('%sElbow' %LR, r = True)
                        cmds.select('%sBendy_Elbow_Joint_GRP' %LR, tgl = True)
                        cmds.pointConstraint(mo = False, weight = 1)
                        cmds.orientConstraint(mo = False, weight = 1)
                        cmds.delete('%sBendy_Elbow_Joint_GRP_pointConstraint1' %LR)
                        cmds.delete('%sBendy_Elbow_Joint_GRP_orientConstraint1' %LR)
                        
                        cmds.select('%sBendy_Elbow' %LR, r = True)
                        cmds.select('%sBendy_Elbow_Joint_GRP' %LR , tgl = True)
                        cmds.parent()
                        cmds.createNode('transform', n = '%sBendy_Joint_GRP' %LR)
                        cmds.select('%sBendy_Elbow_Joint_GRP' %LR , r = True)
                        cmds.select('%sBendy_Shoulder_Joint_GRP' %LR , add = True)
                        cmds.select('%sBendy_Joint_GRP' %LR, tgl = True)
                        cmds.parent()
                        cmds.createNode('transform', n = '%sBendy_GRP' %LR)
                        
                        cmds.select('%sShoulder_Bendy_IKSpline_Handle' %LR, r = True)
                        cmds.select('%sElbow_Bendy_IKSpline_Handle' %LR, add = True)
                        cmds.select('%sBendy_GRP' %LR, tgl = True)
                        cmds.parent()
                        
                        cmds.select('%sShoulder_Elbow_IKSplineCV_Cluster1Handle' %LR, r = True)
                        cmds.select('%sUpperArm_Bend' %LR, tgl = True)
                        cmds.parent()
                        cmds.select('%sElbow_Wrist_IKSplineCV1Handle' %LR, r = True)
                        cmds.select('%sLowerArm_Bend' %LR, tgl = True)
                        cmds.parent()
                        
                        cmds.select('%sShoulder' %LR, r = True)
                        cmds.select('%sBendy_Shoulder_Joint_GRP' %LR, tgl = True)
                        cmds.pointConstraint(weight = 1, mo = True)
                        cmds.select('%sElbow' %LR, r = True)
                        cmds.select('%sBendy_Elbow_Joint_GRP' %LR, tgl = True)
                        cmds.pointConstraint(weight = 1, mo = True)
                        cmds.orientConstraint(weight = 1, mo = True)
                        
                
                        #######Cluster Grouping##########
                        
                        cmds.select('%sShoulder_Elbow_IKSplineCV_Cluster0Handle' %LR, r = True)
                        cmds.select('%sShoulder' %LR, tgl = True)
                        cmds.parent()
                        cmds.select('%sUpperArm_Bend_GRP' %LR, r = True)
                        cmds.select('%sShoulder' %LR, tgl = True)
                        cmds.parent()
                        cmds.select('%sShoulder_Elbow_IKSplineCV_Cluster2Handle' %LR, r = True)
                        cmds.select('%sElbow' %LR, tgl = True)
                        cmds.parent()                   
                        cmds.select('%sElbow_Wrist_IKSplineCV0Handle' %LR, r = True)
                        cmds.select('%sElbow' %LR, tgl = True)
                        cmds.parent()
                        cmds.select('%sLowerArm_Bend_GRP' %LR, r = True)
                        cmds.select('%sElbow' %LR, tgl = True)
                        cmds.parent()
                        cmds.select('%sElbow_Wrist_IKSplineCV2Handle' %LR, r = True)
                        cmds.select('%sWrist' %LR, tgl = True)
                        cmds.parent()
                        cmds.select('%sBendy_Joint_GRP' %LR, r = True)
                        cmds.select('%sBendy_GRP' %LR, tgl = True)
                        cmds.parent()
                        cmds.select('%sBendy_GRP' %LR, r = True)
                        cmds.select('Puck', tgl = True)
                        cmds.parent()
                        cmds.createNode('transform', n = '%sBendyCurve_GRP' %LR)
                        cmds.select('%sShoulder_Elbow_IKSplineCV' %LR, r = True)
                        cmds.select('%sElbow_Wrist_IKSplineCV' %LR, add = True)
                        cmds.select('%sBendyCurve_GRP' %LR, tgl = True)
                        cmds.parent()
                        #cmds.select('%sShoulder_Elbow_IKSplineCV' %LR, r = True)
                        #cmds.select('%sShoulder' %LR, tgl = True)
                        #cmds.parent()
                        #cmds.parent('%sElbow_Wrist_IKSplineCV' %LR, r = True)
                        #cmds.select('%sShoulder' %LR, tgl = True)
                        #cmds.parent()
                        
                        Bendy_Shoulder_destination = cmds.listRelatives('%sBendy_Shoulder_Joint_GRP' %LR, ad = True)
                        Bendy_Shoulder_destination = Bendy_Shoulder_destination[2:-1]
                        Bendy_Elbow_destination = cmds.listRelatives('%sBendy_Elbow_Joint_GRP' %LR, ad = True)
                        Bendy_Elbow_destination = Bendy_Elbow_destination[2:-1]
                        #print Bendy_Shoulder_destination
                        #print Bendy_Elbow_destination
                        
                        for joint in Bendy_Shoulder_destination:
                                cmds.connectAttr('%sBendyArm_UpperCondition.outColorR' %LR, '%s.scaleX' %joint)
                        for joint in Bendy_Elbow_destination:
                                cmds.connectAttr('%sBendyArm_LowerCondition.outColorR' %LR, '%s.scaleX' %joint)                 
                        
                        cmds.setAttr('%sShoulder_Bendy_IKSpline_Handle.visibility' %LR, 0)
                        cmds.setAttr('%sElbow_Bendy_IKSpline_Handle.visibility' %LR, 0)
                        cmds.setAttr('%sShoulder_Elbow_IKSplineCV_Cluster0Handle.visibility' %LR, 0)
                        cmds.setAttr('%sShoulder_Elbow_IKSplineCV_Cluster1Handle.visibility' %LR, 0)
                        cmds.setAttr('%sShoulder_Elbow_IKSplineCV_Cluster2Handle.visibility' %LR, 0)
                        cmds.setAttr('%sElbow_Wrist_IKSplineCV0Handle.visibility' %LR, 0)       
                        cmds.setAttr('%sElbow_Wrist_IKSplineCV1Handle.visibility' %LR, 0)                       
                        cmds.setAttr('%sElbow_Wrist_IKSplineCV2Handle.visibility' %LR, 0)       
                                
                        cmds.addAttr('%sArm_Extra_CTRL' %LR,  ln = 'Bend', at = 'long', min = 0, max = 1)
                        cmds.setAttr('%sArm_Extra_CTRL.Bend' %LR, e = True, keyable = True)
                        cmds.connectAttr('%sArm_Extra_CTRL.Bend' %LR, '%sUpperArm_Bend.visibility' %LR)
                        cmds.connectAttr('%sArm_Extra_CTRL.Bend' %LR, '%sLowerArm_Bend.visibility' %LR)
                        
        def twistArm(self, Stretch_Arm):
                #####Create more Joints#######
                
                for LR in L_o_R:
                        Twist_self.armJoints = ['%sShoulder' %LR, '%sElbow' %LR, '%sWrist' %LR]
                        for i in range(len(Twist_self.armJoints)-1):
                                pos_1 = cmds.xform('%s' %Twist_self.armJoints[i], ws = True, t = True, q = True )
                                pos_2 = cmds.xform('%s' %Twist_self.armJoints[i+1], ws = True, t = True, q = True )
                                if LR == 'L_':
                                        pos_2 = [pos_2[0]-pos_1[0], pos_2[1]-pos_1[1], pos_2[2]-pos_1[2]]
                                        cmds.insertJoint('%s' %Twist_self.armJoints[i])
                                        cmds.joint('joint1', n = '%s_Twist1' %Twist_self.armJoints[i], e = True, co = True, p = [pos_1[0] + pos_2[0]/3, pos_1[1] + pos_2[1]/3, pos_1[2] + pos_2[2]/3])
                                        cmds.insertJoint('%s_Twist1' %Twist_self.armJoints[i])
                                        cmds.joint('joint1', n = '%s_Twist2' %Twist_self.armJoints[i], e = True, co = True, p = [pos_1[0] + 2*pos_2[0]/3, pos_1[1] + 2*pos_2[1]/3, pos_1[2] + 2*pos_2[2]/3])                
                                else:   
                                        pos_2 = [-pos_2[0]+pos_1[0], pos_2[1]-pos_1[1], pos_2[2]-pos_1[2]]
                                        cmds.insertJoint('%s' %Twist_self.armJoints[i])
                                        cmds.joint('joint1', n = '%s_Twist1' %Twist_self.armJoints[i], e = True, co = True, p = [pos_1[0] - pos_2[0]/3, pos_1[1] + pos_2[1]/3, pos_1[2] + pos_2[2]/3])
                                        cmds.insertJoint('%s_Twist1' %Twist_self.armJoints[i])
                                        cmds.joint('joint1', n = '%s_Twist2' %Twist_self.armJoints[i], e = True, co = True, p = [pos_1[0] - 2*pos_2[0]/3, pos_1[1] + 2*pos_2[1]/3, pos_1[2] + 2*pos_2[2]/3])                                
                
                #####Twist Connect######
                        ####Shoulder######
                        #cmds.disconnectAttr('%sFK_Shoulder.rotateX' %LR ,'%sFKIK_Shoulder_Mux.input2R' %LR)
                        cmds.shadingNode('multiplyDivide', n = '%sTwistShoulderMul' %LR, asUtility = True)
                        if LR == 'L_':
                                cmds.setAttr('%sTwistShoulderMul.input2X' %LR, 0.333)
                                cmds.setAttr('%sTwistShoulderMul.input2Y' %LR, 0.666)
                        else:
                                cmds.setAttr('%sTwistShoulderMul.input2X' %LR, -0.333)
                                cmds.setAttr('%sTwistShoulderMul.input2Y' %LR, -0.666)
                        cmds.connectAttr('%sShoulder_FK_CTRL.rotateX' %LR, '%sTwistShoulderMul.input1X' %LR)
                        cmds.connectAttr('%sShoulder_FK_CTRL.rotateX' %LR, '%sTwistShoulderMul.input1Y' %LR)
                        cmds.connectAttr('%sTwistShoulderMul.outputX' %LR, '%sShoulder_Twist1.rotateX' %LR)
                        cmds.connectAttr('%sTwistShoulderMul.outputY' %LR, '%sShoulder_Twist2.rotateX' %LR)
                        
                        #####Wrist#########

                        cmds.shadingNode('multiplyDivide', n = '%sTwistWristMul' %LR, asUtility = True)
                        cmds.setAttr('%sTwistWristMul.input2X' %LR, 0.333)
                        cmds.setAttr('%sTwistWristMul.input2Y' %LR, 0.666)
                        cmds.connectAttr('%sWrist_IKSC_GRP.rotateX' %LR, '%sTwistWristMul.input1X' %LR)
                        cmds.connectAttr('%sWrist_IKSC_GRP.rotateX' %LR, '%sTwistWristMul.input1Y' %LR)
                        cmds.rename('%sElbow_Twist1' %LR, '%sWrist_Twist1' %LR)
                        cmds.rename('%sElbow_Twist2' %LR, '%sWrist_Twist2' %LR)
                        cmds.connectAttr('%sTwistWristMul.outputX' %LR, '%sWrist_Twist1.rotateX' %LR)
                        cmds.connectAttr('%sTwistWristMul.outputY' %LR, '%sWrist_Twist2.rotateX' %LR)
                        
                        
                        ########for Stretch IK Arm############

                        if Stretch_Arm == True:
                                cmds.connectAttr('%sArm_StretchYesNo_Mux.outputR' %LR, '%sWrist_Twist1.scaleX' %LR)                     
                                cmds.connectAttr('%sArm_StretchYesNo_Mux.outputR' %LR, '%sWrist_Twist2.scaleX' %LR)                     
                                cmds.connectAttr('%sArm_StretchYesNo_Mux.outputR' %LR, '%sShoulder_Twist1.scaleX' %LR)                  
                                cmds.connectAttr('%sArm_StretchYesNo_Mux.outputR' %LR, '%sShoulder_Twist2.scaleX' %LR)                  
                        
        ##########Stretch Ik Spine Setting###########
        def stretchIkSpine(self):
                ####Joints for Stretch IK #########
                Stretch_IK_Joints = ['Root', 'Spine1', 'Spine2', 'Spine3', 'Spine4', 'NeckBase']
                
                ####NurbsPlane for StretchIK#######
                cmds.nurbsPlane(n = 'IK_Spine_nPlane', d = 1, v = 5,p = self.rootPos)
                
                ####Adjusting Nurbs Plane#######
                for Joint in range(len(Stretch_IK_Joints)):
                        cmds.select(cl = True)
                        Joint_Position = cmds.xform(Stretch_IK_Joints[Joint], q = True, ws = True, t = True)
                        
                        for i in range(3):
                                cmds.select('IK_Spine_nPlane.cv[%s][%s]' %(i, Joint), r = True )
                                if i == 0:
                                        cmds.move(Joint_Position[0]-0.5, Joint_Position[1], Joint_Position[2])
                                else:   
                                        cmds.move(Joint_Position[0]+0.5, Joint_Position[1], Joint_Position[2])
                        cmds.select(cl = True)
                        cmds.joint(n = 'Stretch_IK_%s' %Stretch_IK_Joints[Joint], p = Joint_Position) #Create Joint
                
                
                for i in range(len(Stretch_IK_Joints)-2):
                        cmds.select('%s_CTRL_GRP' %Stretch_IK_Joints[i+1], r = True)
                        cmds.parent(w = True)
                        cmds.delete('%s_orientConstraint1' %Stretch_IK_Joints[i+1])
                        cmds.select('Stretch_IK_%s' %Stretch_IK_Joints[i+1], r = True)
                        cmds.select('%s_CTRL' %Stretch_IK_Joints[i+1], tgl = True)
                        cmds.parent()
                
                #####Creating Top_Bottom CTRL Joint####
                cmds.createNode('transform', n = 'Stretch_IK_Top_CTRL_GRP')
                cmds.move(self.neckBasePos[0], self.neckBasePos[1], self.neckBasePos[2])
                cmds.createNode('transform', n = 'Stretch_IK_Bottom_CTRL_GRP')
                cmds.move(self.rootPos[0], self.rootPos[1], self.rootPos[2])
                cmds.select('Stretch_IK_NeckBase', r = True)
                cmds.setAttr('Stretch_IK_NeckBase.radius', 3)
                cmds.select('Stretch_IK_Top_CTRL_GRP', tgl = True)
                cmds.parent()
                cmds.select('Stretch_IK_Root', r = True)
                cmds.setAttr('Stretch_IK_Root.radius', 3)
                cmds.select('Stretch_IK_Bottom_CTRL_GRP', tgl = True)
                cmds.parent()
                
                cmds.select('NeckBase', r =True)
                cmds.select('L_Scapula', tgl = True)
                cmds.select('R_Scapula', tgl = True)
                cmds.parent(w = True)
                cmds.select('Stretch_IK_Spine4', tgl = True)
                cmds.parent()
                
                #####Skinning the nurbsPlane#######
                cmds.select('Stretch_IK_NeckBase', r = True)            
                cmds.select('Stretch_IK_Root', add = True)
                                
                cmds.select('IK_Spine_nPlane', tgl = True)
                cmds.skinCluster()
                
                percentage = 0
                '''aaa = len(Stretch_IK_Joints) - 1
                aaa = 1/float(aaa)
                for i in range(len(Stretch_IK_Joints)):
                        print percentage
                        cmds.skinPercent( 'skinCluster1', 'IK_Spine_nPlane.cv[0:1][%s]' %i, tv = [('Stretch_IK_Root', 1-percentage), ('Stretch_IK_NeckBase', percentage) ]) 
                        percentage = percentage + aaa'''
                cmds.skinPercent( 'skinCluster1', 'IK_Spine_nPlane.cv[0:1][0]' , tv = [('Stretch_IK_Root', 1), ('Stretch_IK_NeckBase', 0) ])
                cmds.skinPercent( 'skinCluster1', 'IK_Spine_nPlane.cv[0:1][1]' , tv = [('Stretch_IK_Root', 0.95), ('Stretch_IK_NeckBase', 0.05) ]) 
                cmds.skinPercent( 'skinCluster1', 'IK_Spine_nPlane.cv[0:1][2]' , tv = [('Stretch_IK_Root', 0.8), ('Stretch_IK_NeckBase', 0.2) ]) 
                cmds.skinPercent( 'skinCluster1', 'IK_Spine_nPlane.cv[0:1][3]' , tv = [('Stretch_IK_Root', 0.6), ('Stretch_IK_NeckBase', 0.4) ]) 
                cmds.skinPercent( 'skinCluster1', 'IK_Spine_nPlane.cv[0:1][4]' , tv = [('Stretch_IK_Root', 0.2), ('Stretch_IK_NeckBase', 0.8) ]) 
                cmds.skinPercent( 'skinCluster1', 'IK_Spine_nPlane.cv[0:1][5]' , tv = [('Stretch_IK_Root', 0), ('Stretch_IK_NeckBase', 1) ]) 
                
                ##NodeConnection
                for i in range(len(Stretch_IK_Joints)-2):
                        cmds.createNode('pointOnSurfaceInfo', n = 'pointOnSurfaceInfo_nurbsPlane_%s' %Stretch_IK_Joints[i+1])
                        cmds.setAttr('pointOnSurfaceInfo_nurbsPlane_%s.parameterU' %Stretch_IK_Joints[i+1], 0.5)
                        cmds.setAttr('pointOnSurfaceInfo_nurbsPlane_%s.parameterV' %Stretch_IK_Joints[i+1], 0.2*(i+1))
                        cmds.connectAttr('IK_Spine_nPlaneShape.worldSpace', 'pointOnSurfaceInfo_nurbsPlane_%s.inputSurface' %Stretch_IK_Joints[i+1])
                        cmds.connectAttr('pointOnSurfaceInfo_nurbsPlane_%s.position' %Stretch_IK_Joints[i+1], '%s_CTRL_GRP.translate' %Stretch_IK_Joints[i+1])
                        ##4x4 matrix
                        cmds.createNode('fourByFourMatrix', n = 'fourByFourMatrix_%s' %Stretch_IK_Joints[i+1])
                        cmds.connectAttr('pointOnSurfaceInfo_nurbsPlane_%s.normalX' %Stretch_IK_Joints[i+1], 'fourByFourMatrix_%s.in00' %Stretch_IK_Joints[i+1])
                        cmds.connectAttr('pointOnSurfaceInfo_nurbsPlane_%s.normalY' %Stretch_IK_Joints[i+1], 'fourByFourMatrix_%s.in01' %Stretch_IK_Joints[i+1])
                        cmds.connectAttr('pointOnSurfaceInfo_nurbsPlane_%s.normalZ' %Stretch_IK_Joints[i+1], 'fourByFourMatrix_%s.in02' %Stretch_IK_Joints[i+1])
                        cmds.connectAttr('pointOnSurfaceInfo_nurbsPlane_%s.normalizedTangentUZ' %Stretch_IK_Joints[i+1], 'fourByFourMatrix_%s.in10' %Stretch_IK_Joints[i+1])
                        cmds.connectAttr('pointOnSurfaceInfo_nurbsPlane_%s.normalizedTangentUX' %Stretch_IK_Joints[i+1], 'fourByFourMatrix_%s.in11' %Stretch_IK_Joints[i+1])
                        cmds.connectAttr('pointOnSurfaceInfo_nurbsPlane_%s.normalizedTangentUY' %Stretch_IK_Joints[i+1], 'fourByFourMatrix_%s.in12' %Stretch_IK_Joints[i+1])
                        cmds.connectAttr('pointOnSurfaceInfo_nurbsPlane_%s.normalizedTangentVZ' %Stretch_IK_Joints[i+1], 'fourByFourMatrix_%s.in20' %Stretch_IK_Joints[i+1])
                        cmds.connectAttr('pointOnSurfaceInfo_nurbsPlane_%s.normalizedTangentVX' %Stretch_IK_Joints[i+1], 'fourByFourMatrix_%s.in21' %Stretch_IK_Joints[i+1])
                        cmds.connectAttr('pointOnSurfaceInfo_nurbsPlane_%s.normalizedTangentVY' %Stretch_IK_Joints[i+1], 'fourByFourMatrix_%s.in22' %Stretch_IK_Joints[i+1])
                        ##Decompose Matrix
                        cmds.createNode('decomposeMatrix', n = 'decomposeMatrix_%s' %Stretch_IK_Joints[i+1])
                        cmds.connectAttr('fourByFourMatrix_%s.output' %Stretch_IK_Joints[i+1], 'decomposeMatrix_%s.inputMatrix' %Stretch_IK_Joints[i+1])
                        cmds.connectAttr('decomposeMatrix_%s.outputRotate' %Stretch_IK_Joints[i+1], '%s_CTRL_GRP.rotate' %Stretch_IK_Joints[i+1])
                        
                        cmds.connectAttr('%s_CTRL.rotate' %Stretch_IK_Joints[i+1], '%s.rotate' %Stretch_IK_Joints[i+1])

                cmds.select('Stretch_IK_Top_CTRL_GRP', r = True)
                cmds.select('Spine4', tgl = True)
                cmds.parent()           
                
                cmds.select('Pelvis', r = True)
                cmds.select('Stretch_IK_Root', tgl = True)
                cmds.pointConstraint(weight = 1)

        def bendyLeg(self):
                #######duplicate Hip... Making Bendy Leg, (Hip, Knee, Ankle)##########
                for LR in L_o_R:
                        cmds.select('%sHip' %LR, r = True)
                        cmds.duplicate(rr = True)
                        cmds.rename('%sBendy_Hip' %LR)
                        cmds.select('%sBendy_Hip|%sKnee' %(LR, LR), r =True)
                        cmds.rename('%sBendy_Knee' %LR)
                        cmds.select('%sBendy_Hip|%sBendy_Knee|%sAnkle' %(LR, LR, LR), r = True)                 
                        cmds.rename('%sBendy_Ankle' %LR)
                        cmds.select('%sBendy_Hip|%sBendy_Knee|%sBendy_Ankle|%sBall' %(LR, LR, LR, LR), r = True)
                        cmds.delete()
                        cmds.delete(cmds.listRelatives('%sBendy_Ankle' %LR, f = True, ad = True))
                        #if LR == 'L_':
                        #        cmds.delete(cmds.listRelatives('%sBendy_Ankle', ad = True)
                        #        cmds.select('%sBendy_Hip|%sBendy_Knee|%sBendy_Ankle|effector3' %(LR, LR, LR), r = True)
                        #        cmds.delete()
                        #        cmds.select('%sBendy_Hip|%sBendy_Knee|effector1' %(LR, LR), r = True)
                        #        cmds.delete()
                        #else:
                        #        cmds.select('%sBendy_Hip|%sBendy_Knee|%sBendy_Ankle|effector4' %(LR, LR, LR), r = True)
                        #        cmds.delete()
                        #        cmds.select('%sBendy_Hip|%sBendy_Knee|effector2' %(LR, LR), r = True)
                        #        cmds.delete()
                        
                        bendyLegJoints = ['%sBendy_Hip' %LR, '%sBendy_Knee' %LR, '%sBendy_Knee_End' %LR]
                        
                        ####unparent the Bendy Leg####
                        cmds.select('%sBendy_Hip' %LR, r =True)
                        cmds.parent(w= True)
                        
                        ###Insert Joints#####
                        Number_Of_JointBetween = 6
                        
                        for i in range(len(bendyLegJoints)-2):
                                pos_1 = cmds.xform('%s' %bendyLegJoints[i], ws = True, t = True, q = True )
                                pos_2 = cmds.xform('%s' %bendyLegJoints[i+1], ws = True, t = True, q = True )
                                if LR == 'L_':
                                        pos_2 = [pos_2[0]-pos_1[0], pos_2[1]-pos_1[1], pos_2[2]-pos_1[2]]
                                        cmds.insertJoint('%s' %bendyLegJoints[i])
                                        cmds.joint('joint1', n = '%s_Bendy1' %bendyLegJoints[i], e = True, co = True, p = [pos_1[0] + pos_2[0]/Number_Of_JointBetween, pos_1[1] + pos_2[1]/Number_Of_JointBetween, pos_1[2] + pos_2[2]/Number_Of_JointBetween])
                                        for j in range(Number_Of_JointBetween-2):
                                                cmds.insertJoint('%s_Bendy%s' %(bendyLegJoints[i], j+1))
                                                cmds.joint('joint1', n = '%s_Bendy%s' %(bendyLegJoints[i], j+2), e = True, co = True, p = [pos_1[0] + (j+2)*pos_2[0]/Number_Of_JointBetween, pos_1[1] + (j+2)*pos_2[1]/Number_Of_JointBetween, pos_1[2] + (j+2)*pos_2[2]/Number_Of_JointBetween])             

                                else:   
                                        pos_2 = [-pos_2[0]+pos_1[0], pos_2[1]-pos_1[1], pos_2[2]-pos_1[2]]
                                        cmds.insertJoint('%s' %bendyLegJoints[i])
                                        cmds.joint('joint1', n = '%s_Bendy1' %bendyLegJoints[i], e = True, co = True, p = [pos_1[0] - pos_2[0]/Number_Of_JointBetween, pos_1[1] + pos_2[1]/Number_Of_JointBetween, pos_1[2] + pos_2[2]/Number_Of_JointBetween])
                                        for j in range(Number_Of_JointBetween-2):
                                                cmds.insertJoint('%s_Bendy%s' %(bendyLegJoints[i], j+1))
                                                cmds.joint('joint1', n = '%s_Bendy%s' %(bendyLegJoints[i], j+2), e = True, co = True, p = [pos_1[0] - (j+2)*pos_2[0]/Number_Of_JointBetween, pos_1[1] + (j+2)*pos_2[1]/Number_Of_JointBetween, pos_1[2] + (j+2)*pos_2[2]/Number_Of_JointBetween])
                                
                        #####Making Knee=>Ankle Joint##########
                        #####Duplicate and renaming#############
                        cmds.select('%sBendy_Knee' %LR, r = True)
                        cmds.rename('%sBendy_Hip_End' %LR)
                        cmds.duplicate(rr = True)
                        cmds.parent(w = True)
                        cmds.rename('%sBendy_Knee' %LR)
                        cmds.select('%sBendy_Knee|%sBendy_Ankle' %(LR, LR), r = True)
                        cmds.rename('%sBendy_Knee_End' %LR)
                        cmds.delete('%sBendy_Ankle' %LR)
                        
                        ####Insert Joint########
                        for i in range(len(bendyLegJoints)-2):
                                i = i+1
                                pos_1 = cmds.xform('%s' %bendyLegJoints[i], ws = True, t = True, q = True )
                                pos_2 = cmds.xform('%s' %bendyLegJoints[i+1], ws = True, t = True, q = True )
                                if LR == 'L_':
                                        pos_2 = [pos_2[0]-pos_1[0], pos_2[1]-pos_1[1], pos_2[2]-pos_1[2]]
                                        cmds.insertJoint('%s' %bendyLegJoints[i])
                                        cmds.joint('joint1', n = '%s_Bendy1' %bendyLegJoints[i], e = True, co = True, p = [pos_1[0] + pos_2[0]/Number_Of_JointBetween, pos_1[1] + pos_2[1]/Number_Of_JointBetween, pos_1[2] + pos_2[2]/Number_Of_JointBetween])
                                        for j in range(Number_Of_JointBetween-2):
                                                cmds.insertJoint('%s_Bendy%s' %(bendyLegJoints[i], j+1))
                                                cmds.joint('joint1', n = '%s_Bendy%s' %(bendyLegJoints[i], j+2), e = True, co = True, p = [pos_1[0] + (j+2)*pos_2[0]/Number_Of_JointBetween, pos_1[1] + (j+2)*pos_2[1]/Number_Of_JointBetween, pos_1[2] + (j+2)*pos_2[2]/Number_Of_JointBetween])             

                                else:   
                                        pos_2 = [-pos_2[0]+pos_1[0], pos_2[1]-pos_1[1], pos_2[2]-pos_1[2]]
                                        cmds.insertJoint('%s' %bendyLegJoints[i])
                                        cmds.joint('joint1', n = '%s_Bendy1' %bendyLegJoints[i], e = True, co = True, p = [pos_1[0] - pos_2[0]/Number_Of_JointBetween, pos_1[1] + pos_2[1]/Number_Of_JointBetween, pos_1[2] + pos_2[2]/Number_Of_JointBetween])
                                        for j in range(Number_Of_JointBetween-2):
                                                cmds.insertJoint('%s_Bendy%s' %(bendyLegJoints[i], j+1))
                                                cmds.joint('joint1', n = '%s_Bendy%s' %(bendyLegJoints[i], j+2), e = True, co = True, p = [pos_1[0] - (j+2)*pos_2[0]/Number_Of_JointBetween, pos_1[1] + (j+2)*pos_2[1]/Number_Of_JointBetween, pos_1[2] + (j+2)*pos_2[2]/Number_Of_JointBetween])                     
                        
                        ######IK Spline Curve########
                        Bendy_Hip_Pos = cmds.xform('%s' %bendyLegJoints[0], ws = True, t = True, q = True )
                        Bendy_Hip_Knee_Middle_Pos = cmds.xform('%s_Bendy%s' %(bendyLegJoints[0], Number_Of_JointBetween/2), ws = True, t = True, q = True )
                        Bendy_Knee_Pos = cmds.xform('%s' %bendyLegJoints[1], ws = True, t = True, q = True )
                        Bendy_Knee_Ankle_Middle_Pos = cmds.xform('%s_Bendy%s' %(bendyLegJoints[1], Number_Of_JointBetween/2), ws = True, t = True, q = True )
                        Bendy_Ankle_Pos = cmds.xform('%s' %bendyLegJoints[2], ws = True, t = True, q = True )
                        cmds.curve(n = '%sHip_Knee_IKSplineCV' %LR, d = 2, p = [(Bendy_Hip_Pos[0], Bendy_Hip_Pos[1], Bendy_Hip_Pos[2]), (Bendy_Hip_Knee_Middle_Pos[0], Bendy_Hip_Knee_Middle_Pos[1], Bendy_Hip_Knee_Middle_Pos[2]), (Bendy_Knee_Pos[0], Bendy_Knee_Pos[1], Bendy_Knee_Pos[2])], k = [0,0,1,1])
                        cmds.curve(n = '%sKnee_Ankle_IKSplineCV' %LR, d = 2, p = [(Bendy_Knee_Pos[0], Bendy_Knee_Pos[1], Bendy_Knee_Pos[2]), (Bendy_Knee_Ankle_Middle_Pos[0], Bendy_Knee_Ankle_Middle_Pos[1], Bendy_Knee_Ankle_Middle_Pos[2]), (Bendy_Ankle_Pos[0], Bendy_Ankle_Pos[1], Bendy_Ankle_Pos[2])], k = [0,0,1,1])
                        
                        ######IK Spline Handle#######
                        cmds.select('%sBendy_Hip' %LR, r = True)
                        cmds.select('%sBendy_Hip_End' %LR, add = True)
                        cmds.select('%sHip_Knee_IKSplineCV' %LR, add= True) 
                        cmds.ikHandle(n = '%sHip_Bendy_IKSpline_Handle'%LR, sol = 'ikSplineSolver', ccv = False, roc = False, pcv = False)
                        cmds.select('%sBendy_Knee' %LR, r = True)
                        cmds.select('%sBendy_Knee_End' %LR, add = True)
                        cmds.select('%sKnee_Ankle_IKSplineCV' %LR, add= True) 
                        cmds.ikHandle(n = '%sKnee_Bendy_IKSpline_Handle'%LR, sol = 'ikSplineSolver', ccv = False, roc = False, pcv = False)
                        
                        #######Insert Clusters########
                        for i in range(3):
                                cmds.select('%sHip_Knee_IKSplineCV.cv[%s]' %(LR, i), r = True)
                                cmds.cluster(n = '%sHip_Knee_IKSplineCV_Cluster%s' %(LR, i))
                                cmds.select('%sKnee_Ankle_IKSplineCV.cv[%s]' %(LR, i), r = True)
                                cmds.cluster(n = '%sKnee_Ankle_IKSplineCV%s' %(LR, i))
                        
                        #########Making CTRLs#########
                        cmds.createNode('transform', n = '%sUpperLeg_Bend_GRP' %LR)
                        cmds.circle( n = '%sUpperLeg_Bend' %LR, nr=(0, 1, 0), c=(0, 0, 0), r = 2)
                        cmds.select('%sUpperLeg_Bend_GRP' %LR, tgl = True)
                        cmds.parent()
                        cmds.createNode('transform', n = '%sLowerLeg_Bend_GRP' %LR)
                        cmds.circle( n = '%sLowerLeg_Bend' %LR, nr=(0, 1, 0), c=(0, 0, 0), r = 2)
                        cmds.select('%sLowerLeg_Bend_GRP' %LR, tgl = True)
                        cmds.parent()                   
                        
                        cmds.select('%sBendy_Hip_Bendy%s' %(LR, Number_Of_JointBetween/2), r = True)
                        cmds.select('%sUpperLeg_Bend_GRP' %LR, tgl = True)
                        cmds.pointConstraint(weight = 1)
                        cmds.orientConstraint(weight = 1)
                        cmds.select('%sBendy_Knee_Bendy%s' %(LR, Number_Of_JointBetween/2), r = True)
                        cmds.select('%sLowerLeg_Bend_GRP' %LR, tgl = True)
                        cmds.pointConstraint(weight = 1)
                        cmds.orientConstraint(weight = 1)
                        cmds.delete('%sUpperLeg_Bend_GRP_pointConstraint1' %LR)
                        cmds.delete('%sUpperLeg_Bend_GRP_orientConstraint1' %LR)
                        cmds.delete('%sLowerLeg_Bend_GRP_pointConstraint1' %LR)
                        cmds.delete('%sLowerLeg_Bend_GRP_orientConstraint1' %LR)
                        
                        #######Curve Length########
                        cmds.createNode('curveInfo', n = '%sUpperLeg_Length' %LR)
                        cmds.createNode('curveInfo', n = '%sLowerLeg_Length' %LR)
                        cmds.connectAttr('%sHip_Knee_IKSplineCV.worldSpace' %LR, '%sUpperLeg_Length.inputCurve' %LR)
                        cmds.connectAttr('%sKnee_Ankle_IKSplineCV.worldSpace' %LR, '%sLowerLeg_Length.inputCurve' %LR)
                        
                        #######Original Length#########
                        #####Locators for measuring distance#######
                        Bendy_Loc = ['Hip', 'Knee', 'Ankle']
                        cmds.createNode('transform', n = '%sBendy_Leg_Loc_GRP' %LR)
                        cmds.select('%sBendy_Leg_Loc_GRP' %LR, r = True)
                        cmds.select('Puck', tgl = True)
                        cmds.parent()
                        cmds.setAttr('%sBendy_Leg_Loc_GRP.visibility' %LR, 0)
                        for loc in Bendy_Loc:
                                cmds.spaceLocator(n = '%sBendy_%s_Loc' %(LR, loc))

                                cmds.select('%s%s' %(LR, loc), r = True)
                                cmds.select('%sBendy_%s_Loc' %(LR, loc), tgl = True)
                                cmds.pointConstraint(weight = 1)
                                cmds.select('%sBendy_%s_Loc' %(LR, loc), r = True)
                                cmds.select('%sBendy_Leg_Loc_GRP' %LR, tgl = True)
                                cmds.parent()
                        
                        #######Distance#######
                        cmds.shadingNode('distanceBetween', n = '%sBendyLeg_UpperLength' %LR, asUtility = True)
                        cmds.shadingNode('distanceBetween', n = '%sBendyLeg_LowerLength' %LR, asUtility = True)
                        cmds.connectAttr('%sBendy_Hip_Loc.translate' %LR,'%sBendyLeg_UpperLength.point1' %LR )
                        cmds.connectAttr('%sBendy_Knee_Loc.translate' %LR, '%sBendyLeg_UpperLength.point2' %LR )
                        cmds.connectAttr('%sBendy_Knee_Loc.translate' %LR, '%sBendyLeg_LowerLength.point1' %LR )
                        cmds.connectAttr('%sBendy_Ankle_Loc.translate' %LR, '%sBendyLeg_LowerLength.point2' %LR )

                        cmds.shadingNode('multiplyDivide', n = '%sBendy_Leg_PuckScale' %LR, asUtility = True)
                        cmds.connectAttr('Puck.scaleX', '%sBendy_Leg_PuckScale.input1X' %LR)
                        cmds.connectAttr('Puck.scaleX', '%sBendy_Leg_PuckScale.input1Y' %LR)
                        cmds.connectAttr('%sBendyLeg_UpperLength.distance' %LR, '%sBendy_Leg_PuckScale.input2X' %LR)
                        cmds.connectAttr('%sBendyLeg_LowerLength.distance' %LR, '%sBendy_Leg_PuckScale.input2Y' %LR)
                        
                        #######Stretch Ratio######
                        cmds.shadingNode('multiplyDivide', n = '%sBendyLeg_StretchRatio' %LR, asUtility = True)
                        cmds.setAttr('%sBendyLeg_StretchRatio.operation' %LR, 2)
                                                
                        cmds.connectAttr('%sBendy_Leg_PuckScale.outputX' %LR, '%sBendyLeg_StretchRatio.input2X' %LR)
                        cmds.connectAttr('%sBendy_Leg_PuckScale.outputY' %LR, '%sBendyLeg_StretchRatio.input2Y' %LR)
                        cmds.connectAttr('%sUpperLeg_Length.arcLength' %LR, '%sBendyLeg_StretchRatio.input1X' %LR)
                        cmds.connectAttr('%sLowerLeg_Length.arcLength' %LR, '%sBendyLeg_StretchRatio.input1Y' %LR)
                        
                        #######Bendy Stretch Condition###########
                        cmds.shadingNode('condition', n = '%sBendyLeg_UpperCondition' %LR, asUtility = True)
                        cmds.shadingNode('condition', n = '%sBendyLeg_LowerCondition' %LR, asUtility = True)
                        cmds.setAttr('%sBendyLeg_UpperCondition.secondTerm' %LR, 1)                     
                        cmds.setAttr('%sBendyLeg_LowerCondition.secondTerm' %LR, 1)
                        cmds.setAttr('%sBendyLeg_UpperCondition.operation' %LR, 3)
                        cmds.setAttr('%sBendyLeg_LowerCondition.operation' %LR, 3)
                        cmds.connectAttr('%sUpperLeg_Length.arcLength' %LR, '%sBendyLeg_UpperCondition.firstTerm' %LR)
                        cmds.connectAttr('%sLowerLeg_Length.arcLength' %LR, '%sBendyLeg_LowerCondition.firstTerm' %LR)
                        cmds.connectAttr('%sBendyLeg_UpperLength.distance' %LR, '%sBendyLeg_UpperCondition.secondTerm' %LR)
                        cmds.connectAttr('%sBendyLeg_LowerLength.distance' %LR, '%sBendyLeg_LowerCondition.secondTerm' %LR)
                        cmds.connectAttr('%sBendyLeg_StretchRatio.outputX' %LR, '%sBendyLeg_UpperCondition.colorIfTrueR' %LR)
                        cmds.connectAttr('%sBendyLeg_StretchRatio.outputY' %LR, '%sBendyLeg_LowerCondition.colorIfTrueR' %LR)
                        
                        ########Grouping##########
                        cmds.createNode('transform', n = '%sBendy_Hip_Joint_GRP' %LR)
                        cmds.select('%sBendy_Hip' %LR, r = True)
                        cmds.select('%sBendy_Hip_Joint_GRP' %LR , tgl = True)
                        cmds.parent()
                        cmds.createNode('transform', n = '%sBendy_Knee_Joint_GRP' %LR)
                        cmds.select('%sBendy_Knee' %LR, r = True)
                        cmds.select('%sBendy_Knee_Joint_GRP' %LR , tgl = True)
                        cmds.parent()
                        cmds.createNode('transform', n = '%sBendy_Leg_Joint_GRP' %LR)
                        cmds.select('%sBendy_Knee_Joint_GRP' %LR , r = True)
                        cmds.select('%sBendy_Hip_Joint_GRP' %LR , add = True)
                        cmds.select('%sBendy_Leg_Joint_GRP' %LR, tgl = True)
                        cmds.parent()
                        cmds.createNode('transform', n = '%sBendy_Leg_GRP' %LR)
                        
                        cmds.select('%sHip_Bendy_IKSpline_Handle' %LR, r = True)
                        cmds.select('%sKnee_Bendy_IKSpline_Handle' %LR, add = True)
                        cmds.select('%sBendy_Leg_GRP' %LR, tgl = True)
                        cmds.parent()
                        
                        cmds.select('%sHip_Knee_IKSplineCV_Cluster1Handle' %LR, r = True)
                        cmds.select('%sUpperLeg_Bend' %LR, tgl = True)
                        cmds.parent()
                        cmds.select('%sKnee_Ankle_IKSplineCV1Handle' %LR, r = True)
                        cmds.select('%sLowerLeg_Bend' %LR, tgl = True)
                        cmds.parent()
                        
                        cmds.select('%sHip' %LR, r = True)
                        cmds.select('%sBendy_Hip_Joint_GRP' %LR, tgl = True)
                        cmds.pointConstraint(weight = 1, mo = True)
                        cmds.select('%sKnee' %LR, r = True)
                        cmds.select('%sBendy_Knee_Joint_GRP' %LR, tgl = True)
                        cmds.pointConstraint(weight = 1, mo = True)
                        
                
                        #######Cluster Grouping##########
                        
                        cmds.select('%sHip_Knee_IKSplineCV_Cluster0Handle' %LR, r = True)
                        cmds.select('%sHip' %LR, tgl = True)
                        cmds.parent()
                        cmds.select('%sUpperLeg_Bend_GRP' %LR, r = True)
                        cmds.select('%sHip' %LR, tgl = True)
                        cmds.parent()
                        cmds.select('%sHip_Knee_IKSplineCV_Cluster2Handle' %LR, r = True)
                        cmds.select('%sKnee' %LR, tgl = True)
                        cmds.parent()                   
                        cmds.select('%sKnee_Ankle_IKSplineCV0Handle' %LR, r = True)
                        cmds.select('%sKnee' %LR, tgl = True)
                        cmds.parent()
                        cmds.select('%sLowerLeg_Bend_GRP' %LR, r = True)
                        cmds.select('%sKnee' %LR, tgl = True)
                        cmds.parent()
                        cmds.select('%sKnee_Ankle_IKSplineCV2Handle' %LR, r = True)
                        cmds.select('%sAnkle' %LR, tgl = True)
                        cmds.parent()
                        cmds.select('%sBendy_Leg_Joint_GRP' %LR, r = True)
                        cmds.select('%sBendy_Leg_GRP' %LR, tgl = True)
                        cmds.parent()
                        cmds.select('%sBendy_Leg_GRP' %LR, r = True)
                        cmds.select('Puck', tgl = True)
                        cmds.parent()
                        cmds.createNode('transform', n = '%sBendyCurve_GRP' %LR)
                        cmds.select('%sHip_Knee_IKSplineCV' %LR, r = True)
                        cmds.select('%sKnee_Ankle_IKSplineCV' %LR, add = True)
                        cmds.select('%sBendyCurve_GRP' %LR, tgl = True)
                        cmds.parent()
                        #cmds.select('%sHip_Knee_IKSplineCV' %LR, r = True)
                        #cmds.select('%sHip' %LR, tgl = True)
                        #cmds.parent()
                        #cmds.parent('%sKnee_Ankle_IKSplineCV' %LR, r = True)
                        #cmds.select('%sHip' %LR, tgl = True)
                        #cmds.parent()
                        
                        Bendy_Hip_destination = cmds.listRelatives('%sBendy_Hip_Joint_GRP' %LR, ad = True)
                        Bendy_Hip_destination = Bendy_Hip_destination[2:-1]
                        Bendy_Knee_destination = cmds.listRelatives('%sBendy_Knee_Joint_GRP' %LR, ad = True)
                        Bendy_Knee_destination = Bendy_Knee_destination[2:-1]
                        #print Bendy_Hip_destination
                        #print Bendy_Knee_destination
                        
                        for joint in Bendy_Hip_destination:
                                cmds.connectAttr('%sBendyLeg_UpperCondition.outColorR' %LR, '%s.scaleY' %joint)
                        for joint in Bendy_Knee_destination:
                                cmds.connectAttr('%sBendyLeg_LowerCondition.outColorR' %LR, '%s.scaleY' %joint)                 
                        
                        cmds.setAttr('%sHip_Bendy_IKSpline_Handle.visibility' %LR, 0)
                        cmds.setAttr('%sKnee_Bendy_IKSpline_Handle.visibility' %LR, 0)
                        cmds.setAttr('%sHip_Knee_IKSplineCV_Cluster0Handle.visibility' %LR, 0)
                        cmds.setAttr('%sHip_Knee_IKSplineCV_Cluster1Handle.visibility' %LR, 0)
                        cmds.setAttr('%sHip_Knee_IKSplineCV_Cluster2Handle.visibility' %LR, 0)
                        cmds.setAttr('%sKnee_Ankle_IKSplineCV0Handle.visibility' %LR, 0)        
                        cmds.setAttr('%sKnee_Ankle_IKSplineCV1Handle.visibility' %LR, 0)                        
                        cmds.setAttr('%sKnee_Ankle_IKSplineCV2Handle.visibility' %LR, 0)        
                                
                        cmds.addAttr('%sLeg_Extra_CTRL' %LR,  ln = 'Bend', at = 'long', min = 0, max = 1)
                        cmds.setAttr('%sLeg_Extra_CTRL.Bend' %LR, e = True, keyable = True)
                        cmds.connectAttr('%sLeg_Extra_CTRL.Bend' %LR, '%sUpperLeg_Bend.visibility' %LR)
                        cmds.connectAttr('%sLeg_Extra_CTRL.Bend' %LR, '%sLowerLeg_Bend.visibility' %LR)
                                        
                
        
        def stretchIkLeg(self):
                for LR in L_o_R:
                        cmds.addAttr('%sLeg_Extra_CTRL' %LR, ln = 'Stretch_IK', at = 'long', min = 0, max = 1)
                        cmds.setAttr('%sLeg_Extra_CTRL.Stretch_IK' %LR, e = True, keyable = True)
        
        ###Applies when both L, R leg's lengths are same. 
                        
                        ###Installing Locator
                        cmds.spaceLocator(n = '%sHip_Stretch_Loc' %LR)
                        if LR == 'L_':
                                cmds.move(self.leftHipPos[0], self.leftHipPos[1], self.leftHipPos[2])
                        else:
                                cmds.move(-self.leftHipPos[0], self.leftHipPos[1], self.leftHipPos[2])
                        cmds.select('%sHip' %LR, r = True)
                        cmds.select('%sHip_Stretch_Loc' %LR, tgl = True)
                        cmds.pointConstraint(offset = [0, 0, 0], weight = 1)
                        
                        cmds.spaceLocator(n = '%sAnkle_Stretch_Loc' %LR)
                        if LR == 'L_':
                                cmds.move(self.leftAnklePos[0], self.leftAnklePos[1], self.leftAnklePos[2])
                        else:
                                cmds.move(-self.leftAnklePos[0], self.leftAnklePos[1], self.leftAnklePos[2])
                        cmds.select('%sLeg_CTRL' %LR, r = True)
                        cmds.select('%sAnkle_Stretch_Loc' %LR, tgl = True)
                        cmds.pointConstraint(offset = [0, 0, 0], weight = 1)
        
                        cmds.createNode('transform', n = '%sStretch_Leg_GRP' %LR)
                        cmds.select('%sHip_Stretch_Loc' %LR, r = True)
                        cmds.select('%sAnkle_Stretch_Loc' %LR, add = True)
                        cmds.select('%sStretch_Leg_GRP' %LR, tgl = True)
                        cmds.parent()
                        cmds.select('%sStretch_Leg_GRP' %LR, r = True)
                        cmds.select('Puck', tgl = True)
                        cmds.parent()
                                                                
                        Upper_Leg_Length = [self.leftKneePos[0] - self.leftHipPos[0], self.leftKneePos[1] - self.leftHipPos[1], self.leftKneePos[2] - self.leftHipPos[2]]
                        Lower_Leg_Length = [self.leftAnklePos[0] - self.leftKneePos[0], self.leftAnklePos[1] - self.leftKneePos[1], self.leftAnklePos[2] - self.leftKneePos[2]]
                        Leg_Length = math.sqrt(Upper_Leg_Length[0]*Upper_Leg_Length[0]+Upper_Leg_Length[1]*Upper_Leg_Length[1]+Upper_Leg_Length[2]*Upper_Leg_Length[2])+math.sqrt(Lower_Leg_Length[0]*Lower_Leg_Length[0]+Lower_Leg_Length[1]*Lower_Leg_Length[1]+Lower_Leg_Length[2]*Lower_Leg_Length[2])
                        
                        ####Divided value by the scale of Puck.... distance between shoulder and wrist
                        cmds.shadingNode('multiplyDivide', n = '%sStretch_LegIK_Length_MulDiv' %LR, asUtility = True)
                        cmds.setAttr('%sStretch_LegIK_Length_MulDiv.operation' %LR, 1)
                        cmds.setAttr('%sStretch_LegIK_Length_MulDiv.input1X' %LR, Leg_Length)
                        cmds.connectAttr('Puck.scaleX', '%sStretch_LegIK_Length_MulDiv.input2X' %LR)
                        
                        ####Distance between Hip and Ankle CTRL
                        cmds.shadingNode('distanceBetween', n = '%sStretch_LegIK_Distance' %LR, asUtility = True)
                        cmds.connectAttr('%sHip_Stretch_Loc.translate' %LR, '%sStretch_LegIK_Distance.point1' %LR)
                        cmds.connectAttr('%sAnkle_Stretch_Loc.translate' %LR, '%sStretch_LegIK_Distance.point2' %LR)
                        cmds.connectAttr('%sStretch_LegIK_Distance.distance' %LR, '%sStretch_LegIK_Length_MulDiv.input1Y' %LR)
                        cmds.connectAttr('Puck.scaleX', '%sStretch_LegIK_Length_MulDiv.input2Y' %LR)
                        
                        ###condition node calculate length and compare and do shit
                        cmds.shadingNode('condition', n = '%sStretch_LegIK_Con' %LR, asUtility = True)
                        cmds.connectAttr('%sStretch_LegIK_Length_MulDiv.outputY' %LR, '%sStretch_LegIK_Con.firstTerm' %LR)
                        cmds.connectAttr('%sStretch_LegIK_Length_MulDiv.outputX' %LR, '%sStretch_LegIK_Con.secondTerm' %LR)
                        cmds.setAttr('%sStretch_LegIK_Con.operation' %LR, 2)
                        
                        ####Stretch Ratio
                        cmds.shadingNode('multiplyDivide', n = '%sStretch_LegIK_ratio_MulDiv' %LR, asUtility = True)
                        cmds.connectAttr('%sStretch_LegIK_Length_MulDiv.outputY' %LR, '%sStretch_LegIK_ratio_MulDiv.input1X' %LR)
                        cmds.connectAttr('%sStretch_LegIK_Length_MulDiv.outputX' %LR, '%sStretch_LegIK_ratio_MulDiv.input2X' %LR)
                        cmds.setAttr('%sStretch_LegIK_ratio_MulDiv.operation' %LR, 2)
                        ####Last Mux
                        cmds.shadingNode('blendColors', n = '%sLeg_Stretch_Mux' %LR, asUtility = True)
                        cmds.connectAttr('%sStretch_LegIK_Con.outColorR' %LR, '%sLeg_Stretch_Mux.blender' %LR)
                        cmds.setAttr('%sLeg_Stretch_Mux.color1R' %LR, 1)
                        cmds.connectAttr('%sStretch_LegIK_ratio_MulDiv.outputX' %LR,'%sLeg_Stretch_Mux.color2R' %LR)
                        
                        ####stretch MUX
                        cmds.shadingNode('blendColors', n = '%sLeg_StretchYesNo_Mux' %LR, asUtility = True)
                        cmds.connectAttr('%sLeg_Extra_CTRL.Stretch_IK' %LR, '%sLeg_StretchYesNo_Mux.blender' %LR)
                        cmds.setAttr('%sLeg_StretchYesNo_Mux.color2R' %LR, 1)
                        cmds.connectAttr('%sLeg_Stretch_Mux.outputR' %LR, '%sLeg_StretchYesNo_Mux.color1R' %LR)
                        
                        cmds.connectAttr('%sLeg_StretchYesNo_Mux.outputR' %LR, '%sHip.scaleY' %LR)
                        cmds.connectAttr('%sLeg_StretchYesNo_Mux.outputR' %LR, '%sKnee.scaleY' %LR)
                        
                        cmds.select('%sStretch_Leg_GRP' %LR, r = True)
                        cmds.setAttr('%sStretch_Leg_GRP.visibility' %LR, 0)
                        
                        #######Stretch and Bend##########
                        cmds.shadingNode('multiplyDivide', n = '%sLeg_StretchBend' %LR, asUtility = True)
                        
                        cmds.connectAttr('%sLeg_StretchYesNo_Mux.outputR' %LR, '%sLeg_StretchBend.input1X' %LR)
                        cmds.connectAttr('%sLeg_StretchYesNo_Mux.outputR' %LR, '%sLeg_StretchBend.input1Y' %LR)

                        Bendy_Hip_destination = cmds.listRelatives('%sBendy_Hip_Joint_GRP' %LR, ad = True)
                        Bendy_Hip_destination = Bendy_Hip_destination[2:-1]
                        Bendy_Knee_destination = cmds.listRelatives('%sBendy_Knee_Joint_GRP' %LR, ad = True)
                        Bendy_Knee_destination = Bendy_Knee_destination[2:-1]
                        #print Bendy_Hip_destination
                        #print Bendy_Ankle_destination
                        
                        cmds.connectAttr('%sBendyLeg_UpperCondition.outColorR' %LR, '%sLeg_StretchBend.input2X' %LR)
                        cmds.connectAttr('%sBendyLeg_LowerCondition.outColorR' %LR, '%sLeg_StretchBend.input2Y' %LR)
                        
                        for joint in Bendy_Hip_destination:
                                cmds.connectAttr('%sLeg_StretchBend.outputX' %LR, '%s.scaleY' %joint, f = True)
                        for joint in Bendy_Knee_destination:
                                cmds.connectAttr('%sLeg_StretchBend.outputY' %LR, '%s.scaleY' %joint, f = True)                         
                        
                        
                        
        def head_Orientation_Setting(self):
                
                ########Unparent head joint and CTRL####
                cmds.select('Head', r = True)
                cmds.parent(w = True)
                cmds.select('Head_CTRL_GRP', r = True)
                cmds.parent(w = True)
                cmds.createNode('transform', n = 'Head_World_GRP')
                cmds.createNode('transform', n = 'Head_GRP')
                cmds.move(self.headPos[0], self.headPos[1], self.headPos[2])
                
                ########making locator###### and GRP  ######
                cmds.spaceLocator(n = 'Head_Orientation_Loc_Neck')#Neck
                cmds.move(self.headPos[0], self.headPos[1], self.headPos[2])
                #cmds.spaceLocator(n = 'Head_Orientation_Loc_Root')#Root
                #cmds.move(self.headPos[0], self.headPos[1], self.headPos[2])
                cmds.createNode('transform', n = 'Head_Neck_Orient_GRP')
                cmds.move(self.neckBasePos[0], self.neckBasePos[1], self.neckBasePos[2])
                #cmds.createNode('transform', n = 'Head_Root_Orient_GRP')
                #cmds.move(self.rootPos[0], self.rootPos[1], self.rootPos[2])       
                cmds.select('Head_Orientation_Loc_Neck', r = True)
                cmds.select('Head_Neck_Orient_GRP', tgl = True)
                cmds.parent()
                #cmds.select('Head_Orientation_Loc_Root', r = True)
                #cmds.select('Head_Root_Orient_GRP', tgl = True)
                #cmds.parent()
                ##########Head Attr##########
                cmds.addAttr('Head_CTRL', ln = 'ss', at = 'double')
                cmds.setAttr('Head_CTRL.ss', e = True, channelBox = True)
                cmds.addAttr('Head_CTRL', ln = 'World', at = 'long', min = 0, max = 1)
                cmds.setAttr('Head_CTRL.World', e = True, keyable = True)
                #cmds.addAttr('Head_CTRL', ln = 'Root', at = 'long', min = 0, max = 1 )
                #cmds.setAttr('Head_CTRL.Root', e = True, keyable = True)
        
                #####Parent with Neck....###
                cmds.select('NeckBase', r = True)
                cmds.select('Head_Neck_Orient_GRP', tgl = True)
                cmds.pointConstraint(weight = 1, mo = True)
                cmds.orientConstraint(weight = 1, mo = True)
                
                cmds.select('Head_Orientation_Loc_Neck', r = True)
                cmds.select('Head_GRP', tgl = True)
                cmds.pointConstraint(weight = 1, mo = True)
                cmds.orientConstraint(weight = 1, mo = True)
                
                ####Ctrl Attribute assign###
                cmds.shadingNode('blendColors', n = 'Head_World_con', asUtility = True)
                cmds.connectAttr('Head_CTRL.World', 'Head_World_con.blender')
                cmds.setAttr('Head_World_con.color1R', 0)
                cmds.setAttr('Head_World_con.color2R', 1)
                cmds.connectAttr('Head_World_con.outputR', 'Head_GRP_orientConstraint1.Head_Orientation_Loc_NeckW0')
        
                ####Grouping####

                cmds.select('Head', r = True)
                cmds.select('Head_CTRL_GRP', add = True)
                cmds.select('Head_GRP', add = True)
                cmds.parent()
                cmds.select('Head_GRP', r = True)
                cmds.select('Head_Neck_Orient_GRP', add = True)
                cmds.select('Head_World_GRP', tgl = True)
                cmds.parent()
                cmds.select('Head_World_GRP', r = True)
                cmds.select('Puck', tgl = True)
                cmds.parent()
                cmds.setAttr('Head_Neck_Orient_GRP.visibility', 0)
        
        def Stretch_Spline_IK_Spine(self):
        
                ####Spine Initialize####
                self.spineJoints_Stretch = ['Spine1','Spine2', 'Spine3', 'Spine4' ]
                for joint in self.spineJoints_Stretch:
                        cmds.delete('%s_orientConstraint1' %joint)
                        
                for LR in L_o_R:
                        cmds.select('%sScapula' %LR)
                        cmds.parent(w = True)
                cmds.createNode('transform', n = 'Scapula_GRP')
                cmds.select('L_Scapula', r = True)
                cmds.select('R_Scapula', add = True)
                cmds.select('Scapula_GRP', tgl = True)
                cmds.parent()
                cmds.select('Scapula_GRP', r = True)
                cmds.select('Puck', tgl = True)
                cmds.parent()
                #####Create more Joints#######
                for i in range(len(self.spineJoints_Stretch)-1):
                        pos_1 = cmds.xform('%s' %self.spineJoints_Stretch[i], ws = True, t = True, q = True )
                        pos_2 = cmds.xform('%s' %self.spineJoints_Stretch[i+1], t = True, q = True )
                        cmds.insertJoint('%s' %self.spineJoints_Stretch[i], )
                        cmds.joint('joint1', n = '%s1' %self.spineJoints_Stretch[i], e = True, co = True, p = [0, pos_1[1] + pos_2[1]/3,pos_1[2] + pos_2[2]/3])
                        cmds.insertJoint('%s1' %self.spineJoints_Stretch[i], )
                        cmds.joint('joint1', n = '%s2' %self.spineJoints_Stretch[i], e = True, co = True, p = [0, pos_1[1] + 2*pos_2[1]/3, pos_1[2] + 2*pos_2[2]/3])
                ######Install IK Handle########
                self.spine1Pos_IK = cmds.xform('Spine1', q = True, ws = True, t = True)
                self.spine2Pos_IK = cmds.xform('Spine2', q = True, ws = True, t = True)
                self.spine3Pos_IK = cmds.xform('Spine3', q = True, ws = True, t = True)
                self.spine4Pos_IK = cmds.xform('Spine4', q = True, ws = True, t = True)
                cmds.curve(n = 'Spine_SplineIK_Curve', d =  3, p = [(self.spine1Pos_IK[0], self.spine1Pos_IK[1], self.spine1Pos_IK[2]), (self.spine2Pos_IK[0], self.spine2Pos_IK[1], self.spine2Pos_IK[2]), (self.spine3Pos_IK[0], self.spine3Pos_IK[1], self.spine3Pos_IK[2]), (self.spine4Pos_IK[0], self.spine4Pos_IK[1], self.spine4Pos_IK[2])], k = [0,0,0,1,1,1]) 
                cmds.select('Spine1.rotatePivot', r = True) 
                cmds.select('Spine4.rotatePivot', add = True)
                cmds.select('Spine_SplineIK_Curve', add = True)
                cmds.ikHandle(n = 'SpineIK_Handle', sol = 'ikSplineSolver', ccv  = False)
                cmds.setAttr('SpineIK_Handle.visibility', 0)
                cmds.select('NeckBase_CTRL_GRP', r = True)
                cmds.select('L_Scapula_CTRL_GRP', tgl = True)
                cmds.select('R_Scapula_CTRL_GRP', tgl = True)
                cmds.parent(w = True)
                cmds.select('Spine1_CTRL_GRP', r = True)
                cmds.delete()
                #######Controller########
                for i in range(len(self.spineJoints_Stretch)):
                        cmds.circle( n = '%s_CTRL' %self.spineJoints_Stretch[i], nr=(0, 1, 0), c=(0, 0, 0), r = 5)
                        cmds.createNode('transform', n = '%s_CTRL_GRP' %self.spineJoints_Stretch[i])
                        cmds.select('%s_CTRL' %self.spineJoints_Stretch[i], r = True)
                        cmds.select('%s_CTRL_GRP' %self.spineJoints_Stretch[i], tgl = True)
                        cmds.parent()
                        cmds.select('%s_CTRL_GRP' %self.spineJoints_Stretch[i], r = True)
                        pos = cmds.xform('%s'%self.spineJoints_Stretch[i], q = True, t = True, ws = True)
                        cmds.move(pos[0], pos[1], pos[2] )
                        cmds.select('Spine_SplineIK_Curve.cv[%s]' %i, r = True) 
                        cmds.cluster(n = 'Spine%s_IK_cluster' %str(i+1))
                        cmds.select('%s_CTRL' %self.spineJoints_Stretch[i], tgl = True)
                        cmds.parent()
                        cmds.setAttr('Spine%s_IK_clusterHandle.visibility' %str(i+1), 0)
                
                #######IK FK Settup##########
                cmds.createNode('transform', n = 'Spine4_CTRL_GRP3')
                cmds.move(self.spine1Pos_IK[0], self.spine1Pos_IK[1], self.spine1Pos_IK[2])
                cmds.createNode('transform', n = 'Spine4_CTRL_GRP2')
                cmds.move(self.spine2Pos_IK[0], self.spine2Pos_IK[1], self.spine2Pos_IK[2])
                cmds.createNode('transform', n = 'Spine4_CTRL_GRP1')
                cmds.move(self.spine3Pos_IK[0], self.spine3Pos_IK[1], self.spine3Pos_IK[2])
                cmds.select('Spine4_CTRL_GRP2', r = True)
                cmds.select('Spine4_CTRL_GRP3', tgl = True)
                cmds.parent()
                cmds.select('Spine4_CTRL_GRP1', r = True)
                cmds.select('Spine4_CTRL_GRP2', tgl = True)
                cmds.parent()
                cmds.select('Spine4_CTRL_GRP', r = True)
                cmds.select('Spine4_CTRL_GRP1', tgl = True)
                cmds.parent()
                cmds.createNode('transform', n = 'Spine3_CTRL_GRP2')
                cmds.move(self.spine1Pos_IK[0], self.spine1Pos_IK[1], self.spine1Pos_IK[2])
                cmds.createNode('transform', n = 'Spine3_CTRL_GRP1')
                cmds.move(self.spine2Pos_IK[0], self.spine2Pos_IK[1], self.spine2Pos_IK[2])
                cmds.select('Spine3_CTRL_GRP1', r = True)
                cmds.select('Spine3_CTRL_GRP2', tgl = True)
                cmds.parent()
                cmds.select('Spine3_CTRL_GRP', r = True)
                cmds.select('Spine3_CTRL_GRP1', tgl = True)
                cmds.parent()
                cmds.createNode('transform', n = 'Spine2_CTRL_GRP1')
                cmds.move(self.spine1Pos_IK[0], self.spine1Pos_IK[1], self.spine1Pos_IK[2])
                cmds.select('Spine2_CTRL_GRP', r = True)
                cmds.select('Spine2_CTRL_GRP1', tgl = True)
                cmds.parent()

                cmds.select('Spine1_CTRL', r = True)
                cmds.select('Spine2_CTRL_GRP1', tgl = True)
                cmds.orientConstraint(weight = 1)               
                
                cmds.select('Spine1_CTRL', r = True)
                cmds.select('Spine3_CTRL_GRP2', tgl = True)
                cmds.orientConstraint(weight = 1)
                
                cmds.select('Spine2_CTRL', r = True)
                cmds.select('Spine3_CTRL_GRP1', tgl = True)
                cmds.orientConstraint(weight = 1)

                cmds.select('Spine1_CTRL', r = True)
                cmds.select('Spine4_CTRL_GRP3', tgl = True)
                cmds.orientConstraint(weight = 1)
                
                cmds.select('Spine2_CTRL', r = True)
                cmds.select('Spine4_CTRL_GRP2', tgl = True)
                cmds.orientConstraint(weight = 1)
                
                cmds.select('Spine3_CTRL', r = True)
                cmds.select('Spine4_CTRL_GRP1', tgl = True)
                cmds.orientConstraint(weight = 1)               
                
                cmds.createNode('transform', n = 'Stretch_SpineIK_GRP')
                cmds.select('SpineIK_Handle', r = True)
                cmds.select('Spine1_CTRL_GRP', add = True)
                cmds.select('Spine2_CTRL_GRP1', add = True)
                cmds.select('Spine3_CTRL_GRP2', add = True)
                cmds.select('Spine4_CTRL_GRP3', add = True)
                cmds.select('Stretch_SpineIK_GRP', tgl = True)
                cmds.parent()
                cmds.select('Stretch_SpineIK_GRP', r = True)
                cmds.select('Puck', tgl = True)
                cmds.parent()
                
                cmds.select('Spine_SplineIK_Curve', r = True)
                cmds.parent(w = True)
                
                cmds.setAttr('Spine_SplineIK_Curve.visibility', 0)
                
        ######### Stretch #######       
                cmds.addAttr('Root_CTRL', ln = 'Stretch_Spine',  at = 'long', min = 0, max = 1)
                cmds.setAttr('Root_CTRL.Stretch_Spine', e = True, keyable = True)
                
                ####distance locator####
                cmds.spaceLocator(n = 'Spine1_Loc')
                cmds.move(self.spine1Pos_IK[0], self.spine1Pos_IK[1], self.spine1Pos_IK[2])
                cmds.select('Spine1', r = True)
                cmds.select('Spine1_Loc', tgl = True)
                cmds.pointConstraint(offset = [0, 0, 0], weight = 1)
                cmds.spaceLocator(n = 'Spine4_Loc')
                cmds.move(self.spine4Pos_IK[0], self.spine4Pos_IK[1], self.spine4Pos_IK[2])
                cmds.select('Spine4_CTRL', r = True)
                cmds.select('Spine4_Loc', tgl = True)
                cmds.pointConstraint(offset = [0, 0, 0], weight = 1)
                cmds.select('Spine4', r = True)
                cmds.select('Spine4_Loc', tgl = True)
                cmds.orientConstraint(offset = [0, 0, 0], weight = 1, mo = True)                
                
                cmds.createNode('transform', n = 'Stretch_Spine_Loc_GRP')
                cmds.select('Spine1_Loc', r = True)
                cmds.select('Spine4_Loc', add = True)
                cmds.select('Stretch_Spine_Loc_GRP', tgl = True)
                cmds.parent()
                
                cmds.select('Stretch_Spine_Loc_GRP', r = True)
                cmds.select('Puck', tgl = True)
                cmds.parent()
                
                Spine12_IK_Pos = [self.spine2Pos_IK[0] - self.spine1Pos_IK[0], self.spine2Pos_IK[1] - self.spine1Pos_IK[1], self.spine2Pos_IK[2] - self.spine1Pos_IK[2]]
                Spine23_IK_Pos = [self.spine3Pos_IK[0] - self.spine2Pos_IK[0], self.spine3Pos_IK[1] - self.spine2Pos_IK[1], self.spine3Pos_IK[2] - self.spine2Pos_IK[2]]
                Spine34_IK_Pos = [self.spine4Pos_IK[0] - self.spine3Pos_IK[0], self.spine4Pos_IK[1] - self.spine3Pos_IK[1], self.spine4Pos_IK[2] - self.spine3Pos_IK[2]]
                Spine_Length = math.sqrt((Spine12_IK_Pos[1]*Spine12_IK_Pos[1])+(Spine12_IK_Pos[2]*Spine12_IK_Pos[2])) + math.sqrt((Spine23_IK_Pos[1]*Spine23_IK_Pos[1])+(Spine23_IK_Pos[2]*Spine23_IK_Pos[2])) + math.sqrt((Spine34_IK_Pos[1]*Spine34_IK_Pos[1])+(Spine34_IK_Pos[2]*Spine34_IK_Pos[2]))
                print Spine_Length
                
                #######Loc Distance#####
                cmds.shadingNode('distanceBetween', n = 'Spine_Loc_Distance', asUtility = True)
                cmds.connectAttr('Spine1_Loc.translate', 'Spine_Loc_Distance.point1')
                cmds.connectAttr('Spine4_Loc.translate', 'Spine_Loc_Distance.point2')
                        
                
                #######multiplied spine length#########
                cmds.shadingNode('multiplyDivide', n = 'Spine_Length', asUtility = True)
                cmds.connectAttr('Puck.scaleX', 'Spine_Length.input1X')
                cmds.connectAttr('Puck.scaleX', 'Spine_Length.input1Y')
                cmds.connectAttr('Spine_Loc_Distance.distance', 'Spine_Length.input2Y')
                cmds.setAttr('Spine_Length.input2X', Spine_Length)
                                
                
                #####Stretch Ratio###########
                cmds.shadingNode('multiplyDivide', n = 'Stretch_ratio', asUtility = True)
                cmds.setAttr('Stretch_ratio.operation', 2)
                cmds.connectAttr('Spine_Length.outputX', 'Stretch_ratio.input2X')
                cmds.connectAttr('Spine_Length.outputY', 'Stretch_ratio.input1X')
                
                cmds.shadingNode('blendColors', n = 'Stretch_Mux', asUtility = True)
                cmds.connectAttr('Root_CTRL.Stretch_Spine', 'Stretch_Mux.blender')
                cmds.setAttr('Stretch_Mux.color2R', 1)
                cmds.connectAttr('Spine_Length.outputY', 'Stretch_Mux.color1R')
                
                ######condidition#############
                cmds.shadingNode('condition', n = 'Stretch_Spine_Condition', asUtility = True)
                cmds.connectAttr('Stretch_Mux.outputR', 'Stretch_Spine_Condition.firstTerm')
                cmds.connectAttr('Spine_Length.outputX', 'Stretch_Spine_Condition.secondTerm')
                cmds.setAttr('Stretch_Spine_Condition.operation', 2)
                cmds.connectAttr('Stretch_ratio.outputX', 'Stretch_Spine_Condition.colorIfTrueR')
                cmds.setAttr('Stretch_Spine_Condition.colorIfFalseR', 1)
                
                SpineIK_Temp = ['Spine1', 'Spine11', 'Spine12', 'Spine2', 'Spine21', 'Spine22', 'Spine3', 'Spine31', 'Spine32']
                
                for joint in SpineIK_Temp:
                        cmds.connectAttr('Stretch_Spine_Condition.outColorR', '%s.scaleY' %joint)
                
                cmds.select('Spine1_CTRL_GRP', r = True)
                cmds.select('Root_CTRL', tgl = True)
                cmds.parent()
                
                ######Parenting########
                '''             
                for LR in L_o_R:

                        cmds.select('Spine4', r = True)
                        cmds.select('%sScapula_CTRL_GRP' %LR, tgl = True)
                        cmds.parentConstraint(weight = 1, mo = True)
                        cmds.select('Spine4_Loc', r = True)
                        cmds.select('%sScapula_CTRL_GRP' %LR, tgl = True)
                        cmds.parentConstraint(weight = 1, mo = True)
                        cmds.connectAttr('Root_CTRL.Stretch_Spine', '%sScapula_CTRL_GRP_parentConstraint1.Spine4_LocW1' %LR)
                        cmds.createNode('reverse', n = '%sScapula_Reverse' %LR)
                        cmds.connectAttr('Root_CTRL.Stretch_Spine', '%sScapula_Reverse.inputX' %LR)
                        cmds.connectAttr('%sScapula_Reverse.outputX' %LR, '%sScapula_CTRL_GRP_parentConstraint1.Spine4W0' %LR)                  
                '''
                
                
                cmds.select('NeckBase_CTRL_GRP', r = True)
                cmds.select('Root_CTRL', tgl = True)
                cmds.parent()
                cmds.select('Spine4', r = True)
                cmds.select('NeckBase_CTRL_GRP', tgl = True)
                cmds.parentConstraint(weight = 1, mo = True)
                #cmds.pointConstraint(weight = 1, mo = True)
                #cmds.orientConstraint(weight = 1, mo = True)
                cmds.select('L_Scapula_CTRL_GRP', r = True)
                cmds.select('R_Scapula_CTRL_GRP', add = True)
                cmds.select('Spine4', tgl = True)
                #cmds.select('Root_CTRL', tgl = True)
                cmds.parent()
                #cmds.select('Spine1_CTRL_GRP', r = True)
                #cmds.delete()
                
################Hair##################

        def Hair_Joints(self):
                #######Hair Position###########
                cmds.select(cl = True)
                cmds.spaceLocator( n = 'Hair0_Adjust_CTRL',) #Joint control
                cmds.move(0, 22, -3, r = True)
                cmds.setAttr('Hair0_Adjust_CTRL.tx', lock = True)#CTRL Move
                
                cmds.spaceLocator( n = 'Hair1_Adjust_CTRL',) #Joint control
                cmds.move(0, 22, -8, r = True)
                cmds.setAttr('Hair1_Adjust_CTRL.tx', lock = True)#CTRL Move
                
                cmds.select('Hair1_Adjust_CTRL', r = True)
                cmds.select('Hair0_Adjust_CTRL', tgl = True)
                cmds.parent()
                cmds.setAttr('Hair1_Adjust_CTRL.ty', lock = True)
        
        def Hair_Confirm(self):
                cmds.setAttr('Hair0_Adjust_CTRL.tx', lock = False)
                cmds.setAttr('Hair1_Adjust_CTRL.tx', lock = False)
                cmds.setAttr('Hair1_Adjust_CTRL.ty', lock = False)

                #####Unparent Hair Tip#####
                cmds.select('Hair1_Adjust_CTRL', r = True)
                cmds.parent(w = True)
                                
                ####deciding Hair Joint number########
                Hair0_Pos = cmds.xform('Hair0_Adjust_CTRL', ws = True, q = True, t =True)
                Hair1_Pos = cmds.xform('Hair1_Adjust_CTRL', ws = True, q = True, t =True)
                NO_Hair_Joints = int((Hair0_Pos[2]-Hair1_Pos[2])/(self.rootPos[1]/10))
                Hair_Joint_Space = (Hair1_Pos[2]-Hair0_Pos[2])/NO_Hair_Joints
                
                cmds.select(cl = True)
                ####Create Joints#######
                space_Temp = 0
                for i in range(NO_Hair_Joints+1):
                        cmds.joint(n = 'Hair%s' %i, p =(Hair0_Pos[0], Hair0_Pos[1], Hair0_Pos[2]-space_Temp))
                        space_Temp = space_Temp - Hair_Joint_Space
                        cmds.rotate(0, 90, 0, 'Hair%s.rotateAxis' %i, r = True, os = True) 
                cmds.delete('Hair0_Adjust_CTRL')
                cmds.delete('Hair1_Adjust_CTRL')
                
        
        def FK_Hair_Settup(self):
                cmds.select('Hair0', r = True)
                cmds.duplicate(rr = True)
                cmds.rename('FK_Hair0')
                FK_Hair_Joints_rest = cmds.listRelatives(ad = True)
                FK_Hair_Joints = ['FK_Hair0']
                Length_FK_Hair_Joints = len(FK_Hair_Joints_rest)
                for i in range(Length_FK_Hair_Joints):
                        FK_Hair_Joints.append(FK_Hair_Joints_rest[Length_FK_Hair_Joints-i-1])                   
                
                ########Renaming FK Hair Joints###########
                for i in range(len(FK_Hair_Joints)-1):
                        temp = cmds.listRelatives('%s' %FK_Hair_Joints[i], f = True, c = True)
                        cmds.select('%s' %temp[0])
                        cmds.rename('FK_%s' %FK_Hair_Joints[i+1])
                        temp = cmds.listRelatives('%s' %FK_Hair_Joints[i], c = True)
                        FK_Hair_Joints[i+1] = temp[0]
                
                ########Making Controllers################
                for i in range(len(FK_Hair_Joints)-1):
                        cmds.createNode('transform', n = '%s_CTRL_GRP' %FK_Hair_Joints[i])
                        cmds.circle( n = '%s_CTRL' %FK_Hair_Joints[i], nr=(1, 0, 0), c=(0, 0, 0), r = 1 )
                        cmds.select('%s_CTRL_GRP' %FK_Hair_Joints[i], tgl = True)
                        cmds.parent()
                        cmds.select('%s_CTRL_GRP' %FK_Hair_Joints[i], r = True )
                        Hair_CTRL_Pos = cmds.xform('%s' %FK_Hair_Joints[i], q = True, t = True, ws = True)
                        cmds.move(Hair_CTRL_Pos[0], Hair_CTRL_Pos[1], Hair_CTRL_Pos[2])
                        cmds.select('%s' %FK_Hair_Joints[i], r =True)
                        cmds.select('%s_CTRL_GRP' %FK_Hair_Joints[i], tgl = True )
                        cmds.orientConstraint(weight = True)
                        cmds.delete('%s_CTRL_GRP_orientConstraint1' %FK_Hair_Joints[i])
                        cmds.select('%s_CTRL' %FK_Hair_Joints[i], r = True)
                        cmds.select('%s' %FK_Hair_Joints[i], tgl = True)
                        cmds.orientConstraint(weight = True)
                
                ###########Parenting Controllers#########
                for i in range(len(FK_Hair_Joints)-2):
                        temp = len(FK_Hair_Joints)-2
                        cmds.select('%s_CTRL_GRP' %FK_Hair_Joints[i-temp-1], r = True)
                        cmds.select('%s_CTRL' %FK_Hair_Joints[i-temp-2], tgl = True)
                        cmds.parent()
                
                #for joint in FK_Hair_Joints:
                #       cmds.connectAttr('%s.rotate' %joint, '%s.rotate' %joint[3:])
                
                cmds.createNode('transform', n = 'Hair_Joint_GRP')
                cmds.select('Hair0', r = True)
                cmds.select('Hair_Joint_GRP', tgl = True)
                cmds.parent()
                
                cmds.createNode('transform', n = 'FK_Hair_Joint_GRP')
                cmds.select('FK_Hair0', r = True)
                cmds.select('FK_Hair_Joint_GRP', tgl = True)
                cmds.parent()
                cmds.createNode('transform', n = 'FK_Hair_GRP')
                
                cmds.select('FK_Hair_Joint_GRP', r = True)
                cmds.select('FK_Hair0_CTRL_GRP', add = True)
                cmds.select('FK_Hair_GRP', tgl = True)
                cmds.parent()
                
                cmds.createNode('transform', n = 'Hair_GRP')
                cmds.select('Hair_Joint_GRP', r = True)
                cmds.select('FK_Hair_GRP', add = True)
                cmds.select('Hair_GRP', tgl = True)
                cmds.parent()
                cmds.select('Hair_GRP', r = True)
                cmds.select('Puck', tgl = True)
                cmds.parent()
                
                cmds.select('Head', r = True)
                cmds.select('FK_Hair_GRP', tgl = True)
                cmds.parentConstraint(weight = 1, mo = True)
                
                cmds.select('Head', r = True)
                cmds.select('Hair_Joint_GRP', tgl = True)
                cmds.parentConstraint(weight = 1, mo = True)
                
                cmds.setAttr('FK_Hair0.visibility', 0)
                
        def IK_Hair_Settup(self):
                cmds.select('Hair0', r = True)
                cmds.duplicate(rr = True)
                cmds.parent(w = True)
                cmds.rename('IK_Hair0')
                IK_Hair_Joints_rest = cmds.listRelatives(ad = True)
                IK_Hair_Joints = ['IK_Hair0']
                Length_IK_Hair_Joints = len(IK_Hair_Joints_rest)
                for i in range(Length_IK_Hair_Joints):
                        IK_Hair_Joints.append(IK_Hair_Joints_rest[Length_IK_Hair_Joints-i-1])                   
                
                ########Renaming IK Hair Joints###########
                for i in range(len(IK_Hair_Joints)-1):
                        temp = cmds.listRelatives('%s' %IK_Hair_Joints[i], f = True, c = True)
                        cmds.select('%s' %temp[0])
                        cmds.rename('IK_%s' %IK_Hair_Joints[i+1])
                        temp = cmds.listRelatives('%s' %IK_Hair_Joints[i], c = True)
                        IK_Hair_Joints[i+1] = temp[0]
                
                #####Install IK Handle##########                
                cmds.select('IK_Hair0.rotatePivot', r = True)
                cmds.select('IK_Hair%s.rotatePivot' %str(len(IK_Hair_Joints)-1), add= True)
                cmds.ikHandle(sol = 'ikSplineSolver', n = 'Hair_IK_Handle')
                cmds.rename('curve1', 'Hair_IK_Curve')
                cmds.select('Hair_IK_Curve.cv[0]', r = True)
                cluster0_Pos = cmds.xform('Hair_IK_Curve.cv[0]', q = True, t = True)
                cmds.select('Hair_IK_Curve.cv[1]', r = True)
                cluster1_Pos = cmds.xform('Hair_IK_Curve.cv[1]', q = True, t = True)
                cmds.select('Hair_IK_Curve.cv[2]', r = True)
                cluster2_Pos = cmds.xform('Hair_IK_Curve.cv[2]', q = True, t = True)
                cmds.select('Hair_IK_Curve.cv[3]', r = True)
                cluster3_Pos = cmds.xform('Hair_IK_Curve.cv[3]', q = True, t = True)
                
                ##########Hair IK CTRLs########
                for i in range(4):
                        cmds.createNode('transform', n = 'IK_Hair%s_CTRL_GRP' %i)
                        cmds.circle( n = 'IK_Hair%s_CTRL' %i, nr=(0, 0, 1), c=(0, 0, 0), r = 1 )
                        cmds.select('IK_Hair%s_CTRL_GRP' %i, tgl = True)
                        cmds.parent()
                        cmds.select('IK_Hair%s_CTRL_GRP' %i, r = True )
                        if i == 0:
                                cmds.move(cluster0_Pos[0], cluster0_Pos[1], cluster0_Pos[2])    
                        elif i == 1:
                                cmds.move(cluster1_Pos[0], cluster1_Pos[1], cluster1_Pos[2])    
                        elif i == 2:
                                cmds.move(cluster2_Pos[0], cluster2_Pos[1], cluster2_Pos[2])    
                        elif i == 3:
                                cmds.move(cluster3_Pos[0], cluster3_Pos[1], cluster3_Pos[2])    
                        cmds.select('Hair_IK_Curve.cv[%i]' %i, r = True)                        
                        cmds.cluster(n = 'Hair_Cluster%s' %i)
                        cmds.select('IK_Hair%s_CTRL' %i, tgl = True)
                        cmds.parent()
                        cmds.setAttr('Hair_Cluster%sHandle.visibility' %i, 0)
                
                #########parenting##########
                #cmds.select('Hair_IK_Curve.cv[0]', r = True)
                #cmds.cluster(n = 'Hair_Cluster0')
                #cmds.select('IK_Hair0_CTRL_GRP', tgl = True)
                #cmds.parent()
                cmds.select('IK_Hair0_CTRL_GRP', r = True)
                cmds.select('Head_CTRL', tgl = True)
                cmds.parent()
                
                cmds.createNode('transform', n = 'IK_Hair_Joint_GRP')
                cmds.select('IK_Hair0', r = True)
                cmds.select('IK_Hair_Joint_GRP', tgl = True)
                cmds.parent()
                cmds.createNode('transform', n = 'IK_Hair_GRP')
                cmds.select('Hair_IK_Handle', r = True)
                cmds.select('IK_Hair_Joint_GRP', add = True)
                cmds.select('IK_Hair_GRP', tgl = True)
                cmds.parent()
                cmds.select('IK_Hair_GRP', r = True)
                cmds.select('Puck', tgl = True)
                cmds.parent()

                

                cmds.createNode('transform', n = 'IK_Hair3_CTRL_Pivot0_GRP')
                cmds.move(cluster0_Pos[0], cluster0_Pos[1], cluster0_Pos[2])
                cmds.createNode('transform', n = 'IK_Hair3_CTRL_Pivot1_GRP')
                cmds.move(cluster1_Pos[0], cluster1_Pos[1], cluster1_Pos[2])
                cmds.createNode('transform', n = 'IK_Hair3_CTRL_Pivot2_GRP')
                cmds.move(cluster2_Pos[0], cluster2_Pos[1], cluster2_Pos[2])
                cmds.select('IK_Hair3_CTRL_Pivot2_GRP', r= True)
                cmds.select('IK_Hair3_CTRL_Pivot1_GRP', tgl= True)
                cmds.parent()
                cmds.select('IK_Hair3_CTRL_Pivot1_GRP', r= True)
                cmds.select('IK_Hair3_CTRL_Pivot0_GRP', tgl= True)
                cmds.parent()
                cmds.select('IK_Hair3_CTRL_GRP', r = True)
                cmds.select('IK_Hair3_CTRL_Pivot1_GRP', tgl= True)
                cmds.parent()
                
                
                cmds.createNode('transform', n = 'IK_Hair2_CTRL_Pivot0_GRP')
                cmds.move(cluster0_Pos[0], cluster0_Pos[1], cluster0_Pos[2])
                cmds.createNode('transform', n = 'IK_Hair2_CTRL_Pivot1_GRP')
                cmds.move(cluster1_Pos[0], cluster1_Pos[1], cluster1_Pos[2])
                cmds.select('IK_Hair2_CTRL_Pivot1_GRP', r= True)
                cmds.select('IK_Hair2_CTRL_Pivot0_GRP', tgl= True)
                cmds.parent()
                cmds.select('IK_Hair2_CTRL_GRP', r = True)
                cmds.select('IK_Hair2_CTRL_Pivot1_GRP', tgl= True)
                cmds.parent()
                
                cmds.createNode('transform', n = 'IK_Hair1_CTRL_Pivot0_GRP')
                cmds.move(cluster0_Pos[0], cluster0_Pos[1], cluster0_Pos[2])
                cmds.select('IK_Hair1_CTRL_GRP', r = True)
                cmds.select('IK_Hair1_CTRL_Pivot0_GRP', tgl = True)
                cmds.parent()
                                
                cmds.select('IK_Hair2_CTRL', r = True)
                cmds.select('IK_Hair3_CTRL_Pivot1_GRP', tgl = True)
                cmds.orientConstraint(mo = True, weight = True)

                cmds.select('IK_Hair1_CTRL', r = True)
                cmds.select('IK_Hair2_CTRL_Pivot1_GRP', tgl = True)
                cmds.orientConstraint(mo = True, weight = True)
                
                cmds.select('IK_Hair1_CTRL', r = True)
                cmds.select('IK_Hair3_CTRL_Pivot1_GRP', tgl = True)
                cmds.orientConstraint(mo = True, weight = True)
                
                cmds.select('IK_Hair0_CTRL', r = True)
                cmds.select('IK_Hair1_CTRL_Pivot0_GRP', tgl = True)
                cmds.orientConstraint(mo = True, weight = True)
                
                cmds.select('IK_Hair0_CTRL', r = True)
                cmds.select('IK_Hair2_CTRL_Pivot0_GRP', tgl = True)
                cmds.orientConstraint(mo = True, weight = True)
                
                cmds.select('IK_Hair0_CTRL', r = True)
                cmds.select('IK_Hair3_CTRL_Pivot0_GRP', tgl = True)
                cmds.orientConstraint(mo = True, weight = True)         
        
                cmds.createNode('transform', n = 'IK_Hair_CTRL_GRP')
                cmds.select('IK_Hair1_CTRL_Pivot0_GRP', r = True)
                cmds.select('IK_Hair2_CTRL_Pivot0_GRP', add = True)
                cmds.select('IK_Hair3_CTRL_Pivot0_GRP', add = True)
                #cmds.select('Hair_IK_Curve', add = True)
                cmds.select('IK_Hair_CTRL_GRP', tgl = True)
                cmds.parent()
                cmds.select('IK_Hair_CTRL_GRP', r = True)
                cmds.select('Puck', tgl = True)
                cmds.parent()
                
                cmds.setAttr('IK_Hair_GRP.visibility', 0)
                cmds.setAttr('Hair_IK_Curve.visibility', 0)
        
######### Stretch #######       
                cmds.addAttr('Head_CTRL', ln = 'Stretch_Hair',  at = 'long', min = 0, max = 1)
                cmds.setAttr('Head_CTRL.Stretch_Hair', e = True, keyable = True)
                
                ####distance locator####
                cmds.spaceLocator(n = 'Hair0_Loc')
                cmds.move(cluster0_Pos[0], cluster0_Pos[1], cluster0_Pos[2])
                cmds.select('Hair0', r = True)
                cmds.select('Hair0_Loc', tgl = True)
                cmds.pointConstraint(offset = [0, 0, 0], weight = 1)
                cmds.spaceLocator(n = 'Hair1_Loc')
                cmds.move(cluster3_Pos[0], cluster3_Pos[1], cluster3_Pos[2])
                cmds.select('IK_Hair3_CTRL', r = True)
                cmds.select('Hair1_Loc', tgl = True)
                cmds.pointConstraint(offset = [0, 0, 0], weight = 1)
                
                cmds.createNode('transform', n = 'Stretch_Hair_Loc_GRP')
                cmds.select('Hair0_Loc', r = True)
                cmds.select('Hair1_Loc', add = True)
                cmds.select('Stretch_Hair_Loc_GRP', tgl = True)
                cmds.parent()
                
                cmds.select('Stretch_Hair_Loc_GRP', r = True)
                cmds.select('Puck', tgl = True)
                cmds.parent()
                
                
                Hair_Length = cmds.arclen('Hair_IK_Curve')
                print Hair_Length
                
                #######Loc Distance#####
                cmds.shadingNode('distanceBetween', n = 'Hair_Loc_Distance', asUtility = True)
                cmds.connectAttr('Hair0_Loc.translate', 'Hair_Loc_Distance.point1')
                cmds.connectAttr('Hair1_Loc.translate', 'Hair_Loc_Distance.point2')
                        
                
                #######multiplied spine length#########
                cmds.shadingNode('multiplyDivide', n = 'Hair_Length', asUtility = True)
                cmds.connectAttr('Puck.scaleX', 'Hair_Length.input1X')
                cmds.connectAttr('Puck.scaleX', 'Hair_Length.input1Y')
                cmds.connectAttr('Hair_Loc_Distance.distance', 'Hair_Length.input2Y')
                cmds.setAttr('Hair_Length.input2X', Hair_Length)
                                
                
                #####Stretch Ratio###########
                cmds.shadingNode('multiplyDivide', n = 'Hair_Stretch_ratio', asUtility = True)
                cmds.setAttr('Hair_Stretch_ratio.operation', 2)
                cmds.connectAttr('Hair_Length.outputX', 'Hair_Stretch_ratio.input2X')
                cmds.connectAttr('Hair_Length.outputY', 'Hair_Stretch_ratio.input1X')
                
                cmds.shadingNode('blendColors', n = 'Hair_Stretch_Mux', asUtility = True)
                cmds.connectAttr('Head_CTRL.Stretch_Hair', 'Hair_Stretch_Mux.blender')
                cmds.setAttr('Hair_Stretch_Mux.color2R', 1)
                cmds.connectAttr('Hair_Length.outputY', 'Hair_Stretch_Mux.color1R')
                
                ######condidition#############
                cmds.shadingNode('condition', n = 'Stretch_Hair_Condition', asUtility = True)
                cmds.connectAttr('Hair_Stretch_Mux.outputR', 'Stretch_Hair_Condition.firstTerm')
                cmds.connectAttr('Hair_Length.outputX', 'Stretch_Hair_Condition.secondTerm')
                cmds.setAttr('Stretch_Hair_Condition.operation', 2)
                cmds.connectAttr('Hair_Stretch_ratio.outputX', 'Stretch_Hair_Condition.colorIfTrueR')
                cmds.setAttr('Stretch_Hair_Condition.colorIfFalseR', 1)
                
                
                for joint in IK_Hair_Joints:
                        joint = joint[3:]
                        cmds.connectAttr('Stretch_Hair_Condition.outColorR', '%s.scaleZ' %joint)
                
        
        def FKIK_Hair_Settup(self):
                Hairs = cmds.listRelatives('Hair_Joint_GRP', ad = True)
                Hairs = Hairs[0:-1]
                print Hairs
                
                cmds.select('Head_CTRL', r = True)
                cmds.addAttr(ln = 'Hair', at = 'long', min = 0, max = 1)
                cmds.setAttr('Head_CTRL.Hair', e = True, keyable = True)
                
                ###########Head Attr => IK Hair CTRL visibility
                cmds.connectAttr('Head_CTRL.Hair', 'IK_Hair0_CTRL.visibility')
                cmds.connectAttr('Head_CTRL.Hair', 'IK_Hair1_CTRL.visibility')
                cmds.connectAttr('Head_CTRL.Hair', 'IK_Hair2_CTRL.visibility')
                cmds.connectAttr('Head_CTRL.Hair', 'IK_Hair3_CTRL.visibility')
                
                cmds.createNode('reverse', n = 'FKIK_Hair_Inverter')
                cmds.connectAttr('Head_CTRL.Hair', 'FKIK_Hair_Inverter.inputX')
                cmds.connectAttr('FKIK_Hair_Inverter.outputX', 'FK_Hair0_CTRL.visibility')
                
                ##########Hair Last Mux############
                for Hair in Hairs:
                        cmds.shadingNode('blendColors', n = '%s_Mux' %Hair, asUtility = True)
                        cmds.connectAttr('Head_CTRL.Hair', '%s_Mux.blender' %Hair, f = True)
                        cmds.connectAttr('IK_%s.rotateX' %Hair, '%s_Mux.color1R' %Hair, f = True)
                        cmds.connectAttr('IK_%s.rotateY' %Hair, '%s_Mux.color1G' %Hair, f = True)
                        cmds.connectAttr('IK_%s.rotateZ' %Hair, '%s_Mux.color1B' %Hair, f = True)
                        cmds.connectAttr('FK_%s.rotateX' %Hair, '%s_Mux.color2R' %Hair, f = True)
                        cmds.connectAttr('FK_%s.rotateY' %Hair, '%s_Mux.color2G' %Hair, f = True)
                        cmds.connectAttr('FK_%s.rotateZ' %Hair, '%s_Mux.color2B' %Hair, f = True)

                        cmds.connectAttr('%s_Mux.outputR' %Hair, '%s.rotateX' %Hair, f = True)
                        cmds.connectAttr('%s_Mux.outputG' %Hair, '%s.rotateY' %Hair, f = True)
                        cmds.connectAttr('%s_Mux.outputB' %Hair, '%s.rotateZ' %Hair, f = True)                  