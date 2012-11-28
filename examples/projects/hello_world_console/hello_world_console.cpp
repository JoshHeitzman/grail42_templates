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
	return 1;
}

#if defined(_WIN32)

int _tmain(int argc, _TCHAR* argv[])
{
	faux_main();
	return 0;
}

#elif defined(__ANDROID__)

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
	int result = faux_main();

	// Stdout isn't automatically flushed, so explicitly flush it to ensure all output is logged prior to shutdown.
	// Also the stdout buffer between the JVM and native code doesn't appear to be shared as flushing from the 
	// activity has no apparent effect.
	fflush(stdout);

	return result;
}

#endif