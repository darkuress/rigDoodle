import os
import maya.cmds as cmds

def loadGeo(char):
    """
    """
    if char.geoFolder:
        path = os.path.join(char.geoFolder, "%s_geo.ma" %char.name)
        cmds.file(path,
                  i = True, 
                  type = "mayaAscii", 
                  ignoreVersion = True,
                  mergeNamespacesOnClash = False, 
                  rpr = "%s_geo" %char.name, 
                  options = "v=0", 
                  pr = True)
