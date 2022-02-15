import maya.cmds as cmds 
import os
import json

class LocatorSetup(object):
    """
    This class will create locators for joint placement
    part needs to be
    {'name' : ['translate', 'scale', 'lock attr info']}
    """
    
    def __init__(self):
        self.adjustCtrls = []
        
    def createLocator(self, part):
        self.placeLocs = part
        
        for oneLoc in self.placeLocs.keys():
            cmds.spaceLocator( n = oneLoc) #Joint control
            cmds.move(self.placeLocs[oneLoc][0][0], self.placeLocs[oneLoc][0][1], self.placeLocs[oneLoc][0][2], r = True)
            cmds.scale(self.placeLocs[oneLoc][1], self.placeLocs[oneLoc][1], self.placeLocs[oneLoc][1]) 
            if self.placeLocs[oneLoc][2]: 
                cmds.setAttr(oneLoc + '.' + self.placeLocs[oneLoc][2] , lock = True)#CTRL Move
            
            self.adjustCtrls.append(oneLoc)
            
        return self.placeLocs.keys()

    def installAllAdjustCtl(self):
        """
        create top node for scaling
        """
        allCtls = [cmds.listRelatives(x, p = True)[0] for x in cmds.ls(type = 'locator')]
        topCtl = cmds.createNode('transform', n = 'all_ctl')
        cmds.parent(allCtls, topCtl)    
        cmds.select(cl = True)

    def saveLocatorPos(self, char):
        """
        save locator pos as json file
        
        @param char chracter instance
        """
        path = os.path.join(char.locatorFolder, "%s_locators.json" %char.name)
        
        posDict = {}
        
        posDict['all_ctl'] = cmds.xform('all_ctl', s = True, q = True)
        for loc in cmds.ls("*djust_ctl") + ['l_heel_PivotPosition', 'l_sidein_PivotPosition', 'l_sideout_PivotPosition']:
            posDict[loc] = cmds.xform(loc, t = True, q = True)
        
        with open(path, 'w') as outfile:
            json.dump(posDict, outfile)
            
        print "...saving locator json file %s" %path

    def loadLocatorPos(self, char):
        """
        load locators from json file
        
        @param char chracter instance
        """
        path = os.path.join(char.locatorFolder, "%s_locators.json" %char.name)
        
        with open(path) as datafile:    
            locData = json.load(datafile)
        
        for loc in locData.keys():
            if loc == 'all_ctl':
                cmds.xform(loc, s = locData[loc])
            else:
                cmds.xform(loc, t = locData[loc])
