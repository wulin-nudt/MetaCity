from containernet.node import DockerSta
from containernet.node import Docker
import errno
import os
import re
import pty
import select
import docker
import json
from subprocess import check_output
from time import sleep
from re import findall
import threading
import signal

from mininet.node import Node, Host
from mininet.moduledeps import moduleDeps, pathCheck, TUN
from mininet.util import ( quietRun, errRun, which)
from mininet.log import info, error, warn, debug
from mn_wifi.node import Station
from containernet.link import Intf, TCIntf, OVSIntf
from distutils.version import StrictVersion
from mininet.util import encode


class OSMDockerCloud(Docker):

    def __init__(self, name, dimage=None, dcmd=None, did=None, **kwargs):

        super().__init__(name, dimage=dimage, dcmd=dcmd, did=did, **kwargs)

        if 'position' in kwargs:
            self.pos_to_array()


    def pos_to_array(self):
        pos = self.params['position']
        if isinstance(pos, str):
            pos = pos.split(',')
        self.position = [float(pos[0]), float(pos[1]), float(pos[2])]
        self.params.pop('position', None)

    def getxyz(self):
        pos = self.position
        x,y = round(pos[0], 2), round(pos[1], 2)
        #only access third element if it exists
        if len(pos) == 3:
            z = round(pos[2], 2)
        #otherwise, set z to 0
        else:
            z = 0
        return x, y, z
    def startShell( self, *args, **kwargs ):
        "Start a shell process for running commands"
        threadid = hash(threading.current_thread())
        if not hasattr(self,'shells'):
            self.shells={}
            self.masters={}
            self.slaves={}
            self.stdins={}
            self.stdouts = {}
            self.pollOuts={}
            self.waitings={}
            self.readbufs={}
            self.lastPids = {}
            self.lastCmds={}

        # mnexec: (c)lose descriptors, (d)etach from tty,
        # (p)rint pid, and run in (n)amespace
        # opts = '-cd' if mnopts is None else mnopts
        # if self.inNamespace:
        #     opts += 'n'
        # bash -i: force interactive
        # -s: pass $* to shell, and make process easy to find in ps
        # prompt is set to sentinel chr( 127 )
        if hasattr(self, 'existing_container'):
            cmd = ['docker', 'exec', '-it', '%s' % self.did, 'env', 'PS1=' + chr(127),
                   'bash', '--norc', '-is', 'mininet:' + self.name]
        else:
            cmd = [ 'docker', 'exec', '-it',  '%s.%s' % ( self.dnameprefix, self.name ), 'env', 'PS1=' + chr( 127 ),
                    'bash', '--norc', '-is', 'mininet:' + self.name ]
        # Spawn a shell subprocess in a pseudo-tty, to disable buffering
        # in the subprocess and insulate it from signals (e.g. SIGINT)
        # received by the parent
        master, slave = pty.openpty()
        # mastername = os.ttyname(master) if master else None
        # threadid = os.ttyname(slave) if slave else None
        # print(mastername)
        # print(threadid)
        self.masters.update({threadid:master})
        self.slaves.update({threadid:slave})
        shell = self._popen( cmd, stdin=slave, stdout=slave, stderr=slave,
                                  close_fds=False )
        self.shells.update({threadid:shell})
        stdin = os.fdopen(master, 'r' )
        self.stdins.update({threadid:stdin})
        stdout = stdin
        self.stdouts.update({threadid:stdout})
        self.pid = self._get_pid()
        pollOut = select.poll()
        pollOut.register(stdout)
        self.pollOuts.update({threadid:pollOut})
        # Maintain mapping between file descriptors and nodes
        # This is useful for monitoring multiple nodes
        # using select.poll()
        self.outToNode[ stdout.fileno() ] = self
        self.inToNode[ stdin.fileno() ] = self

        #下面2个参数不需要
        self.execed = False
        lastPid=[]
        lastCmd=[]
        readbuf=['']
        self.lastCmds.update({threadid:lastCmd})
        self.lastPids.update({threadid:lastPid})
        self.readbufs.update({threadid:readbuf})
        # Wait for prompt
        while True:
            data = self.read(1024)
            if data[ -1 ] == chr( 127 ):
                break
            pollOut.poll()
        # self.waiting = False
        waiting=[]
        self.waitings.update({threadid:waiting})

        # self.master, self.slave, self.shell, self.stdin, self.stdout, self.pollOut = (
        # master, slave, shell, stdin, stdout, pollOut)
        # print(self.temp_cmd(threadid,'ping www.baidu.com -c 1'))
        # print(self.cmd('ping www.baidu.com -c 1'))
        # os.write(stdin.fileno(), encode('touch 1.txt' + ' \n'))
        # return (master,slave,shell,stdin,stdout,pollOut)
        if not self.shell or (not self.shells.get(self.main_thread_id,None) and threadid==self.main_thread_id):
            self.main_thread_id=threadid
            self.shell=shell
            self.stdin=stdin
            self.stdout=stdout
            self.pollOut=pollOut
            self.lastCmd = lastCmd
            self.lastPid = lastPid
            self.readbuf = readbuf
            self.waiting = waiting
        # +m: disable job control notification
        self.cmd('unset HISTFILE; stty -echo; set +m')

    def read( self, size=1024 ):
        """Buffered read from node, potentially blocking.
           size: maximum number of characters to return"""
        threadid = hash(threading.current_thread())
        count = len( self.readbufs[threadid][0] )
        if count < size:
            data = os.read( self.stdouts[threadid].fileno(), size - count )
            self.readbufs[threadid][0]  += self.decoder.decode( data )
        if size >= len( self.readbufs[threadid][0]  ):
            result = self.readbufs[threadid][0]
            self.readbufs[threadid][0]  = ''
        else:
            result = self.readbufs[threadid][0][ :size ]
            self.readbufs[threadid][0]  = self.readbufs[threadid][0][ size: ]
        return result

    def cmd(self, *args, **kwargs ):
        """Send a command, wait for output, and return it.
           cmd: string"""
        threadid = hash(threading.current_thread())
        kwargs.update(threadid=threadid)
        verbose = kwargs.get( 'verbose', False )
        log = info if verbose else debug
        log( '*** %s : %s\n' % ( self.name, args ) )
        self.sendCmd( *args, **kwargs )
        return self.waitOutput( verbose,**kwargs )

    def sendCmd( self, *args, **kwargs ):
        """Send a command, followed by a command to echo a sentinel,
           and return without waiting for the command to complete."""
        threadid=kwargs.get('threadid',None)
        if not threadid:
            threadid = hash(threading.current_thread())
            kwargs.update(threadid=threadid)
        self._check_shell(**kwargs)
        if not self.shells.get(threadid,None):
            return

        """Send a command, followed by a command to echo a sentinel,
           and return without waiting for the command to complete.
           args: command and arguments, or string
           printPid: print command's PID? (False)"""

        assert self.shells[threadid] and not self.waitings[threadid]
        printPid = kwargs.get( 'printPid', False )
        # Allow sendCmd( [ list ] )
        if len( args ) == 1 and isinstance( args[ 0 ], list ):
            cmd = args[ 0 ]
        # Allow sendCmd( cmd, arg1, arg2... )
        elif len( args ) > 0:
            cmd = args
        # Convert to string
        if not isinstance( cmd, str ):
            cmd = ' '.join( [ str( c ) for c in cmd ] )
        if not re.search( r'\w', cmd ):
            # Replace empty commands with something harmless
            cmd = 'echo -n'
        self.lastCmds[threadid].append(cmd)
        # if a builtin command is backgrounded, it still yields a PID
        if len( cmd ) > 0 and cmd[ -1 ] == '&':
            # print ^A{pid}\n so monitor() can set lastPid
            cmd += ' printf "\\001%d\\012" $! '
        elif printPid and not isShellBuiltin( cmd ):
            cmd = 'mnexec -p ' + cmd
        self.write( cmd + '\n',**kwargs)
        self.lastPids[threadid].clear()
        self.waitings[threadid].append(1)

    def _check_shell(self,**kwargs):
        """Verify if shell is alive and
           try to restart if needed"""
        threadid=kwargs.get('threadid',None)
        if not threadid:
            threadid = hash(threading.current_thread())
        if self._is_container_running():
            if self.shells.get(threadid,None):
                self.shells[threadid].poll()
                if self.shells[threadid].returncode is not None:
                    debug("*** Shell died for docker host \'%s\'!\n" % self.name )
                    self.shells.pop(threadid)
                    debug("*** Restarting Shell of docker host \'%s\'!\n" % self.name )
                    self.startShell()
            else:
                debug("*** Restarting Shell of docker host \'%s\'!\n" % self.name )
                self.startShell()
        else:
            error( "ERROR: Can't connect to Container \'%s\'' for docker host \'%s\'!\n" % (self.did, self.name) )
            if self.shells.get(threadid,None):
                self.shells.pop(threadid)

    def write( self, data,**kwargs ):
        """Write data to node.
           data: string"""
        threadid=kwargs.get('threadid',None)
        if not threadid:
            threadid = hash(threading.current_thread())
        # print(data)
        # print('in: '+data)
        os.write( self.stdins[threadid].fileno(), encode( data ) )

    def popen( self, *args, **kwargs ):
        """Return a Popen() object in node's namespace
           args: Popen() args, single list, or string
           kwargs: Popen() keyword args"""
        if not self._is_container_running():
            error( "ERROR: Can't connect to Container \'%s\'' for docker host \'%s\'!\n" % (self.did, self.name) )
            return
        mncmd = ["docker", "exec", "-t", "%s.%s" % (self.dnameprefix, self.name)]

        # print(*args)

        return Node.popen( self, *args, mncmd=mncmd, **kwargs )

    def waitOutput( self, verbose=False, findPid=True,**kwargs ):
        """Wait for a command to complete.
           Completion is signaled by a sentinel character, ASCII(127)
           appearing in the output stream.  Wait for the sentinel and return
           the output, including trailing newline.
           verbose: print output interactively"""
        prefix=chr(27)+chr(91)+chr(63)+chr(50)+chr(48)+chr(48)+chr(52)+chr(108)+chr(13)
        suffix=chr(27)+chr(91)+chr(63)+chr(50)+chr(48)+chr(48)+chr(52)+chr(104)
        threadid=kwargs.get('threadid',None)
        if not threadid:
            threadid = hash(threading.current_thread())
            kwargs.update(threadid=threadid)
        log = info if verbose else debug
        output = ''
        while self.waitings[threadid]:
            data = self.monitor( findPid=findPid,**kwargs)
            output += data
            log( data )
        # print('out: '+output)
        output=  output.replace(prefix,'')
        output = output.replace(suffix,'')
        return output

    def monitor( self, timeoutms=None, findPid=True,**kwargs ):
        """Monitor and return the output of a command.
           Set self.waiting to False if command has completed.
           timeoutms: timeout in ms or None to wait indefinitely
           findPid: look for PID from mnexec -p"""
        threadid=kwargs.get('threadid',None)
        if not threadid:
            threadid = hash(threading.current_thread())
            kwargs.update(threadid=threadid)
        ready = self.waitReadable( timeoutms,**kwargs)
        if not ready:
            return ''
        data = self.read( 1024 )
        pidre = r'\[\d+\] \d+\r\n'
        # Look for PID
        marker = chr( 1 ) + r'\d+\r\n'
        if findPid and chr( 1 ) in data:
            # suppress the job and PID of a backgrounded command
            if re.findall( pidre, data ):
                data = re.sub( pidre, '', data )
            # Marker can be read in chunks; continue until all of it is read
            while not re.findall( marker, data ):
                data += self.read( 1024 )
            markers = re.findall( marker, data )
            if markers:
                self.lastPids[threadid].append(int( markers[ 0 ][ 1: ] ))
                data = re.sub( marker, '', data )
        # Look for sentinel/EOF
        if len( data ) > 0 and data[ -1 ] == chr( 127 ):
            self.waitings[threadid].clear()
            data = data[ :-1 ]
        elif chr( 127 ) in data:
            self.waitings[threadid].clear()
            data = data.replace( chr( 127 ), '' )
        return data

    def waitReadable( self, timeoutms=None,**kwargs):
        """Wait until node's output is readable.
           timeoutms: timeout in ms or None to wait indefinitely.
           returns: result of poll()"""
        threadid=kwargs.get('threadid',None)
        if not threadid:
            threadid = hash(threading.current_thread())

        if len( self.readbufs[threadid][0] ) == 0:
            return self.pollOuts[threadid].poll( timeoutms )
        return None

    def cleanup( self ):
        "Help python collect its garbage."
        # We used to do this, but it slows us down:
        # Intfs may end up in root NS
        # for intfName in self.intfNames():
        # if self.name in intfName:
        # quietRun( 'ip link del ' + intfName )
        for k,shell in self.shells.items():
            # Close ptys
            self.stdins[k].close()
            os.close(self.slaves[k])
            if self.waitExited:
                debug( 'waiting for', self.pid, 'to terminate\n' )
                shell.wait()
        self.shells.pop(k)

class OSMDockerStaion(DockerSta):

    def startShell( self, *args, **kwargs ):
        "Start a shell process for running commands"
        threadid = hash(threading.current_thread())
        if not hasattr(self,'shells'):
            self.shells={}
            self.masters={}
            self.slaves={}
            self.stdins={}
            self.stdouts = {}
            self.pollOuts={}
            self.waitings={}
            self.readbufs={}
            self.lastPids = {}
            self.lastCmds={}

        # mnexec: (c)lose descriptors, (d)etach from tty,
        # (p)rint pid, and run in (n)amespace
        # opts = '-cd' if mnopts is None else mnopts
        # if self.inNamespace:
        #     opts += 'n'
        # bash -i: force interactive
        # -s: pass $* to shell, and make process easy to find in ps
        # prompt is set to sentinel chr( 127 )
        if hasattr(self, 'existing_container'):
            cmd = ['docker', 'exec', '-it', '%s' % self.did, 'env', 'PS1=' + chr(127),
                   'bash', '--norc', '-is', 'mininet:' + self.name]
        else:
            cmd = [ 'docker', 'exec', '-it',  '%s.%s' % ( self.dnameprefix, self.name ), 'env', 'PS1=' + chr( 127 ),
                    'bash', '--norc', '-is', 'mininet:' + self.name ]
        # Spawn a shell subprocess in a pseudo-tty, to disable buffering
        # in the subprocess and insulate it from signals (e.g. SIGINT)
        # received by the parent
        master, slave = pty.openpty()
        # mastername = os.ttyname(master) if master else None
        # threadid = os.ttyname(slave) if slave else None
        # print(mastername)
        # print(threadid)
        self.masters.update({threadid:master})
        self.slaves.update({threadid:slave})
        shell = self._popen( cmd, stdin=slave, stdout=slave, stderr=slave,
                                  close_fds=False )
        self.shells.update({threadid:shell})
        stdin = os.fdopen(master, 'r' )
        self.stdins.update({threadid:stdin})
        stdout = stdin
        self.stdouts.update({threadid:stdout})
        self.pid = self._get_pid()
        pollOut = select.poll()
        pollOut.register(stdout)
        self.pollOuts.update({threadid:pollOut})
        # Maintain mapping between file descriptors and nodes
        # This is useful for monitoring multiple nodes
        # using select.poll()
        self.outToNode[ stdout.fileno() ] = self
        self.inToNode[ stdin.fileno() ] = self

        #下面2个参数不需要
        self.execed = False
        lastPid=[]
        lastCmd=[]
        readbuf=['']
        self.lastCmds.update({threadid:lastCmd})
        self.lastPids.update({threadid:lastPid})
        self.readbufs.update({threadid:readbuf})
        # Wait for prompt
        while True:
            data = self.read(1024)
            if data[ -1 ] == chr( 127 ):
                break
            pollOut.poll()
        # self.waiting = False
        waiting=[]
        self.waitings.update({threadid:waiting})

        # self.master, self.slave, self.shell, self.stdin, self.stdout, self.pollOut = (
        # master, slave, shell, stdin, stdout, pollOut)
        # print(self.temp_cmd(threadid,'ping www.baidu.com -c 1'))
        # print(self.cmd('ping www.baidu.com -c 1'))
        # os.write(stdin.fileno(), encode('touch 1.txt' + ' \n'))
        # return (master,slave,shell,stdin,stdout,pollOut)
        if not self.shell or (not self.shells.get(self.main_thread_id,None) and threadid==self.main_thread_id):
            self.main_thread_id=threadid
            self.shell=shell
            self.stdin=stdin
            self.stdout=stdout
            self.pollOut=pollOut
            self.lastCmd = lastCmd
            self.lastPid = lastPid
            self.readbuf = readbuf
            self.waiting = waiting
        # +m: disable job control notification
        self.cmd('unset HISTFILE; stty -echo; set +m')

    def read( self, size=1024 ):
        """Buffered read from node, potentially blocking.
           size: maximum number of characters to return"""
        threadid = hash(threading.current_thread())
        count = len( self.readbufs[threadid][0] )
        if count < size:
            data = os.read( self.stdouts[threadid].fileno(), size - count )
            self.readbufs[threadid][0]  += self.decoder.decode( data )
        if size >= len( self.readbufs[threadid][0]  ):
            result = self.readbufs[threadid][0]
            self.readbufs[threadid][0]  = ''
        else:
            result = self.readbufs[threadid][0][ :size ]
            self.readbufs[threadid][0]  = self.readbufs[threadid][0][ size: ]
        return result

    def cmd(self, *args, **kwargs ):
        """Send a command, wait for output, and return it.
           cmd: string"""
        threadid = hash(threading.current_thread())
        kwargs.update(threadid=threadid)
        verbose = kwargs.get( 'verbose', False )
        log = info if verbose else debug
        log( '*** %s : %s\n' % ( self.name, args ) )
        self.sendCmd( *args, **kwargs )
        return self.waitOutput( verbose,**kwargs )

    def sendCmd( self, *args, **kwargs ):
        """Send a command, followed by a command to echo a sentinel,
           and return without waiting for the command to complete."""
        threadid=kwargs.get('threadid',None)
        if not threadid:
            threadid = hash(threading.current_thread())
            kwargs.update(threadid=threadid)
        self._check_shell(**kwargs)
        if not self.shells.get(threadid,None):
            return

        """Send a command, followed by a command to echo a sentinel,
           and return without waiting for the command to complete.
           args: command and arguments, or string
           printPid: print command's PID? (False)"""

        assert self.shells[threadid] and not self.waitings[threadid]
        printPid = kwargs.get( 'printPid', False )
        # Allow sendCmd( [ list ] )
        if len( args ) == 1 and isinstance( args[ 0 ], list ):
            cmd = args[ 0 ]
        # Allow sendCmd( cmd, arg1, arg2... )
        elif len( args ) > 0:
            cmd = args
        # Convert to string
        if not isinstance( cmd, str ):
            cmd = ' '.join( [ str( c ) for c in cmd ] )
        if not re.search( r'\w', cmd ):
            # Replace empty commands with something harmless
            cmd = 'echo -n'
        self.lastCmds[threadid].append(cmd)
        # if a builtin command is backgrounded, it still yields a PID
        if len( cmd ) > 0 and cmd[ -1 ] == '&':
            # print ^A{pid}\n so monitor() can set lastPid
            cmd += ' printf "\\001%d\\012" $! '
        elif printPid and not isShellBuiltin( cmd ):
            cmd = 'mnexec -p ' + cmd
        self.write( cmd + '\n',**kwargs)
        self.lastPids[threadid].clear()
        self.waitings[threadid].append(1)

    def _check_shell(self,**kwargs):
        """Verify if shell is alive and
           try to restart if needed"""
        threadid=kwargs.get('threadid',None)
        if not threadid:
            threadid = hash(threading.current_thread())
        if self._is_container_running():
            if self.shells.get(threadid,None):
                self.shells[threadid].poll()
                if self.shells[threadid].returncode is not None:
                    debug("*** Shell died for docker host \'%s\'!\n" % self.name )
                    self.shells.pop(threadid)
                    debug("*** Restarting Shell of docker host \'%s\'!\n" % self.name )
                    self.startShell()
            else:
                debug("*** Restarting Shell of docker host \'%s\'!\n" % self.name )
                self.startShell()
        else:
            error( "ERROR: Can't connect to Container \'%s\'' for docker host \'%s\'!\n" % (self.did, self.name) )
            if self.shells.get(threadid,None):
                self.shells.pop(threadid)

    def write( self, data,**kwargs ):
        """Write data to node.
           data: string"""
        threadid=kwargs.get('threadid',None)
        if not threadid:
            threadid = hash(threading.current_thread())
        # print(data)
        # print('in: '+data)
        os.write( self.stdins[threadid].fileno(), encode( data ) )

    def popen( self, *args, **kwargs ):
        """Return a Popen() object in node's namespace
           args: Popen() args, single list, or string
           kwargs: Popen() keyword args"""
        if not self._is_container_running():
            error( "ERROR: Can't connect to Container \'%s\'' for docker host \'%s\'!\n" % (self.did, self.name) )
            return
        mncmd = ["docker", "exec", "-t", "%s.%s" % (self.dnameprefix, self.name)]

        # print(*args)

        return Node.popen( self, *args, mncmd=mncmd, **kwargs )

    def waitOutput( self, verbose=False, findPid=True,**kwargs ):
        """Wait for a command to complete.
           Completion is signaled by a sentinel character, ASCII(127)
           appearing in the output stream.  Wait for the sentinel and return
           the output, including trailing newline.
           verbose: print output interactively"""
        prefix=chr(27)+chr(91)+chr(63)+chr(50)+chr(48)+chr(48)+chr(52)+chr(108)+chr(13)
        suffix=chr(27)+chr(91)+chr(63)+chr(50)+chr(48)+chr(48)+chr(52)+chr(104)
        threadid=kwargs.get('threadid',None)
        if not threadid:
            threadid = hash(threading.current_thread())
            kwargs.update(threadid=threadid)
        log = info if verbose else debug
        output = ''
        while self.waitings[threadid]:
            data = self.monitor( findPid=findPid,**kwargs)
            output += data
            log( data )
        # print('out: '+output)
        output=  output.replace(prefix,'')
        output = output.replace(suffix,'')
        return output

    def monitor( self, timeoutms=None, findPid=True,**kwargs ):
        """Monitor and return the output of a command.
           Set self.waiting to False if command has completed.
           timeoutms: timeout in ms or None to wait indefinitely
           findPid: look for PID from mnexec -p"""
        threadid=kwargs.get('threadid',None)
        if not threadid:
            threadid = hash(threading.current_thread())
            kwargs.update(threadid=threadid)
        ready = self.waitReadable( timeoutms,**kwargs)
        if not ready:
            return ''
        data = self.read( 1024 )
        pidre = r'\[\d+\] \d+\r\n'
        # Look for PID
        marker = chr( 1 ) + r'\d+\r\n'
        if findPid and chr( 1 ) in data:
            # suppress the job and PID of a backgrounded command
            if re.findall( pidre, data ):
                data = re.sub( pidre, '', data )
            # Marker can be read in chunks; continue until all of it is read
            while not re.findall( marker, data ):
                data += self.read( 1024 )
            markers = re.findall( marker, data )
            if markers:
                self.lastPids[threadid].append(int( markers[ 0 ][ 1: ] ))
                data = re.sub( marker, '', data )
        # Look for sentinel/EOF
        if len( data ) > 0 and data[ -1 ] == chr( 127 ):
            self.waitings[threadid].clear()
            data = data[ :-1 ]
        elif chr( 127 ) in data:
            self.waitings[threadid].clear()
            data = data.replace( chr( 127 ), '' )
        return data

    def waitReadable( self, timeoutms=None,**kwargs):
        """Wait until node's output is readable.
           timeoutms: timeout in ms or None to wait indefinitely.
           returns: result of poll()"""
        threadid=kwargs.get('threadid',None)
        if not threadid:
            threadid = hash(threading.current_thread())

        if len( self.readbufs[threadid][0] ) == 0:
            return self.pollOuts[threadid].poll( timeoutms )
        return None

    def cleanup( self ):
        "Help python collect its garbage."
        # We used to do this, but it slows us down:
        # Intfs may end up in root NS
        # for intfName in self.intfNames():
        # if self.name in intfName:
        # quietRun( 'ip link del ' + intfName )
        for k,shell in self.shells.items():
            # Close ptys
            self.stdins[k].close()
            os.close(self.slaves[k])
            if self.waitExited:
                debug( 'waiting for', self.pid, 'to terminate\n' )
                shell.wait()
        self.shells.pop(k)

    def setIP( self, ip, prefixLen=8, intf=None, **kwargs ):
        """Set the IP address for an interface.
           intf: intf or intf name
           ip: IP address as a string
           prefixLen: prefix length, e.g. 8 for /8 or 16M addrs
           kwargs: any additional arguments for intf.setIP"""
        return self.getNameToWintf(intf).setIP(ip, prefixLen, **kwargs)

    def IP( self, intf=None ):
        "Return IP address of a node or specific interface."
        return self.getNameToWintf(intf).IP()
# ch = input("请输入一个字符: ")
# # 用户输入ASCII码，并将输入的数字转为整型
# uch = int(input("请输入一个ASCII码: "))
# print( ch + " 的ASCII 码为", ord(ch))
# print( uch , " 对应的字符为", chr(uch))
# print('*** %(1)s : %(2)s\n' % {'1':44, '2':44 })

# print(id(a))
# print(id(b))
# a=['']
# b=a
# if a[0]:
#     print('test')
