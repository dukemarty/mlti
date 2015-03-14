# MLTemplateInstaller

## Overview

The goal of this project is to provide the means of simple generation of skeleton files for basically every purpose where text-based files are used.

You can simply gather all your templates in one directory, and it is already possible to install the template into an arbitrary directory. By adding certain patterns into the template, the text substitution facilities can be used to adapt the template to its current application. To further adapt a certain template, special substitutions can be assigned by adding a .templ file (with the same name as the template) which contains substitutions described in a specific format.

## Usage

Usually, `mlti.py` is called for installing one or more templates into the current directory (although it is absolutely legal to use it for installation into an arbitrary directory). Called without an argument (or invalid arguments), the valid usage is shown:

    mlti.py templatename [target_filename [target_directory]]

The most important parameter is templatename, which can also be only a part of a valid template name (valid are all names which denote a template in one of the chosen template directories). E.g., the call

    mlti.py pyth

should normally result in at least two possible templates (namely for a python source file or a new python project). These two possibly meant templates are then presented to the user which can choose one or more of these template to be installed (or none, if the desired one is not amongst them). Templates can be chosen by one or more of the numbers associated with the template names.

The chosen templates are then installed into the current directory or, if the target_directory parameter was given, into the chosen directory (but be aware, a target_directory can only be given if also a target_filename is present, see below for details on this one). Installing means thereby copying the template to the chosen directory and doing the defined substitutions. If more than one template is installed, the same value is used for common substitutions (e.g. the same project name, author etc.).

In most cases, it is desirable to have the file(s) renamed, in particular because often the file name is also used inside the file for documentation purposes. To this means, the target_filename parameter can be used. There is a little bit a different usage of this parameter, depending on whether one or more templates are installed. If only one template ist installed, and the target name has a suffix, not only the name, but also the suffix is used when renaming the copied template. If no suffix is given or more than one template is installed, then the suffix of the template is used and only the base name given in the call is used for the renaming.
