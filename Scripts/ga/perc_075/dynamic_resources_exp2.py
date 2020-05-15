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
    num_resources = [4, 8, 16, 32, 64, 128]
    results = pd.DataFrame(columns=['size','planner','plan','makespan','time'])
    campaign, num_oper = campaign_creator(num_workflows=1024)
    for res_num in num_resources:
        print('Number of resources: %d' % res_num)
        resources = resdf_to_dict(res_df=total_resources, size=res_num)
        for _ in range(repetitions):
            planner = GAPlanner(campaign=campaign, resources=resources, num_oper=num_oper, sid='test1', random_init=0.75)
            tic = time()
            plan = planner.plan()
            toc = time()
            makespan = get_makespan(plan, dyn_resources[0:res_num,:])
            results.loc[len(results)]= [res_num, 'GA-25', plan, makespan, toc - tic]
            del planner

    results.to_csv('../../../Data/ga/perc_075/DynFixedHomoResources_StHomoCampaignsGA25.csv', index=False)
