/*! \if exist This is -*- C++ -*- from nbg \endif

    \file  !!file-name!!
    \brief 

    Please put your documentation for this file here.

    \par Last Author: !!userinfo-fullname!! (<!!userinfo-email!!>)
    \par Date of last change:  !!actual-date!!

    \author   !!userinfo-fullname!! (<!!userinfo-email!!>)
    \date     !!actual-date!!
    \par Copyright:
               !!userinfo-fullname!!, Chair Prof. Dillmann (HIS)\n
	       Institute for Anthropomatics (IFA)\n
	       Karlsruhe Institute of Technology (KIT). All rights reserved\n
	       http://his.anthropomatik.kit.edu
*/

#ifndef !!header-define-name!!_H
#define !!header-define-name!!_H

/* system includes */
#include <string>

/* my includes */
#include <cppunit/TestFixture.h>
#include <cppunit/extensions/HelperMacros.h>


/*!
  \class !!class-name!!
  \brief


*/
class !!class-name!! : public CPPUNIT_NS::TestFixture {
  CPPUNIT_TEST_SUITE (!!class-name!!);
  CPPUNIT_TEST (MyNewTest);
  CPPUNIT_TEST_SUITE_END ();

 private:

protected:
  void MyNewTest(void);
  
public:
  void setUp(void);
  void tearDown(void);
};

#endif /* !!header-define-name!!_H */
