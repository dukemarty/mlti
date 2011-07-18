# -*- cmake -*-
#
# Last Author: !!userinfo-fullname!! (<!!userinfo-email!!>)
# Date of last change: !!actual-date!!
#
# Author: !!userinfo-fullname!! (<!!userinfo-email!!>)
# Date: !!actual-date!!
#
# Copyright: !!userinfo-fullname!!, Chair Prof. Dillmann (HIS)
#            Institute for Anthropomatics (IFA)
#            Karlsruhe Institute of Technology (KIT). All rights reserved
#            http://his.anthropomatik.kit.edu


project(!!project-name!!)

cmake_minimum_required( VERSION 2.8 )

# set( CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/cmake/Modules/" )


find_package( Boost "1.37" REQUIRED COMPONENTS program_options thread )


# add_subdirectory( subproj )

include_directories(
  .
  )

set( !!project-name!!Headers

  )

set( !!project-name!!Sources

  )

add_executable( !!project-name!! ${!!project-name!!Headers} ${!!project-name!!Sources} )

#add_dependencies( !!project-name!!
#
#  )

#target_link_libraries( !!project-name!!
#
#  )

