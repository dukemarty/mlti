#! /usr/bin/python
# This is -*- Python -*- from nbg -*- coding: latin1 -*-
#
##   \file  !!file-name!!
#    \brief Please put your documentation for this file here.
#
#    \par Last Author: !!userinfo-fullname!! (<!!userinfo-email!!>)
#    \par Date of last change: !!actual-date!!
#
#    \author   !!userinfo-fullname!! (<!!userinfo-email!!>)
#    \date     !!actual-date!!
#    \par Copyright:
#              !!userinfo-fullname!!, Chair Prof. Dillmann (HIS)\n
#              Institute for Anthropomatics (IFA)\n
#	       Karlsruhe Institute of Technology (KIT). All rights reserved\n
#	       http://his.anthropomatik.kit.edu
#

from xml.dom import minidom
import os

class ConfigurationEntry:

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        result = ""
        result = result + "Name:        " + self.name + "\n"
        result = result + "Description: " + self.description

        return result


class ConfigurationList:

    def __init__(self):
        self.entries = []

    def appendEntry(self, entry):
        self.entries.append(entry)

    def getConfigEntries(self):
        return self.entries

def load(filename):
    result = ConfigurationList

    # load xml configuration file
    xtree = minidom.parse(filename)
    rootnode = xtree.getElementsByTagName("!!root-tag!!")[0]

    # load sensor entries


ClassifierConfiguration = load("!!config-xml!!")


## TRUE MAIN PROGRAM
#
## \cond false
if __name__ == '__main__':
    print "Testing !!file-name!!\n"

    config = load("!!config-xml!!")

    for c in config.getConfigEntries():
        print "---------------------------------------------"
        print c
        print "---------------------------------------------\n"

## \endcond
    
