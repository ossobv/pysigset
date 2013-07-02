pysigset, signal blocking under GNU/Linux & OS X
================================================

Provides access to sigprocmask(2) and friends and convenience wrappers
to python application developers wanting to SIG\_BLOCK and SIG\_UNBLOCK
signals in critical sections of their code.


Most common usage
-----------------

    from signal import SIGINT, SIGTERM
    from pysigset import suspended_signals

    with suspended_signals(SIGINT, SIGTERM):
        # Signals are blocked here..
        pass
    # Any pending signal is fired now..


Also available
--------------

    sigaddset(*args)
        int sigaddset(sigset_t *set, int signum)
    
    sigdelset(*args)
        int sigdelset(sigset_t *set, int signum)
    
    sigemptyset(*args)
        int sigemptyset(sigset_t *set)
    
    sigfillset(*args)
        int sigfillset(sigset_t *set)
    
    sigismember(*args)
        int sigismember(const sigset_t *set, int signum)
    
    sigpending(*args)
        int sigpending(sigset_t *set)
    
    sigprocmask(*args)
        int sigprocmask(int how, const sigset_t *set, sigset_t *oldset)
    
    sigsuspend(*args)
        int sigsuspend(const sigset_t *mask)


Similar tools
-------------

[python-signalfd](https://pypi.python.org/pypi/python-signalfd) provides
access to ``sigprocmask`` and ``signalfd``. Its advantage is access to
``signalfd``. Its disadvantage is a compilation requirement.

pysigset has a pythonic interface and requires only ``ctypes`` access to
``libc.so.6`` or ``libSystem.B.dylib``.


Copyright
---------

Copyright 2013, Walter Doekes (OSSO B.V.) <wjdoekes osso nl>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
