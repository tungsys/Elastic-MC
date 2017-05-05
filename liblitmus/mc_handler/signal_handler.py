import os
import time
import signal
import sys
import random
import subprocess


class signal_handler:
    """Abstract out the signal handling part."""

    def __init__(self, log= False):
        self.log = log
        self.pids = []
        self.val =  []
        self.alarm_callback = None # User specific alarm action.
        self.signal_callback = None # User specific signal action.


    def alarm_handler(self, signum, stack):
        if self.log:
            print("Alarm recieved.")
        if self.alarm_callback:
            self.alarm_callback()


    def sig_handler(self, sig):
        if self.log:
            print("Signal : {} Recieved.\n", sig)
        if self.signal_callback:
            self.signal_callback()


    def list_signal_handlers(self):
        """List the currently registered signal handlers."""
        signal_name_dict = {}
        for n in dir(signal):
            if n.startwith('SIG')and not n.startwith('SIG_'):
                signal_name_dict[getattr(signal, n)] = n

        for s, name in sorted(signal_name_dict.items()):
            handler = signal.getsignal(s)

            if handler is signal.SIG_DFL:
                handler = 'SIG_DFL'
            elif handler is signal.IGN:
                handler = 'SIG_IGN'
            if self.log:
                print("{:<10d} -- {:<10d}".format(s, handler))


    def raise_signal_to_pid(self, pid, sig):
        """Raise a USR signal to given pid."""
        if sig is signal.SIGUSR1 or signal.SIGUSR2:
            if self.log:
                print("Raise signal to pid:{0}\n".format(pid))
            os.kill(pid, getattr(signal, str(sig)))
        else:
            print("Only user signals SIGUSR1 and SIGUSR2 are supported.\n")


    def common_handler(self, args):
        
        if self.log:
            print("Common handler invoked..\n")
        if len(args) < 2:
            print("Signal Handler: No valid argument provided.\n")
            sys.exit()

        arg = args[0]
        if arg == 'signal':
            # Register a handler  for user signals.
            if self.log:
                print("Registering for signal handler..\n")
            try:
                signame = args[1]
                self.signal_callback = args[2]
            except AttributeError:
                print("Invalid signal attribute provided.\n")
            signal.signal(signame, self.sig_handler)
        elif arg == 'list':
            # List all the current registered handlers for signal.
            self.list_signal_handlers()
        elif arg == 'raise':
            # Raise a signal of user provided value.
            pid = int(args[1])
            sig = args[2]
            self.raise_signal_to_pid(pid, sig)
        elif arg == 'alarm':
            # Arm an alarm.
            if self.log:
                print("Alarm call raised..\n")
            signal.signal(signal.SIGALRM, self.alarm_handler)
            try:
                alarm_time = int(args[1])
                self.alarm_callback = args[2]
            except AttributeError:
                print("Invalid alarm attributes provided.\n")
                sys.exit()
            signal.alarm(alarm_time)
        else:
            print("Undefined parameter recieved.")
   

    def register_signal_callback(self, callback = None):
        """Register user specific callback"""
        if callback:
            self.signal_callback = callback
        else:
            print("Warning: Callback set to None.")


    def register_alarm_callback(self, callback = None):
        if callback:
            self.alarm_callback = callback
        else:
            print("Warning: Callback set to None.")


#***Test stub.******
# step = 0
# def dummy_signal_callback():
#     global step
#     print("Dummy signal callback called..\n")
#     step = 1
# 
# def dummy_alarm_callback():
#     global step
#     print("Dummy alarm callback called..\n")
#     step = 2
# 
# 
# def main():
#     global step
#     print("Test stub invoked..\n")
#     pid = int(sys.argv[1])
#     args_alarm = {
#             0: 'alarm',
#             1: 5,
#             2: dummy_signal_callback
#             }
#     
#     args_signal = {
#             0: 'signal',
#             1: signal.SIGUSR1,
#             2: dummy_signal_callback
#             }
#     arg_raise = {
#             0: 'raise',
#             1: pid,
#             2: 'SIGUSR1'
#             }
# 
#     handler = signal_handler(log=True)
#     handler.common_handler(args_alarm)
#     usleep = lambda x: time.sleep(x/1000000.0)
#     while step == 0:
#         usleep(500)
#     print("Raise signal.\n")
#     handler.common_handler(args_signal)
#     while step == 1:
#         usleep(500)
#     handler.common_handler(arg_raise)
# 
# 
# if __name__ =='__main__':
#     main()
#*******************
