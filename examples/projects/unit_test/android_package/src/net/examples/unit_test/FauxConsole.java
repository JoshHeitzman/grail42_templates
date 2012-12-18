/*                   Copyright (C) 2012 Josh Heitzman
Distributed under the Boost Software License, Version 1.0.
See accompanying file LICENSE_1_0.txt or online copies at:
* http://www.boost.org/LICENSE_1_0.txt
* http://opensource.org/licenses/BSL-1.0
* http://directory.fsf.org/wiki/License:Boost1.0
* http://en.wikipedia.org/wiki/Boost_Software_License                */

package net.examples.unit_test;

import android.app.Activity;
import android.os.Bundle;
import android.util.Log;

public class FauxConsole extends Activity
{
    // Load the shared library generated from the C++ code
    static {
        System.loadLibrary("unit_test");
    }

    private static native int main();

    @Override
    public void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);

        Log.i("13380324612F4E3184624E7AD706141A", "4D85BA47C2364027A09FBF016A5C2C2A");
        int result = main();
        Log.i("13380324612F4E3184624E7AD706141A", "ECD3B7A023654F9D99F2EF3D4AA33925");
        Log.i("13380324612F4E3184624E7AD706141A", String.format("DAB25FDC5A974392AA39ED7928A31561:%d", result));

        finish();

        // Get a head start on garbage collection and finalization since we're waiting for 
        // onDestroy to be called before calling System.exit.
        System.gc();
        System.runFinalization();
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        System.runFinalizersOnExit(true);
        System.exit(0);
    }
}
