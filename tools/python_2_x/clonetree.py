#                  Copyright (C) 2012 Josh Heitzman
# Distributed under the Boost Software License, Version 1.0.
# See accompanying file LICENSE_1_0.txt or online copies at:
# * http://www.boost.org/LICENSE_1_0.txt
# * http://opensource.org/licenses/BSL-1.0
# * http://directory.fsf.org/wiki/License:Boost1.0
# * http://en.wikipedia.org/wiki/Boost_Software_License

import sys
import os.path
import re
import sets
import tempfile
import subprocess
import uuid

from grail42.core import annot
from grail42.core.ease import invoke

requireAllPairsChanged = True
verbosity = 0 # 1 Useful for debugging.  TODO pick this up from an environment variable.

def print_usage_and_exit(error_msg=None):
    if error_msg is not None:
        print "ERROR:", error_msg
    print """Clones an annotated project making token replacements as directed.
    
    clonetree.py target
    
    target       The root directory of the project to clone.
    
    The destination will be a new subdirectory created in the current workding 
    directory.
    
    For example:
    %grail_python2_x_exe% clonetree.py %grail42_root%\templates\examples\projects\hello_world_console
    """
    exit(1)

# Steps for testing this script:
# 1. cd /d %temp%
# 2. %grail_python2_x_exe% %grail42_root%\templates\tools\python_2_x\clonetree.py %grail42_root%\templates\examples\projects\hello_world_console >clonetree.expected.txt
# 3. Make changes that need to be tested
# 4. %grail_python2_x_exe% %grail42_root%\templates\tools\python_2_x\clonetree.py %grail42_root%\templates\examples\projects\hello_world_console >out.txt
# 5. "%ProgramFiles(x86)%\Microsoft SDKs\Windows\v7.0A\Bin\windiff.exe" clonetree.expected.txt out.txt
#
# Repeat steps 3-5 as needed.

def get_files_and_annotations(target):
    make_query = annot.prepare_query_maker(
        local_filesytem_limits=(annot.prepare_query_maker.local_filesytem_limits_tree,), 
        filters=(annot.prepare_query_maker.local_filesytem_gitignore_pruner,))
    local_filesystem_query = make_query(trees=(target,))
    results = local_filesystem_query()
    annotations_for_elements = results['annotations_for_elements']
    
    # Only one set of annotations is expected for all files in the target directory
    # tree, so none should be present just for specific files, directories, or
    # or the contents of a directory.
    assert 'dirs' not in annotations_for_elements
    assert 'files' not in annotations_for_elements
    assert 'contents_of_dirs' not in annotations_for_elements
    annotations_for_trees = annotations_for_elements['trees']
    assert len(annotations_for_trees) == 1
    assert len(annotations_for_trees[target]) == 1
    
    # Since only one tree was provided and that entire tree is expected to be
    # annotated, there should not be any unannotated elements.
    assert 'unannotated_elements' not in results
    
    annotations = annotations_for_trees[target][0]
    
    # Remove the part of the path that isn't specific to the project, so that
    # it will not be modified by replacements.  It will be added back after
    # replacement.  Then the partial paths and filenames to get the portion
    # of the full file path that should be subjected to replacement.
    sourceFiles = []
    for path, names_for_path in results['annotated_elements']:
        path = path[len(sourcedir)+1:] # +1 to remove the path seperator not included in sourcedir
        filenames_for_path = names_for_path.get('filenames')
        if filenames_for_path is not None:
            sourceFiles.extend(
                [path + os.path.sep + filename for filename in filenames_for_path])
    assert sourceFiles
    
    return annotations, sourceFiles

class AccumulateStringsToReplace():
    subkeys_of_interest = (
        'application.ide.vs.project.identifier',
        'application.ide.vs.solution.identifier',
        'application.ide.vs.solution.filter.identifier',
        'abstract.component.identifier',
        'filesystem.file.name.complete.without.extension',
        'filesystem.directory.name.complete',
        'c.headerguard.partial'
        )
    def __init__(self):
        self.toReplace = sets.Set()
        self.toRegenerate = sets.Set()
    @staticmethod
    def _has_subkey(get_subkey, subkey):
        return invoke.try_except(lambda: get_subkey(subkey))
    @classmethod
    def _try_getting_subkeys_of_interest(cls, get_subkey):
        for subkey in cls.subkeys_of_interest:
            if cls._has_subkey(get_subkey, subkey):
                return True
        return False
    def __call__(self, key, get_subkey):
        if self._try_getting_subkeys_of_interest(get_subkey):
            if not self._has_subkey(get_subkey, 'uuid.random'):
                self.toReplace.add(key)
                try:
                    self.toReplace.update(get_subkey('aliases'))
                    pass
                except:
                    pass
            else:
                if self._has_subkey(get_subkey, 'aliases'):
                    raise Exception("Regenerating aliased GUIDs is not supported yet.")
                self.toRegenerate.add(key)

# REVIEW refactor and move to core to make it available for general use?
def append_guid_find_replace_pairs(strings_to_replace_accmulator, find_replace_pairs):
    # TODO support for additional GUID formats
    hex_with_4_dashes_guid_spec = re.compile(
        "^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}$")
    hex_lower_with_4_dashes_guid_spec = re.compile(
        "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")
    hex_guid_spec = re.compile(
        "^[0-9A-Fa-f]{32}$")
    hex_lower_guid_spec = re.compile(
        "^[0-9a-f]{32}$")
    # regex spec, lower, 4 dashes
    guid_specs = (
        (hex_lower_with_4_dashes_guid_spec, True, True),
        (hex_with_4_dashes_guid_spec, False, True),
        (hex_lower_guid_spec, True, False),
        (hex_guid_spec, False, False),
        )
    for random_guid in strings_to_replace_accmulator.toRegenerate:
        for spec in guid_specs:
            if spec[0].match(random_guid):
                _, lower, dashes4 = spec
                break
        else:
            raise Exception("Unknown random GUID specification.")
        new_guid = str(uuid.uuid4()) if dashes4 else uuid.uuid4().hex
        if not lower:
            new_guid = new_guid.upper()
        find_replace_pairs.append((random_guid, new_guid)) 

def create_and_write_control_file(editing_instructions, strings_to_replace, mapping_delimiter):
    controlFileHandle, controlFilename = tempfile.mkstemp(text=True, suffix='.txt')    
    controlFile = os.fdopen(controlFileHandle, 'w')    
    controlFile.write(editing_instructions)
    controlFile.write("\n\n\n")
    for string_to_replace in strings_to_replace:
        controlFile.write(string_to_replace)
        controlFile.write(mapping_delimiter)
        controlFile.write(string_to_replace)
        controlFile.write("\n\n")
    controlFile.flush()
    controlFile.close()
    return controlFilename

def read_and_delete_control_file(controlFilename, strings_to_replace, mapping_delimiter):
    controlFile = open(controlFilename)
    find_replace_pairs = []
    for line in controlFile.readlines():
        if mapping_delimiter in line:
            lhs, rhs = line.rstrip('\n\r').split(mapping_delimiter)
            if lhs in strings_to_replace:
                if requireAllPairsChanged and lhs == rhs:
                    controlFile.close()
                    os.remove(controlFilename)
                    print_usage_and_exit("Not all mapping pairs were modified.")
                find_replace_pairs.append((lhs, rhs))
                if verbosity >= 2:
                    print "find:", lhs
                    print "replace:", rhs
                    print
    controlFile.close()
    os.remove(controlFilename)
    if len(strings_to_replace) != len(find_replace_pairs):
        print_usage_and_exit("Not all mapping pairs were present in the modified file.")
    return find_replace_pairs

def find_and_replace(text, find_replace_pairs):
    text_parts = [(True, text),]
    for find, replace in find_replace_pairs:
        # NOTE While tThis isn't a performance optimal implementation, but 
        # it's simple and perf isn't currently an issue.
        text_parts_old = text_parts
        text_parts = []
        find_token = re.compile("("+re.escape(find)+")")
        for original_text_part_pair in text_parts_old:
            if not original_text_part_pair[0]:
                text_parts.append(original_text_part_pair)
            else:
                for part in find_token.split(original_text_part_pair[1]):
                    text_parts.append((False, replace) if part == find else (True, part))
    return "".join([pair[1] for pair in text_parts])

def make_dirs_and_write_files(source_dest_file_pairs, find_replace_pairs):
    for source, dest in source_dest_file_pairs:
        if verbosity >= 1:
            print "source: ", source
            print "dest  : ", dest
            print
        destdir = os.path.dirname(dest)
        if not os.path.exists(destdir):
            os.makedirs(destdir)
        sourcefile = open(source, 'r')
        destfile = open(dest, 'w')
        for sourceline in sourcefile.readlines():
            skip = False
            for partial in partial_lines_to_remove:
                if partial in sourceline:
                    skip = True
                    break            
            if skip:
                if verbosity >= 1:
                    print "skipped sourceline: ", sourceline.rstrip()
                continue
            destline = find_and_replace(sourceline, find_replace_pairs)
            if verbosity >= 1:
                if sourceline != destline:
                    print "sourceline: ", sourceline.rstrip()
                    print "destline  : ", destline.rstrip()
                    print
            destfile.write(destline)
        sourcefile.close()
        destfile.close()

if __name__ != '__main__':
    print_usage_and_exit("This file is only expected to be run as a script, and is not "
                         "intended to be loaded as a module.")

target = sys.argv[1]

# Included as Wing IDE doesn't expand env vars in arguments before providing 
# the arguments to the script.
target = os.path.expandvars(target)

if not os.path.exists(target):
    print_usage_and_exit("The target directory does not exist.  Target directory provided: "+target)

target = os.path.abspath(target)
sourcedir = os.path.dirname(target)
destdir = os.getcwd()

#
# Do all of the processing necessary to to generate the control file for the
# user to edit.
#

annotations, sourceFiles = get_files_and_annotations(target)

if not 'grail42_clone_retain_copyright_notice' in os.environ:
    partial_lines_to_remove = annotations.get(('legal.copyright.notice', 'partial_lines'))
else:
    partial_lines_to_remove = tuple()

strings_to_replace_accmulator = AccumulateStringsToReplace()
annotations.for_each_key(strings_to_replace_accmulator)
strings_to_replace = tuple(strings_to_replace_accmulator.toReplace)

#
# Generate the control file as a temporary file and then open it with notepad
# and wait for the user close notepad.  Then process the file and create the
# list of pairs to be used to find and replace strings in file paths and the
# lines of the content text files.
#

mapping_delimiter = '<-===->'

editing_instructions = """
Please modify each right hand value in the list of pairs that follows and then
close this editor process.

Each pair is seperated by '"""+mapping_delimiter+"""'.  Only the right hand value should be 
modified.  Modifying the seperator or the left hand value will result in an 
error.  Any modification to whitespace in right hand values will be reflected
in the final output.
"""

controlFilename = create_and_write_control_file(
    editing_instructions, strings_to_replace, mapping_delimiter)

subprocess.call([os.path.expandvars(r"%windir%\system32\notepad.exe"), controlFilename])

find_replace_pairs = read_and_delete_control_file(controlFilename, strings_to_replace, mapping_delimiter)

append_guid_find_replace_pairs(strings_to_replace_accmulator, find_replace_pairs)

# sort the string from longest to shortest, so that shorter strings, which may
# be a subset of longer strings, are only replaced after the longer string.
find_replace_pairs.sort(cmp=lambda x,y: len(y[0]) - len(x[0]))

#
# Finally do the replacements necessary to forming the destination file paths,
# create any destination directories that do no exist already, and then read
# in the source files lines, make necessary replacements to each line, and then
# write out the lines.
#

source_dest_file_pairs = [(sourcedir + os.path.sep + sourceFile, destdir + os.path.sep + find_and_replace(sourceFile, find_replace_pairs)) for sourceFile in sourceFiles]

make_dirs_and_write_files(source_dest_file_pairs, find_replace_pairs)
