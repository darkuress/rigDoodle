import os
import maya.cmds as cmds
from .. Pipeline import project
from .. Pipeline import character

def save(char):
    """
    @param char pipeline.character instance
    """
    versionFolder = char.versionFolder
    allVersions = os.listdir(versionFolder)
    
    thisVersion = len(allVersions) + 1
    fileName = '%s_wip_v%s.ma' %(char.name, thisVersion) 
    
    confirm = cmds.confirmDialog(title='Save', 
                                 message='Save as %s' %fileName, 
                                 button=['Yes', 'No', 'Cancel'], 
                                 defaultButton = 'Yes', 
                                 cancelButton = 'Cancel', 
                                 dismissString = 'Cancel' )
    if confirm == 'Yes':
        cmds.file(rename = os.path.join(versionFolder, fileName))
        cmds.file(f = True, save = True)
    