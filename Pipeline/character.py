import os
import project as proj
reload(proj)

class Character:
    """
    """
    def __init__(self, project = '', char = ''):
        """
        @param project : str of project name
        @param char    : str of character name
        """
        self.project_ = project
        self.char = char
        
    def __repr__(self):
        return '<%s %s>' %(self.__class__.__name__, self.char)
    
    @property
    def name(self):
        """
        @rtype str
        """
        return self.char
    
    @property
    def project(self):
        """
        @rtype instance of Project 
        """
        project = proj.Project(project = self.project_)
        
        if project.isExists:
            return project
        else:
            return None
            
    @property
    def base(self):
        """
        @rtype str
        """
        return os.path.join( self.project.base, "Characters", self.char)
    
    @property
    def isExists(self):
        """
        @rtype bool
        """
        if os.path.exists(self.base):
            return True
        else:
            return False
    
    @property
    def geoFolder(self):
        """
        @rtype str
        """
        path = os.path.join(self.base, 'geo')
        if os.path.exists(path):
            return path
        else:
            return False

    @property
    def versionFolder(self):
        """
        @rtype str
        """
        path = os.path.join(self.base, 'versions')
        if os.path.exists(path):
            return path
        else:
            return False

    @property
    def publishedFolder(self):
        """
        @rtype str
        """
        path = os.path.join(self.base, 'published')
        if os.path.exists(path):
            return path
        else:
            return False

    @property
    def skinFolder(self):
        """
        @rtype str
        """
        path = os.path.join(self.base, 'skin')
        if os.path.exists(path):
            return path
        else:
            return False

    @property
    def locatorFolder(self):
        """
        @rtype str
        """
        path = os.path.join(self.base, 'locators')
        if os.path.exists(path):
            return path
        else:
            return False

    @property
    def controllerFolder(self):
        """
        @rtype str
        """
        path = os.path.join(self.base, 'controller')
        if os.path.exists(path):
            return path
        else:
            return False            
            
    @property
    def scriptFolder(self):
        """
        @rtype str
        """
        path = os.path.join(self.base, 'scripts')
        if os.path.exists(path):
            return path
        else:
            return False

    def create(self):
        """
        create character folder under project base and subfolders
        """
        print self.project.base
        if self.isExists:
            return False
        else:
            if not os.path.exists(self.project.base):
                os.makedirs(self.project.base)
                
            try:
                os.makedirs(self.base)
                subdirs = ['geo', 'skin', 'locators', 'controller', 'scripts', 'versions', 'published']
                for subdir in subdirs:
                    os.makedirs(os.path.join(self.base, subdir))
                return True
            
            except:
                print "error creating character"
                return False
                
    @property
    def createdBy(self):
        pass
    
    @property
    def assignedTo(self):
        pass
        
    @property
    def allCharacters(self):
        """
        @rtype list
        """
        return os.listdir(os.path.join(self.project.base, 'Characters'))