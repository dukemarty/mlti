/*! \if exist This is -*- C++ -*- from nbg \endif

    \file  !!file-name!!
    \brief 

    Please put your documentation for this file here.

    \par Last Author: !!userinfo-fullname!! (<!!userinfo-email!!>)
    \par Date of last change:  !!actual-date!!

    \author   !!userinfo-fullname!! (<!!userinfo-email!!>)
    \date     !!actual-date!!
    \par Copyright:
               !!userinfo-fullname!!, Chair Prof. Dillmann (IAIM)\n
               Institute for Computer Science and Engineering (CSE)\n
	       University of Karlsruhe. All rights reserved\n
	       http://wwwiaim.ira.uka.de
*/

#ifndef !!header-define-name!!_H
#define !!header-define-name!!_H

/* system includes */
#include <bgtools.h>

/* my includes */
#include <cppunit/TestFixture.h>
#include <cppunit/extensions/HelperMacros.h>


/*!
  \class !!class-name!!
  \brief


*/
class !!class-name!! : public CPPUNIT_NS::TestFixture {
  CPPUNIT_TEST_SUITE (!!class-name!!);
  CPPUNIT_TEST (!TestMethod!);
  CPPUNIT_TEST_SUITE_END ();
private:

protected:
  void !TestMethod!(void);
  
public:
  void setUp(void);
  void tearDown();
};

#endif /* !!header-define-name!!_H */
