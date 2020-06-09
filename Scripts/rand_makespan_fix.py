import pandas as pd
import numpy as np
from random import gauss, uniform

def get_makespan(curr_plan, num_resources, workflow_inaccur, positive=False, dynamic_res=False):
    '''
    Calculate makespan
    '''
    under = False
    reactive_resource_usage = [0] * num_resources
    resource_usage = [0] * num_resources
    expected = [0] * num_resources
    tmp_idx = [0] * num_resources
    for placement in curr_plan:
        workflow = placement[0]
        resource = placement[1]
        resource_id = resource['id']
        expected_finish = placement[3]
        if dynamic_res:
            perf = gauss(resource['performance'], resource['performance'] * 0.0644)
        else:
            pref = resource['performance']

        if positive:
            inaccur = uniform(0, workflow_inaccur)
        else:
            inaccur = uniform(-workflow_inaccur, workflow_inaccur)

        exec_time = (workflow['num_oper'] * (1 + inaccur)) / perf
        reactive_resource_usage[resource_id - 1] += exec_time
        resource_usage[resource_id - 1] = max(resource_usage[resource_id - 1] + exec_time, expected_finish)
        expected[resource_id - 1] = expected_finish
           
        tmp_idx[resource_id - 1] += 1
    return max(resource_usage), max(reactive_resource_usage), max(expected)


# ------------------------------------------------------------------------------
#
test_case = pd.read_csv('../Data/random/DynHeteroResources_StHeteroCampaignsRAND.csv')
results = pd.DataFrame(columns=['size','planner','plan','makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])

for idx, row in test_case.iterrows():
    size = row['size']
    planner = row['planner']
    plan = eval(row['plan'])
    makespan, reactive, expected = get_makespan(plan, size, 0, dynamic_res=True)
    time = row['time']
    results.loc[len(results)] = [size, planner, plan, makespan, reactive, expected, makespan - expected, reactive - expected, time]
results.to_csv('../Data/random/DynHeteroResources_StHeteroCampaignsRAND.csv', index=False)

test_case = pd.read_csv('../Data/random/DynHeteroResources_StHomoCampaignsRAND.csv')
results = pd.DataFrame(columns=['size','planner','plan','makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])

for idx, row in test_case.iterrows():
    size = row['size']
    planner = row['planner']
    plan = eval(row['plan'])
    makespan, reactive, expected = get_makespan(plan, size, 0, dynamic_res=True)
    time = row['time']
    results.loc[len(results)] = [size, planner, plan, makespan, reactive, expected, makespan - expected, reactive - expected, time]
results.to_csv('../Data/random/DynHeteroResources_StHomoCampaignsRAND.csv', index=False)

test_case = pd.read_csv('../Data/random/DynHomoResources_StHeteroCampaignsRAND.csv')
results = pd.DataFrame(columns=['size','planner','plan','makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])

for idx, row in test_case.iterrows():
    size = row['size']
    planner = row['planner']
    plan = eval(row['plan'])
    makespan, reactive, expected = get_makespan(plan, size, 0, dynamic_res=True)
    time = row['time']
    results.loc[len(results)] = [size, planner, plan, makespan, reactive, expected, makespan - expected, reactive - expected, time]
results.to_csv('../Data/random/DynHomoResources_StHeteroCampaignsRAND.csv', index=False)

test_case = pd.read_csv('../Data/random/DynHomoResources_StHomoCampaignsRAND.csv')
results = pd.DataFrame(columns=['size','planner','plan','makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])

for idx, row in test_case.iterrows():
    size = row['size']
    planner = row['planner']
    plan = eval(row['plan'])
    makespan, reactive, expected = get_makespan(plan, size, 0, dynamic_res=True)
    time = row['time']
    results.loc[len(results)] = [size, planner, plan, makespan, reactive, expected, makespan - expected, reactive - expected, time]
results.to_csv('../Data/random/DynHomoResources_StHomoCampaignsRAND.csv', index=False)

test_case = pd.read_csv('../Data/random/StHeteroCampaigns_4DynHeteroResourcesRAND.csv')
results = pd.DataFrame(columns=['size','planner','plan','makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])

for idx, row in test_case.iterrows():
    size = row['size']
    planner = row['planner']
    plan = eval(row['plan'])
    makespan, reactive, expected = get_makespan(plan, 4, 0, dynamic_res=True)
    time = row['time']
    results.loc[len(results)] = [size, planner, plan, makespan, reactive, expected, makespan - expected, reactive - expected, time]
results.to_csv('../Data/random/StHeteroCampaigns_4DynHeteroResourcesRAND.csv', index=False)

test_case = pd.read_csv('../Data/random/StHeteroCampaigns_4DynHomoResourcesRAND.csv')
results = pd.DataFrame(columns=['size','planner','plan','makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])

for idx, row in test_case.iterrows():
    size = row['size']
    planner = row['planner']
    plan = eval(row['plan'])
    makespan, reactive, expected = get_makespan(plan, 4, 0, dynamic_res=True)
    time = row['time']
    results.loc[len(results)] = [size, planner, plan, makespan, reactive, expected, makespan - expected, reactive - expected, time]
results.to_csv('../Data/random/StHeteroCampaigns_4DynHomoResourcesRAND.csv', index=False)

test_case = pd.read_csv('../Data/random/StHomoCampaigns_4DynHomoResourcesRAND.csv')
results = pd.DataFrame(columns=['size','planner','plan','makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])

for idx, row in test_case.iterrows():
    size = row['size']
    planner = row['planner']
    plan = eval(row['plan'])
    makespan, reactive, expected = get_makespan(plan, 4, 0, dynamic_res=True)
    time = row['time']
    results.loc[len(results)] = [size, planner, plan, makespan, reactive, expected, makespan - expected, reactive - expected, time]
results.to_csv('../Data/random/StHomoCampaigns_4DynHomoResourcesRAND.csv', index=False)