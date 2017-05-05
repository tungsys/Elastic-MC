#!/usr/bin/python3.5

"""Main process pipe-line, read taskset , launch processes."""
import task_handler as task_handler
import sys
import subprocess
import os

EXEC_PATH = "/home/guest/Documents/litmus/liblitmus"
EXEC_BIN  = EXEC_PATH + "/" + "syscrit"

def main():
    print("Starting the experimental pipeline.")
    try:
        sys_crit = sys.argv[1]
    except IndexError:
        print("Provide input as: ./pipeline <crit> ")
        sys.exit()
    # raise system criticality.

    # Process task set.
    
    # Start Tasks.

    # Start overhead tracing.

    # Start schedule tracing.

    # Release Tasks.

    # End tracing, raise key  commands.

if __name__ == '__main__':
    main()
