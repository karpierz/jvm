
package org.jt.ref;

import java.util.List;
import java.util.ArrayList;
import static java.lang.System.out;

import org.jt.ref.Reference;
import org.jt.ref.ReferenceQueue;

public class TestReferenceQueue
{
    public static void testReferenceQueue(int[] pyObjectIds) throws InterruptedException
    {
        ReferenceQueue refQueue = new ReferenceQueue();
        refQueue.start();
        out.println();
        out.println("ReferenceQueue started");

        assert refQueue.poll() == null : "Queue is not empty just after start!";

        Object javaObject1 = new Object();
        Object javaObject2 = new Object();
        Object javaObject3 = new Object();

        Reference reference1 = new TestReference(javaObject1, pyObjectIds[0], refQueue);
        Reference reference2 = new TestReference(javaObject2, pyObjectIds[1], refQueue);
        Reference reference3 = new TestReference(javaObject3, pyObjectIds[2], refQueue);

        // its always returns null
        assert reference1.get() == null : "reference1 is not null!";
        assert reference2.get() == null : "reference2 is not null!";
        assert reference3.get() == null : "reference3 is not null!";

        //Creating Phantom Reference to A-type object to which 'a' is also pointing
        //PhantomReference<Object> ref = new PhantomReference<>(a, refQueue);
        //int i = 0;
        //Object javaObject = new Object();
        //int    pyObjectId = pyObjectIds.clear();

        out.println("Before setting null...");
        javaObject1 = null;
        javaObject2 = null;
        javaObject3 = null;
        //Now, A-type objects to which 'a' is pointing earlier are available for garbage collection.
        //But, those objects are kept in 'refQueue' before removing it from the memory.
        out.println("After  setting null...");

        out.println("Before GC...");
        System.gc();
        Thread.sleep(100);
        out.println("After  GC...");

        refQueue.stop();
        out.println("ReferenceQueue stopped");
    }

    static class TestReference extends Reference
    {
        public TestReference(Object referent, long target, ReferenceQueue queue)
        {
            super(referent, target, queue);
            out.println("ref.initialized(): " + this); 
        }

        @Override
        protected synchronized void dispose()
        {
            super.dispose();
            out.println("ref.disposed(): " + this);
        }
    }
}
