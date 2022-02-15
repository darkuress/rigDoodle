xx = cmds.ls(sl = True)
jntSet = []
for x in xx:
     jntSet += cmds.listRelatives(x, ad = True, type = 'joint')
     jntSet.append(x)


for jnt in jntSet:    
    cnt = jnt.replace('jnt', 'cnt')
    cmds.circle(n = cnt, nr = [1,0,0])
    cmds.group(n = cnt + '_grp')
    cmds.parentConstraint(jnt, cnt + '_grp')
    constraints = cmds.listRelatives(cnt + '_grp', type = 'parentConstraint')
    cmds.delete(constraints)
    cmds.pointConstraint(cnt, jnt)
    cmds.orientConstraint(cnt, jnt)
    