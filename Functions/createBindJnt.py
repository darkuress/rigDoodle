jnts = ['head_jnt', 'jaw_jnt', 
'l_bendy_elbow_bendy1_jnt', 'l_bendy_elbow_bendy2_jnt', 'l_bendy_elbow_bendy3_jnt', 'l_bendy_elbow_bendy4_jnt', 'l_bendy_elbow_bendy5_jnt', 'l_bendy_elbow_jnt', 'l_wrist_jnt', 
'l_bendy_shoulder_jnt', 'l_bendy_shoulder_bendy1_jnt', 'l_bendy_shoulder_bendy2_jnt', 'l_bendy_shoulder_bendy3_jnt', 'l_bendy_shoulder_bendy4_jnt', 'l_bendy_shoulder_bendy5_jnt', 
'l_clavicle_jnt', 
'l_hip_jnt', 'l_knee_jnt', 'l_ankle_jnt', 'l_toe_jnt', 'l_ball_jnt', 
'l_index1_jnt', 'l_index2_jnt', 'l_index3_jnt', 'l_index4_jnt', 'l_index5_jnt', 
'l_middle1_jnt', 'l_middle2_jnt', 'l_middle3_jnt', 'l_middle4_jnt', 'l_middle5_jnt', 
'l_palm_jnt', 
'l_pinky1_jnt', 'l_pinky2_jnt', 'l_pinky3_jnt', 'l_pinky4_jnt', 'l_pinky5_jnt', 
'l_ring1_jnt', 'l_ring2_jnt', 'l_ring3_jnt', 'l_ring4_jnt', 'l_ring5_jnt', 
'l_thumb1_jnt', 'l_thumb2_jnt', 'l_thumb3_jnt', 'l_thumb4_jnt', 
'neck1_jnt', 'neckbase_jnt', 'pelvis_jnt', 
'r_bendy_elbow_bendy1_jnt', 'r_bendy_elbow_bendy2_jnt', 'r_bendy_elbow_bendy3_jnt', 'r_bendy_elbow_bendy4_jnt', 'r_bendy_elbow_bendy5_jnt', 'r_bendy_elbow_jnt', 'r_wrist_jnt', 
'r_bendy_shoulder_jnt', 'r_bendy_shoulder_bendy1_jnt', 'r_bendy_shoulder_bendy2_jnt', 'r_bendy_shoulder_bendy3_jnt', 'r_bendy_shoulder_bendy4_jnt', 'r_bendy_shoulder_bendy5_jnt', 
'r_clavicle_jnt', 
'r_hip_jnt', 'r_knee_jnt', 'r_ankle_jnt', 'r_toe_jnt', 'r_ball_jnt', 
'r_index1_jnt', 'r_index2_jnt', 'r_index3_jnt', 'r_index4_jnt', 'r_index5_jnt', 
'r_middle1_jnt', 'r_middle2_jnt', 'r_middle3_jnt', 'r_middle4_jnt', 'r_middle5_jnt', 
'r_palm_jnt', 
'r_pinky1_jnt', 'r_pinky2_jnt', 'r_pinky3_jnt', 'r_pinky4_jnt', 'r_pinky5_jnt', 
'r_ring1_jnt', 'r_ring2_jnt', 'r_ring3_jnt', 'r_ring4_jnt', 'r_ring5_jnt', 
'r_thumb1_jnt', 'r_thumb2_jnt', 'r_thumb3_jnt', 'r_thumb4_jnt', 
'spine1_jnt', 'spine2_jnt', 'spine3_jnt', 'spine4_jnt']

cmds.select(cl = True)
for jnt in jnts:
    bndJnt = cmds.joint(n = jnt.replace('_jnt', '_bnd_jnt'))
    cmds.select(cl = True)
    cmds.parentConstraint(jnt, bndJnt, mo = False)

bindJntGrp = cmds.createNode('transform', n = 'bind_jnt_grp')
cmds.parent(cmds.ls('*bnd_jnt'), bindJntGrp)
cmds.parent(bindJntGrp, 'joints')
cmds.setAttr('root_jnt_grp.v', 0)
cmds.setAttr('hand_jnt_grp.v', 0)