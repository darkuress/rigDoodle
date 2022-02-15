#!/bin/env python
 ###############################################################################
 #
 #  Copying weight by txt file maya python scripts. Copyleft (c) 2013 Jon Hwang
 #
 #    $HeadURL: $
 #    $Revision: $ 2
 #    $Author:  $ Jonghwan Hwang
 #    $Date: $ 2013 - 08 - 13
 #
 ###############################################################################
"""
This script is used to save skin value as a txt file, and import skin value from the txt file. 

usage : 
	
	1. Select all the vertex from the skinned mesh first##########
	2. This will print out name of joints attached to the skinned mesh
		You can create as many as instances depending on the skinned mesh you have
		
		#instance 1
		run1 = CopyWeightByTxt('weight1.txt')
		run1.joint()
		run1.vertex()
		
		#instance 2
		run2 = CopyWeightByTxt('weight2.txt')
		run2.joint()
		run2.vertex()
		.
		.
		.
		
	3. You can detach skin and modify joint location###########
	
	4. Skin back with the joints printed out in before, 
		select all the vertex and run next
		
		run1.paste()
		run2.paste()
		.
		.
		.

"""

import maya.cmds as cmds
import string
import sys
import os


class CopyWeightByTxt(object):
    def __init__(self, file_base, char_name, mesh):
        ''' Initializing txt file name and file path '''
        # Getting txt file name
        self.name_path = os.path.join(file_base, char_name.replace('|', '_'))
        self.name_mesh = mesh

        # Getting selected name of mesh and vertex        
        self.number_of_vertex = cmds.polyEvaluate(self.name_mesh, vertex = True)            
        
    @staticmethod
    def findMeshes():
        '''
        find all skinned meshes under geo
        '''
        allSkinnedMeshes = []

        for mesh in cmds.listRelatives('geo', ad = True, type = 'mesh', f = True):
            if cmds.listConnections(mesh):
                for conn in cmds.listConnections(mesh):
                    if cmds.objectType(conn) == 'skinCluster':
                        allSkinnedMeshes.append(cmds.listRelatives(mesh, p = True, f = True)[0])
        print allSkinnedMeshes
        return allSkinnedMeshes
                		
    def joint(self):
        ''' Getting vertax info and saves weights into txt file'''
        
        self.name_vertexes = "%s.vtx[0:%s]" %(self.name_mesh, self.number_of_vertex-1)
        self.name_splited_vertex = string.split(self.name_vertexes, '[')
           
        # Getting joint from skinned mesh
        try :
            self.name_skincluster = cmds.skinCluster(self.name_mesh, q=True, dt=True)
            self.name_skincluster = self.name_skincluster[-1][0:-7]
            self.name_joint = cmds.skinCluster(self.name_mesh, q=True, inf=True)
            print self.name_joint                 

        # Check if proper mesh is selected
        except :
            print "please select skinned mesh"

    def vertex(self):
        ''' Getting vertax info and saves weights into txt file '''	

        # Getting skin value from selected vertexes	and write txt file
        txtFile = open(self.name_path, 'w')
        for vertexIndex in range(self.number_of_vertex):
            transformValue = []
            for joint in self.name_joint:
                tvTemp = cmds.skinPercent(self.name_skincluster,'%s[%s]' 
                                        %(self.name_splited_vertex[0], vertexIndex), 
                                        transform='%s' %joint, query=True 
                                        )
                transformValue.append(tvTemp)
            txtFile.write('%s\n' %transformValue)	
        txtFile.close()
        print "Finished writing txt file at %s" %self.name_path

    def paste(self):	
        ''' Read txt file and paste weight '''		

        # Read File
        txtFile = open(self.name_path)
        skinValue = txtFile.readline()
        transformValuePaste = ''

        # Redefinding skincluster to be safe from naming conflict
        self.name_skincluster = cmds.skinCluster(self.name_mesh, q=True, dt=True)
        self.name_skincluster = self.name_skincluster[-1][0:-7]

        # Making array of transform value from txt		
        vertexIndex = 0
        while(vertexIndex < self.number_of_vertex):
            skinValue = string.split(skinValue[1:-2], ',')			
            transformValuePaste = []
            for jointIndex in range(len(self.name_joint)):
                skinValueFloat = float(skinValue[jointIndex])
                jointName = str(self.name_joint[jointIndex])
                tvTemp = [jointName, skinValueFloat]
                transformValuePaste.append(tvTemp)
            
            # Assigning skin value to the mesh 
            cmds.skinPercent(self.name_skincluster, '%s[%s]' 
                            %(self.name_splited_vertex[0], vertexIndex), 
                            transformValue = transformValuePaste
                            )
                            
            skinValue = txtFile.readline()
            vertexIndex = vertexIndex + 1
        print "Finished transferring skin weight from %s" %self.name_path