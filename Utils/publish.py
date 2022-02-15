import os
import maya.cmds as cmds
from .. Pipeline import project
from .. Pipeline import character

def publish(char):
    """
    @param char pipeline.character instance
    """
    publishFolder = char.publishedFolder
    allVersions = os.listdir(publishFolder)
    
    thisVersion = len(allVersions) + 1
    fileName = '%s_rig_v%s.ma' %(char.name, thisVersion) 
    
    confirm = cmds.confirmDialog(title='Publish', 
                                 message='Publish as %s' %fileName, 
                                 button=['Yes', 'No', 'Cancel'], 
                                 defaultButton = 'Yes', 
                                 cancelButton = 'Cancel', 
                                 dismissString = 'Cancel' )
    if confirm == 'Yes':
        cmds.file(rename = os.path.join(publishFolder, fileName))
        cmds.file(f = True, save = True)
    
    #connect to database