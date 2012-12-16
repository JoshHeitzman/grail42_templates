/*                   Copyright (C) 2012 Josh Heitzman
Distributed under the Boost Software License, Version 1.0.
See accompanying file LICENSE_1_0.txt or online copies at:
* http://www.boost.org/LICENSE_1_0.txt
* http://opensource.org/licenses/BSL-1.0
* http://directory.fsf.org/wiki/License:Boost1.0
* http://en.wikipedia.org/wiki/Boost_Software_License                */

#include "stdafx.h"

int faux_main()
{
    printf("Hello world.\n");
    return 0;
}

// 1 means that the nexe will be run from the commandline in sel_ldr (e.g. using %grail42_core_cmd%\nacl\faux_console\run_nexe_standalone.cmd)
// 0 means that the nexe will be run in Chrome (e.g. using %grail42_core_cmd%\nacl\faux_console\run_nexe_in_chrome.cmd).
// If main is defined the nexe will not load correctly in Chrome (even if CreateModule is present).
// Having CreateModule present doesn't prevent loading in sel_ldr, but it is not included to avoid 
// unintentional errors.  If VS allowed cloning project platforms rather than just solution platforms
// then this would be setup as a seperate NaCl64-Standalone platform.
#if 1
#define HWC_PLATFORM_NACL_STANDALONE
#endif

#if defined(HWC_PLATFORM_WIN32) || (defined(HWC_PLATFORM_NACL) && defined(HWC_PLATFORM_NACL_STANDALONE))

#if defined(HWC_PLATFORM_WIN32)
int _tmain(int, _TCHAR* [])
#elif defined(HWC_PLATFORM_NACL_STANDALONE)
int main(int, char* [])
#endif
{
    return faux_main();
}

#elif defined(HWC_PLATFORM_ANDROID) || (defined(HWC_PLATFORM_NACL) && !defined(HWC_PLATFORM_NACL_STANDALONE))

inline int faux_main_wrapper()
{
    int result = faux_main();

    // Stdout isn't automatically flushed on Android or NaCL, so explicitly flush it to ensure all output is logged 
    // prior to shutdown.  On Android the stdout buffer between the JVM and native code doesn't appear to be shared 
    // as flushing from the activity has no apparent effect.
    fflush(stdout);

    return result;
}

#if defined(HWC_PLATFORM_ANDROID)

extern "C" JNIEXPORT jint JNICALL JNI_OnLoad(JavaVM * vm, void * reserved)
{
    // Flush the emmission of "In mgmain JNI_OnLoad" by another component prior to
    // entering the faux main function, so it will be emitted prior to the start 
    // marker emitted by the activity.
    fflush(stdout);

    // Returning JNI_VERSION_1_1 on Android 2.2 results in "JNI_OnLoad returned bad version (65537)".
    return JNI_VERSION_1_2;
}

extern "C" JNIEXPORT jint JNICALL Java_net_examples_hello_1world_1console_FauxConsole_main(JNIEnv * env, jobject  obj)
{
    return faux_main_wrapper();
}

#elif defined(HWC_PLATFORM_NACL)

class Instance : public pp::Instance
{
public:
    explicit Instance(PP_Instance instance):
        pp::Instance(instance)
    {}

    virtual ~Instance() {}

    virtual bool Init(uint32_t, const char* [], const char* [])
    {
        int result = faux_main_wrapper();
        ((void)result);
        // TODO log result so it can be picked up by run_nexe_in_chrome.cmd
        this->Instance::PostMessage(pp::Var("quit"));
        return true;
    }
};

class Module : public pp::Module
{
public:
    // auto-generated default constructor is sufficient

    virtual ~Module() {}

    virtual pp::Instance* CreateInstance(PP_Instance instance)
    {
        return new Instance(instance);
    }
};

namespace pp
{

Module* CreateModule()
{
    return new ::Module();
}

}

#endif

#endif // defined(HWC_PLATFORM_ANDROID) || defined(HWC_PLATFORM_NACL)