import os
import json

class Config:
    def __init__(self):
        """
        """
        with open(os.path.join(os.path.dirname(__file__), 'config.json' )) as datafile: 
            configData = json.load(datafile)    
        self.baseDir = configData['baseDir']  
        self.allProjects = configData['allProjects']
    
    @property
    def baseDir():
        """
        project base dir
        """
        return self.baseDir  
    
    @property
    def allProjects():
        """
        return all project name
        """
        return self.allProjects
    