from radical.cm.planner import HeftPlanner
from random import gauss, uniform
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

if __name__ == "__main__":

    repetitions = int(sys.argv[1])
    resources = [{'id': 1, 'performance': 1},
                 {'id': 2, 'performance': 1},
                 {'id': 3, 'performance': 1},
                 {'id': 4, 'performance': 1}]
    dyn_resources = np.load('../../Data/homogeneous_resources_dyn.npy')
    campaign_sizes = [2048]
    results = pd.DataFrame(columns=['size','planner','plan','makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])
    for cm_size in campaign_sizes:
        print('Current campaign size: %d' % cm_size)
        campaign, num_oper = campaign_creator(num_workflows=cm_size)
        for _ in range(repetitions):
            planner = HeftPlanner(campaign=campaign, resources=resources, num_oper=num_oper, sid='help_exp')
            tic = time()
            plan = planner.plan()
            toc = time()
            makespan, reactive, expected = get_makespan(plan, 4, 0, dynamic_res=True)
            results.loc[len(results)] = [cm_size, 'HEFT', plan, makespan, reactive, expected, makespan - expected, reactive - expected, time]
            del planner

    results.to_csv('../../Data/heft/StHomoCampaigns_4DynHomoResourcesHEFT2.csv', index=False)
