import maya.cmds as cmds

def getPolVectorPos(joint1, joint2, joint3, mul):
#get world translate value
    joint1Trans = cmds.xform(joint1, q = True, t = True, ws = True)
    joint2Trans = cmds.xform(joint2, q = True, t = True, ws = True)
    joint3Trans = cmds.xform(joint3, q = True, t = True, ws = True)
    
    joint12Vec = [joint2Trans[0] - joint1Trans[0], joint2Trans[1] - joint2Trans[1], joint2Trans[2] - joint2Trans[2]]
    joint32Vec = [joint2Trans[0] - joint3Trans[0], joint2Trans[1] - joint3Trans[1], joint2Trans[2] - joint3Trans[2]]
    
    poleVec = [joint12Vec[0] + joint32Vec[0], joint12Vec[1] + joint32Vec[1], joint12Vec[2] + joint32Vec[2]]
    poleVecPos = [joint2Trans[0] + mul * poleVec[0], joint2Trans[1] + mul * poleVec[1], joint2Trans[2] + mul * poleVec[2] ]
    
    return poleVecPos
