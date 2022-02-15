import os
import config
reload(config)

class Project:
    """
    """
    def __init__(self, project = ''):
        """
        @param name : str of project name
        """
        self.CONFIG = config.Config()
        self.allProjects = self.CONFIG.allProjects
        
        self.baseDir = self.CONFIG.baseDir
        self.name = project

    def allProjects(self):
        """
        return all Project names
        
        @rtype list
        """
        self.allProjects
        
    @property
    def base(self):
        """
        @rtype str
        """
        return os.path.join(self.baseDir,os.sep, "projects", self.name)
    
    @property
    def isExists(self):
        """
        rtype bool
        """
        if os.path.exists(self.base):
            return True
        else:
            return False
        
    @property
    def name(self):
        """
        @rtype str
        """
        return self.name

    def children(self):
        """
        @rtype list of character object
        """
        pass
    
    @property    
    def isActive(self):
        return True
	
    def activate(self):
        pass
    
    def deActivate(self):
        pass
    
    @property
    def createdAt(self):
        pass
    
    @property
    def createdBy(self):
        pass
        
    @property
    def allProjects(self):
        pass
    
    @property
    def allCharacters(self):
        """
        @rtype list
        """
        import character
        reload(character)
        try:
            chars = os.listdir(os.path.join(self.base, 'Characters'))
            return [character.Character(project = self.name, char = x) for x in chars]  
        except:
            return []
    
    
    def createCharacter(self, char):
        """
        create character with given name
        @param char str
        """
        import character
        reload(character)
        
        char_ = character.Character(project = self.name, char = char)
        char_.create()