#! /usr/bin/python
# This is -*- Python -*- from nbg -*- coding: latin1 -*-
#
##   \file  tests_mltihelpers.py
#    \brief This file contains tests for the mltihelpers module.
#
#    \par Last Author: Martin Loesch (loesch@@ira.uka.de)
#    \par Date of last change: 2008-11-21
#
#    \author   Martin Loesch (loesch@@ira.uka.de)
#    \date     2008-11-21
#    \par Copyright:
#              Martin Loesch, Chair Prof. Dillmann (IAIM)\n
#              Institute for Computer Science and Engineering (CSE)\n
#	       University of Karlsruhe. All rights reserved\n
#	       http://wwwiaim.ira.uka.de
#

from mltihelpers import *

def testGetSecureIntegers():

    print "Test 1 for getSecureIntegers()..."
    result = getSecureIntegers("Zahl zwischen 3 und 13 bitte [7]:  ", 3, 13, 7)
    print "Got the following result:  ", result

    print "Test 2 for getSecureIntegers()..."
    result = getSecureIntegers("Zahl zwischen 3 und 13 bitte [7]:  ", 3, 13, 7)
    print "Got the following result:  ", result


## TRUE MAIN PROGRAM
#
## \cond false
if __name__ == '__main__':
    print "Running tests_mltihelpers.py\n"

    testGetSecureIntegers()
    
## \endcond
    
