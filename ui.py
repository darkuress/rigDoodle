import maya.cmds as cmds
from Functions import main
from Pipeline import project
from Pipeline import character
from Utils import save
from Utils import publish
from Utils import loadGeo
reload(loadGeo)
reload(publish)
reload(save)
reload(project)
reload(main)

"""
uasage
from rigDoodle import ui
reload(ui)
x = ui.UI()
x.loadInMaya()
"""

#- initialize window
if cmds.window('rigDoodleUI', ex = True):
    cmds.deleteUI('rigDoodleUI')    

class UI:
    def __init__(self):
        """
        initializing ui
        """
        cmds.window('rigDoodleUI', menuBar=True, width=200, title = 'Rig Doodle')
        cmds.menu(label='File', tearOff=True )
        cmds.menuItem(label='Create Character', c = self.createCharacterCB)
        cmds.menuItem(label='Open',    c = self.openCB)
        cmds.menuItem(label='Save',    c = self.saveCB)
        cmds.menuItem(label='Publish', c = self.publishCB)
        cmds.menuItem(divider=True )
        cmds.menuItem(label='Quit' )
        cmds.menu(label='Tools')
        cmds.menuItem(label='TF Skinning Tool', c = self.tfSmoothToolCB)
        cmds.menu(label='Help', helpMenu=True )
        cmds.menuItem('Application..."', label='"About' )
        
        cmds.columnLayout()
        
        cmds.rowLayout(nc = 2)
        self.optionMenuProj = cmds.optionMenu(label = 'Project', cc = self.charOptionMenuCB)
        self.optionMenuChar = cmds.optionMenu(label = 'Character', cc = self.charOptionMenuChangeCB) 
        cmds.setParent("..")
        
        cmds.separator()
        cmds.separator()
        cmds.separator()
        cmds.separator()
        
        cmds.button(label = 'Load Geo', width = 124, c = self.loadGeoCB)
        
        cmds.rowLayout(nc = 3)
        self.buttonCreateLoc = cmds.button(label = 'Create Position Locator', c = self.createLocCB)
        self.buttonSaveLoc   = cmds.button(label = 'Save', c = self.saveLocCB)
        self.buttonLoadLoc   = cmds.button(label = 'Load', c = self.loadLocCB)
        cmds.setParent("..")
        
        self.buttonBuildJnt = cmds.button(label = 'Build Joint', width = 124, c = self.buildJntCB) 
        
        cmds.rowLayout(nc = 3)
        self.buildCtrl = cmds.button(label = 'Build Controller', width = 124, c = self.buildCtrlCB)
        cmds.button(label = 'Save', c = self.saveCtrlCB)
        cmds.button(label = 'Load', c = self.loadCtrlCB)
        cmds.setParent("..")
        
        cmds.button(label = 'Run Custom Script', width = 124, c = self.scriptCB)
        
        cmds.rowLayout(nc = 3)
        cmds.button(label = 'Skinning', width = 124, en = False)
        cmds.button(label = 'Save', c = self.copySkinWeightCB)
        cmds.button(label = 'Load', c = self.loadSkinWeightCB)
        cmds.setParent("..")
        
        #running Callbacks
        self.projOptionMenuCB()
        
        # create mainBuild instance
        self.mainBuild = main.MainBuild()

    def clearList(self, optionMenu, *args):
        """
        """
        menuItems = cmds.optionMenu(optionMenu, q = True, itemListLong = True)
        if menuItems:
            cmds.deleteUI(menuItems)
            
    def projOptionMenuCB(self,*args):
        """
        add project in option box
        """
        self.clearList(self.optionMenuProj)
        allProj = project.Project()
        for proj in allProj.allProjects:
            cmds.menuItem(p = self.optionMenuProj, label = proj) 
        self.projName = cmds.optionMenu(self.optionMenuProj, q = True, v = True)
        self.project = project.Project(project = self.projName)
        self.charOptionMenuCB()

    def charOptionMenuCB(self,*args):
        """
        add characters under the project
        """
        self.projName = cmds.optionMenu(self.optionMenuProj, q = True, v = True)
        self.project = project.Project(project = self.projName)
        allChars = project.Project(project = self.projName).allCharacters
        
        self.clearList(self.optionMenuChar)
        for item in [x.name for x in allChars]:
            cmds.menuItem(p = self.optionMenuChar, label = item) 
        self.charOptionMenuChangeCB()
        
    def charOptionMenuChangeCB(self, *args):
        """
        self.char
        """
        self.charName = cmds.optionMenu(self.optionMenuChar, q = True, v = True)
        self.char = character.Character(project = self.projName, char = self.charName)
        
        #cmds.workspace(self.char.base, n = True)
        #cmds.workspace(self.char.base, o = True)
        #cmds.workspace(self.char.base, s = True)

    def createCharacterCB(self, *args):
        """
        craete character
        """
        result = cmds.promptDialog(
                title='Character Name',
                message='Enter Name:',
                button=['OK', 'Cancel'],
                defaultButton='OK',
                cancelButton='Cancel',
                dismissString='Cancel')

        if result == 'OK':
            text = cmds.promptDialog(query=True, text=True)
        
        self.project.createCharacter(char = text)

    def openCB(self, *args):
        """
        open wip file
        """
        if cmds.file(q=True, modified=True):
            saveChange = cmds.confirmDialog(title = 'Save Changes', 
                                            message = 'Save Changes?', 
                                            button=['Yes','No', 'Cancel'], 
                                            defaultButton = 'Yes', 
                                            cancelButton = 'No', 
                                            dismissString = 'Cancel' )
            
            if saveChange == 'Yes':
                cmds.SaveScene()                                
        file = cmds.fileDialog2(startingDirectory = self.char.versionFolder, 
                                cap = 'Open', 
                                dialogStyle=2, 
                                okCaption = 'Open', 
                                fileMode = 1)
        cmds.file(new = True, f = True)
        cmds.file(file[0], o = True)
       
    def saveCB(self, *args):
        """
        save working file
        """
        save.save(self.char)

    def publishCB(self, *args):
        """
        publish rig
        """
        publish.publish(self.char)

    def loadGeoCB(self, *args):
        """
        loading geo
        """
        loadGeo.loadGeo(self.char)
        
    def createLocCB(self, *args):
        """
        create locator
        """
        self.mainBuild.createLocators()
        from Functions import locatorSetup  
        createLoc = locatorSetup.LocatorSetup()
        createLoc.installAllAdjustCtl()
        
    def saveLocCB(self, *args):
        """
        save locator as json file, 
        char.locatorFolder / char_locators.json
        """
        from Functions import locatorSetup
        saveLoc = locatorSetup.LocatorSetup()
        saveLoc.saveLocatorPos(self.char)

    def loadLocCB(self, *args):    
        """
        load locator from json file, 
        char.locatorFolder / char_locators.json
        """
        from Functions import locatorSetup  
        loadLoc = locatorSetup.LocatorSetup()
        loadLoc.loadLocatorPos(self.char) 
 
    def buildJntCB(self, *args):
        """
        build joint
        """
        self.mainBuild.setupBase()
        self.mainBuild.confirmJoints()

    def buildCtrlCB(self, *args):
        """
        build joint
        """
        self.mainBuild.setupParts()
        self.mainBuild.partAssembly()
    
    def saveCtrlCB(self, *args):
        """
        save controller's info 
        """
        from Functions import controller
        reload(controller)
        controller.saveAllCtlInfo(self.char)

    def loadCtrlCB(self, *args):
        """
        save controller's info 
        """
        from Functions import controller
        reload(controller)
        controller.loadAllCtlInfo(self.char)        

    def tfSmoothToolCB(self, *args):
        """
        open external skinning tool 
        
        #this does not work
        from Utils import tf_smoothSkinWeight
        reload(tf_smoothSkinWeight)
        tf_smoothSkinWeight.paint()
        """
        import tf_smoothSkinWeight
        tf_smoothSkinWeight.paint()

    def copySkinWeightCB(self, *args):
        """
        copy skin weight per meshes
        """
        from rigDoodle.Utils import copyWeight  as cw
        reload(cw)
        
        allSkinnedMeshes = cw.CopyWeightByTxt.findMeshes()        
        for mesh in allSkinnedMeshes:
            fileName = '%s.txt' %mesh
            run = cw.CopyWeightByTxt(self.char.skinFolder, fileName, mesh)
            run.joint()
            run.vertex()
        
    def loadSkinWeightCB(self, *args):
        """
        load skin weight from file
        """
        from rigDoodle.Utils import copyWeight  as cw
        reload(cw)
        
        allSkinnedMeshes = cw.CopyWeightByTxt.findMeshes()  
        for mesh in allSkinnedMeshes:
            fileName = '%s.txt' %mesh
            run = cw.CopyWeightByTxt(self.char.skinFolder, fileName, mesh)
            run.joint()
            run.paste()
    
    def scriptCB(self, *args):
        """
        running extra scripts
        """
        from Functions import scriptSetup
        reload(scriptSetup)
        scriptSetup.runExternalScript(self.char.scriptFolder)
    
    def loadInMaya(self, *args):
        """
        """
        cmds.showWindow()
