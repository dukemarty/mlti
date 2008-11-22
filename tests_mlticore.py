#! /usr/bin/python
# This is -*- Python -*- from nbg -*- coding: latin1 -*-
#
##   \file  tests_mlticore.py
#    \brief This file contains unit tests for the mlticore module of the mlti project.
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
from mlticore import *


class TestSubstitutionsFileFormatException(unittest.TestCase):

    def suite():
        tests = ['testConstructor', 'test2str']
        return unittest.TestSuite(map(TestSubstitutionsFileFormatException, tests))
    suite = staticmethod(suite)
    
    def setUp(self):
        self.e1 = SubstitutionsFileFormatException("blabla1")
        self.e2 = SubstitutionsFileFormatException("blabla2", 13)
        self.e3 = SubstitutionsFileFormatException("blabla3", -123)
    
    def testConstructor(self):
        self.assertEqual(self.e1.cause, "blabla1")
        self.assertEqual(self.e1.linenumber, 0)
        self.assertEqual(self.e2.cause, "blabla2")
        self.assertEqual(self.e2.linenumber, 13)
        self.assertEqual(self.e3.cause, "blabla3")
        self.assertEqual(self.e3.linenumber, -123)

    def test2str(self):
        self.assertEqual(str(self.e1), "blabla1 in line 0")
        self.assertEqual(str(self.e2), "blabla2 in line 13")
        self.assertEqual(str(self.e3), "blabla3 in line -123")

        
class TestTemplateSubstitutionClass(unittest.TestCase):

    test_template_file_correct = "testcorrect.templ"
    test_template_file_false1 = "testfalse1.templ"
    test_template_file_false2 = "testfalse2.templ"

    def suite():
        tests = ['testConstructor', 'testSetExternalInformation', 'testPerformSubstitutions', 'testLoadAdditionalSubstitutions', 'testGetVarVal']
        return unittest.TestSuite(map(TestTemplateSubstitutionClass, tests))
    suite = staticmethod(suite)
        
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
        t1 = TemplateSubstitutions("myname1", "myemail1")
        t2 = TemplateSubstitutions("myname2", "myemail2","hallo.txt")
        self.assertEqual(t1.provided_resultfilename, "")
        self.assertEqual(t1.user_name, "myname1")
        self.assertEqual(t1.user_email, "myemail1")
        self.assertEqual(t2.provided_resultfilename, "hallo.txt")
        self.assertEqual(t2.user_name, "myname2")
        self.assertEqual(t2.user_email, "myemail2")

    def testSetExternalInformation(self):
        t = TemplateSubstitutions("myname", "andmyemail")
        self.assertEqual(t.user_name, "myname")
        self.assertEqual(t.user_email, "andmyemail")
        self.assertEqual(t.provided_resultfilename, "")
        t.setExternalInformation(resultfilename="blabla1")
        self.assertEqual(t.user_name, "myname")
        self.assertEqual(t.user_email, "andmyemail")
        self.assertEqual(t.provided_resultfilename, "blabla1")
        
        
    def testPerformSubstitutions(self):
        t = TemplateSubstitutions("myname", "myemail")
        orig = "Das ist irgend ein blabla Text.\n Irgendwo hier sind Variablen versteckt, wie etwa !!userinfo-fullname!! hähä\n\n"
        res = t.performSubstitutions(orig)
        self.assertEqual(res, "Das ist irgend ein blabla Text.\n Irgendwo hier sind Variablen versteckt, wie etwa myname hähä\n\n")
        
    def testLoadAdditionalSubstitutions(self):
        t = TemplateSubstitutions("myname", "myemail")
        t.loadAdditionalSubstitutions(self.test_template_file_correct)
        orig = ""
        res = t.performSubstitutions(orig)
        self.assertEqual(res, "")
        tcorr = TemplateSubstitutions("myname", "myemail")
        tfalse1 = TemplateSubstitutions("myname", "myemail")
        tfalse2 = TemplateSubstitutions("myname", "myemail")
        self.assertRaises(SubstitutionsFileFormatException, tfalse1.loadAdditionalSubstitutions, self.test_template_file_false1)
        self.assertRaises(SubstitutionsFileFormatException, tfalse2.loadAdditionalSubstitutions, self.test_template_file_false2)

    def testGetVarVal(self):
        t = TemplateSubstitutions("myname", "my@email.com", "/org/share/myresfile.ext")
        self.assertEqual(t.getVarVal("!!userinfo-fullname!!"), "myname")
        self.assertEqual(t.getVarVal("!!userinfo-email!!"), "my@email.com")
        self.assertEqual(t.getVarVal("!!file-name!!"), "myresfile.ext")

        
class TestTemplateInstallerClass(unittest.TestCase):

    templfile_correct1 = "blablacorr1.cc"
    templtemplfile_correct1 = "blablacorr1.templ"
    templfile_correct2 = "blablacorr2.cc"
    filenamepattern_correct = "bla"
    filenamepattern_false = "zyxw"
    testtarget1 = "unittesttarget1.cc"
    
    def suite():
        tests = ['testConstructor', 'testCheckTemplateExistance','testFindCandidateTemplates',
                 'getGetCandidateNameList', 'testChooseCandidate', 'testInstall',
                 'testDoSubstitutionsUpdateSubstitutions']
        return unittest.TestSuite(map(TestTemplateInstallerClass, tests))
    suite = staticmethod(suite)

    def setUp(self):
        self.generateTemplFiles()
        
    def tearDown(self):
        self.removeTemplFiles()

    def generateTemplFiles(self):
        templfile_correct1 = os.path.join(default_template_directory, self.templfile_correct1)
        tsrc1 = open(templfile_correct1, 'w')
        tsrc1.write("Foobar template with !!SPECIALSUB1!! \n\nIn here, there is just some !!SPECIALSUB2!! text ...")
        tsrc1.close()
        templtemplfile_correct1 = os.path.join(default_template_directory, self.templtemplfile_correct1)
        ttmpl1 = open(templtemplfile_correct1, 'w')
        ttmpl1.write("!!SPECIALSUB1!! #!# s #!# FIRST INSERTED TEXT\n!!SPECIALSUB2!!   #!#s#!# SECOND INSERTED TEXT   \n\n")
        ttmpl1.close()
        templfile_correct2 = os.path.join(default_template_directory, self.templfile_correct2)
        tsrc2 = open(templfile_correct2, 'w')
        tsrc2.write("Foobar template with !!SPECIALSUB1!! \n\nIn here, there is just some !!SPECIALSUB2!! text ...")
        tsrc2.close()

    def removeTemplFiles(self):
        os.remove(os.path.join(default_template_directory,self.templfile_correct1))
        os.remove(os.path.join(default_template_directory,self.templtemplfile_correct1))
        os.remove(os.path.join(default_template_directory,self.templfile_correct2))
        
    def testConstructor(self):
        ti_correct = TemplateInstaller(self.templfile_correct1)
        ti_halfcorrect = TemplateInstaller(self.filenamepattern_correct)
        ti_false = TemplateInstaller(self.filenamepattern_false)
        self.assertEqual(ti_correct.valid, True)
        self.assertEqual(ti_halfcorrect.valid, False)
        self.assertNotEqual(ti_halfcorrect.candidates, [])
        self.assertEqual(ti_false.valid, False)
        self.assertEqual(ti_false.candidates, [])

    def testCheckTemplateExistance(self):
        ti_correct = TemplateInstaller(self.templfile_correct1)
        ti_halfcorrect = TemplateInstaller(self.filenamepattern_correct)
        ti_false = TemplateInstaller(self.filenamepattern_false)
        self.assertEqual(ti_correct.checkTemplateExistence(), True)
        self.assertEqual(ti_halfcorrect.checkTemplateExistence(), False)
        self.assertEqual(ti_false.checkTemplateExistence(), False)

    def testFindCandidateTemplates(self):
        ti_halfcorrect = TemplateInstaller(self.filenamepattern_correct)
        ti_false = TemplateInstaller(self.filenamepattern_false)
        self.assertEqual(ti_false.candidates, [])
        self.assertEqual(ti_halfcorrect.candidates, [(default_template_directory, self.templfile_correct1), (default_template_directory, self.templfile_correct2)])

    def getGetCandidateNameList(self):
        ti_halfcorrect = TemplateInstaller(self.filenamepattern_correct)
        ti_false = TemplateInstaller(self.filenamepattern_false)
        self.assertEqual(ti_false.getCandidateNameList(), [])
        self.assertEqual(ti_halfcorrect.getCandidateNameList(), [self.templfile_correct1, self.templfile_correct2])
        
    def testChooseCandidate(self):
        ti_halfcorrect = TemplateInstaller(self.filenamepattern_correct)
        self.assertEqual(ti_halfcorrect.valid, False)
        self.assertEqual(ti_halfcorrect.template_name, self.filenamepattern_correct)
        self.assertRaises(IndexError, ti_halfcorrect.chooseCandidate, -1)
        self.assertRaises(IndexError, ti_halfcorrect.chooseCandidate, -10)
        self.assertRaises(IndexError, ti_halfcorrect.chooseCandidate, 2)
        self.assertRaises(IndexError, ti_halfcorrect.chooseCandidate, 19)
        ti_halfcorrect.chooseCandidate(0)
        self.assertEqual(ti_halfcorrect.valid, True)
        self.assertEqual(ti_halfcorrect.template_name, self.templfile_correct1)

    def testInstall(self):
        targetpath = os.path.join(default_template_directory, "unittestdirectory")
        os.mkdir(targetpath)
        ti1 = TemplateInstaller(self.templfile_correct1)
        ti1.install(targetpath, self.testtarget1)
        file1 = open(os.path.join(targetpath, self.testtarget1))
        self.assertEqual(file1.readline(), "Foobar template with FIRST INSERTED TEXT \n")
        file1.readline()
        self.assertEqual(file1.readline(), "In here, there is just some SECOND INSERTED TEXT text ...")
        file1.close()
        os.remove(os.path.join(targetpath, self.testtarget1))
        os.rmdir(targetpath)
        
    def testDoSubstitutionsUpdateSubstitutions(self):
        ti1 = TemplateInstaller(self.templfile_correct1)
        ti2 = TemplateInstaller(self.templfile_correct2)
        ti1.doSubstitutions(os.path.join(default_template_directory,self.templfile_correct1))
        ti2.doSubstitutions(os.path.join(default_template_directory,self.templfile_correct2))
        file1 = open(os.path.join(default_template_directory,self.templfile_correct1))
        self.assertEqual(file1.readline(), "Foobar template with FIRST INSERTED TEXT \n")
        file1.readline()
        self.assertEqual(file1.readline(), "In here, there is just some SECOND INSERTED TEXT text ...")
        file1.close()
        file2 = open(os.path.join(default_template_directory,self.templfile_correct2))
        self.assertEqual(file2.readline(), "Foobar template with !!SPECIALSUB1!! \n")
        file2.readline()
        self.assertEqual(file2.readline(), "In here, there is just some !!SPECIALSUB2!! text ...")
        file2.close()
        
        
## TRUE MAIN PROGRAM
#
#
#
if __name__ == '__main__':
    print "Performing unit tests for mlti.py ...\n"

    alltests = unittest.TestSuite([TestSubstitutionsFileFormatException.suite(), TestTemplateSubstitutionClass.suite(), TestTemplateInstallerClass.suite()])

    unittest.TextTestRunner(verbosity=2).run(alltests)
