# -*- coding: utf-8 -*-

__author__ = "Pywikipedia bot team"
__license__ = "MIT"

import init
import datetime
from Queue import Queue
from threading import Thread
import pywikibot

class ThreadPool(object):
    def wait_completion(self):
        """Pending threads finish."""
        def remaining():
            remainingItems = self.pool.qsize() - 1
                # -1 because we added a None element to stop the queue
            remainingSeconds = datetime.timedelta(
                    seconds=remainingItems)
            return (remainingItems, remainingSeconds)

        self.pool.put((None, [], {}))

        if self.pool.qsize() > 1:
            pywikibot.output(u'Waiting for %i items to be put. Estimated time remaining: %s'
                   % remaining())

        while(self.thread.isAlive()):
            try:
                self.thread.join(1)
            except KeyboardInterrupt:
                answer = pywikibot.inputChoice(u"""\
    There are %i items remaining in the queue. Estimated time remaining: %s
    Really exit?"""
                                         % remaining(),
                                     ['yes', 'no'], ['y', 'N'], 'N')
                if answer == 'y':
                    return

    # Create a separate thread for asynchronous page saves (and other requests)

    def async_manager(self):
        """Daemon; take requests from the queue and execute them in background."""
        while True:
            (request, args, kwargs) = self.pool.get()
            if request is None:
                break
            request(*args, **kwargs)

    def add_task(self, request, *args, **kwargs):
        """Put a request on the queue, and start the daemon if necessary."""
        if not self.thread.isAlive():
            try:
                self.pool.mutex.acquire()
                try:
                    self.thread.start()
                except (AssertionError, RuntimeError):
                    pass
            finally:
                self.pool.mutex.release()
        self.pool.put((request, args, kwargs))

    def __init__(self, numthread, name=None):
        # queue to hold pending requests
        self.pool = Queue(numthread)
        # set up the background thread
        self.thread = Thread(target=self.async_manager)
        # identification for debugging purposes
        self.thread.setName(name or "Thread")
        self.thread.setDaemon(True)

class LockObject(object):
    def __init__(self, func):
        self.func = func
        self.lock = False
        
    def do(self, s):
        while self.lock:
            print "Can't do!"
            time.sleep(2)
            
        self.lock = True
        print "lock acquired"
        self.func(s)
        self.lock = False
        print "lock released"
