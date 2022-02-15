def headOrientationSetting():
    
    ########Unparent head joint and CTRL####
    headJnt = 'head_jnt'
    neckBaseJnt = 'neckbase_jnt'
    headPos = cmds.xform(headJnt, q = True, t = True, ws = True)
    neckBasePos = cmds.xform(neckBaseJnt, q = True, t = True, ws = True)
    cmds.select(headJnt, r = True)
    cmds.parent(w = True)
    cmds.select('head_ctl_grp', r = True)
    cmds.parent(w = True)
    cmds.createNode('transform', n = 'head_world_grp')
    cmds.createNode('transform', n = 'head_grp')
    cmds.move(headPos[0], headPos[1], headPos[2])
    
    ########making locator###### and GRP  ######
    cmds.spaceLocator(n = 'head_orientation_neck_loc')#Neck
    cmds.move(headPos[0], headPos[1], headPos[2])
    #cmds.spaceLocator(n = 'head_orientation_root_loc')#Root
    #cmds.move(headPos[0], headPos[1], headPos[2])
    cmds.createNode('transform', n = 'head_neck_orient_grp')
    cmds.move(neckBasePos[0], neckBasePos[1], neckBasePos[2])
    #cmds.createNode('transform', n = 'Head_Root_Orient_GRP')
    #cmds.move(Root_Pos[0], Root_Pos[1], Root_Pos[2])	
    cmds.select('head_orientation_neck_loc', r = True)
    cmds.select('head_neck_orient_grp', tgl = True)
    cmds.parent()
    #cmds.select('Head_Orientation_Loc_Root', r = True)
    #cmds.select('Head_Root_Orient_GRP', tgl = True)
    #cmds.parent()
    ##########Head Attr##########
    cmds.addAttr('head_ctl', ln = 'ss', at = 'double')
    cmds.setAttr('head_ctl.ss', e = True, channelBox = True)
    cmds.addAttr('head_ctl', ln = 'World', at = 'enum', en = 'No:Yes:')
    cmds.setAttr('head_ctl.World', e = True, keyable = True)
    #cmds.addAttr('head_ctl', ln = 'Root', at = 'enum', en ='No:Yes:' )
    #cmds.setAttr('head_ctl.Root', e = True, keyable = True)

    #####Parent with Neck....###
    cmds.select(neckBaseJnt, r = True)
    cmds.select('head_neck_orient_grp', tgl = True)
    cmds.pointConstraint(weight = 1, mo = True)
    cmds.orientConstraint(weight = 1, mo = True)
    
    cmds.select('head_orientation_neck_loc', r = True)
    cmds.select('head_grp', tgl = True)
    cmds.pointConstraint(weight = 1, mo = True)
    cmds.orientConstraint(weight = 1, mo = True)
    
    ####Ctrl Attribute assign###
    cmds.shadingNode('blendColors', n = 'head_world_con', asUtility = True)
    cmds.connectAttr('head_ctl.World', 'head_world_con.blender')
    cmds.setAttr('head_world_con.color1R', 0)
    cmds.setAttr('head_world_con.color2R', 1)
    cmds.connectAttr('head_world_con.outputR', 'head_grp_orientConstraint1.head_orientation_neck_locW0')

    ####Grouping####

    cmds.select(headJnt, r = True)
    cmds.select('head_ctl_grp', add = True)
    cmds.select('head_grp', add = True)
    cmds.parent()
    cmds.select('head_grp', r = True)
    cmds.select('head_neck_orient_grp', add = True)
    cmds.select('head_world_grp', tgl = True)
    cmds.parent()
    cmds.select('head_world_grp', r = True)
    
    cmds.setAttr('head_neck_orient_grp.visibility', 0)
headOrientationSetting()    