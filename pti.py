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
import fileinput, re
import datetime

user_name = "Martin Loesch"
user_email = "loesch@ira.uka.de"

template_directory = "/Users/martinloesch/Source/projects/ProjectTemplateInstaller/templates"

def printUsage(progname):
    print  "Usage:  ", progname, " templatename [target directory]\n"

## \class TemplateInstaller
# \brief 
#
#
class TemplateInstaller:

    ## \brief substitutions which are performed on the copied templates
    substitutions = [("!!userinfo-fullname!!", "s", user_name),
                     ("!!userinfo-email!!", "s", user_email),
                     ("!!file-name!!", "f", "os.path.basename(target)"),
                     ("!!actual-date!!", "f", "datetime.date.today().isoformat()")]
    
    def __init__(self, template):
        self.template_name = template
        self.full_template_name = os.path.join(template_directory, template)
        self.full_templsubst_name = os.path.splitext(self.full_template_name)[0] + ".templ"
        if self.checkTemplateExistence():
            self.valid = True
        else:
            self.valid = False
        self.updateSubstitutions()
    
    def checkTemplateExistence(self):
        return os.path.exists(self.full_template_name)

    def checkTemplateSubstitutionsExistence(self, template):
        return os.path.exists(self.full_templsubst_name)

    def updateSubstitutions(self):
        if os.path.isfile(self.full_templsubst_name):
            for  l in fileinput.input(self.full_templsubst_name):
                s = re.split(" *#!# *", l)
                if len(s)!=3:
                    raise "Format error in template substitutions file!"
                if s[1]=="a":
                    substvalue = raw_input("Insert "+s[0]+" ["+s[2]+"]:  ")
                    self.substitutions.append((s[0], "s", substvalue))
                else:
                    self.substitutions.append((s[0], s[1], s[2].rstrip()))
            fileinput.close()
    
    def install(self, target):
        full_target_name = os.path.join(target, self.template_name)
        if os.path.isfile(self.full_template_name):
            shutil.copy(self.full_template_name, target)
            self.doSubstitutions(full_target_name)
        else:
            shutil.copytree(self.full_template_name, full_target_name)
            for f in os.listdir(full_target_name):
                self.doSubstitutions(os.path.join(full_target_name, f))
    
    def doSubstitutions(self, target):
        for line in fileinput.input(target, 1):
            for s in self.substitutions:
                if s[1]=="s":
                    line = re.sub(s[0], s[2], line)
                elif s[1]=="f":
                    line = re.sub(s[0], eval(s[2]), line)
            print line,
        fileinput.close()
        

        
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

    installer = TemplateInstaller(templatename)
    if not installer.valid:
        print "Sorry, template does not exist!\n"
        exit(2)
        
    installer.install(targetdir)
    
