def individualStretchArm():
    
    for LR in ['l_', 'r_']:
        lElbowPos = cmds.xform('l_elbow_jnt', q = True, t = True, ws = True)
        lWristPos = cmds.xform('l_wrist_jnt', q = True, t = True, ws = True)
        ########add Attribute########
        cmds.select('%sarm_extra_ctl' %LR)
        cmds.addAttr(ln = 'UpperArmStretch', at = 'double', min = -5, max = 5)
        cmds.setAttr('%sarm_extra_ctl.UpperArmStretch' %LR, e = True, keyable = True)
        cmds.select('%sarm_extra_ctl' %LR)
        cmds.addAttr(ln = 'LowerArmStretch', at = 'double', min = -5, max = 5)
        cmds.setAttr('%sarm_extra_ctl.LowerArmStretch' %LR, e = True, keyable = True)
        
        ######Elbow Stretch Loc#######
        cmds.createNode('transform', n = '%selbow_jnt_stretch_loc_grp' %LR)
        cmds.spaceLocator(n = '%selbow_jnt_stretch_loc' %LR)
        cmds.select('%selbow_jnt_stretch_loc_grp' %LR, tgl = True)
        cmds.parent()
        cmds.select('%selbow_jnt_stretch_loc_grp' %LR, r = True)
        if LR == 'L_':
            cmds.move(lElbowPos[0], lElbowPos[1], lElbowPos[2])
        else:	
            cmds.move(-lElbowPos[0], lElbowPos[1], lElbowPos[2])
        cmds.select('%sshoulder_jnt' %LR, r = True)
        cmds.select('%selbow_jnt_stretch_loc_grp' %LR, tgl = True)
        cmds.orientConstraint(weight = 1)
        cmds.delete('%selbow_jnt_stretch_loc_grp_orientConstraint1' %LR)
        #if LR == 'R_':
        #	cmds.rotate(0, 180, 0, '%selbow_jnt_stretch_loc_grp' %LR)
        #	cmds.setAttr('%selbow_jnt_stretch_loc_grp.rotateY' %LR, 0)
        cmds.select('%selbow_jnt_stretch_loc_grp' %LR, r = True)
        cmds.select('%sshoulder_jnt' %LR, tgl = True)
        cmds.parent()
        
        
        ######Wrist Stretch Loc#######
        cmds.createNode('transform', n = '%swrist_stretch_loc1_grp' %LR)
        cmds.spaceLocator(n = '%swrist_jnt_stretch_loc1' %LR)
        cmds.select('%swrist_stretch_loc1_grp' %LR, tgl = True)
        cmds.parent()
        cmds.select('%swrist_stretch_loc1_grp' %LR, r = True)			
        if LR == 'l_':
            cmds.move(lWristPos[0], lWristPos[1], lWristPos[2])
        else:	
            cmds.move(-lWristPos[0], lWristPos[1], lWristPos[2])			
        cmds.select('%selbow_jnt' %LR, r = True)
        cmds.select('%swrist_stretch_loc1_grp' %LR, tgl = True)
        cmds.orientConstraint(weight = 1)
        cmds.delete('%swrist_stretch_loc1_grp_orientConstraint1' %LR)
        cmds.select('%swrist_stretch_loc1_grp' %LR, r = True)
        cmds.select('%selbow_jnt' %LR, tgl = True)
        cmds.parent()
        
        ###########Connect Attr translate Stretch###########
        '''cmds.select('%selbow_jnt_stretch_loc' %LR, r = True)
        cmds.select('%selbow_jnt' %LR, tgl = True)
        cmds.pointConstraint(mo = True, weight = 1)
        cmds.connectAttr('%selbow_jnt.translateX' %LR, '%sFK_Elbow.translateX' %LR)
        cmds.connectAttr('%selbow_jnt.translateX' %LR, '%sIK_Elbow.translateX' %LR)	
        cmds.select('%selbow_jnt_stretch_loc' %LR, r = True)
        cmds.select('%sfk_elbow_ctl' %LR, tgl = True)
        cmds.pointConstraint(mo = True, weight = 1)'''
        
        cmds.select('%swrist_jnt_stretch_loc1' %LR, r = True)
        cmds.select('%swrist_jnt' %LR, tgl = True)
        cmds.pointConstraint(mo = True, weight = 1)
        cmds.connectAttr('%swrist_jnt.translateX' %LR, '%sfk_wrist_jnt.translateX' %LR)
        cmds.connectAttr('%swrist_jnt.translateX' %LR, '%sik_wrist_jnt.translateX' %LR)	
        cmds.select('%swrist_jnt_stretch_loc1' %LR, r = True)
        cmds.select('%swrist_jnt_FK_CTRL' %LR, tgl = True)
        cmds.pointConstraint(mo = True, weight = 1)
        #cmds.select('%swrist_jnt' %LR, r = True)
        #cmds.select('%sarm_ik_ctl_grp' %LR, tgl = True)
        #cmds.pointConstraint(mo = True, weight = 1)a
individualStretchArm()        