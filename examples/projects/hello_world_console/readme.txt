Configuration|Platfrom Caveats and Notes
----------------------------------------

*|Android and *|PPAPI and *|NaCl*

The preprocessor define HWC_PLATFORM_ANDROID and HWC_PLATFORM_NACL included in 
the project file isn't necessary to build successfully, but its presence ensures 
the IDE pickups up the correct define.

Release|Android

The Ant Build Type property is set to Debug rather than Release so that the apk 
will be signed witha debug key.  Setting the property to Release requires 
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
