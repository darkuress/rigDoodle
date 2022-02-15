import baseSetup
import armSetup
import legSetup
import spineSetup
import headSetup
import rootSetup
import assembleParts
import handSetup

reload(baseSetup)
reload(armSetup)
reload(legSetup)
reload(spineSetup)
reload(headSetup)
reload(rootSetup)
reload(assembleParts)
reload(handSetup)

class MainBuild(object):
    def __init__(self, isArm = True, isLeg = True, isHead = True, isSpine = True, isHand = True):
        """
        initialize parameters
        """
        self.isArm = isArm
        self.isLeg = isLeg
        self.isHead = isHead
        self.isSpine = isSpine
        self.isHand = isHand
        
        self.baseSetup = baseSetup.BaseSetup()
        self.rootSetup = rootSetup.RootSetup()
        
        if self.isArm:
            self.armSetup = armSetup.ArmSetup()
        if self.isLeg:
            self.legSetup = legSetup.LegSetup()
        if self.isHead:
            self.headSetup = headSetup.HeadSetup()
        if self.isSpine:
            self.spineSetup = spineSetup.SpineSetup()
        if self.isHand:
            self.handSetup = handSetup.HandSetup(isThumb = True, numFingers = 4)
            
        self.assembleParts = assembleParts.AssemblelParts()

    def setupBase(self):
        """
        setting up basic containers
        """
        self.baseSetup.createMainCtl()
        self.baseSetup.createContainers()
    
    def createLocators(self):
        """
        setting up locators
        """
        
        self.rootSetup.createLocator()
        if self.isSpine:
            self.spineSetup.createLocator()
        if self.isArm:
            self.armSetup.createLocator()
        if self.isLeg:
            self.legSetup.createLocator()
        if self.isHead:
            self.headSetup.createLocator()   
        if self.isHand:
            self.handSetup.createLocator()   
        
    def confirmJoints(self):
        """
        confim joints, mirror as well
        """
        self.rootSetup.confirmJoints()
        if self.isSpine:
            self.spineSetup.confirmJoints()
        if self.isArm:
            self.armSetup.confirmJoints()
            self.armSetup.mirrorJoints()
        if self.isLeg:
            self.legSetup.confirmJoints()
            self.legSetup.mirrorJoints()
        if self.isHead:
            self.headSetup.confirmJoints()
        if self.isHand:
            self.handSetup.confirmJoints()
            self.handSetup.mirrorJoints()
            
    def setupParts(self):
        """
        setting up each parts
        """
        self.rootSetup.rootSetup()
        self.rootSetup.rootCleanup()
        
        if self.isSpine:
            self.spineSetup.fkSpineSetup()
            self.spineSetup.spineCleanup()
        
        if self.isArm:
            self.armSetup.fkArmSetup()
            self.armSetup.ikArmSetup()
            self.armSetup.fkikCombine()
            self.armSetup.stretchIkArm()
            self.armSetup.bendyArmSetup()
            self.armSetup.armCleanup()
            
        if self.isLeg:
            self.legSetup.ikLegSetup()
            self.legSetup.fkLegSetup()
            self.legSetup.stretchIkLeg()
            self.legSetup.legCleanup()
        
        if self.isHead:
            self.headSetup.fkHeadSetup()
            self.headSetup.headCleanup()
        
        if self.isHand:
            self.handSetup.fkFingerSetup()
            self.handSetup.fingerCleanup()
    
        self.rootSetup.deleteAllCtl()
        
    def partAssembly(self):
        """
        assemble parts so that the rig becomes one
        """

        self.assembleParts.rootAssembly()
        if self.isSpine:
            self.assembleParts.spineAssembly()
        if self.isArm:
            self.assembleParts.armAssembly()
        if self.isLeg:
            self.assembleParts.legAssembly()
        if self.isHead:
            self.assembleParts.headAssembly()
        if self.isHand:
            self.assembleParts.handAssembly()