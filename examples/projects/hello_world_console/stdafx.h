/*                   Copyright (C) 2012 Josh Heitzman
Distributed under the Boost Software License, Version 1.0.
See accompanying file LICENSE_1_0.txt or online copies at:
* http://www.boost.org/LICENSE_1_0.txt
* http://opensource.org/licenses/BSL-1.0
* http://directory.fsf.org/wiki/License:Boost1.0
* http://en.wikipedia.org/wiki/Boost_Software_License                */

#ifndef HG_6ED6281E3B354BAE95FD2C7E72CAF8D7
#define HG_6ED6281E3B354BAE95FD2C7E72CAF8D7

#pragma warning(push)
#pragma warning(disable : 4068)
#pragma once
#pragma warning(pop)

#include <stdio.h>

#if defined(_WIN32)

#include <tchar.h>

#elif defined(__ANDROID__)

#include <jni.h>
#include <android/log.h>

#else

#error Could not deduce target platform.

#endif

#endif // HG_6ED6281E3B354BAE95FD2C7E72CAF8D7