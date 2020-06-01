from radical.cm.planner import L2FFPlanner 
from random import gauss, uniform
import pandas as pd
import numpy as np
import sys
from time import time


def df_to_lists(cmp, size):

    tmp_workflows = list()
    tmp_numoper = list()
    for i in range(size):
        point = cmp.loc[i] 
        workflow = {'description': None}
        workflow['id'] = int(point['id'])
        workflow['num_oper'] = point['num_oper']
        tmp_workflows.append(workflow)
        tmp_numoper.append(workflow['num_oper'])

    return tmp_workflows, tmp_numoper

def resdf_to_dict(res_df, size, prev_set=None):

    if size == len(res_df):
        tmp_resources = list()
        for i in range(size):
            point = res_df.loc[i]
            tmp_res = {'id': i + 1,
                       #'performance': 1.0}
                       'performance': point['PFlops Mean']}
            tmp_resources.append(tmp_res)
        return tmp_resources
    else:
        new_res = size - len(prev_set)
        tmp_resources = list()
        for i in range(new_res):
            point = res_df.loc[i % 4]
            tmp_res = {'id': len(prev_set) + i + 1,
                       'performance': gauss(point['PFlops Mean'], point['Pflops STD'])}
            tmp_resources.append(tmp_res)
        return prev_set + tmp_resources

def get_makespan(curr_plan, dyn_resources, used_resources, workflow_inaccur):
    '''
    Calculate makespan
    '''

    resource_usage = [0] * len(dyn_resources)
    tmp_idx = [0] * len(dyn_resources)
    for placement in curr_plan:
        workflow = placement[0]
        resource_id = placement[1]['id']
        perf = used_resources[resource_id - 1]['performance']
        resource_usage[resource_id - 1] += (workflow['num_oper'] * (1 + uniform(-workflow_inaccur, workflow_inaccur))) / gauss(perf, perf * 0.0644)
        
        tmp_idx[resource_id - 1] += 1

    return max(resource_usage)

if __name__ == "__main__":

    repetitions = int(sys.argv[1])
    workflow_inaccur = float(sys.argv[2]) / 100
    print(workflow_inaccur)
    dyn_resources = np.load('../../Data/homogeneous_resources_dyn.npy')
    total_resources = pd.read_csv('../../Data/heterogeneous_resources.csv')
    total_cmp = pd.read_csv('../../Data/heterogeneous_campaign.csv')
    num_resources = [4, 8, 16, 32, 64, 128]
    results = pd.DataFrame(columns=['size','planner','plan','makespan','time'])
    campaign, num_oper = df_to_lists(cmp=total_cmp, size=1024)
    resources = None
    for res_num in num_resources:
        print('Number of resources: %d' % res_num)
        resources = resdf_to_dict(res_df=total_resources, size=res_num, prev_set=resources)
        for _ in range(repetitions):
            planner = L2FFPlanner(campaign=campaign, resources=resources, num_oper=num_oper, sid='test1')
            tic = time()
            plan = planner.plan()
            toc = time()
            planner._logger.close()
            makespan = get_makespan(plan, dyn_resources[0:res_num,:], used_resources=resources, workflow_inaccur=workflow_inaccur)
            results.loc[len(results)]= [res_num, 'L2FF', plan, makespan, toc - tic]
            del planner

    results.to_csv('../../Data/l2ff/DynHeteroResources_StHeteroCampaignsL2FF_inaccur_%sperc.csv' % (sys.argv[2]), index=False)
