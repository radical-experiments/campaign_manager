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
        #resource_usage[resource_id - 1] += workflow['num_oper'] / \
        #                                   dyn_resources[resource_id - 1,
        #                                                 tmp_idx[resource_id - 1]]
        
        tmp_idx[resource_id - 1] += 1

    return max(resource_usage)


if __name__ == "__main__":

    repetitions = int(sys.argv[1])
    #resources = [{'id': 1, 'performance': 1},
    #             {'id': 2, 'performance': 1},
    #             {'id': 3, 'performance': 1},
    #             {'id': 4, 'performance': 1}]
    resources = [{'id': 1, 'performance': 1.3},
                 {'id': 2, 'performance': 2.76},
                 {'id': 3, 'performance': 10.68},
                 {'id': 4, 'performance': 23.516}]
    dyn_resources = np.load('../../../Data/homogeneous_resources_dyn.npy')
    campaign_sizes = [4, 8, 16, 32, 64, 128, 256, 512, 1024]
    results = pd.DataFrame(columns=['size','planner','plan','makespan','time'])
    total_cmp = pd.read_csv('../../../Data/heterogeneous_campaign.csv')
    for cm_size in campaign_sizes:
        print('Current campaign size: %d' % cm_size)
        campaign, num_oper = df_to_lists(cmp=total_cmp, size=cm_size)
        for _ in range(repetitions):
            planner = GAPlanner(campaign=campaign, resources=resources, num_oper=num_oper, sid='test1', random_init=0.75)
            tic = time()
            plan = planner.plan()
            toc = time()
            makespan = get_makespan(plan, dyn_resources[0:cm_size,:], used_resources=resources)
            results.loc[len(results)]= [cm_size, 'GA-25', plan, makespan, toc - tic]
            del planner

    results.to_csv('../../../Data/ga/perc_075/StHeteroCampaigns_4DynHeteroResourcesGA25.csv', index=False)
