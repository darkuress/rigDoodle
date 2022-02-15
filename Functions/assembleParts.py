import util
import partDict
import maya.cmds as cmds

reload(util)

class AssemblelParts(object):
    def __init__(self):
        """
        it assemble parts
        """
        self.util = util.Util()
    
    def rootAssembly(self):
        """
        assemble global to root
        """
        self.util.parent('root_ctl_grp', 'controller')
        self.util.parent('root_jnt_grp', 'joints')
    
    def spineAssembly(self):
        """
        assemble spine to root
        """
        
        self.util.parent('spine1_ctl_grp', 'root_ctl')
        self.util.parent('spine_jnt_grp', 'root_jnt')
        
    def armAssembly(self):
        """
        assemble arm to spine
        """
        
        self.util.parent('arm_ctl_grp', 'spine3_ctl')
        self.util.parent('arm_jnt_grp', 'spine3_jnt')
        self.util.parent('arm_misc_grp', 'misc')

    def legAssembly(self):
        """
        assemble leg to pelvis
        """
        
        self.util.parent('leg_jnt_grp', 'pelvis_jnt')
        self.util.parent('leg_ctl_grp', 'controller')
        self.util.parent('leg_misc_grp', 'misc')

    def headAssembly(self):
        """
        assemble head to spine
        """
        self.util.parent('neckbase_jnt_grp', 'spine4_jnt')
        self.util.parent('neckbase_ctl_grp', 'spine4_ctl')
        
    def handAssembly(self):
        """
        assemble hand to arm
        """
        for lr in partDict.lrPrefix:
            self.util.match('%shandCon_loc' %lr, '%spalm_jnt' %lr)
            
            #self.util.toggleSelect('%shandCon_loc' %lr, '%spalm_jnt_grp' %lr)
            #cmds.pointConstraint(mo = False, weight = 1)
            #self.util.toggleSelect('%shandCon_loc' %lr, '%spalm_jnt_grp' %lr)
            #cmds.orientConstraint(mo = False, weight = 1)
            
            self.util.toggleSelect('%swrist_jnt' %lr, '%spalm_jnt_grp' %lr)
            cmds.parentConstraint(mo = True, weight = 1)
            
        self.util.parent('hand_misc_grp', 'misc')
        self.util.parent('hand_jnt_grp', 'joints')
        self.util.parent('hand_ctl_grp', 'controller')
