/* \if exist This is -*- C -*- from nbg \endif

   \file  !!file-name!!
   \brief 

   Please put your documentation for this file here.
   
   Last Author: !!userinfo-fullname!! (<!!userinfo-email!!>)
   Date of last change:  !!actual-date!!

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
#include <string>
#include <nbgcorba_impl.h>

/* my includes */
#include "!!class-name!!.hh"

class !!class-name!!_impl:
  public virtual POA_!!module-name!!::!!class-name!!,
  public virtual nbgcorba::base_impl
{
public:
  !!class-name!!_impl();
private:
  // CHANGE THIS:
  // Here are the variables that hold slot objects. The "defaultSlot"
  // is just an example. Delete it and put your stuff here.
  NEW_SLOTVAR(defaultSlot,nbgcorba::base_ptr);

  void setObjectForSlotPrivate(nbgcorba::base_ptr sender,
			       nbg::string slotname,
			       CORBA::Object_ptr obj)
    throw (nbgcorba::InvalidTypeError);
  nbg::strlist getInterfaceNamesPrivate(void);
};

#endif /* !!header-define-name!!_H */
