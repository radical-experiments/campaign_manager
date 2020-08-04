from radical.cm.planner import GAPlanner
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
    #resources = [{'id': 1, 'performance': 1},
    #             {'id': 2, 'performance': 1},
    #             {'id': 3, 'performance': 1},
    #             {'id': 4, 'performance': 1}]
    resources = [{'id': 1, 'performance': 1.3},
                 {'id': 2, 'performance': 2.76},
                 {'id': 3, 'performance': 10.68},
                 {'id': 4, 'performance': 23.516}]
    dyn_resources = np.load('../../../Data/homogeneous_resources_dyn.npy')
    campaign_sizes = [2048]
    results = pd.DataFrame(columns=['size','planner','plan','makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])
    for cm_size in campaign_sizes:
        print('Current campaign size: %d' % cm_size)
        campaign, num_oper = df_to_lists(cmp=total_cmp, size=cm_size)
        for _ in range(repetitions):
            planner = GAPlanner(campaign=campaign, resources=resources, num_oper=num_oper, sid='test1', random_init=0.50)
            tic = time()
            plan = planner.plan()
            toc = time()
            makespan, reactive, expected = get_makespan(plan, 4, 0, dynamic_res=True)
            results.loc[len(results)] = [cm_size, 'GA-50', plan, makespan, reactive, expected, makespan - expected, reactive - expected, time]
            del planner

    results.to_csv('../../../Data/ga/perc_050/StHeteroCampaigns_4DynHeteroResourcesGA502.csv', index=False)
