import json
import sys

FILE = './data/taskset.json'

data = {}
data['syscrit'] = 2 # System criticality.
data['high'] = []
data['high'].append({
    'crit': 2,
    'budget_lo': 10,
    'budget_hi': 20,
    'period_lo': 100,
    'period_hi': 200,
    'deadline_lo': 200,
    'deadline_hi': 200
    })

data['low'] = []
data['low'].append({
    'crit': 1,
    'budget_lo': 10,
    'period_lo': 100,
    'deadline_lo': 100
    })

with open(FILE, 'w') as f:
    json.dump(data, f)
