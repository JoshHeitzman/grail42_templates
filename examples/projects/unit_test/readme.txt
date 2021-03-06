Overview
--------

  Demonstrates a skeletal unit test project targeting Android NDK, the Chrome Native Client SDK, 
  and the Windows SDK all the same Visual Studio 2010 project.  Both 32-bit and 64-bit platforms 
  are supported for Windows and Chrome Native Client (NaCl).
  
Use as a template
-----------------

  <grail42 root> - e.g. c:\grail42
  <python root> - e.g. c:\python27
  <projects root> - e.g. c:\myprojects
  <devenv path> - e.g. "C:\Program Files (x86)\Microsoft Visual Studio 10.0\Common7\IDE\devenv.exe"
  <batch file that set env vars required by Android and NaCl VS plug-ins> - batch file that sets:
  ANDROID_SDK_ROOT, ANDROID_NDK_ROOT, ANT_HOME, NACL_SDK_ROOT, CHROME_PATH, NACL_EXE_STDOUT,
  NACL_EXE_STDERR, and NACLLOG as per the instructions for the Android NDK and NaCl SDK.

  If you only desire to use the Win32 and/or x64 platforms, you can skip steps 1 and 7 and just open
  the solution normally and delete the Android and NaCl platforms.

  1. <batch file that set env vars required by Android and NaCl VS plug-ins>
  2. cd <grail42 root>\core\tools\windows_any\
  3. grail42set_env_core_python_2_x.cmd <python root>\python.exe
  4. cd <projects root>
  5. %grail42_python2_x_exe% %grail42_root%\templates\tools\python_2_x\clonetree.py %grail42_root%\templates\examples\projects\unit_test
  
    Modify the file that appears in notepad to be:

net\examples\unit_test<-===->net\examples\mytest
net.examples.unit_test<-===->net.examples.mytest
unit_test<-===->mytest
net_examples_unit_1test<-===->net_examples_mytest
  
    and close notepad saving the file.
  
  6. cd mytest
  7. <devenv path> mytest.sln
  
Dependencies
------------

  This project depends on the boost library and the Core subproject of the Grail42 poject located at
  https://github.com/JoshHeitzman/grail42 .  The Visual C++ includes need to contain the Grail42 
  Core header directory %grail42_core_root%\library\cpp\include .
  
  The project makes use of the Grail42 faux console app infrastructure for Android and NaCl that 
  allows the unit test executable to executed from a Windows command prompt.  For Android this is
  accomplished via the batch file %grail42_core_cmd%\android\faux_console\run_app.cmd supplied by 
  the Core subproject of Grail42 (see).  For NaCl this is
  via the batch files %grail42_core_cmd%\nacl\faux_console\run_nexe_in_chrome.cmd and 
  %grail42_core_cmd%\nacl\run_nexe_standalone.cmd also supplied by Grail42 Core.
  
  The Win32 platform configurations are configured to run the unit test executable as a post build
  step, and the NaCl64 platform will do so if grail42_core_cmd is defined.  Defining the env var
  GRAIL42_TEST_POST_BUILD_EXECUTION_DISABLE_ALL will prevent executing the executables as part of 
  the build.

Configuration|Platfrom Caveats and Notes
----------------------------------------

*|Android and *|PPAPI and *|NaCl*

The preprocessor define HWC_PLATFORM_ANDROID and HWC_PLATFORM_NACL included in the project file 
isn't necessary to build successfully, but its presence ensures the IDE pickups up the correct 
define.

*|Android

Defining the env var GRAIL42_TEST_POST_BUILD_EXECUTION_ENABLE_ANDROID will enable the unit test 
app to be executed as a post build step. Executing the Android unit tests is disabled by default
as the overall deployment and execution process isn't 100% reliable.

Release|Android

The Ant Build Type property is set to Debug rather than Release so that the apk will be signed 
with a debug key.  Setting the property to Release requires additional configuration or deployment 
will fail.

*|PPAPI

Stdout isn't redircted to %NACL_EXE_STDOUT% as it is for *|NaCl64.

*|NaCl32

The resultant binary has not been executed by the author, and is included simply for completeness.

*|x64

Defining the env var GRAIL42_TEST_POST_BUILD_EXECUTION_ENABLE_X64 will enable the unit test app 
to be executed as a post build step. Executing the x64 unit tests is disabled by default to 
provide a Win target that doesn't run the tests to allow starting under the debuggeer without
it first being executed (such as if the EXE hangs).

--------------------------------------------------------------------------------

                   Copyright (C) 2012 Josh Heitzman
Distributed under the Boost Software License, Version 1.0.
See accompanying file LICENSE_1_0.txt or online copies at:
* http://www.boost.org/LICENSE_1_0.txt
* http://opensource.org/licenses/BSL-1.0
* http://directory.fsf.org/wiki/License:Boost1.0
* http://en.wikipedia.org/wiki/Boost_Software_License                
