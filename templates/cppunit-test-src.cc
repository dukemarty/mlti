/*! \if exist This is -*- C++ -*- from nbg \endif

    \file  !!file-name!!

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

/* system includes */
#include <assert.h>

/* my includes */
#include "!!header-name!!"


CPPUNIT_TEST_SUITE_REGISTRATION(!!class-name!!);


void !!class-name!!::setUp(void)
{
}

void !!class-name!!::tearDown(void)
{
}

void !!class-name!!::MyNewTest(void)
{

}


#if !!file-base-name!!_test
#include <stdio.h>
int main(int argc, char **argv)
{
  // This is a module-test block. You can put code here that tests
  // just the contents of this C file, and build it by saying
  //             make !!file-base-name!!_test
  // Then, run the resulting executable (!!file-base-name!!_test).
  // If it works as expected, the module is probably correct. ;-)

  fprintf(stderr, "Testing !!file-base-name!!\n");

  return 0;
}
#endif /* !!file-base-name!!_test */
