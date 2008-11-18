# config.make (this is -*- Makefile -*- from nbg)
# 
# This is a makefile skeleton. In a lot of projects, this doesn't have
# to be modified at all. If you do have to or want to modify it,
# please let the comments guide you.
# 
#    Last Author: !!userinfo-fullname!! (<!!userinfo-email!!>)
#    Date of last change: !!actual-date!!
#
#    Revision: 0.1
#
#    Author:    !!userinfo-fullname!! (<!!userinfo-email!!>)
#    Date:      !!actual-date!!
#    Copyright: !!userinfo-fullname!!, Chair Prof. Dillmann (IAIM)
#               Institute for Computer Science and Engineering (CSE)
#	        University of Karlsruhe. All rights reserved
#	        http://wwwiaim.ira.uka.de


#
# Flags for compiler and linker:
#         "How exactly do I want the program to be built?
#

# MY_CCFLAGS: Additional arguments for the compiler.
MY_CCFLAGS+=

# MY_LDFLAGS: Additional arguments for the linker.
MY_LDFLAGS+=

# MY_IDLFLAGS: Additional arguments for the stubber.
MY_IDLFLAGS+=

#
# Include / Library specifications:
#         "What things other people have written go into the program?"
#

# MY_INCPATHS: Contains paths to additional include files.
MY_INCPATHS+=

# MY_LIBPATHS: Contains paths to additional libraries.
MY_LIBPATHS+=

# MY_IDLPATHS: Contains paths to additional IDL files.
MY_IDLPATHS+=

# MY_LIBS: Contains additional libraries the program is to be linked with.
MY_LIBS+=

# MY_TESTINCPATHS: Additional include paths for single-module tests.
MY_TESTINCPATHS=

# MY_TESTLIBPATHS: Additional library paths for single-module tests.
MY_TESTLIBPATHS=

# MY_TESTINCPATHS: Additional libraries for single-module tests.
MY_TESTLIBS=

# VERBOSE: Set this to "yes" to get more information about the build
# process (compiler and linker arguments, etc.)
VERBOSE=yes

# DEBUG: Set this to "no" to prevent generation of debugging
# info. Saves a bit in disk space.
DEBUG=yes

# AUTODOC: Set this to "no" to prevent automatical documentation
# generation. Saves a bit in compile time.
AUTODOC=no

# ESSENTIAL: Set this to "no" to continue compiling the parent project
# even if something in this subproject generated an error.
ESSENTIAL=yes

# USECORBA: Set this to "yes" if you don't have any IDL files but
# want to use CORBA anyway. If you do have IDL files, don't worry
# about this; having IDL files overrides this setting.
USECORBA=no

# USEQT: Set this to "yes" if you don't have any .moc or .ui files but
# want to use Qt anyway. If you do have .moc or .ui files, don't worry
# about this; having such files overrides this setting.
USEQT=no


#
# To differentiate more between linux / mac use the following or additional files:
#        config.make.linux / config.make.macos
#

ifeq (Linux, $(shell uname))
MY_CCFLAGS+=

MY_INCPATHS+=

MY_LIBPATHS+=

else
ifeq (Darwin, $(shell uname))
MY_LDFLAGS+=

MY_INCPATHS+=

MY_LIBPATHS+=

endif  # Darwin
endif  # Linux


ifeq ($(USEUNITTESTS),yes)
MY_INCPATHS+=/opt/local/include/cppunit/
MY_LIBPATHS+=/opt/local/lib
MY_LIBS+=cppunit
endif



