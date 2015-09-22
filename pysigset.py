"""
pysigset, signal blocking under GNU/Linux & OS X
================================================

Provides access to sigprocmask(2) and friends and convenience wrappers to
python application developers wanting to SIG_BLOCK and SIG_UNBLOCK signals in
critical sections of their code.

Requires ctypes access to libc.so.6 or libSystem.B.dylib.

See usage example at the bottom.

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

"""
import ctypes
import platform
import signal


# Get the signal names from the signal library.
# {1: 'HUP', 2: 'INT', ...}
SIGNAMES = dict((getattr(signal, i), i[3:])
                for i in dir(signal)
                if i.startswith('SIG') and i[3:4] != '_')

# A bunch of constants.
SIG_BLOCK = 0
SIG_UNBLOCK = 1
SIG_SETMASK = 2
NULL = 0


class SIGSET(ctypes.Structure):
    """
    sigset_t container, usable for sigprocmask(2), sigpending(2) etc..

    """
    NWORDS = int(1024 / (8 * ctypes.sizeof(ctypes.c_uint)))

    def __repr__(self):
        ret = []
        for i, bitmask in enumerate(self.val):
            if bitmask:
                if mask2list and i <= 1:  # 64 bits in the first two int32s
                    numbers = mask2list(bitmask)  # sorted from low to high
                    if i == 1:
                        numbers = [i << 1 for i in numbers]
                    for number in numbers:
                        ret.append(SIGNAMES.get(number, 'SIG%d' % (number,)))
                else:
                    strvalue = binrepr and binrepr(bitmask) or str(bitmask)
                    ret.append('%d: %s' % (i, strvalue))
        return '{%s}' % (', '.join(ret),)

    _fields_ = (
        # This is a 32 uint32 list where the first two integers contain
        # the signal masks for signals 1..64.
        ('val', ctypes.c_uint * NWORDS),
    )


def binrepr(integer):
    """
    Convert an integer to a string representation of bits:

    >>> binrepr(1)
    '0b1'
    >>> binrepr(-(16384 | 1))
    '-(0b01000000<<8 | 0b00000001)'
    """
    if not integer:
        return '0b0'
    if integer < 0:
        return '-' + binrepr(-integer)
    out = []
    i = 0
    while integer > 0:
        i += 1
        out.append('01'[integer & 1])
        integer >>= 1
        if (i % 8) == 0:
            out.append('<<%d | 0b' % (i,))
    if out[-1].startswith('<'):
        out.pop()
    if i > 8:
        return '(0b%s)' % (''.join(reversed(out)),)
    return '0b%s' % (''.join(reversed(out)),)


def mask2list(bitmask, number=1):
    """
    Convert an integer bitmask into a list of integers.

    >>> mask2list((1 << 14) | (1 << 0))
    [1, 15]
    """
    if not bitmask:
        return []
    this = []
    if bitmask & 1:
        this = [number]
    return this + mask2list(bitmask >> 1, number + 1)


# Time to get the goodies, and wrapping them.
if platform.system() == 'Darwin':
    libc = ctypes.CDLL('libSystem.B.dylib')
else:  # platform.system() == 'Linux'
    libc = ctypes.CDLL('libc.so.6')


def _wrap(function, sigset_args):
    """
    Wrap libc functions taking a sigset_t, ensuring that ctypes.pointer() is
    called on the appropriate arguments.
    """

    def wrapped(*args):
        # Call ctypes.pointer on sigsets.
        args = list(args)
        for arg in sigset_args:
            if args[arg]:  # don't translate NULL
                args[arg] = ctypes.pointer(args[arg])
        return function(*args)

    wrapped.__name__ = function.__name__
    return wrapped


sigemptyset = _wrap(libc.sigemptyset, [0])
sigemptyset.__doc__ = 'int sigemptyset(sigset_t *set)'

sigfillset = _wrap(libc.sigfillset, [0])
sigfillset.__doc__ = 'int sigfillset(sigset_t *set)'

sigaddset = _wrap(libc.sigaddset, [0])
sigaddset.__doc__ = 'int sigaddset(sigset_t *set, int signum)'

sigdelset = _wrap(libc.sigdelset, [0])
sigdelset.__doc__ = 'int sigdelset(sigset_t *set, int signum)'

sigismember = _wrap(libc.sigismember, [0])
sigismember.__doc__ = 'int sigismember(const sigset_t *set, int signum)'

sigpending = _wrap(libc.sigpending, [0])
sigpending.__doc__ = 'int sigpending(sigset_t *set)'

sigprocmask = _wrap(libc.sigprocmask, [1, 2])
sigprocmask.__doc__ = ('int sigprocmask(int how, const sigset_t *set, '
                       'sigset_t *oldset)')

# > Normally, sigsuspend() is used in conjunction with sigprocmask(2) in order
# > to prevent delivery of a signal during the execution of a critical code
# > section. The caller first blocks the signals with sigprocmask(2). When the
# > critical code has completed, the caller then waits for the signals by
# > calling sigsuspend() with the signal mask that was returned by
# > sigprocmask(2) (in the oldset argument).
#
# Shouldn't that be: "returned by sigpending(2)"?? Calling suspend after
# unblocking causes a new block.
sigsuspend = _wrap(libc.sigsuspend, [0])
sigsuspend.__doc__ = 'int sigsuspend(const sigset_t *mask)'


class suspended_signals(object):
    """
    Suspend the supplied signals in the 'with' block.

    Usage:

        with suspended_signals(SIGINT, SIGTERM):
            # Signals are blocked here...
            pass
    """

    def __init__(self, *signals):
        self.oldset = SIGSET()
        self.newset = SIGSET()  # empty by default
        for signum in signals:
            sigaddset(self.newset, signum)

    def __enter__(self):
        sigprocmask(SIG_SETMASK, self.newset, self.oldset)

    def __exit__(self, type, value, tb):
        sigprocmask(SIG_SETMASK, self.oldset, 0)


if __name__ == '__main__':
    from signal import signal, SIGINT, SIGTERM
    from time import sleep

    signals = (SIGINT, SIGTERM)
    done = False

    def sighandler(signum, frame):
        global done
        done = True

    for signum in signals:
        signal(signum, sighandler)

    while not done:
        with suspended_signals(SIGINT, SIGTERM):
            # These three seconds are uninterruptible.
            print('uninterruptible')
            sleep(3)

        if done:
            break
        print('interruptible')
        sleep(3)
    print('done')

# vim: set ts=8 sw=4 sts=4 et ai tw=79:
