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
            perf = resource['performance']

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
# 5%
test_case = pd.read_csv('../Data/l2ff/DynHeteroResources_StHeteroCampaignsL2FF_inaccur_p5perc.csv')
results = pd.DataFrame(columns=['size','planner','plan','makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])

for idx, row in test_case.iterrows():
    size = row['size']
    planner = row['planner']
    plan = eval(row['plan'])
    makespan, reactive, expected = get_makespan(plan, size, 0.05, dynamic_res=True, positive=True)
    time = row['time']
    results.loc[len(results)] = [size, planner, plan, makespan, reactive, expected, makespan - expected, reactive - expected, time]
results.to_csv('../Data/l2ff/DynHeteroResources_StHeteroCampaignsL2FF_inaccur_p5perc.csv', index=False)

results = pd.DataFrame(columns=['size','planner','plan','makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])

for idx, row in test_case.iterrows():
    size = row['size']
    planner = row['planner']
    plan = eval(row['plan'])
    makespan, reactive, expected = get_makespan(plan, size, 0.05, dynamic_res=False, positive=True)
    time = row['time']
    results.loc[len(results)] = [size, planner, plan, makespan, reactive, expected, makespan - expected, reactive - expected, time]
results.to_csv('../Data/l2ff/StHeteroResources_StHeteroCampaignsL2FF_inaccur_p5perc.csv', index=False)

# ------------------------------------------------------------------------------
# 10%
test_case = pd.read_csv('../Data/l2ff/DynHeteroResources_StHeteroCampaignsL2FF_inaccur_p10perc.csv')
results = pd.DataFrame(columns=['size','planner','plan','makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])

for idx, row in test_case.iterrows():
    size = row['size']
    planner = row['planner']
    plan = eval(row['plan'])
    makespan, reactive, expected = get_makespan(plan, size, 0.1, dynamic_res=True, positive=True)
    time = row['time']
    results.loc[len(results)] = [size, planner, plan, makespan, reactive, expected, makespan - expected, reactive - expected, time]
results.to_csv('../Data/l2ff/DynHeteroResources_StHeteroCampaignsL2FF_inaccur_p10perc.csv', index=False)

results = pd.DataFrame(columns=['size','planner','plan','makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])

for idx, row in test_case.iterrows():
    size = row['size']
    planner = row['planner']
    plan = eval(row['plan'])
    makespan, reactive, expected = get_makespan(plan, size, 0.1, dynamic_res=False, positive=True)
    time = row['time']
    results.loc[len(results)] = [size, planner, plan, makespan, reactive, expected, makespan - expected, reactive - expected, time]
results.to_csv('../Data/l2ff/StHeteroResources_StHeteroCampaignsL2FF_inaccur_p10perc.csv', index=False)

# ------------------------------------------------------------------------------
# 20%
test_case = pd.read_csv('../Data/l2ff/DynHeteroResources_StHeteroCampaignsL2FF_inaccur_p20perc.csv')
results = pd.DataFrame(columns=['size','planner','plan','makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])

for idx, row in test_case.iterrows():
    size = row['size']
    planner = row['planner']
    plan = eval(row['plan'])
    makespan, reactive, expected = get_makespan(plan, size, 0.2, dynamic_res=True, positive=True)
    time = row['time']
    results.loc[len(results)] = [size, planner, plan, makespan, reactive, expected, makespan - expected, reactive - expected, time]
results.to_csv('../Data/l2ff/DynHeteroResources_StHeteroCampaignsL2FF_inaccur_p20perc.csv', index=False)

results = pd.DataFrame(columns=['size','planner','plan','makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])

for idx, row in test_case.iterrows():
    size = row['size']
    planner = row['planner']
    plan = eval(row['plan'])
    makespan, reactive, expected = get_makespan(plan, size, 0.2, dynamic_res=False, positive=True)
    time = row['time']
    results.loc[len(results)] = [size, planner, plan, makespan, reactive, expected, makespan - expected, reactive - expected, time]
results.to_csv('../Data/l2ff/StHeteroResources_StHeteroCampaignsL2FF_inaccur_p20perc.csv', index=False)

# ------------------------------------------------------------------------------
# 30%
test_case = pd.read_csv('../Data/l2ff/DynHeteroResources_StHeteroCampaignsL2FF_inaccur_p30perc.csv')
results = pd.DataFrame(columns=['size','planner','plan','makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])

for idx, row in test_case.iterrows():
    size = row['size']
    planner = row['planner']
    plan = eval(row['plan'])
    makespan, reactive, expected = get_makespan(plan, size, 0.3, dynamic_res=True, positive=True)
    time = row['time']
    results.loc[len(results)] = [size, planner, plan, makespan, reactive, expected, makespan - expected, reactive - expected, time]
results.to_csv('../Data/l2ff/DynHeteroResources_StHeteroCampaignsL2FF_inaccur_p30perc.csv', index=False)

results = pd.DataFrame(columns=['size','planner','plan','makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])

for idx, row in test_case.iterrows():
    size = row['size']
    planner = row['planner']
    plan = eval(row['plan'])
    makespan, reactive, expected = get_makespan(plan, size, 0.3, dynamic_res=False, positive=True)
    time = row['time']
    results.loc[len(results)] = [size, planner, plan, makespan, reactive, expected, makespan - expected, reactive - expected, time]
results.to_csv('../Data/l2ff/StHeteroResources_StHeteroCampaignsL2FF_inaccur_p30perc.csv', index=False)

# ------------------------------------------------------------------------------
# 40%
test_case = pd.read_csv('../Data/l2ff/DynHeteroResources_StHeteroCampaignsL2FF_inaccur_p40perc.csv')
results = pd.DataFrame(columns=['size','planner','plan','makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])

for idx, row in test_case.iterrows():
    size = row['size']
    planner = row['planner']
    plan = eval(row['plan'])
    makespan, reactive, expected = get_makespan(plan, size, 0.4, dynamic_res=True, positive=True)
    time = row['time']
    results.loc[len(results)] = [size, planner, plan, makespan, reactive, expected, makespan - expected, reactive - expected, time]
results.to_csv('../Data/l2ff/DynHeteroResources_StHeteroCampaignsL2FF_inaccur_p40perc.csv', index=False)

results = pd.DataFrame(columns=['size','planner','plan','makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])

for idx, row in test_case.iterrows():
    size = row['size']
    planner = row['planner']
    plan = eval(row['plan'])
    makespan, reactive, expected = get_makespan(plan, size, 0.4, dynamic_res=False, positive=True)
    time = row['time']
    results.loc[len(results)] = [size, planner, plan, makespan, reactive, expected, makespan - expected, reactive - expected, time]
results.to_csv('../Data/l2ff/StHeteroResources_StHeteroCampaignsL2FF_inaccur_p40perc.csv', index=False)

# ------------------------------------------------------------------------------
# 50%
test_case = pd.read_csv('../Data/l2ff/DynHeteroResources_StHeteroCampaignsL2FF_inaccur_p50perc.csv')
results = pd.DataFrame(columns=['size','planner','plan','makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])

for idx, row in test_case.iterrows():
    size = row['size']
    planner = row['planner']
    plan = eval(row['plan'])
    makespan, reactive, expected = get_makespan(plan, size, 0.5, dynamic_res=True, positive=True)
    time = row['time']
    results.loc[len(results)] = [size, planner, plan, makespan, reactive, expected, makespan - expected, reactive - expected, time]
results.to_csv('../Data/l2ff/DynHeteroResources_StHeteroCampaignsL2FF_inaccur_p50perc.csv', index=False)

results = pd.DataFrame(columns=['size','planner','plan','makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])

for idx, row in test_case.iterrows():
    size = row['size']
    planner = row['planner']
    plan = eval(row['plan'])
    makespan, reactive, expected = get_makespan(plan, size, 0.5, dynamic_res=False, positive=True)
    time = row['time']
    results.loc[len(results)] = [size, planner, plan, makespan, reactive, expected, makespan - expected, reactive - expected, time]
results.to_csv('../Data/l2ff/StHeteroResources_StHeteroCampaignsL2FF_inaccur_p50perc.csv', index=False)

# ------------------------------------------------------------------------------
# 60%
test_case = pd.read_csv('../Data/l2ff/DynHeteroResources_StHeteroCampaignsL2FF_inaccur_p60perc.csv')
results = pd.DataFrame(columns=['size','planner','plan','makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])

for idx, row in test_case.iterrows():
    size = row['size']
    planner = row['planner']
    plan = eval(row['plan'])
    makespan, reactive, expected = get_makespan(plan, size, 0.6, dynamic_res=True, positive=True)
    time = row['time']
    results.loc[len(results)] = [size, planner, plan, makespan, reactive, expected, makespan - expected, reactive - expected, time]
results.to_csv('../Data/l2ff/DynHeteroResources_StHeteroCampaignsL2FF_inaccur_p60perc.csv', index=False)

results = pd.DataFrame(columns=['size','planner','plan','makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])

for idx, row in test_case.iterrows():
    size = row['size']
    planner = row['planner']
    plan = eval(row['plan'])
    makespan, reactive, expected = get_makespan(plan, size, 0.6, dynamic_res=False, positive=True)
    time = row['time']
    results.loc[len(results)] = [size, planner, plan, makespan, reactive, expected, makespan - expected, reactive - expected, time]
results.to_csv('../Data/l2ff/StHeteroResources_StHeteroCampaignsL2FF_inaccur_p60perc.csv', index=False)


# ------------------------------------------------------------------------------
# 70%
test_case = pd.read_csv('../Data/l2ff/DynHeteroResources_StHeteroCampaignsL2FF_inaccur_p70perc.csv')
results = pd.DataFrame(columns=['size','planner','plan','makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])

for idx, row in test_case.iterrows():
    size = row['size']
    planner = row['planner']
    plan = eval(row['plan'])
    makespan, reactive, expected = get_makespan(plan, size, 0.7, dynamic_res=True, positive=True)
    time = row['time']
    results.loc[len(results)] = [size, planner, plan, makespan, reactive, expected, makespan - expected, reactive - expected, time]
results.to_csv('../Data/l2ff/DynHeteroResources_StHeteroCampaignsL2FF_inaccur_p70perc.csv', index=False)

results = pd.DataFrame(columns=['size','planner','plan','makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])

for idx, row in test_case.iterrows():
    size = row['size']
    planner = row['planner']
    plan = eval(row['plan'])
    makespan, reactive, expected = get_makespan(plan, size, 0.7, dynamic_res=False, positive=True)
    time = row['time']
    results.loc[len(results)] = [size, planner, plan, makespan, reactive, expected, makespan - expected, reactive - expected, time]
results.to_csv('../Data/l2ff/StHeteroResources_StHeteroCampaignsL2FF_inaccur_p70perc.csv', index=False)

# ------------------------------------------------------------------------------
# 80%
test_case = pd.read_csv('../Data/l2ff/DynHeteroResources_StHeteroCampaignsL2FF_inaccur_p80perc.csv')
results = pd.DataFrame(columns=['size','planner','plan','makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])

for idx, row in test_case.iterrows():
    size = row['size']
    planner = row['planner']
    plan = eval(row['plan'])
    makespan, reactive, expected = get_makespan(plan, size, 0.8, dynamic_res=True, positive=True)
    time = row['time']
    results.loc[len(results)] = [size, planner, plan, makespan, reactive, expected, makespan - expected, reactive - expected, time]
results.to_csv('../Data/l2ff/DynHeteroResources_StHeteroCampaignsL2FF_inaccur_p80perc.csv', index=False)

results = pd.DataFrame(columns=['size','planner','plan','makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])

for idx, row in test_case.iterrows():
    size = row['size']
    planner = row['planner']
    plan = eval(row['plan'])
    makespan, reactive, expected = get_makespan(plan, size, 0.8, dynamic_res=False, positive=True)
    time = row['time']
    results.loc[len(results)] = [size, planner, plan, makespan, reactive, expected, makespan - expected, reactive - expected, time]
results.to_csv('../Data/l2ff/StHeteroResources_StHeteroCampaignsL2FF_inaccur_p80perc.csv', index=False)

# ------------------------------------------------------------------------------
# 90%
test_case = pd.read_csv('../Data/l2ff/DynHeteroResources_StHeteroCampaignsL2FF_inaccur_p90perc.csv')
results = pd.DataFrame(columns=['size','planner','plan','makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])

for idx, row in test_case.iterrows():
    size = row['size']
    planner = row['planner']
    plan = eval(row['plan'])
    makespan, reactive, expected = get_makespan(plan, size, 0.9, dynamic_res=True, positive=True)
    time = row['time']
    results.loc[len(results)] = [size, planner, plan, makespan, reactive, expected, makespan - expected, reactive - expected, time]
results.to_csv('../Data/l2ff/DynHeteroResources_StHeteroCampaignsL2FF_inaccur_p90perc.csv', index=False)

results = pd.DataFrame(columns=['size','planner','plan','makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])

for idx, row in test_case.iterrows():
    size = row['size']
    planner = row['planner']
    plan = eval(row['plan'])
    makespan, reactive, expected = get_makespan(plan, size, 0.9, dynamic_res=False, positive=True)
    time = row['time']
    results.loc[len(results)] = [size, planner, plan, makespan, reactive, expected, makespan - expected, reactive - expected, time]
results.to_csv('../Data/l2ff/StHeteroResources_StHeteroCampaignsL2FF_inaccur_p90perc.csv', index=False)
