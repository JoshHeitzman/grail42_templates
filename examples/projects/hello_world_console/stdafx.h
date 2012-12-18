/*                   Copyright (C) 2012 Josh Heitzman
Distributed under the Boost Software License, Version 1.0.
See accompanying file LICENSE_1_0.txt or online copies at:
* http://www.boost.org/LICENSE_1_0.txt
* http://opensource.org/licenses/BSL-1.0
* http://directory.fsf.org/wiki/License:Boost1.0
* http://en.wikipedia.org/wiki/Boost_Software_License                */

#ifndef HG_6ED6281E3B354BAE95FD2C7E72CAF8D7
#define HG_6ED6281E3B354BAE95FD2C7E72CAF8D7

#pragma once

#include <stdio.h>

#if !defined(HWC_PLATFORM_WIN32) && !defined(HWC_PLATFORM_ANDROID) && !defined(HWC_PLATFORM_NACL)
#if defined(_WIN32) && !defined(PPAPI)
#define HWC_PLATFORM_WIN32
#elif defined(__ANDROID__)
#define HWC_PLATFORM_ANDROID
#elif defined(__native_client__) || defined(PPAPI)
#define HWC_PLATFORM_NACL
#else
#error Could not deduce target platform.
#endif
#endif // !defined(HWC_PLATFORM_WIN32) && !defined(HWC_PLATFORM_ANDROID) && !defined(HWC_PLATFORM_NACL)

#if defined(HWC_PLATFORM_WIN32)

#include <tchar.h>

#elif defined(HWC_PLATFORM_ANDROID)

#include <jni.h>
#include <android/log.h>

#elif defined(HWC_PLATFORM_NACL)

#include <ppapi/cpp/instance.h>
#include <ppapi/cpp/module.h>
#include <ppapi/cpp/var.h>

#endif // HWC_PLATFORM_*

#endif // HG_6ED6281E3B354BAE95FD2C7E72CAF8D7