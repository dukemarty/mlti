/*! \if exist This is -*- C++ -*- from nbg \endif

    \file  !!file-name!!

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

/* system includes */
#include <assert.h>

/* my includes */
/* !!file-name!! */

!!class-name!!::!!class-name!!()
{

}

!!class-name!!::~!!class-name!!()
{
}


#if !!file-name!!_test
#include <stdio.h>
int main(int argc, char **argv)
{
  // This is a module-test block. You can put code here that tests
  // just the contents of this C file, and build it by saying
  //             make !nbg-module-name!_test
  // Then, run the resulting executable (!nbg-module-name!_test).
  // If it works as expected, the module is probably correct. ;-)

  fprintf(stderr, "Testing !!file-name!!\n");

  return 0;
}
#endif /* !!file-name!!_test */
