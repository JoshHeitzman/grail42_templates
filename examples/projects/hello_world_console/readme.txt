Overview
--------

  Demonstrates targeting the Android NDK, the Chrome Native Client SDK, and the 
  Windows SDK all from the same Visual Studio 2010 project.  Both 32-bit and 
  64-bit platforms are supported for Windows and Chrome Native Client (NaCl).
  
  Also demonstrates creating a faux console app for Android that allows the apps 
  stdout to be easily emitted in a Windows command prompt via the batch file 
  %grail42_core_cmd%\android\faux_console\run_app.cmd supplied by the Grail42 
  Core sibling project (see the Grail42 project referenced above).
  
  The NaCl platform is configured by default to run from the standalone 
  commandline tool sel_ldr*.exe rather than from Chrome to provide a consistent 
  console experience.  When run in Chrome, the project demonstrates doing so 
  as a faux console app that allows the plug-ins stdout to be easily emitted 
  in a Windows command prompt via the batch file that also starts and stops 
  the necessary simple web server.  The batch file is supplied by the Grail42 
  Core project at %grail42_core_cmd%\nacl\faux_console\run_nexe_in_chrome.cmd 
  and %grail42_core_cmd%\nacl\run_nexe_standalone.cmd provides a convienence 
  batch file o run the plug-in standalone in sel_ldr*.exe

Configuration|Platfrom Caveats and Notes
----------------------------------------

*|Android and *|PPAPI and *|NaCl*

The preprocessor define HWC_PLATFORM_ANDROID and HWC_PLATFORM_NACL included in 
the project file isn't necessary to build successfully, but its presence ensures 
the IDE pickups up the correct define.

Release|Android

The Ant Build Type property is set to Debug rather than Release so that the apk 
will be signed with a debug key.  Setting the property to Release requires 
additional configuration or deployment will fail.

*|PPAPI

Stdout isn't redircted to %NACL_EXE_STDOUT% as it is for *|NaCl64.

*|NaCl32

The resultant binary has not been executed by the author, and is included
simply for completeness.

--------------------------------------------------------------------------------

                   Copyright (C) 2012 Josh Heitzman
Distributed under the Boost Software License, Version 1.0.
See accompanying file LICENSE_1_0.txt or online copies at:
* http://www.boost.org/LICENSE_1_0.txt
* http://opensource.org/licenses/BSL-1.0
* http://directory.fsf.org/wiki/License:Boost1.0
* http://en.wikipedia.org/wiki/Boost_Software_License                
