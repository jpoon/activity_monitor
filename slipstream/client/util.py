from threading import *
import os, signal, sys, operator
import math

class StoppableThread(Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self):
        super(StoppableThread, self).__init__()
        self._stop = Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

class Watcher:
    """this class solves two problems with multithreaded
    programs in Python, (1) a signal might be delivered
    to any thread (which is just a malfeature) and (2) if
    the thread that gets the signal is waiting, the signal
    is ignored (which is a bug).

    The watcher is a concurrent process (not thread) that
    waits for a signal and the process that contains the
    threads.  See Appendix A of The Little Book of Semaphores.
    http://greenteapress.com/semaphores/

    I have only tested this on Linux.  I would expect it to
    work on the Macintosh and not work on Windows.

    http://code.activestate.com/recipes/496735-workaround-for-missed-sigint-in-multithreaded-prog/
    """
    
    def __init__(self):
        """ Creates a child thread, which returns.  The parent
            thread waits for a KeyboardInterrupt and then kills
            the child thread.
        """
        self.child = os.fork()
        if self.child == 0:
            return
        else:
            self.watch()

    def watch(self):
        try:
            os.wait()
        except KeyboardInterrupt:
            # I put the capital B in KeyBoardInterrupt so I can
            # tell when the Watcher gets the SIGINT
            print 'KeyBoardInterrupt'
            self.kill()
        sys.exit()

    def kill(self):
        try:
            os.kill(self.child, signal.SIGKILL)
        except OSError: pass

class Progress_Bar:
    def __init__(self):
        self.width = 50
        self.current_progress = 0
        self.__progress(self.current_progress)

    def add(self, percent):
        self.current_progress += percent
        self.__progress(self.current_progress)

    def done(self):
        if self.current_progress != 100:
            self.current_progress = 100
            self.__progress(self.current_progress)

    def __progress(self, percent):
        marks = math.floor(self.width * (percent/ 100.0))
        spaces = math.floor(self.width - marks)

        loader = '[' + ('=' * int(marks)) + (' ' * int(spaces)) + ']'
        sys.stdout.write("%s %d%%\r" % (loader, percent))
        if percent >= 100:
            sys.stdout.write("\r\n")
        sys.stdout.flush()
