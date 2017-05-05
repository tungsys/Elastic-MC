import pprint
"""Container class for task."""

class task:

    """
    params:
    task_def: task definition as per aux_json_writer.py
    """
    def __init__(self, task_def):
         
        self.c   = task_def['crit']  
        self.blo = task_def['budget_lo']
        self.plo = task_def['period_lo']
        self.dlo = task_def['deadline_lo']
        if self.c > 1:
            self.bhi = task_def['budget_hi']
            self.phi = task_def['period_hi']
            self.dhi = task_def['deadline_hi']
        else:
            self.bhi = 0
            self.phi = 0
            self.dhi = 0

    def get_budget(self):
        return (self.blo, self.bhi)

    def get_period(self):
        return (self.plo, self.phi)

    def get_deadline(self):
        return (self.dlo, self.dhi)

    def get_crit(self):
        return self.c
