#! /usr/bin/python
# This is -*- Python -*- from nbg -*- coding: latin1 -*-
#
##   \file  mltiparamfile.py
#    \brief This file contains all parts of mlti which are concerned with reading, parsing and writing the private parameter file .mltirc.
#
#    \par Last Author: Martin Loesch (<martin.loesch@@kit.edu>)
#    \par Date of last change: Eingegebenes Datum kann nicht übernommen werden.
Geben Sie das neue Datum ein: (TT-MM-JJ)
#
#    \author   Martin Loesch (loesch@ira.uka.de)
#    \date     2008-11-18
#    \par Copyright:
#              Martin Loesch, Chair Prof. Dillmann (IAIM)\n
#              Institute for Computer Science and Engineering (CSE)\n
#	       University of Karlsruhe. All rights reserved\n
#	       http://wwwiaim.ira.uka.de
#

import os, shutil
import subprocess
import fileinput
import logging

import mltihelpers


## \namespace mltiparamfile
# This namespace contains all parameter file handling modules for the MLTemplateInstaller project.


## \class MissingFileException
# \brief Exception raised if a file is missing which was expected to exist.
class MissingFileException(Exception):

    def __init__(self, filename):
        self.filename = filename

    def __str__(self):
        return repr(self.filename)


## \class FileContentError
# \brief Exception raised if the content of a file is erronous.
class FileContentError(Exception):
    
    def __init__(self, filename, error_description):
        self.filename = filename
        self.description = error_description

    def __str__(self):
        return repr(self.filename) + " :  " + repr(self.description)


## \var private_parameter_file
# Globally used name (and path) of private parameter file.
#
# Can e.g. be changed for testing purposes.
private_parameter_file = os.path.join(os.path.expanduser("~"), ".mltirc")
# print " Path to parameter file: " + private_parameter_file)


## \brief Create private parameter file with user-specific parameters (interactive!)
def createUserParamFile():
    default_template_directory = "~/.mlti/"
    correct_input = False

    while not correct_input:
        name = raw_input("User name: ")
        email = raw_input("Email address: ")
        template_directory = raw_input("Template directory [" + default_template_directory + "]: ")
        if template_directory == "":
            template_directory = default_template_directory

        print
        print " Got the following information:"
        print " User name          = ", name
        print " Email address      = ", email
        print " Template directory = ", template_directory
        correct_input = mltihelpers.getYesOrNo("Is this information correct? ")
        print

    paramfile = open(private_parameter_file, 'w')
    paramfile.write("username = " + name + "\n")
    paramfile.write("useremail = " + email + "\n")
    paramfile.write("template directory = " + template_directory + "\n")
    

## \brief Read specific parameter from private parameter file.
def readParameterFromFile(requested_parameter):
    res = ""
    found = False
    pathtofile = private_parameter_file
    if os.path.isfile(pathtofile):
        for line in fileinput.input(pathtofile):
            param, value = parseParamFileLine(line)
            if param == requested_parameter:
                found = True
                res = value
        fileinput.close()
        if found:
            logging.info(" Found requested parameter: " + requested_parameter + " -> " + res)
            return res
        else:
            logging.warning(" Parameter missing in private parameter file: " + requested_parameter)
            raise FileContentError(pathtofile, "Missing parameter: " + requested_parameter)
    else:
        logging.error(" Parameter file missing!")
        raise MissingFileException(pathtofile)


## \brief Try to load ~/.mltirc for user-specific parameters.
#
# @return true if file could be loaded, false else
def loadUserParamFile():
    parameter_list = {}
    pathtofile = private_parameter_file
    if os.path.exists(private_parameter_file):
        self.template_directories = []
        ## \todo Müsste ich hier noch die template_directories direkt fertig parsen?
        for line in fileinput.input(pathtofile):
            param, arg = self.parseParamFileLine(line)
            logging.debug(" Parsed parameter file line:  " + param + " -> " + arg)
            parameter_list[param] = arg
        fileinput.close()
        return parameter_list
    else:
        logging.error(" Parameter file missing!")
        raise MissingFileException(pathtofile)


## \brief Parse a single line of the parameter file.
#
# @param line text which shall be parsed
# @return tuple: (parameter name, parameter value)
def parseParamFileLine(line):
    parts = line.split("=")
    return (parts[0].strip(), parts[1].strip())

## \brief Check existence of the private parameter file.
def existsPrivateParameterFile():
    pathtofile = private_parameter_file
    if os.path.isfile(pathtofile):
        return True
    else:
        return False


## \brief Create template directory and copy standard templates if desired (interactive!).
def createTemplateDir(template_directory, command):
    do_create_dir = mltihelpers.getYesOrNo("Shall the template directory (" + template_directory + ") be created? ")
    do_copy_templates = mltihelpers.getYesOrNo("Shall the standard templates be copied to the new directory? ")

    if do_create_dir and do_copy_templates:
        mlti_command = subprocess.Popen("which " + command, shell=True, stdout=subprocess.PIPE).communicate()[0]
        print "found command: ", mlti_command
        mlti_directory = os.path.dirname(mlti_command)
        shutil.copytree(os.path.join(mlti_directory, "templates"), template_directory)
    elif do_create_dir: # and not do_copy_templates
        os.mkdir(template_directory)
        
        
