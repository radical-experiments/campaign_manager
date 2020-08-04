from radical.cm.planner import HeftPlanner, GAPlanner, L2FFPlanner, RandomPlanner
from random import gauss, uniform
import pandas as pd
import numpy as np
import sys
from time import time


def df_to_lists(size):

    tmp_workflows = list()
    tmp_numoper = list()
    for i in range(size):
        point = gauss(75000, 6000)
        workflow = {'description': None}
        workflow['id'] = int(i + 1)
        workflow['num_oper'] = point
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


if __name__ == "__main__":

    repetitions = int(sys.argv[1])
    workflow_inaccur = float(sys.argv[2]) / 100
    resources = [{'id': 1, 'performance': 1.3},
                 {'id': 2, 'performance': 2.76},
                 {'id': 3, 'performance': 10.68},
                 {'id': 4, 'performance': 23.516}]
    campaign_sizes = [4, 8, 16, 32, 64, 128, 256, 512, 1024]
    resultsHEFT = pd.DataFrame(columns=['size', 'planner', 'plan', 'makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])
    resultsGA50 = pd.DataFrame(columns=['size', 'planner', 'plan', 'makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])
    resultsL2FF = pd.DataFrame(columns=['size', 'planner', 'plan', 'makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])
    resultsRAND = pd.DataFrame(columns=['size', 'planner', 'plan', 'makespan', 'reactive', 'expected','mpn_snt', 'rect_snt', 'time'])
    for cm_size in campaign_sizes:
        print('Current campaign size: %d' % cm_size)
        for _ in range(repetitions):
            campaign, num_oper = df_to_lists(size=cm_size)
            planner1 = HeftPlanner(campaign=campaign, resources=resources, num_oper=num_oper, sid='heft_exp')
            planner2 = GAPlanner(campaign=campaign, resources=resources, num_oper=num_oper, sid='ga50', random_init=0.5)
            planner3 = L2FFPlanner(campaign=campaign, resources=resources, num_oper=num_oper, sid='l2ff')
            planner4 = RandomPlanner(campaign=campaign, resources=resources, num_oper=num_oper, sid='random')
            
            tic = time()
            plan = planner1.plan()
            toc = time()
            makespan, reactive, expected = get_makespan(plan, 4, workflow_inaccur=workflow_inaccur)
            resultsHEFT.loc[len(resultsHEFT)] = [cm_size, 'HEFT', plan, makespan, reactive, expected, makespan - expected, reactive - expected, toc-tic]

            tic = time()
            plan = planner2.plan()
            toc = time()
            makespan, reactive, expected = get_makespan(plan, 4, workflow_inaccur=workflow_inaccur)
            resultsGA50.loc[len(resultsGA50)] = [cm_size, 'GA-50', plan, makespan, reactive, expected, makespan - expected, reactive - expected, toc-tic]

            tic = time()
            plan = planner3.plan()
            toc = time()
            makespan, reactive, expected = get_makespan(plan, 4, workflow_inaccur=workflow_inaccur)
            resultsL2FF.loc[len(resultsL2FF)] = [cm_size, 'L2FF', plan, makespan, reactive, expected, makespan - expected, reactive - expected, toc-tic]

            tic = time()
            plan = planner4.plan()
            toc = time()
            makespan, reactive, expected = get_makespan(plan, 4, workflow_inaccur=workflow_inaccur)
            resultsRAND.loc[len(resultsRAND)] = [cm_size, 'RANDOM', plan, makespan, reactive, expected, makespan - expected, reactive - expected, toc-tic]

            del planner1, planner2, planner3, planner4

    resultsHEFT.to_csv('../Data/heft/StHeteroCampaigns_4StHeteroResourcesHEFT_inaccur%d_new.csv' % sys.argv[2], index=False)
    resultsGA50.to_csv('../Data/ga/perc_050/StHeteroCampaigns_4StHeteroResourcesGA50_inaccur%d_new.csv' % sys.argv[2], index=False)
    resultsL2FF.to_csv('../Data/l2ff/StHeteroCampaigns_4StHeteroResourcesL2FF_inaccur%d_new.csv' % sys.argv[2], index=False)
    resultsRAND.to_csv('../Data/random/StHeteroCampaigns_4StHeteroResourcesRAND_inaccur%d_new.csv' % sys.argv[2], index=False)
