#                  Copyright (C) 2012 Josh Heitzman
# Distributed under the Boost Software License, Version 1.0.
# See accompanying file LICENSE_1_0.txt or online copies at:
# * http://www.boost.org/LICENSE_1_0.txt
# * http://opensource.org/licenses/BSL-1.0
# * http://directory.fsf.org/wiki/License:Boost1.0
# * http://en.wikipedia.org/wiki/Boost_Software_License

# Load annotations for all files and directories in the source directory tree.
# 
# Section names and their aliases to be replaced in paths and files are:
# *[application.ide.vs.project.identifier]
# *[application.ide.vs.solution.identifier]
# *[application.ide.vs.solution.filter.identifier]
# *[logical.component.identifier]
#
# Remove lines that contain:
#    - CopyrightNotice[linepart*]

editing_instructions = ("""
Please modify each right hand value in the list of pairs that follows and then
close this editor process.

Each pair is seperated by '<-===->'.  Only the right hand value should be 
modified.  Modifying the seperator or the left hand value will result in an 
error.  Any modification to whitespace in right hand values will be reflected
in the final output.
""")

# Create a .txt file in the user's temporary directory, add editing instructions
# for the user, add a name value pair for the project path, then append the 
# pairs to the temp text file, open it using the default .txt editor, and wait 
# for the process to exit.

# Validate that all name value pairs in the template are present in the user
# edited text file, and that the right hand side of each has been changed.

# Use the values to modify the necessary file and directory names.

# Create the new directory structure.

# Load each source file, process each line making the necessary replacments, 
# and then write the processed lines to the destination.


