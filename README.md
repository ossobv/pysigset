pysigset, signal blocking under linux
=====================================

Provides access to sigprocmask(2) and friends and convenience wrappers to
python application developers wanting to SIG_BLOCK and SIG_UNBLOCK signals in
critical sections of their code.

Requires ctypes access to libc.so.6. See usage example at the bottom.


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
