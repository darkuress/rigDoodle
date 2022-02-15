import os

def runExternalScript(path):
    """
    """
    script = os.path.join(path, 'run.py')
    
    if os.path.exists(script):
        file = open(script, "r") 
        exec(file.read())