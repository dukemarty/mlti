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


## \class SubstitutionItem
# \brief
#
#
class SubstitutionItem:

    def __init__(self, varname, type, inserttext):
        self.var = varname
        self.type = type
        self.insert = inserttext


## \class TemplateSubstitutions
# \brief
#
#
class TemplateSubstitutions:

    ## \brief list of substitutions which can be applied to a text, initialized with a number of standard substitutions
    substitution_list = [SubstitutionItem("!!userinfo-fullname!!", "s", user_name),
                         SubstitutionItem("!!userinfo-email!!", "s", user_email),
                         SubstitutionItem("!!file-name!!", "f", "os.path.basename(self.resultfilename)"),
                         SubstitutionItem("!!actual-date!!", "f", "datetime.date.today().isoformat()")]

    def __init__(self, resultfilename=""):
        self.resultfilename = resultfilename
    
    def performSubstitutions(self, text):
        for s in self.substitution_list:
            if s.type=="s":
                text = re.sub(s.var, s.insert, text)
            elif s.type=="f":
                text = re.sub(s.var, eval(s.insert), text)
        return text

    def loadAdditionalSubstitutions(self, filename):
        for  l in fileinput.input(filename):
            s = re.split(" *#!# *", l)
            if len(s)!=3:
                raise "Format error in template substitutions file!"
            if s[1]=="a":
                substvalue = raw_input("Insert "+s[0]+" ["+s[2].rstrip()+"]:  ")
                self.substitution_list.append(SubstitutionItem(s[0], "s", substvalue.rstrip()))
            else:
                self.substitution_list.append(SubstitutionItem(s[0], s[1], s[2].rstrip()))
        fileinput.close()
        
    
## \class TemplateInstaller
# \brief 
#
#
class TemplateInstaller:

    substitutions = TemplateSubstitutions()
    
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
            self.substitutions.loadAdditionalSubstitutions(self.full_templsubst_name)
            
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
        self.substitutions.resultfilename = target
        for line in fileinput.input(target, 1):
            line = self.substitutions.performSubstitutions(line)
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
    
