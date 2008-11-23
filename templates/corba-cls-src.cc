/*! \if exist This is -*- C++ -*- from nbg \endif

    \file !!file-name!!

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

/* system includes */
/* (none) */

/* my includes */
#include "!!class-name!!_impl.h"

!!class-name!!_impl::!!class-name!!_impl()
{
  // CHANGE THIS:
  // This defines the slots that this object has. newSlot() creates
  // a new slot. The first argument is the name of the slot, the
  // second the class name, and the third argument is the
  // documentation.
  // The "DefaultSlot" is just an example. Delete it and put your
  // stuff here.
  newSlot("DefaultSlot", "nbgcorba.base",
	  "Example slot. This doesn't really do anything.");
}

// CHANGE THIS:
// This method gets called when somebody calls "setObjectForSlot()"
// on this object. Adapt it to fill the slots defined above, do
// error checking and cleanup.
void
!!class-name!!_impl::setObjectForSlotPrivate(nbgcorba::base_ptr sender,
					      nbg::string slotname,
					      CORBA::Object_ptr obj)
  throw (nbgcorba::InvalidTypeError)
{
  // Update the slot variables here like this:
  if(slotname == "DefaultSlot")
    {
      // Check if the type is correct, and throw an exception if it
      // isn't.
      nbgcorba::base_ptr tmp = nbgcorba::base::_narrow(obj);
      if(CORBA::is_nil(tmp)) throw nbgcorba::InvalidTypeError();
      
      // Set the slot variable, protected by a lock.
      LOCK_SLOT(defaultSlot);   // IMPORTANT!
      defaultSlot = tmp;
      UNLOCK_SLOT(defaultSlot); // IMPORTANT!
    }
}
  
// DON'T CHANGE THIS:
// This method is used to identify this class. It should have been
// filled automatically by Emacs.
nbg::strlist
!!class-name!!_impl::getInterfaceNamesPrivate(void)
{
  return nbg::strlist("nbgcorba.base",
		      "!!module-name!!.!!class-name!!",
		      NULL);
}

#if !!class-name!!_impl_test
int main(int argc, char **argv)
{
  nbgcorba::init(argc, argv);
  
  // Create a new instance of the implementation 
  !!class-name!!_impl *impl = new !!class-name!!_impl;

  int retval =  nbgcorba::main(impl);

  delete impl;

  return retval;
}
#endif /* !!class-name!!_impl_test */

