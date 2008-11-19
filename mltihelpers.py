#! /usr/bin/python
# This is -*- Python -*- from nbg -*- coding: latin1 -*-
#
##   \file  mltihelpers.py
#    \brief In this file, some little helpers for the mlti project are assembled.
#
#    \par Last Author: Martin Loesch (loesch@@ira.uka.de)
#    \par Date of last change: 2008-11-18
#
#    \author   Martin Loesch (loesch@@ira.uka.de)
#    \date     2008-11-18
#    \par Copyright:
#              Martin Loesch, Chair Prof. Dillmann (IAIM)\n
#              Institute for Computer Science and Engineering (CSE)\n
#	       University of Karlsruhe. All rights reserved\n
#	       http://wwwiaim.ira.uka.de
#

## \namespace mltihelpers
# This namespace contains all absolutely not project specific helper classes, for example for more comfortable input.


## \brief Get integer in a certain range from command line.
#
# @param text command prompt shown to the user
# @param lowerbound minimum allowed number
# @param upperbound maximum allowed number
# @param default default number (if just ENTER is typed)
def getSecureInteger(text, lowerbound, upperbound, default):
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
def getYesOrNo(text, default=True):
    choice = raw_input(text)
    if choice=="":
        choice = default
    if choice==True or choice.lower()=="yes" or choice.lower()=="y":
        res = True
    else:
        res = False
    return res


## TRUE MAIN PROGRAM
#
## \cond false
if __name__ == '__main__':
    print "Testing mltihelpers.py\n"

## \endcond
    
