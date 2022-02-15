import maya.cmds as cmds
import maya.mel as mm

def getJoints():
	global jointChain
	joint = cmds.ls(sl = True)

	try:
		jointChain = cmds.listRelatives(joint, ad = True)
		jointChain.append(joint[0])
		jointChain.reverse()
		print jointChain
		
	except:
		cmds.confirmDialog( title='Confirm', message='Select Joint')

def makeHairCurve():
	#######getting Joint Position##########
	jointPosition = []
	for jnt in jointChain:
		pos = cmds.xform(jnt, q = True, t = True, ws = True)
		jointPosition.append(pos)
	print jointPosition
	
	######Making curve##########
	cmds.curve(n = 'Dynamic_Handle', p = jointPosition, d = 1)
	cmds.select('Dynamic_Handle', r = True)
	
	######Dynamic#########
	cmd = '''makeCurvesDynamicHairs 1 0 1;'''
	mm.eval(cmd)
	cmds.rename('curve33', 'Dynamic_Curve')

	#######Spline IK########
	cmds.select(cl = True)
	for i in range(len(jointPosition)):
		cmds.joint( n = '%s_bind_JNT' %jointChain[i], p = jointPosition[i])
	cmds.select('%s_bind_JNT' %jointChain[0], r = True)
	cmds.joint(e = True, oj = 'xzy', secondaryAxisOrient = 'xup', ch = True, zso = True)

	cmds.select('%s_bind_JNT.rotatePivot' %jointChain[0], r = True)
	cmds.select('%s_bind_JNT.rotatePivot' %jointChain[-1], add = True)
	cmds.select('Dynamic_Curve', add = True)
	cmds.ikHandle(n = 'Dynamic_SplineIK', sol = 'ikSplineSolver', ccv = False, ns = 2)

	#####Smooth bind curve######
	cmds.select('Dynamic_Handle', r = True)
	cmds.select('%s' %jointChain[0], add = True)
	cmds.bindSkin()

getJoints()
makeHairCurve()