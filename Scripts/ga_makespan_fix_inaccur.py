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
test_case = pd.read_csv('../Data/ga/perc_050/StHeteroCampaigns_4DynHeteroResourcesGA50_inaccur_5perc.csv')
results = pd.DataFrame(columns=['size','planner','plan','makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])

for idx, row in test_case.iterrows():
    size = row['size']
    planner = row['planner']
    plan = eval(row['plan'])
    makespan, reactive, expected = get_makespan(plan, 4, 0.05, dynamic_res=True)
    time = row['time']
    results.loc[len(results)] = [size, planner, plan, makespan, reactive, expected, makespan - expected, reactive - expected, time]
results.to_csv('../Data/ga/perc_050/StHeteroCampaigns_4DynHeteroResourcesGA50_inaccur_5perc.csv', index=False)

results = pd.DataFrame(columns=['size','planner','plan','makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])

for idx, row in test_case.iterrows():
    size = row['size']
    planner = row['planner']
    plan = eval(row['plan'])
    makespan, reactive, expected = get_makespan(plan, 4, 0.05, dynamic_res=False)
    time = row['time']
    results.loc[len(results)] = [size, planner, plan, makespan, reactive, expected, makespan - expected, reactive - expected, time]
results.to_csv('../Data/ga/perc_050/StHeteroCampaigns_4StHeteroResourcesGA50_inaccur_5perc.csv', index=False)

# ------------------------------------------------------------------------------
# 10%
test_case = pd.read_csv('../Data/ga/perc_050/StHeteroCampaigns_4DynHeteroResourcesGA50_inaccur_10perc.csv')
results = pd.DataFrame(columns=['size','planner','plan','makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])

for idx, row in test_case.iterrows():
    size = row['size']
    planner = row['planner']
    plan = eval(row['plan'])
    makespan, reactive, expected = get_makespan(plan, 4, 0.1, dynamic_res=True)
    time = row['time']
    results.loc[len(results)] = [size, planner, plan, makespan, reactive, expected, makespan - expected, reactive - expected, time]
results.to_csv('../Data/ga/perc_050/StHeteroCampaigns_4DynHeteroResourcesGA50_inaccur_10perc.csv', index=False)

results = pd.DataFrame(columns=['size','planner','plan','makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])

for idx, row in test_case.iterrows():
    size = row['size']
    planner = row['planner']
    plan = eval(row['plan'])
    makespan, reactive, expected = get_makespan(plan, 4, 0.1, dynamic_res=False)
    time = row['time']
    results.loc[len(results)] = [size, planner, plan, makespan, reactive, expected, makespan - expected, reactive - expected, time]
results.to_csv('../Data/ga/perc_050/StHeteroCampaigns_4StHeteroResourcesGA50_inaccur_10perc.csv', index=False)

# ------------------------------------------------------------------------------
# 20%
test_case = pd.read_csv('../Data/ga/perc_050/StHeteroCampaigns_4DynHeteroResourcesGA50_inaccur_20perc.csv')
results = pd.DataFrame(columns=['size','planner','plan','makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])

for idx, row in test_case.iterrows():
    size = row['size']
    planner = row['planner']
    plan = eval(row['plan'])
    makespan, reactive, expected = get_makespan(plan, 4, 0.2, dynamic_res=True)
    time = row['time']
    results.loc[len(results)] = [size, planner, plan, makespan, reactive, expected, makespan - expected, reactive - expected, time]
results.to_csv('../Data/ga/perc_050/StHeteroCampaigns_4DynHeteroResourcesGA50_inaccur_20perc.csv', index=False)

results = pd.DataFrame(columns=['size','planner','plan','makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])

for idx, row in test_case.iterrows():
    size = row['size']
    planner = row['planner']
    plan = eval(row['plan'])
    makespan, reactive, expected = get_makespan(plan, 4, 0.2, dynamic_res=False)
    time = row['time']
    results.loc[len(results)] = [size, planner, plan, makespan, reactive, expected, makespan - expected, reactive - expected, time]
results.to_csv('../Data/ga/perc_050/StHeteroCampaigns_4StHeteroResourcesGA50_inaccur_20perc.csv', index=False)

# ------------------------------------------------------------------------------
# 30%
test_case = pd.read_csv('../Data/ga/perc_050/StHeteroCampaigns_4DynHeteroResourcesGA50_inaccur_30perc.csv')
results = pd.DataFrame(columns=['size','planner','plan','makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])

for idx, row in test_case.iterrows():
    size = row['size']
    planner = row['planner']
    plan = eval(row['plan'])
    makespan, reactive, expected = get_makespan(plan, 4, 0.3, dynamic_res=True)
    time = row['time']
    results.loc[len(results)] = [size, planner, plan, makespan, reactive, expected, makespan - expected, reactive - expected, time]
results.to_csv('../Data/ga/perc_050/StHeteroCampaigns_4DynHeteroResourcesGA50_inaccur_30perc.csv', index=False)

results = pd.DataFrame(columns=['size','planner','plan','makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])

for idx, row in test_case.iterrows():
    size = row['size']
    planner = row['planner']
    plan = eval(row['plan'])
    makespan, reactive, expected = get_makespan(plan, 4, 0.3, dynamic_res=False)
    time = row['time']
    results.loc[len(results)] = [size, planner, plan, makespan, reactive, expected, makespan - expected, reactive - expected, time]
results.to_csv('../Data/ga/perc_050/StHeteroCampaigns_4StHeteroResourcesGA50_inaccur_30perc.csv', index=False)

# ------------------------------------------------------------------------------
# 40%
test_case = pd.read_csv('../Data/ga/perc_050/StHeteroCampaigns_4DynHeteroResourcesGA50_inaccur_40perc.csv')
results = pd.DataFrame(columns=['size','planner','plan','makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])

for idx, row in test_case.iterrows():
    size = row['size']
    planner = row['planner']
    plan = eval(row['plan'])
    makespan, reactive, expected = get_makespan(plan, 4, 0.4, dynamic_res=True)
    time = row['time']
    results.loc[len(results)] = [size, planner, plan, makespan, reactive, expected, makespan - expected, reactive - expected, time]
results.to_csv('../Data/ga/perc_050/StHeteroCampaigns_4DynHeteroResourcesGA50_inaccur_40perc.csv', index=False)

results = pd.DataFrame(columns=['size','planner','plan','makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])

for idx, row in test_case.iterrows():
    size = row['size']
    planner = row['planner']
    plan = eval(row['plan'])
    makespan, reactive, expected = get_makespan(plan, 4, 0.4, dynamic_res=False)
    time = row['time']
    results.loc[len(results)] = [size, planner, plan, makespan, reactive, expected, makespan - expected, reactive - expected, time]
results.to_csv('../Data/ga/perc_050/StHeteroCampaigns_4StHeteroResourcesGA50_inaccur_40perc.csv', index=False)

# ------------------------------------------------------------------------------
# 50%
test_case = pd.read_csv('../Data/ga/perc_050/StHeteroCampaigns_4DynHeteroResourcesGA50_inaccur_50perc.csv')
results = pd.DataFrame(columns=['size','planner','plan','makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])

for idx, row in test_case.iterrows():
    size = row['size']
    planner = row['planner']
    plan = eval(row['plan'])
    makespan, reactive, expected = get_makespan(plan, 4, 0.5, dynamic_res=True)
    time = row['time']
    results.loc[len(results)] = [size, planner, plan, makespan, reactive, expected, makespan - expected, reactive - expected, time]
results.to_csv('../Data/ga/perc_050/StHeteroCampaigns_4DynHeteroResourcesGA50_inaccur_50perc.csv', index=False)

results = pd.DataFrame(columns=['size','planner','plan','makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])

for idx, row in test_case.iterrows():
    size = row['size']
    planner = row['planner']
    plan = eval(row['plan'])
    makespan, reactive, expected = get_makespan(plan, 4, 0.5, dynamic_res=False)
    time = row['time']
    results.loc[len(results)] = [size, planner, plan, makespan, reactive, expected, makespan - expected, reactive - expected, time]
results.to_csv('../Data/ga/perc_050/StHeteroCampaigns_4StHeteroResourcesGA50_inaccur_50perc.csv', index=False)

# ------------------------------------------------------------------------------
# 60%
test_case = pd.read_csv('../Data/ga/perc_050/StHeteroCampaigns_4DynHeteroResourcesGA50_inaccur_60perc.csv')
results = pd.DataFrame(columns=['size','planner','plan','makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])

for idx, row in test_case.iterrows():
    size = row['size']
    planner = row['planner']
    plan = eval(row['plan'])
    makespan, reactive, expected = get_makespan(plan, 4, 0.6, dynamic_res=True)
    time = row['time']
    results.loc[len(results)] = [size, planner, plan, makespan, reactive, expected, makespan - expected, reactive - expected, time]
results.to_csv('../Data/ga/perc_050/StHeteroCampaigns_4DynHeteroResourcesGA50_inaccur_60perc.csv', index=False)

results = pd.DataFrame(columns=['size','planner','plan','makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])

for idx, row in test_case.iterrows():
    size = row['size']
    planner = row['planner']
    plan = eval(row['plan'])
    makespan, reactive, expected = get_makespan(plan, 4, 0.6, dynamic_res=False)
    time = row['time']
    results.loc[len(results)] = [size, planner, plan, makespan, reactive, expected, makespan - expected, reactive - expected, time]
results.to_csv('../Data/ga/perc_050/StHeteroCampaigns_4StHeteroResourcesGA50_inaccur_60perc.csv', index=False)


# ------------------------------------------------------------------------------
# 70%
test_case = pd.read_csv('../Data/ga/perc_050/StHeteroCampaigns_4DynHeteroResourcesGA50_inaccur_70perc.csv')
results = pd.DataFrame(columns=['size','planner','plan','makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])

for idx, row in test_case.iterrows():
    size = row['size']
    planner = row['planner']
    plan = eval(row['plan'])
    makespan, reactive, expected = get_makespan(plan, 4, 0.7, dynamic_res=True)
    time = row['time']
    results.loc[len(results)] = [size, planner, plan, makespan, reactive, expected, makespan - expected, reactive - expected, time]
results.to_csv('../Data/ga/perc_050/StHeteroCampaigns_4DynHeteroResourcesGA50_inaccur_70perc.csv', index=False)

results = pd.DataFrame(columns=['size','planner','plan','makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])

for idx, row in test_case.iterrows():
    size = row['size']
    planner = row['planner']
    plan = eval(row['plan'])
    makespan, reactive, expected = get_makespan(plan, 4, 0.7, dynamic_res=False)
    time = row['time']
    results.loc[len(results)] = [size, planner, plan, makespan, reactive, expected, makespan - expected, reactive - expected, time]
results.to_csv('../Data/ga/perc_050/StHeteroCampaigns_4StHeteroResourcesGA50_inaccur_70perc.csv', index=False)

# ------------------------------------------------------------------------------
# 80%
test_case = pd.read_csv('../Data/ga/perc_050/StHeteroCampaigns_4DynHeteroResourcesGA50_inaccur_80perc.csv')
results = pd.DataFrame(columns=['size','planner','plan','makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])

for idx, row in test_case.iterrows():
    size = row['size']
    planner = row['planner']
    plan = eval(row['plan'])
    makespan, reactive, expected = get_makespan(plan, 4, 0.8, dynamic_res=True)
    time = row['time']
    results.loc[len(results)] = [size, planner, plan, makespan, reactive, expected, makespan - expected, reactive - expected, time]
results.to_csv('../Data/ga/perc_050/StHeteroCampaigns_4DynHeteroResourcesGA50_inaccur_80perc.csv', index=False)

results = pd.DataFrame(columns=['size','planner','plan','makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])

for idx, row in test_case.iterrows():
    size = row['size']
    planner = row['planner']
    plan = eval(row['plan'])
    makespan, reactive, expected = get_makespan(plan, 4, 0.8, dynamic_res=False)
    time = row['time']
    results.loc[len(results)] = [size, planner, plan, makespan, reactive, expected, makespan - expected, reactive - expected, time]
results.to_csv('../Data/ga/perc_050/StHeteroCampaigns_4StHeteroResourcesGA50_inaccur_80perc.csv', index=False)

# ------------------------------------------------------------------------------
# 90%
test_case = pd.read_csv('../Data/ga/perc_050/StHeteroCampaigns_4DynHeteroResourcesGA50_inaccur_90perc.csv')
results = pd.DataFrame(columns=['size','planner','plan','makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])

for idx, row in test_case.iterrows():
    size = row['size']
    planner = row['planner']
    plan = eval(row['plan'])
    makespan, reactive, expected = get_makespan(plan, 4, 0.9, dynamic_res=True)
    time = row['time']
    results.loc[len(results)] = [size, planner, plan, makespan, reactive, expected, makespan - expected, reactive - expected, time]
results.to_csv('../Data/ga/perc_050/StHeteroCampaigns_4DynHeteroResourcesGA50_inaccur_90perc.csv', index=False)

results = pd.DataFrame(columns=['size','planner','plan','makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])

for idx, row in test_case.iterrows():
    size = row['size']
    planner = row['planner']
    plan = eval(row['plan'])
    makespan, reactive, expected = get_makespan(plan, 4, 0.9, dynamic_res=False)
    time = row['time']
    results.loc[len(results)] = [size, planner, plan, makespan, reactive, expected, makespan - expected, reactive - expected, time]
results.to_csv('../Data/ga/perc_050/StHeteroCampaigns_4StHeteroResourcesGA50_inaccur_90perc.csv', index=False)
