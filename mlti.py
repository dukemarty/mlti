#! /usr/bin/python
# This is -*- Python -*- from nbg -*- coding: latin1 -*-
#
##   \file  mlti.py
#    \brief This script installs templates for arbitrary projects or similar by copying data from a template directory and accordingly adapting some predefined variables in the files.
#
#    \par Last Author: Martin Loesch (<martin.loesch@@kit.edu>)
#    \par Date of last change: Eingegebenes Datum kann nicht übernommen werden.
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
import logging

if sys.version_info < (2,7):
    import getopt
else:
    import argparse

LEVELS = {'debug': logging.DEBUG,
          'info': logging.INFO,
          'warning': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL}

default_logging_level = 'debug'

import mltihelpers 
import mlticore
import mltiparamfile


## \brief Print usage information to standard output.
def printUsage(progname):
    print "Usage:   ", os.path.split(progname)[1], " templatename [target_filename [target_directory]]"
    print "         ", os.path.split(progname)[1], " -l"
    print
    print "Options:"
    print "          -l, --list  Print complete list of available templates to standard"
    print "                      out."
    print "          -p, --path  Provide template directory."
    print "          -d, --debug Set debug level, valid levels are:"
    print "                        debug, info, warning, error, critical"
    print
    print "  The program tries to access ~/.mltirc - if this file does not exist, you get"
    print "  the choice to let the program create this file. In it, some user data which"
    print "  is used in substitutions during the installation of a template."


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
    # @param templatedir directory containing templates
    def __init__(self, templatename, targetdirectory, targetname, templatedir):
        self.targetdir = targetdirectory
        self.targetname = targetname
        self.installer = mlticore.TemplateInstaller(templatename, templatedir)

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
            print " {0:>3})  ".format(i) + templ
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
                createTemplateDir(os.path.join(os.path.expanduser("~"), ".mlti"), sys.argv[0])
                
        
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
                choices = mltihelpers.getSecureIntegers("Choose at least one option [none]:  ", 0, i, i)
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
        

def processCommandlineArguments_argparse(argv):
    parser = argparse.ArgumentParser(description="The program tries to access ~/.mltirc - if this file does not exist, you get the choice to let the program create this file. In it, some user data which is used in substitutions during the installation of a template.")
    parser.add_argument("-l, --list", nargs=0, help="Print complete list of available templates to standard out.")

    parser.add_argument("templatename")
    parser.add_argument("target_filename")
    parser.add_argument("target_directory")

    print "THIS IS THE USAGE MESSAGE:"
    parser.print_usage()

    print "THIS IS THE HELP MESSAGE:"
    parser.print_help()


def processCommandlineArguments_getopt(argv):
    try:
        optlist, arglist = getopt.getopt(argv[1:], 'ld:p:', ['list', 'debug=', 'path='])
#        print " Arguments =  " + ", ".join(arglist)
#        print " Options = " + str(optlist)
    except getopt.GetoptError:
#        print " Invalid command line parameter(s) found."
        printUsage(argv[0])
        exit(1)

    template_name = ""
    target_name = ""
    target_dir = ""
    template_dir = ""

    log_level = default_logging_level

    # first, check for logging level parameter
    for opt, arg in optlist:
        if opt in ("-d", "--debug"):
            print " Setting now new logging level: <" + arg + ">"
            log_level = arg
    print "Log_Level will be set to: " + str(LEVELS.get(log_level, logging.NOTSET))
    logging.basicConfig(level=LEVELS.get(log_level, logging.NOTSET))

    # now check for other options
    for opt, arg in optlist:
        logging.info(" Iterating optlist, current = (" + opt + " , " + arg + ")")
        if opt in ("-l", "--list"):
            return ("", "", "", "")
        elif opt in ("-p", "--path"):
            template_dir = arg
        
    # finally, process arguments
    logging.info(" Number of arguments: " + str(len(arglist)))

    if len(arglist) == 0:
        logging.info(" No arguments were given.")
        printUsage(argv[0])
        exit(1)

    if len(arglist) >= 1:
        template_name = arglist[0]
        logging.info(" Got (partial) template name:  " + template_name)
        target_name = template_name
        target_dir = "."

    if len(arglist) >= 2:
        target_name = arglist[1]
        logging.info(" Got target name: " + target_name)
            
    if len(arglist) == 3:
        target_dir = arglist[2]
        logging.info(" Got target directory: " + target_dir)

    return (template_name, target_dir, target_name, template_dir)

## \brief Process command line arguments.
#
# Set missing arguments to default values, or exit if not all necessary arguments were given.
def processCommandlineArguments(argv):

    if sys.version_info < (2,7):
        res = processCommandlineArguments_getopt(argv)
    else:
        res = processCommandlineArguments_argparse(argv)

    return res

def checkOperability(template_name, target_name, target_dir, template_dir):
    logging.info(" Check for existence of private parameter file ~/.mltirc ...")
    if not mltiparamfile.existsPrivateParameterFile():
        logging.warning(" Private parameter file not found!")
        handleParamFileProblem()
    if template_dir != "":
        check_template_dir = template_dir
    else:
        check_template_dir = mltiparamfile.readParameterFromFile("template directory")
    check_template_dir = os.path.expanduser(check_template_dir)
    logging.info(" Check for existence of template directory: " + check_template_dir)
    if (not os.path.isdir(check_template_dir)):
        logging.error(" Template directory does not exists!")
        handleTemplateDirProblem(check_template_dir)
    logging.info(" Check for existence of templates ...")
    
    
def handleParamFileProblem():
    logging.info("Fixing problems with parameter file...")
    createUserParamFile()

def handleTemplateDirProblem(directory):
    print "Fixing problems with missing template directory..."
    createTemplateDir(directory, sys.argv[0])
        
## TRUE MAIN PROGRAM
#
## \cond false
        
if __name__ == '__main__':

    (templatename, targetdir, targetname, templatedir) = processCommandlineArguments(sys.argv)
    isOperable = checkOperability(templatename, targetdir, targetname, templatedir)

    logging.info("templatename = " + templatename)
    logging.info("targetdir    = " + targetdir)
    logging.info("targetname   = " + targetname)
    logging.info("templatedir  = " + templatedir)

    cliinstaller = CLIforTemplateInstaller(templatename, targetdir, targetname, templatedir)
    if templatename != "":
        cliinstaller.run()
    else:
        allTemplates = cliinstaller.printFullTemplateList()
    
## \endcond
