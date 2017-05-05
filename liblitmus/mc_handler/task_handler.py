import sys
import math
import subprocess 
import random
import json_handler as json_handler
import signal_handler as signal_handler
class task_handler:

    """
    taskset: Task details. 
    perc_overrun   : Amount of overrun to be introduced per process. 
    hi_overrun_perc: Percentage of hi tasks exibiting budget overrun. 
    crit_time      : Amount to which system to remain in budget overrun. 
    """
    def __init__(self,sys_crit, task_files, perc_overrun=0.4,
            hi_overrun_perc=0.6, crit_time=40 ):
        self.crit_time = crit_time
        self.sys_crit = sys.crit
        self.taskset = taskset
        self.litmus_path = "/home/guest/Documents/litmus/liblitmus/"
        self.crit_binary = self.litmus_path  + "syscrit"
        self.rtspin = self.litmus_path + "rtspin"
        self.release_ts = self.litmus_path + "release_ts"
        self.high_pids = [] # Store the high crit task pids.
        self.active_high_pids = []
        self.perc_overrun = perc_overrun # Percentage overrun in high crit tasks.
        self.hi_overr = hi_overrun_perc # Percentange of high crit task exibiting overrun.
        self.sig = signal_handler()
        self.json = json_handler()
        self.json.parse_files(['./data/taskset.json'])

    
    def stop_hi_mode(self):
        """Callback for alarm, bring task to low mode."""
        self.set_system_criticality(1)

    
    def start_hi_mode(self, duration = self.crit_time):
        """Start a high criticality mode."""
        alarm_args = {
                0: 'alarm',
                1: duration,
                2: self.stop_hi_mode
                }
        self.sig.common_handler(alarm_args)
        self.set_system_criticality(self.sys_crit)
        
    def raise_task_criticalities(self, pids = self.high_pids):
        """Raise budget overrun over set of high crit tasks."""
        arg_raise = {
                0: 'signal',
                1: None,
                2: 'SIGUSR1'
                }
        data_len = len(pids)
        if data_len < 1:
            print("Task Handler: Atleast one high task id to be provided.")
            sys.exit()
        data_len = math.floor(data_len * self.hi_overr)
        if data_len < 1:
            data_len = 1
        val_range = [i for i in range(len(pids))]
        random.random(val_range)
        val_range = val_range[:data_len]
        for id in val_range:
            arg_raise[1] = id
            self.sig.common_handler(arg_raise)
        self.active_high_pids = val_range

    def lower_task_criticalities(self):
        """Disable overrun execution in active overrun tasks."""
        arg_raise = {
                0: 'signal',
                1: None,
                2: 'SIGUSR2'
                }
        if len(self.active_high_pids):
            for id in self.active_high_pids:
                arg_raise[1] = id
                self.sig.common_handler(arg_raise)
        self.active_high_pids = []
                        

    def set_system_criticality(self, newval = 1):
        """Raise the overall system criticality to the new value."""
        args = (self.crit_binary, str(newval))
        ppopen = subprocess.Popen(args, stdout=subprocess.PIPE)
        ppopen.wait()
        output = ppopen.stdout.read()
        return output

    def task_start(self):
        """Move task from wait mode to run mode."""
        args = (self.release_ts)
        ppopen = subprocess.Popen(args, stdout=subprocess.PIPE)
        ppopen.wait()
        output = ppopen.stdout.read()
        return output

    def task_launch(self, params):
        """Launch a rtspin instance with given parameters."""
        hi_tasks = self.json.high_crit_tasks()
        lo_tasks = self.json.low_crit_tasks()
        for t in hi_tasks:
            c = t.get_crit()
            b = t.get_budget() #(Lo, Hi)
            p = t.get_period() # (lo, Hi)
            d = t.get_deadline() # (lo, Hi)
            args = (self.rtspin, '-Z', str(c), '-w',
                    str(b[0]), str(p[0]), str(d[0]), 
                    str(b[1]), str(p[1]), str(d[1]))
            ppopen = subprocess.Popen(args, stdout=subprocess.PIPE)

       


