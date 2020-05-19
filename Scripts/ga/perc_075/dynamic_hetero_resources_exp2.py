from radical.cm.planner import GAPlanner
from random import gauss
import pandas as pd
import numpy as np
import sys
from time import time


def campaign_creator(num_workflows):

    tmp_campaign = list()
    tmp_num_oper = list()
    for i in range(num_workflows):
        workflow = {'description':None}
        workflow['id'] = i + 1
        workflow['num_oper'] = 75000
        
        tmp_campaign.append(workflow)
        tmp_num_oper.append(workflow['num_oper'])

    return tmp_campaign, tmp_num_oper

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

def get_makespan(curr_plan, dyn_resources, used_resources):
    '''
    Calculate makespan
    '''

    resource_usage = [0] * len(dyn_resources)
    tmp_idx = [0] * len(dyn_resources)
    for placement in curr_plan:
        workflow = placement[0]
        resource_id = placement[1]['id']
        perf = used_resources[resource_id - 1]['performance']
        resource_usage[resource_id - 1] += workflow['num_oper'] / gauss(perf, perf * 0.0644)
        
        tmp_idx[resource_id - 1] += 1

    return max(resource_usage)


if __name__ == "__main__":

    repetitions = int(sys.argv[1])
    dyn_resources = np.load('../../../Data/homogeneous_resources_dyn.npy')
    total_resources = pd.read_csv('../../../Data/heterogeneous_resources.csv')
    num_resources = [4, 8, 16, 32, 64, 128]
    results = pd.DataFrame(columns=['size','planner','plan','makespan','time'])
    campaign, num_oper = campaign_creator(num_workflows=1024)
    resources = None
    for res_num in num_resources:
        print('Number of resources: %d' % res_num)
        resources = resdf_to_dict(res_df=total_resources, size=res_num, prev_set=resources)
        for _ in range(repetitions):
            planner = GAPlanner(campaign=campaign, resources=resources, num_oper=num_oper, random_init=0.75, sid='ga_exps')
            tic = time()
            plan = planner.plan()
            toc = time()
            makespan = get_makespan(plan, dyn_resources[0:res_num,:],used_resources=resources)
            results.loc[len(results)]= [res_num, 'GA-25', plan, makespan, toc - tic]
            del planner

    results.to_csv('../../../Data/ga/perc_075/DynHeteroResources_StHomoCampaignsGA25.csv', index=False)
