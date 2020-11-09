// Copyright (c) 2004-2020 Adam Karpierz
// Licensed under CC BY-NC-ND 4.0
// Licensed under proprietary License
// Please refer to the accompanying LICENSE file.

package org.jt.ref;

public class ReferenceQueue extends java.lang.ref.ReferenceQueue<Object>
{
    private static final long REMOVING_REFERENCE_TIMEOUT = 250L;
    private static final long STOPPING_REFQUEUE_TIMEOUT  = 5000L;

    private volatile boolean stopped = false;
    private Object queueStopMutex = new Object();  /* as mutex */
    private Thread queueThread;

    /**
     * Start the threading queue.
     *
     * This method is long running.
     * It will return only if the queue gets stopped.
     */
    public void start()
    {
        this.stopped = false;
        this.queueThread = new Thread(new Worker());
        this.queueThread.setDaemon(true);
        this.queueThread.start();
    }

    /**
     * Stops the reference queue.
     */
    public void stop()
    {
        try
        {
            /* wait for the thread to finish... */
            synchronized ( this.queueStopMutex )
            {
                this.stopped = true;
                this.queueStopMutex.wait(STOPPING_REFQUEUE_TIMEOUT);
            }
        }
        catch ( InterruptedException exc )
        {
            /* who cares... */
            return;
        }
    }

    /**
     * Checks the status of the reference queue.
     * @return true is the queue is running.
     */
    public boolean isRunning()
    {
        return ! this.stopped;
    }

    /**
     * Create a new managed reference between Java and the Python object.
     */
    public Reference registerReference(Object referent, long pyobj)
    {
        return new Reference(referent, pyobj, this);
    }

    /*
     * Thread to monitor the queue and delete resources.
     */
    private class Worker implements Runnable
    {
        @Override
        public void run()
        {
            while ( ! stopped )
            {
                try
                {
                    /* Check if a reference has been queued and check if
                       the thread has been stopped every 0.25 seconds */
                    Reference reference = (Reference) remove(REMOVING_REFERENCE_TIMEOUT);
                    if ( reference != null )
                    {
                        reference.dispose();
                        reference.clear();
                    }
                }
                catch ( InterruptedException exc )
                {
                    /* don't know why... don't really care... */
                }
            }

            /* reference queue thread has stopped */
            synchronized ( queueStopMutex )
            {
                queueStopMutex.notifyAll();
            }
        }
    }
}
