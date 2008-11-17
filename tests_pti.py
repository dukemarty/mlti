#! /usr/bin/python
# This is -*- Python -*- from nbg -*- coding: latin1 -*-
#
##   \file  pti-tests.py
#    \brief This file contains unit tests for the pti project.
#
#    Last Author: Martin Loesch (loesch@ira.uka.de)
#    Date of last change: 2008-11-14
#
#    \author   Martin Loesch (loesch@ira.uka.de)
#    \date     2008-11-14
#    \par Copyright:
#              Martin Loesch, Chair Prof. Dillmann (IAIM)\n
#              Institute for Computer Science and Engineering (CSE)\n
#	       University of Karlsruhe. All rights reserved\n
#	       http://wwwiaim.ira.uka.de
#

import unittest
import os, datetime
from pti import *

class TestTemplateSubstitutionClass(unittest.TestCase):

    test_template_file_correct = "testcorrect.templ"
    test_template_file_false1 = "testfalse1.templ"
    test_template_file_false2 = "testfalse2.templ"
    
    def setUp(self):
        self.generateTestfiles()

    def tearDown(self):
        self.removeTestfiles()

    def generateTestfiles(self):
        f = open(self.test_template_file_correct, 'w')
        f.write("!!testvar1!!     #!# s #!# foobarfoobarfoobar\n")
        f.write("!!mytest-var2!! #!# f #!#   datetime.date.today().isoformat()\n")
#        f.write("!!my3!!            #!# a #!# MyDefaultValue\n")
        f.write("!!mytest-var4!! #!#f#!#   datetime.date.today().isoformat()\n")
        f.close()
        f = open(self.test_template_file_false1, 'w')
        f.write("!!testvar1!!     #!# s ##\n")
        f.write("!!mytest-var2!! #!# f #!#   datetime.date.today().isoformat()\n")
        f.write("!!my3!!            #!# a #!# MyDefaultValue")
        f.close()
        f = open(self.test_template_file_false2, 'w')
        f.write("!!testvar1!!     #!# s #!# foobarfoobarfoobar\n")
        f.write("!!mytest-var2!! #!# f #!#   datetime.date.today().isoformat()\n")
        f.write(" #!# a #!# MyDefaultValue\n")
        f.close()

    def removeTestfiles(self):
        os.remove(self.test_template_file_correct)
        os.remove(self.test_template_file_false1)
        os.remove(self.test_template_file_false2)
        
    def testConstructor(self):
        t1 = TemplateSubstitutions()
        t2 = TemplateSubstitutions("hallo.txt")
        self.assertEqual(t1.provided_resultfilename, "")
        self.assertEqual(t2.provided_resultfilename, "hallo.txt")

    def testPerformSubstitutions(self):
        t = TemplateSubstitutions()
        orig = "Das ist irgend ein blabla Text.\n Irgendwo hier sind Variablen versteckt, wie etwa !!userinfo-fullname!! hähä\n\n"
        res = t.performSubstitutions(orig)
        self.assertEqual(res, "Das ist irgend ein blabla Text.\n Irgendwo hier sind Variablen versteckt, wie etwa Martin Loesch hähä\n\n")
        
    def testLoadAdditionalSubstitutions(self):
        t = TemplateSubstitutions()
        t.loadAdditionalSubstitutions(self.test_template_file_correct)
        orig = ""
        res = t.performSubstitutions(orig)
        self.assertEqual(res, "")
        tcorr = TemplateSubstitutions()
        tfalse1 = TemplateSubstitutions()
        tfalse2 = TemplateSubstitutions()
        self.assertRaises(SubstitutionsFileFormatException, tfalse1.loadAdditionalSubstitutions, self.test_template_file_false1)
        self.assertRaises(SubstitutionsFileFormatException, tfalse2.loadAdditionalSubstitutions, self.test_template_file_false2)
        

class TestTemplateInstallerClass(unittest.TestCase):

    def testConstructor(self):
        print "Not implemented yes"
        # 1. construct unique temporary file, delete it -> name does not exist
        # 2. construct with this file -> should not be valid
        # 3. construct temp file
        # 4. fill file
        # 5. construct object with it -> should be valid
        # 6. delete file


## TRUE MAIN PROGRAM
#
#
#
if __name__ == '__main__':
    print "Performing unit tests for pti.py ...\n"

    suite = unittest.TestLoader().loadTestsFromTestCase(TestTemplateSubstitutionClass)

    unittest.TextTestRunner(verbosity=2).run(suite)
