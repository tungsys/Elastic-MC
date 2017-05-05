"""
Read the process description in json files and create rtspin task set.
"""
import sys
import json
import os
import glob
from pprint import pprint
from task import task

class json_handler:

    """
    path: Path to json file.
    pretty: Pretty print the json output.
    """
    def __init__(self, path='./data', pretty=False):
        self.path = path
        self.high_tasks = []
        self.low_tasks = []
        self.crit = 0
        if pretty:
            # Do a pretty print of json data.
            pprint(self.data)

    def read_taskset(self, file):
        taskset = None
        try:
            with open(file, 'r') as f:
                taskset = json.load(f)
        except (OSError, IOError) as e:
            print("Error opening file: ", e)
        return taskset
            

    def parse_files(self, files = None):
        """Create the task structure."""
        crit = None
        taskset = []
        if files:
            for file in files:
                print(file)
                taskset.append(self.read_taskset(file))
        else:
            # Parse the default files and read taskset.
            for file in glob.glob('./data/*.json'):
                taskset.append(self.read_taskset(file))
        # Process task set.
        for t in taskset:
            if t['syscrit'] > self.crit:
                self.crit = t['syscrit']
            if t["high"]:
                for hi_task in t["high"]:
                    print(hi_task)
                    self.high_tasks.append(task(hi_task))
            if t["low"]:
                for lo_task in t["low"]:
                    print(lo_task)
                    self.low_tasks.append(task(lo_task))
    

    def pretty_print_data(self):
        """Debugging stub to print data."""
        pprint(self.high_tasks[0].get_crit())
        pprint(self.low_tasks[0].get_crit())


    def get_system_criticality(self):
        """Retrieve the system criticality requested."""
        return self.crit


    def get_task_set(self):
        """Retrieve the task set processed."""
        return (self.high_tasks, self.low_tasks)


    def high_crit_tasks(self):
        """Get dictionary of all the high criticality tasks."""
        return self.high_tasks


    def low_crit_tasks(self):
        """Get the dictionary of all low crit tasks."""
        return self.low_tasks

# ******* Test stub*******************
def main():
    jshn = json_handler()
    jshn.parse_files(["./data/taskset.json"])
    jshn.pretty_print_data()

if __name__ == '__main__':
    main()
# ************************************
