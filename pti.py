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

templsubst_userinfo_fullname = "Martin Loesch"
templsubst_userinfo_email = "loesch@ira.uka.de"

template_directory = "/Users/martinloesch/Source/projects/ProjectTemplateInstaller/templates"

def printUsage(progname):
    print  "Usage:  ", progname, " templatename [target directory]\n"

class TemplateInstaller:

    def checkTemplateExistance(template):
        full_template_name = os.path.join(template_directory, template)
        return os.path.exists(full_template_name)

    def installTemplate(template, target):
        full_template_name = os.path.join(template_directory, template)
        full_target_name = os.path.join(target, template)
        if os.path.isfile(full_template_name):
            shutil.copy(full_template_name, target)
            TemplateInstaller.doSubstitutions(full_target_name)
        else:
            shutil.copytree(full_template_name, full_target_name)
            print "Missing feature: no text substitution os done"
    
    def doSubstitutions(target):
        for line in fileinput.input(target, 1):
            line = re.sub("!!userinfo-fullname!!", templsubst_userinfo_fullname, line)
            line = re.sub("!!userinfo-email!!", templsubst_userinfo_email, line)
            line = re.sub("!!file-name!!", os.path.basename(target), line)
            line = re.sub("!!actual-date!!", datetime.date.today().isoformat(), line)
            print line,
        fileinput.close()
        
    checkTemplateExistance = staticmethod(checkTemplateExistance)
    install = staticmethod(installTemplate)
    doSubstitutions = staticmethod(doSubstitutions)


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
    
