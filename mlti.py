#! /usr/bin/python
# This is -*- Python -*- from nbg -*- coding: latin1 -*-
#
##   \file  mlti.py
#    \brief This script installs templates for arbitrary projects or similar by copying data from a template directory and accordingly adapting some predefined variables in the files.
#
#    \par Last Author: Martin Loesch (<loesch@@ira.uka.de>)
#    \par Date of last change: 15.12.08
#
#    \author   Martin Loesch (<loesch@@ira.uka.de>)
#    \date     12.11.08
#    \par Copyright:
#              Martin Loesch, Chair Prof. Dillmann (IAIM)\n
#              Institute for Computer Science and Engineering (CSE)\n
#	       University of Karlsruhe. All rights reserved\n
#	       http://wwwiaim.ira.uka.de
#

## \namespace mlti
# This namespace contains all the core modules for the MLTemplateInstaller project.

import sys, os

from mltihelpers import *
from mlticore import *


## \brief Print usage information to standard output.
def printUsage(progname):
    print "Usage:  ", progname, " templatename [target_filename [target_directory]]"
    print
    print "  The program tries to access ~/.mltirc - if this file does not exist, you get the"
    print "  choice to let the program create this file. In it, some user data which is used"
    print "  in substitutions during the installation of a template."


## \class CLIforTemplateInstaller
# \brief Provide a CommandLine-Interface for the TemplateInstaller.
#
# In particular, the choice between different candidates for a not uniquely selected template has to be handled.
class CLIforTemplateInstaller:

    ## \var targetdir
    # directory where the template(s) are installed to

    ## \var targetname
    # name which is assigned to the installed template

    ## \var installer
    # instance of TemplateInstaller used to install one or more template files
    
    ## \brief Constructor new instances.
    #
    # @param templatename name or part of name of chosen template
    # @param targetdirectory directory to install the template in
    # @param targetname name the installed template shall have
    def __init__(self, templatename, targetdirectory, targetname):
        self.targetdir = targetdirectory
        self.targetname = targetname
        self.installer = TemplateInstaller(templatename)

    ## \brief Run the installer wrapped in the CLI.
    #
    # This method mirrors the standard steps:
    #  -# check correctness of requested template
    #  -# install template 
    def run(self):
        self.checkForParamFileProblems()
        self.checkTemplateExistance()
        self.install()

    ## \brief Print list of all available templates.
    # 
    def printFullTemplateList(self):
        allTemplates = self.installer.getFullTemplateList()
        i = 1
        for templ in allTemplates:
            print " " + str(i) + ")  " + templ
            i = i + 1
        
    ## \brief Check if param file was found, if not, repare it.
    def checkForParamFileProblems(self):
        if not self.installer.paramFileValid:
            if getYesOrNo("Shall ~/.mltirc and private template directory ~/.mlti be created? [Y/n]  "):
                paramfile = open(os.path.join(os.path.expanduser("~"), ".mltirc"), 'w')
                name = raw_input("Your name:  ")
                if name!="":
                    paramfile.write("username = " + name + "\n")
                email = raw_input("Your email address:  ")
                if email!="":
                    paramfile.write("useremail = " + email + "\n")
                paramfile.write("template directory = " + os.path.join(os.path.expanduser("~"), ".mlti") + "\n")
                if getYesOrNo("Use default template directory besides private one? [Y/n]  "):
                    paramfile.write("template directory = " + default_template_directory + "\n")
                paramfile.write("\n")
                paramfile.close()
                os.mkdir(os.path.join(os.path.expanduser("~"), ".mlti"))
        
    ## \brief Check for existance of template file(s).
    def checkTemplateExistance(self):
        if not self.installer.valid:
            cands = self.installer.getCandidateNameList()
            if cands!=[]:
                i = 0
                for c in cands:
                    print str(i) + ") " + c
                    i = i + 1
                print str(i) + ") none"
                choices = getSecureIntegers("Choose at least one option [none]:  ", 0, i, i)
                if i not in choices:
                    self.installer.chooseCandidate(choices)
                else:
                    exit(0)
            else:
                print "Sorry, template does not exist!\n"
                exit(2)

        if not self.installer.valid:
            print "Sorry, template does not exist!\n"
            exit(2)

    ## \brief Install template to the target directory.
    def install(self):
        self.installer.install(self.targetdir, self.targetname)
        
## \brief Process command line arguments.
#
# Set missing arguments to default values, or exit if not all necessary arguments were given.
def processCommandlineArguments():
    for param in sys.argv:
        if param=="-l":
            return ("", "", "")

    if sys.argv[1:] == []:
        printUsage(sys.argv[0])
        exit(1)
    else:
        templatename = sys.argv[1]
        
    if sys.argv[2:] == []:
        targetname = templatename
    else:
        targetname = sys.argv[2]
        
    if sys.argv[3:] == []:
        targetdir = "."
    else:
        targetdir = sys.argv[3]

    return (templatename, targetdir, targetname)
    
        
## TRUE MAIN PROGRAM
#
## \cond false
        
if __name__ == '__main__':

    (templatename, targetdir, targetname) = processCommandlineArguments()

    cliinstaller = CLIforTemplateInstaller(templatename, targetdir, targetname)
    if templatename != "":
        cliinstaller.run()
    else:
        allTemplates = cliinstaller.printFullTemplateList()
    
## \endcond
