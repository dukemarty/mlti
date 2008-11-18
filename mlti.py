#! /usr/bin/python
# This is -*- Python -*- from nbg -*- coding: latin1 -*-
#
##   \file  mlti.py
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

## \namespace mlti
# This namespace contains all the core modules for the MLTemplateInstaller project.

import sys, os, shutil
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
default_template_directory = "/Users/martinloesch/Source/projects/MLTemplateInstaller/templates"


## \brief Print usage information to standard output.
def printUsage(progname):
    print "Usage:  ", progname, " templatename [target_filename [target_directory]]"
    print
    print "  The program tries to access ~/.mltirc - if this file does not exist, you get the"
    print "  choice to let the program create this file. In it, some user data which is used"
    print "  in substitutions during the installation of a template."


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
        self.substitution_list = [SubstitutionItem("!!userinfo-fullname!!", "s", self.user_name),
                                  SubstitutionItem("!!userinfo-email!!", "s", self.user_email),
                                  SubstitutionItem("!!file-name!!", "f", "os.path.basename(self.provided_resultfilename)"),
                                  SubstitutionItem("!!actual-date!!", "f", "datetime.date.today().isoformat()")]
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
            if s.type=="s":
                text = re.sub(s.var, s.insert, text)
            elif s.type=="f":
                text = re.sub(s.var, eval(s.insert), text)
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
                lineno = fileinput.filelineno()
                fileinput.close()
                raise SubstitutionsFileFormatException("Format error in template substitutions file!", lineno)
            if s[0]=="":
                lineno = fileinput.filelineno()
                fileinput.close()
                raise SubstitutionsFileFormatException("Template variable empty in template substitutions file!", lineno)
            if s[1]=="a":
                substvalue = raw_input("Insert "+s[0]+" ["+s[2].rstrip()+"]:  ")
                self.substitution_list.append(SubstitutionItem(s[0], "s", substvalue.rstrip()))
            else:
                self.substitution_list.append(SubstitutionItem(s[0], s[1], s[2].rstrip()))
        fileinput.close()
        
    
## \class TemplateInstaller
# \brief This class provides an installer for prepared templates.
#
# Also the substitutions applied to the installed template(s) are managed here.
class TemplateInstaller:

    ## \var substitutions
    # substitutions which are applied to the template

    ## \var candidates
    # possible template candidates if given name is not uniquely identifying

    ## \var template_name
    # name of the template (does not contain any additional pathes)

    ## \var full_template_name
    # full name of template including all path components so that the file can be accessed

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
    def __init__(self, template):
        self.user_name = default_user_name
        self.user_email = default_user_email
        self.template_directory = default_template_directory
        self.paramFileValid = self.loadUserParamFile()
        self.substitutions = TemplateSubstitutions(self.user_name, self.user_email)
        self.candidates = []
        self.template_name = template
        self.full_template_name = os.path.join(self.template_directory, template)
        if self.checkTemplateExistence():
            self.valid = True
            self.updateSubstitutions()
        else:
            self.valid = False
            self.findCandidateTemplates()

    ## \brief Try to load ~/.mltirc for user-specific parameters.
    #
    # @return true if file could be loaded, false else
    def loadUserParamFile(self):
        pathtofile = os.path.join(os.path.expanduser("~"), ".mltirc")
        if os.path.exists(pathtofile):
            for line in fileinput.input(pathtofile):
                self.parseParamFileLine(line)
            fileinput.close()
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
            self.template_directory = parts[1].strip()
            
    ## \brief check whether template exists or not
    def checkTemplateExistence(self):
        return os.path.exists(self.full_template_name)

    ## \brief Assemble candidate list, i.e. find templates which contain the current template name.
    def findCandidateTemplates(self):
        for f in os.listdir(os.path.split(self.full_template_name)[0]):
            if (os.path.split(f)[1].find(self.template_name)!=-1) and os.path.splitext(f)[1]!=".templ":
                self.candidates.append(f)

    ## \brief Choose one of the assembled candidates.
    #
    # @param index index of chosen candidate           
    def chooseCandidate(self, index):
        if (index < 0) or (index > len(self.candidates)):
            raise IndexError("Index does not denote an existing candidate.")
        self.full_template_name = os.path.join(self.template_directory, self.candidates[index])
        self.template_name = self.candidates[index]
        if self.checkTemplateExistence():
            self.valid = True
            self.updateSubstitutions()
        else:
            self.valid = False

    ## \brief Load additional, template-specific substitutions.
    def updateSubstitutions(self):
        full_templsubst_name = os.path.splitext(self.full_template_name)[0] + ".templ"
        if os.path.isfile(full_templsubst_name):
            self.substitutions.loadAdditionalSubstitutions(full_templsubst_name)

    ## \brief Installs the chosen template.
    #
    # @param self reference to object
    # @param targetplace location where the template ist copied to
    # @param targetname file name which is given to the template after copying
    def install(self, targetplace, targetname):
        if not self.valid:
            raise RuntimeError("TemplateInstaller is not in a valid state!")
        full_target_name = os.path.join(targetplace, targetname)
        if os.path.isfile(self.full_template_name):
            shutil.copy(self.full_template_name, targetplace)
            os.rename(os.path.join(targetplace, self.template_name), full_target_name)
            self.doSubstitutions(full_target_name)
        else:
            shutil.copytree(self.full_template_name, full_target_name)
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

    ## \brief Check if param file was found, if not, repare it.
    def checkForParamFileProblems(self):
        if not self.installer.paramFileValid:
            if self.getYesOrNo("Shall ~/.mltirc be created? [Y/n]  "):
                paramfile = open(os.path.join(os.path.expanduser("~"), ".mltirc"), 'w')
                name = raw_input("Your name:  ")
                if name!="":
                    paramfile.write("username = " + name + "\n")
                email = raw_input("Your email address:  ")
                if email!="":
                    paramfile.write("useremail = " + email + "\n")
                templatedir = raw_input("Template directory:  ")
                if templatedir!="":
                    paramfile.write("template directory = " + templatedir + "\n")
                paramfile.write("\n")
                paramfile.close()
        
    ## \brief Check for existance of template file(s).
    #
    def checkTemplateExistance(self):
        if not self.installer.valid:
            if self.installer.candidates!=[]:
                i = 0
                for c in self.installer.candidates:
                    print str(i)+") "+c
                    i = i + 1
                print str(i) + ") none"
                choice = -1
                while choice<0 or choice>i:
                    choice = raw_input("Choose one option [none]:  ")
                    if choice=="":
                        choice = i
                    else:
                        choice = int(choice)
                if choice<i:
                    self.installer.chooseCandidate(choice)
                else:
                    exit(0)
            else:
                print "Sorry, template does not exist!\n"
                exit(2)

        if not self.installer.valid:
            print "Sorry, template does not exist!\n"
            exit(2)

    ## \brief Get integer in a certain range from command line.
    #
    # @param self reference to object
    # @param text command prompt shown to the user
    # @param lowerbound minimum allowed number
    # @param upperbound maximum allowed number
    # @param default default number (if just ENTER is typed)
    def getSecureInteger(self, text, lowerbound, upperbound, default):
        choice = -1
        while choice<lowerbound or choice>upperbound:
            choice = raw_input(text)
            if choice=="":
                choice = default
            else:
                choice = int(choice)
        return choice

    ## \brief Get yes or no from command line.
    #
    # In the following, yes corresponds to True, and no to False.
    #
    # @param text command prompt which is shown to the user
    # @param default default value if nothing is entered (just enter)
    # @return true if yes was chosen, false else
    def getYesOrNo(self, text, default=True):
        choice = raw_input(text)
        if choice=="":
            choice = default
        if choice==True or choice.lower()=="yes" or choice.lower()=="y":
            res = True
        else:
            res = False
        return res
    
    ## \brief Install template to the target directory.
    def install(self):
        self.installer.install(self.targetdir, self.targetname)
        
## \brief Process command line arguments.
#
# Set missing arguments to default values, or exit if not all necessary arguments were given.
def processCommandlineArguments():
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
    cliinstaller.run()
    
## \endcond
