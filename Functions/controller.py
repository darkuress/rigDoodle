import maya.cmds as cmds
import util
import json
import os
util = util.Util()
##########################
#Class Making controllers#
##########################

#color blue : 6
#      red  : 12
#      yellow : 16

#[tr, ro, sc, vi]
#circleController([tr])  => lock tr

def circleController(name, mode, radius, color = 0, lockAttr = ['sc', 'vi'], doublePadding = False, lock = True):
        if mode == 'xy':
            cmds.circle( n = name, nr=(0, 0, 1), c=(0, 0, 0), r = radius )
        if mode == 'yz':
            cmds.circle( n = name, nr=(1, 0, 0), c=(0, 0, 0), r = radius )
        if mode == 'zx':
            cmds.circle( n = name, nr=(0, 1, 0), c=(0, 0, 0), r = radius )
        
        #lock Attribute
        for attr in lockAttr:
                if attr == 'tr':
                        cmds.setAttr('%s.translateX' %name, lock = lock, keyable = False, channelBox = False)
                        cmds.setAttr('%s.translateY' %name, lock = lock, keyable = False, channelBox = False)
                        cmds.setAttr('%s.translateZ' %name, lock = lock, keyable = False, channelBox = False)
                elif attr == 'ro':
                        cmds.setAttr('%s.rotateX' %name, lock = lock, keyable = False, channelBox = False)
                        cmds.setAttr('%s.rotateY' %name, lock = lock, keyable = False, channelBox = False)
                        cmds.setAttr('%s.rotateZ' %name, lock = lock, keyable = False, channelBox = False)
                elif attr == 'sc':
                        cmds.setAttr('%s.scaleX' %name, lock = lock, keyable = False, channelBox = False)
                        cmds.setAttr('%s.scaleY' %name, lock = lock, keyable = False, channelBox = False)
                        cmds.setAttr('%s.scaleZ' %name, lock = lock, keyable = False, channelBox = False)
                elif attr == 'vi':
                        cmds.setAttr('%s.visibility' %name, lock = lock, keyable = False, channelBox = False)
        
        #adding color
        cmds.setAttr(name + 'Shape.overrideEnabled', 1)
        cmds.setAttr(name + 'Shape.overrideColor', color)

        if doublePadding:
            cmds.createNode('transform', n = '%s_ofs' %name)
            cmds.createNode('transform', n = '%s_grp' %name)
            cmds.select(name, r = True)
            cmds.select('%s_ofs' %name, tgl = True)
            cmds.parent()
            cmds.select('%s_ofs' %name, r = True)
            cmds.select('%s_grp' %name, tgl = True)
            cmds.parent()        
        else:
            cmds.createNode('transform', n = '%s_grp' %name)
            cmds.select(name, r = True)
            cmds.select('%s_grp' %name, tgl = True)
            cmds.parent()
            
        return name
        
def boxController(name, color = 0, lockAttr = ['sc', 'vi'], lock = True):
        cmds.curve(n = name, d =  1, p =[(-1, 1, 1),(1, 1, 1), (1, -1, 1), (-1, -1, 1), (-1, 1, 1), (-1, 1, -1), (-1, -1, -1), (-1, -1, 1), (1, -1, 1), (1, -1, -1),(-1, -1, -1), (-1, 1, -1), (1, 1, -1), (1, -1, -1), (1, 1, -1), (1, 1, 1) ], k = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15, 16]) 
        cmds.createNode('transform', n = '%s_grp' %name)

        shapeNode = cmds.listRelatives(name)
        cmds.rename(shapeNode, name + 'Shape')

        #lock Attribute
        for attr in lockAttr:
                if attr == 'tr':
                        cmds.setAttr('%s.translateX' %name, lock = lock, keyable = False, channelBox = False)
                        cmds.setAttr('%s.translateY' %name, lock = lock, keyable = False, channelBox = False)
                        cmds.setAttr('%s.translateZ' %name, lock = lock, keyable = False, channelBox = False)
                elif attr == 'ro':
                        cmds.setAttr('%s.rotateX' %name, lock = lock, keyable = False, channelBox = False)
                        cmds.setAttr('%s.rotateY' %name, lock = lock, keyable = False, channelBox = False)
                        cmds.setAttr('%s.rotateZ' %name, lock = lock, keyable = False, channelBox = False)
                elif attr == 'sc':
                        cmds.setAttr('%s.scaleX' %name, lock = lock, keyable = False, channelBox = False)
                        cmds.setAttr('%s.scaleY' %name, lock = lock, keyable = False, channelBox = False)
                        cmds.setAttr('%s.scaleZ' %name, lock = lock, keyable = False, channelBox = False)
                elif attr == 'vi':
                        cmds.setAttr('%s.visibility' %name, lock = lock, keyable = False, channelBox = False)
        
        #color change   
        cmds.setAttr(name + 'Shape.overrideEnabled', 1)
        cmds.setAttr(name + 'Shape.overrideColor', color)       
        cmds.select(name, r = True)
        cmds.select('%s_grp' %name, tgl = True)
        cmds.parent()
        
        return name
        
def arrowController(name, color = 0, lockAttr = ['sc', 'vi'], lock = True):
        cmds.curve(n = name , d =  1, p = [(0, 2, 1),(0, 3, 1),(0, 0, 3), (0, -3, 1), (0, -2, 1), (0, -2, -2), (0, 2, -2), (0, 2, 1), (0, -2, -2), (0, 2, -2), (0, -2, 1)], k = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        cmds.createNode('transform', n = '%s_grp' %name)

        #lock Attribute
        for attr in lockAttr:
                if attr == 'tr':
                        cmds.setAttr('%s.translateX' %name, lock = lock, keyable = False, channelBox = False)
                        cmds.setAttr('%s.translateY' %name, lock = lock, keyable = False, channelBox = False)
                        cmds.setAttr('%s.translateZ' %name, lock = lock, keyable = False, channelBox = False)
                elif attr == 'ro':
                        cmds.setAttr('%s.rotateX' %name, lock = lock, keyable = False, channelBox = False)
                        cmds.setAttr('%s.rotateY' %name, lock = lock, keyable = False, channelBox = False)
                        cmds.setAttr('%s.rotateZ' %name, lock = lock, keyable = False, channelBox = False)
                elif attr == 'sc':
                        cmds.setAttr('%s.scaleX' %name, lock = lock, keyable = False, channelBox = False)
                        cmds.setAttr('%s.scaleY' %name, lock = lock, keyable = False, channelBox = False)
                        cmds.setAttr('%s.scaleZ' %name, lock = lock, keyable = False, channelBox = False)
                elif attr == 'vi':
                        cmds.setAttr('%s.visibility' %name, lock = lock, keyable = False, channelBox = False)
        
        #color change
        shapeNode = cmds.listRelatives(name)
        cmds.rename(shapeNode, name + 'Shape')
        
        cmds.setAttr(name + 'Shape.overrideEnabled', 1)
        cmds.setAttr(name + 'Shape.overrideColor', color)       
        cmds.select(name, r = True)
        cmds.select('%s_grp' %name, tgl = True)
        cmds.parent()
        
        return name
        
def sphereContorller(name, color = 0, lockAttr = ['sc', 'vi'], lock = True):
        cmds.createNode('transform', n = '%s_grp' %name)
        cmds.circle( n = '%s1' %name, nr=(1, 0, 0), c=(0, 0, 0), r = 1 )
        cmds.circle( n = '%s2' %name, nr=(0, 1, 0), c=(0, 0, 0), r = 1 )
        cmds.circle( n = '%s3' %name, nr=(0, 0, 1), c=(0, 0, 0), r = 1 )
        cmds.createNode('transform', n = name)
        
        cmds.select('%s1Shape' %name, r = True)
        cmds.select('%s2Shape' %name, tgl = True)
        cmds.select('%s3Shape' %name, tgl = True)
        cmds.select(name, tgl = True)
        cmds.parent(s = True, r = True)
        cmds.delete('%s1' %name)
        cmds.delete('%s2' %name)
        cmds.delete('%s3' %name)

        #lock Attribute
        for attr in lockAttr:
                if attr == 'tr':
                        cmds.setAttr('%s.translateX' %name, lock = lock, keyable = False, channelBox = False)
                        cmds.setAttr('%s.translateY' %name, lock = lock, keyable = False, channelBox = False)
                        cmds.setAttr('%s.translateZ' %name, lock = lock, keyable = False, channelBox = False)
                elif attr == 'ro':
                        cmds.setAttr('%s.rotateX' %name, lock = lock, keyable = False, channelBox = False)
                        cmds.setAttr('%s.rotateY' %name, lock = lock, keyable = False, channelBox = False)
                        cmds.setAttr('%s.rotateZ' %name, lock = lock, keyable = False, channelBox = False)
                elif attr == 'sc':
                        cmds.setAttr('%s.scaleX' %name, lock = lock, keyable = False, channelBox = False)
                        cmds.setAttr('%s.scaleY' %name, lock = lock, keyable = False, channelBox = False)
                        cmds.setAttr('%s.scaleZ' %name, lock = lock, keyable = False, channelBox = False)
                elif attr == 'vi':
                        cmds.setAttr('%s.visibility' %name, lock = lock, keyable = False, channelBox = False)
        
        
        shapeNode = cmds.listRelatives(name)
        cmds.rename(shapeNode, name + 'Shape')
        cmds.setAttr(name + 'Shape.overrideEnabled', 1)
        cmds.setAttr(name + 'Shape.overrideColor', color)       
        
        cmds.select(name, r = True)
        cmds.select('%s_grp' %name, tgl = True)
        cmds.parent()
        
        return name

def extraController(name, color = 0, lockAttr = ['sc', 'vi'], lock = True):

        cmds.createNode('transform', n =  '%s_grp' %name)
        cmds.curve(n = name, d = 1, p =[(-4, 0, -3),(-1, 0, -3),(-1, 0, -2),(-3, 0, -2),(-3, 0, -1), (-1, 0, -1),(-1, 0, 0),(-3, 0, 0),(-3, 0, 1),(-1, 0, 1),(-1, 0, 2),(-4, 0, 2),(-4, 0, -3),(3, 0, -3),(2, 0, -1),(2, 0, 0),(3, 0, 2),(2, 0, 2),(1, 0, 0),(0, 0, 2),(-1, 0, 2),(0, 0, 0),(0, 0, -1),(-1, 0, -3),(0, 0, -3),(1, 0, -1),(2, 0, -3),(3, 0, -3),(3, 0, 2),(-4, 0, 2)], k= [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29])
        cmds.scale(0.2,0.2,0.2) 
        for attr in lockAttr:
                if attr == 'tr':
                        cmds.setAttr('%s.translateX' %name, lock = lock, keyable = False, channelBox = False)
                        cmds.setAttr('%s.translateY' %name, lock = lock, keyable = False, channelBox = False)
                        cmds.setAttr('%s.translateZ' %name, lock = lock, keyable = False, channelBox = False)
                elif attr == 'ro':
                        cmds.setAttr('%s.rotateX' %name, lock = lock, keyable = False, channelBox = False)
                        cmds.setAttr('%s.rotateY' %name, lock = lock, keyable = False, channelBox = False)
                        cmds.setAttr('%s.rotateZ' %name, lock = lock, keyable = False, channelBox = False)
                elif attr == 'sc':
                        cmds.setAttr('%s.scaleX' %name, lock = lock, keyable = False, channelBox = False)
                        cmds.setAttr('%s.scaleY' %name, lock = lock, keyable = False, channelBox = False)
                        cmds.setAttr('%s.scaleZ' %name, lock = lock, keyable = False, channelBox = False)
                elif attr == 'vi':
                        cmds.setAttr('%s.visibility' %name, lock = lock, keyable = False, channelBox = False)
                
        shapeNode = cmds.listRelatives(name)
                
        cmds.setAttr('%s.overrideEnabled' %shapeNode[0], 1)
        cmds.setAttr('%s.overrideColor' %shapeNode[0], color)
        
        return name

def lollipopController(name, color = 0, size = [1, 1, 1], lockAttr = ['tr', 'ro', 'sc', 'vi'], lock = True):

        #cmds.createNode('transform', n =  '%s_grp' %name)
        cmds.curve(n = name, d = 1, p = [ (0, 0, 0), (0, 3, 0),(0, 4, 1),(0, 5, 0), (0, 4, -1),(0, 3, 0),(0, 4, 1),(0, 4, -1)], k = [1,2,3,4,5,6,7,8])
        cmds.scale(size[0],size[1],size[2]) 
        for attr in lockAttr:
                if attr == 'tr':
                        cmds.setAttr('%s.translateX' %name, lock = lock, keyable = False, channelBox = False)
                        cmds.setAttr('%s.translateY' %name, lock = lock, keyable = False, channelBox = False)
                        cmds.setAttr('%s.translateZ' %name, lock = lock, keyable = False, channelBox = False)
                elif attr == 'ro':
                        cmds.setAttr('%s.rotateX' %name, lock = lock, keyable = False, channelBox = False)
                        cmds.setAttr('%s.rotateY' %name, lock = lock, keyable = False, channelBox = False)
                        cmds.setAttr('%s.rotateZ' %name, lock = lock, keyable = False, channelBox = False)
                elif attr == 'sc':
                        cmds.setAttr('%s.scaleX' %name, lock = lock, keyable = False, channelBox = False)
                        cmds.setAttr('%s.scaleY' %name, lock = lock, keyable = False, channelBox = False)
                        cmds.setAttr('%s.scaleZ' %name, lock = lock, keyable = False, channelBox = False)
                elif attr == 'vi':
                        cmds.setAttr('%s.visibility' %name, lock = True, keyable = False, channelBox = False)
                
        shapeNode = cmds.listRelatives(name)
                
        cmds.setAttr('%s.overrideEnabled' %shapeNode[0], 1)
        cmds.setAttr('%s.overrideColor' %shapeNode[0], color)

        util.group(name, '%s_grp' %name)
        
        return name
        
        
def saveAllCtlInfo(char):
    """
    save out all the controller information
    """
    ctlInfo = {}
    for ctl in cmds.ls('*ctl'):
        ctlInfo[ctl] = []
        ctlCVInfo = {}
        for span in range(int(cmds.getAttr(ctl + '.spans'))):
            ctlCVInfo[ctl + '.cv[%s]' %span] = cmds.xform(ctl + '.cv[%s]' %span, t = True, q = True)
        try:
            ctlCVInfo[ctl + '.cv[%s]' %(span + 1)] = cmds.xform(ctl + '.cv[%s]' %(span + 1), t = True, q = True)
        except:
            pass
        ctlInfo[ctl].append(ctlCVInfo)

    path = os.path.join(char.controllerFolder, "%s_controller.json" %char.name)
    
    print ".... saving at location %s" %path
    
    with open(path, 'w') as outfile:
        json.dump(ctlInfo, outfile)

def loadAllCtlInfo(char):
    """
    read json file and retrieve controller shape
    """
    path = os.path.join(char.controllerFolder, "%s_controller.json" %char.name)
    print path
    with open(path) as datafile:    
        ctlData = json.load(datafile)
    
    for ctl in ctlData.keys():
        for cvInfo in ctlData[ctl]:
            for cv in cvInfo.keys():
                cmds.xform(cv, t = cvInfo[cv])