#! /usr/bin/python
# This is -*- Python -*- from nbg -*- coding: latin1 -*-
#
##   \file  pti.py
#    \brief This script installs templates for arbitrary projects or similar by copying data from a template directory and accordingly adapting some predefined variables in the files.
#
#    Last Author: Martin Loesch (<loesch@@ira.uka.de>)
#    Date of last change: 12.11.08
#
#    \author   Martin Loesch (<loesch@@ira.uka.de>)
#    \date     12.11.08
#    \par Copyright:
#              Martin Loesch, Chair Prof. Dillmann (IAIM)\n
#              Institute for Computer Science and Engineering (CSE)\n
#	       University of Karlsruhe. All rights reserved\n
#	       http://wwwiaim.ira.uka.de
#

import sys, os, shutil

template_directory = "/Users/martinloesch/Source/projects/ProjectTemplateInstaller/templates"

def printUsage(progname):
    print  "Usage:  ", progname, " templatename [target directory]\n"

class TemplateInstaller:

    def checkTemplateExistance(template):
        full_template_name = os.path.join(template_directory, template)
        return os.path.exists(full_template_name)

    def install(template, target):
        full_template_name = os.path.join(template_directory, template)
        if os.path.isfile(full_template_name):
            shutil.copy(full_template_name, target)
        else:
            shutil.copytree(full_template_name, target)
        print "Missing feature: no text substitution os done"
    

    checkTemplateExistance = staticmethod(checkTemplateExistance)
    install = staticmethod(install)


## TRUE MAIN PROGRAM
#
#
#
if __name__ == '__main__':

    if sys.argv[1:] == []:
        printUsage(sys.argv[0])
        exit(1)

    templatename = sys.argv[1]
    if sys.argv[2:] == []:
        targetdir = "."
    else:
        targetdir = sys.argv[2]

    if not TemplateInstaller.checkTemplateExistance(templatename):
        print "Sorry, template does not exist!\n"
        exit(2)
        
    TemplateInstaller.install(templatename, targetdir)
    
