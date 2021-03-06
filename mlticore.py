#! /usr/bin/python
# This is -*- Python -*- from nbg -*- coding: latin1 -*-
#
##   \file  mlticore.py
#    \brief This file contains all parts of mlti-core, i.e. all components which actually make up the template substitution system.
#
#    \par Last Author: Martin Loesch (<loesch@@ira.uka.de>)
#    \par Date of last change: 07.03.09
#
#    \author   Martin Loesch (loesch@ira.uka.de)
#    \date     2008-11-18
#    \par Copyright:
#              Martin Loesch, Chair Prof. Dillmann (IAIM)\n
#              Institute for Computer Science and Engineering (CSE)\n
#	       University of Karlsruhe. All rights reserved\n
#	       http://wwwiaim.ira.uka.de
#

## \namespace mlticore
# This namespace contains all core modules for the MLTemplateInstaller project.

import os, shutil
import fileinput, re
import datetime


## \var default_user_name
# Globally used name of user for template substitutions.
default_user_name = "DEFAULTUSERNAME"
## \var default_user_email
# Globally used email address of standard user for template substitutions.
default_user_email = "DEFAULTUSER@EMAIL"

## \var default_template_directory
# Directory where all templates are placed.
default_template_directory = os.path.expanduser("~/.mlti/")


## \class SubstitutionsFileFormatException
# \brief Exception class for errors in substitution files.
class SubstitutionsFileFormatException(Exception):

    ## \var cause
    # cause for the exception

    ## \var linenumber
    # number of line in the file where the error occured
    
    ## \brief Constructor for new exception.
    #
    # @param self reference to object
    # @param cause text explaining the error more detailled
    # @param linenumber default is line 0, i.e. the first line
    def __init__(self, cause, linenumber=0):
        self.cause = cause
        self.linenumber = linenumber

    ## \brief Convert exception string.
    def __str__(self):
        return self.cause + " in line " + str(self.linenumber)

    
## \class SubstitutionItem
# \brief Representation for a single substitution.
#
# A substitution in the context of this project has three parts:
#  -# the pattern which ist substituted (called var for variable name in this context)
#  -# the type of substitution, we distinct s for simple string substitution, f for a python function call which results in the substitute, and a for a variable which is filled by user input
#  -# the substitute, basically a string or a function call which provides the string
class SubstitutionItem:

    ## \var var
    # pattern which is substituted

    ## \var type
    # type of substitution (s, f or a)

    ## \var insert
    # substitute for the pattern

    ## \brief Constructor for new SubstitutionItems
    def __init__(self, varname, type, inserttext):
        self.var = varname
        self.type = type
        self.insert = inserttext


## \class TemplateSubstitutions
# \brief Representation for a set of substitutions.
#
# This class not only provides a container for substitutions; it also allows to load additional substitutions, and to apply the currently loaded substitutions to a given string.
#
# It is also possible to externally set a number of attributes which can then be accessed during the substitutions; all these attributes' names start with provided_... .
class TemplateSubstitutions:

    ## \var user_name
    # name of user which is used for substitutions

    ## \var user_email
    # email address of user which is used for substitutions

    ## \var substitution_list
    # list of substitutions which can be applied to a text, initialized with a number of standard substitutions

    ## \var provided_resultfilename
    # name of the result file, i.e. if the text to which the substitutions are applied goes into a file, the name of this file

    ## \brief Constructor for new TemplateSubstitutions objects.
    #
    # @param username name of the calling user (will be used in substitutions)
    # @param useremail email address of the calling user (will be used in substitutions)
    # @param resultfilename if possible, the name of the file containing the text which is used in the substitutions can be set here
    def __init__(self, username, useremail, resultfilename=""):
        self.user_name = username
        self.user_email = useremail
        self.substitution_list = {'!!userinfo-fullname!!' : SubstitutionItem("!!userinfo-fullname!!", "s", self.user_name),
                                  '!!userinfo-email!!' : SubstitutionItem("!!userinfo-email!!", "s", self.user_email),
                                  '!!file-name!!' : SubstitutionItem("!!file-name!!", "f", "os.path.basename(self.provided_resultfilename)"),
                                  '!!actual-date!!' : SubstitutionItem("!!actual-date!!", "f", "datetime.date.today().isoformat()")}
        self.provided_resultfilename = resultfilename

    ## \brief Set the provided attributes for the substitutions with externally available information.
    #
    # This method is best be used with named parameters, so that only the necessary values for the current usage are set.
    def setExternalInformation(self, resultfilename):
        self.provided_resultfilename = resultfilename
        
    ## \brief Apply the substitutions to a string.
    #
    # @param self pointer to object
    # @param text string where the substitutions shall be done on
    # @return changed input string
    def performSubstitutions(self, text):
        for s in self.substitution_list:
            sub = self.substitution_list[s]
            if sub.type=="s":
                text = re.sub(sub.var, sub.insert, text)
            elif sub.type=="f":
                text = re.sub(sub.var, eval(sub.insert), text)
        return text

    ## \brief Load additional substitutions from file.
    #
    # The loaded substitutions are appended to the standard substitutions, but don't replace them!
    #
    # If there are problems with the file, an exception is raised to inform the caller about the problem.
    #
    # @throw SubstitutionsFileFormatException
    #
    # @param self pointer to object
    # @param filename name of substitutions file
    def loadAdditionalSubstitutions(self, filename):
        for  l in fileinput.input(filename):
            s = re.split(" *#!# *", l)
            if len(s)!=3:
                if  l.strip()!="":
                    lineno = fileinput.filelineno()
                    fileinput.close()
                    raise SubstitutionsFileFormatException("Format error in template substitutions file!", lineno)
                else:
                    fileinput.close()
                    return
            if s[0]=="":
                lineno = fileinput.filelineno()
                fileinput.close()
                raise SubstitutionsFileFormatException("Template variable empty in template substitutions file!", lineno)
            if s[1]=="a":
                if s[0] not in self.substitution_list:
                    substvalue = raw_input("Insert "+s[0]+" ["+s[2].rstrip()+"]:  ")
                    self.substitution_list[s[0]] = SubstitutionItem(s[0], "s", substvalue.rstrip())
            else:
                if s[0] not in self.substitution_list:
                    self.substitution_list[s[0]] = SubstitutionItem(s[0], s[1], s[2].rstrip())
        fileinput.close()

    ## \brief Get value of variable of a substitution.
    #
    # @param self reference to object
    # @param varname name of the variable (i.e. unique substitution identifier)
    # @return insert value of the substitutions, already evaluated if it is a function, "" if the variable does not exist
    def getVarVal(self, varname):
        if varname in self.substitution_list:
            if self.substitution_list[varname].type == 'f':
                return eval(self.substitution_list[varname].insert)
            else:
                return self.substitution_list[varname].insert
        else:
            return ""
    
## \class TemplateInstaller
# \brief This class provides an installer for prepared templates.
#
# Also the substitutions applied to the installed template(s) are managed here.
class TemplateInstaller:

    ## \var user_name
    # name of user which will be used for substitutions

    ## \var user_email
    # email address of user which will be used for substitutions

    ## \var template_directories
    # directories which is searched for templates

    ## \var paramFileValid
    # flag whether a parameter file was found (and could be loaded) = true, or if not (= false)

    ## \var substitutions
    # substitutions which are applied to the template

    ## \var candidates
    # possible template candidates if given name is not uniquely identifying

    ## \var template_name
    # name of the template (does not contain any additional pathes)

    ## \var valid
    # true if the object is valid and can be used to do an installation of a template, false else
    #
    # Reasons for an invalid status can e.g. be that the given template name does not exist.

    ## \brief Constructor for new TemplateInstaller object.
    #
    # Template names and pathes are prepared for installation; if template with given name does not exist, but there are templates' names which contain the given name, these are assembled in a candidate list.
    #
    # @param self reference to object
    # @param template (part of) name of template which shall be installed
    # @param template_dir "personalized" template directory
    def __init__(self, template, template_dir):
        self.user_name = default_user_name
        self.user_email = default_user_email
        self.template_directories = [template_dir, default_template_directory]
        self.paramFileValid = self.loadUserParamFile()
        self.substitutions = TemplateSubstitutions(self.user_name, self.user_email)
        self.template_name = {template:""}
        if self.checkTemplateExistence(template):
            self.valid = True
            self.updateSubstitutions()
        else:
            self.valid = False
            self.findCandidateTemplates(template)

    ## \brief Try to load ~/.mltirc for user-specific parameters.
    #
    # @return true if file could be loaded, false else
    def loadUserParamFile(self):
        pathtofile = os.path.join(os.path.expanduser("~"), ".mltirc")
        if os.path.exists(pathtofile):
            self.template_directories = []
            for line in fileinput.input(pathtofile):
                self.parseParamFileLine(line)
            fileinput.close()
            if self.template_directories==[]:
                self.template_directories.append(default_template_directory)
            return True
        else:
            return False

    ## \brief Parse a single line of the parameter file.
    #
    # @param line text which shall be parsed
    def parseParamFileLine(self, line):
        parts = line.split("=")
        if parts[0].strip()=="username":
            self.user_name = parts[1].strip()
        elif parts[0].strip()=="useremail":
            self.user_email = parts[1].strip()
        elif parts[0].strip()=="template directory":
            self.template_directories.append(os.path.expanduser(parts[1].strip()))
            
    ## \brief Check whether template exists or not
    #
    # @param templatename name of the template which is checked
    # @return true if the template exists somewhere in the template directory(ies), false else
    def checkTemplateExistence(self, templatename):
        for dir in self.template_directories:
            self.template_name[templatename] = os.path.join(dir, templatename)
            if os.path.exists(self.template_name[templatename]):
                return True
        return False

    ## \brief Assemble candidate list, i.e. find templates which contain the current template name.
    #
    # @param pattern pattern for which to find candidates
    def findCandidateTemplates(self, pattern):
        candlist = {}
        self.candidates = []
        for dir in self.template_directories:
            for f in os.listdir(os.path.join(dir,os.path.split(pattern)[0])):
                if (os.path.split(f)[1].lower().find(pattern)!=-1) and os.path.splitext(f)[1]!=".templ":
                    if f not in candlist:
                        self.candidates.append((dir, f))
                        candlist[f] = dir

    ## \brief Get list of actual candidates file names.
    #
    # @return list of candidate file names
    def getCandidateNameList(self):
        res = []
        for c in self.candidates:
            res.append(c[1])
        return res
                        
    ## \brief Choose one of the assembled candidates.
    #
    # @param indices one or more indices of chosen candidate
    def chooseCandidate(self, indices):
        self.template_name = {}
        for index in indices:
            if (index < 0) or (index > len(self.candidates)):
                raise IndexError("Index does not denote an existing candidate.")
            if self.checkTemplateExistence(self.candidates[index][1]):
                self.valid = True
                self.updateSubstitutions()
            else:
                self.valid = False

    ## \brief Load additional, template-specific substitutions.
    def updateSubstitutions(self):
        for templ in self.template_name:
            full_templsubst_name = os.path.splitext(self.template_name[templ])[0] + ".templ"
            if os.path.isfile(full_templsubst_name):
                self.substitutions.loadAdditionalSubstitutions(full_templsubst_name)

    ## \brief Get full list of all available templates.
    #
    # @return
    def getFullTemplateList(self):
        res = []
        for dir in self.template_directories:
            for f in os.listdir(os.path.join(dir, os.path.split(self.template_name.keys()[0])[0])):
                if os.path.splitext(f)[1]!=".templ":
                    res.append(f)
        return res
                
    ## \brief Installs the chosen template.
    #
    # @param self reference to object
    # @param targetplace location where the template ist copied to
    # @param targetname file name which is given to the template after copying
    def install(self, targetplace, targetname):
        if not self.valid:
            raise RuntimeError("TemplateInstaller is not in a valid state!")
        installed_extensions = []
        for templ in self.template_name:
            if os.path.splitext(targetname)[1]=="":
                full_target_name = os.path.join(targetplace, targetname + os.path.splitext(templ)[1])
            else:
                full_target_name = os.path.join(targetplace, targetname)
            if os.path.splitext(full_target_name) not in installed_extensions:
                installed_extensions.append(os.path.splitext(full_target_name))
                if os.path.isfile(self.template_name[templ]):
                    shutil.copy(self.template_name[templ], targetplace)
                    os.rename(os.path.join(targetplace, templ), full_target_name)
                    self.doSubstitutions(full_target_name)
                else:
                    shutil.copytree(self.template_name[templ], full_target_name)
                    for f in os.listdir(full_target_name):
                        self.doSubstitutions(os.path.join(full_target_name, f))

    ## \brief Let substitutions run over all template copies.
    #
    # @param target new name of the template file
    def doSubstitutions(self, target):
        self.substitutions.setExternalInformation(resultfilename=target)
        for line in fileinput.input(target, 1):
            line = self.substitutions.performSubstitutions(line)
            print line,
        fileinput.close()
        

        
## TRUE MAIN PROGRAM
#
## \cond
if __name__ == '__main__':
    print "Testing mlti-core.py\n"

## \endcond
