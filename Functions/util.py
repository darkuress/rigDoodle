import maya.cmds as cmds

class Util(object):
    def __init__(self):
        pass
        
    def mirrorJoints(self, topJoint):
        """
        mirroring joint, top node needs to contain 'l_' as prefix
        """
        
        cmds.select(cl = True)
        cmds.joint(n = 'temp_jnt')
        cmds.select(topJoint, r = True)
        cmds.select('temp_jnt', tgl = True)
        self.toggleSelect(topJoint, 'temp_jnt')
        cmds.parent()
        
        cmds.select(topJoint, r = True)
        cmds.mirrorJoint(mirrorYZ = True, mirrorBehavior  = True, searchReplace =  ['l_', 'r_'])
        
        rJoint = 'r_' + topJoint.split('l_')[-1]
        cmds.select(topJoint, rJoint)
        cmds.parent(w = True)
        
        cmds.delete('temp_jnt')    
        
    def group(self, children = [], parent = ''):
        """
        create parent node and parent children under it
        """
        cmds.createNode('transform', n = parent)
        self.toggleSelect(children, parent)
        cmds.parent()
        
    def parent(self, children = [], parent = ''):
        """
        parent children to parent
        """
        cmds.select(children, r = True)
        cmds.select(parent, tgl = True)
        cmds.parent()
        
    def match(self, dest = '', source = ''):
        """
        dest = thing to match
        run orient, point constraint to match tr and orientation
        """
        self.toggleSelect(source, dest)
        orc = cmds.orientConstraint(mo = False, weight = 1)
        self.toggleSelect(source, dest)
        ptc = cmds.pointConstraint(mo = False, weight = 1)
        
        cmds.delete(orc)
        cmds.delete(ptc)
    
    def toggleSelect(self, r = '', tgl = ''):
        """
        toggle select two object
        """
        cmds.select(r, r = True)
        cmds.select(tgl, tgl = True)
        