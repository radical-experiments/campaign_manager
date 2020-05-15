from radical.cm.planner import GAPlanner
from random import gauss
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

def resdf_to_dict(res_df, size):

    tmp_resources = list()
    for i in range(size):
        point = res_df.loc[i]
        tmp_res = {'id': int(point['id']),
                   'performance': 1.0}
        tmp_resources.append(tmp_res)

    return tmp_resources

def get_makespan(curr_plan, dyn_resources):
    '''
    Calculate makespan
    '''

    resource_usage = [0] * len(dyn_resources)
    tmp_idx = [0] * len(dyn_resources)
    for placement in curr_plan:
        workflow = placement[0]
        resource_id = placement[1]['id']
        #resource_usage[resource_id - 1] += workflow['num_oper'] / gauss(1, 4900 / 76000)
        resource_usage[resource_id - 1] += workflow['num_oper'] / \
                                           dyn_resources[resource_id - 1,
                                                         tmp_idx[resource_id - 1]]
        tmp_idx[resource_id - 1] += 1

    return max(resource_usage)


if __name__ == "__main__":

    repetitions = int(sys.argv[1])
    dyn_resources = np.load('../../../Data/homogeneous_resources_dyn.npy')
    total_resources = pd.read_csv('../../../Data/heterogeneous_resources.csv')
    total_cmp = pd.read_csv('../../../Data/heterogeneous_campaign.csv')
    num_resources = [4, 8, 16, 32, 64, 128]
    results = pd.DataFrame(columns=['size','planner','plan','makespan','time'])
    campaign, num_oper = df_to_lists(cmp=total_cmp, size=1024)
    for res_num in num_resources:
        print('Number of resources: %d' % res_num)
        resources = resdf_to_dict(res_df=total_resources, size=res_num)
        for _ in range(repetitions):
            planner = GAPlanner(campaign=campaign, resources=resources, num_oper=num_oper, sid='test1', random_init=0.50)
            tic = time()
            plan = planner.plan()
            toc = time()
            makespan = get_makespan(plan, dyn_resources[0:res_num,:])
            results.loc[len(results)]= [res_num, 'GA-50', plan, makespan, toc - tic]
            del planner

    results.to_csv('../../../Data/ga/perc_050/DynFixedHomoResources_StHeteroCampaignsGA50.csv', index=False)
