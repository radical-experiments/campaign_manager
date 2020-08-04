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
        point = 75000 # gauss(75000, 6000)
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
    resources = [{'id': 1, 'performance': 1},
                 {'id': 2, 'performance': 1},
                 {'id': 3, 'performance': 1},
                 {'id': 4, 'performance': 1}]
    campaign_sizes = [4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]

    resultsHEFT = pd.DataFrame(columns=['size', 'planner', 'plan', 'makespan', 'reactive', 'expected', 'mpn_snt', 'rect_snt', 'time'])
    resultsGA00 = pd.DataFrame(columns=['size', 'planner', 'plan', 'makespan', 'reactive', 'expected', 'mpn_snt', 'rect_snt', 'time'])
    resultsGA25 = pd.DataFrame(columns=['size', 'planner', 'plan', 'makespan', 'reactive', 'expected', 'mpn_snt', 'rect_snt', 'time'])
    resultsGA50 = pd.DataFrame(columns=['size', 'planner', 'plan', 'makespan', 'reactive', 'expected', 'mpn_snt', 'rect_snt', 'time'])
    resultsL2FF = pd.DataFrame(columns=['size', 'planner', 'plan', 'makespan', 'reactive', 'expected', 'mpn_snt', 'rect_snt', 'time'])
    resultsRAND = pd.DataFrame(columns=['size', 'planner', 'plan', 'makespan', 'reactive', 'expected', 'mpn_snt', 'rect_snt', 'time'])

    for cm_size in campaign_sizes:
        print('Current campaign size: %d' % cm_size)
        for _ in range(repetitions):
            campaign, num_oper = df_to_lists(size=cm_size)
            planner1 = HeftPlanner(campaign=campaign, resources=resources, num_oper=num_oper, sid='heft_exp')
            planner2 = GAPlanner(campaign=campaign, resources=resources, num_oper=num_oper, sid='ga50', random_init=0.5)
            planner3 = L2FFPlanner(campaign=campaign, resources=resources, num_oper=num_oper, sid='l2ff')
            planner4 = RandomPlanner(campaign=campaign, resources=resources, num_oper=num_oper, sid='random')
            planner5 = GAPlanner(campaign=campaign, resources=resources, num_oper=num_oper, sid='ga00', random_init=1.0)
            planner6 = GAPlanner(campaign=campaign, resources=resources, num_oper=num_oper, sid='ga25', random_init=0.75)
            
            tic = time()
            plan = planner1.plan()
            toc = time()
            makespan, reactive, expected = get_makespan(plan, 4, 0, dynamic_res=True)
            resultsHEFT.loc[len(resultsHEFT)] = [cm_size, 'HEFT', plan, makespan, reactive, expected, makespan - expected, reactive - expected, toc-tic]

            tic = time()
            plan = planner2.plan()
            toc = time()
            makespan, reactive, expected = get_makespan(plan, 4, 0, dynamic_res=True)
            resultsGA50.loc[len(resultsGA50)] = [cm_size, 'GA-50', plan, makespan, reactive, expected, makespan - expected, reactive - expected, toc-tic]

            tic = time()
            plan = planner3.plan()
            toc = time()
            makespan, reactive, expected = get_makespan(plan, 4, 0, dynamic_res=True)
            resultsL2FF.loc[len(resultsL2FF)] = [cm_size, 'L2FF', plan, makespan, reactive, expected, makespan - expected, reactive - expected, toc-tic]

            tic = time()
            plan = planner4.plan()
            toc = time()
            makespan, reactive, expected = get_makespan(plan, 4, 0, dynamic_res=True)
            resultsRAND.loc[len(resultsRAND)] = [cm_size, 'RANDOM', plan, makespan, reactive, expected, makespan - expected, reactive - expected, toc-tic]
                        
            tic = time()
            plan = planner5.plan()
            toc = time()
            makespan, reactive, expected = get_makespan(plan, 4, 0, dynamic_res=True)
            resultsGA00.loc[len(resultsGA00)] = [cm_size, 'GA', plan, makespan, reactive, expected, makespan - expected, reactive - expected, toc-tic]
            
            tic = time()
            plan = planner6.plan()
            toc = time()
            makespan, reactive, expected = get_makespan(plan, 4, 0, dynamic_res=True)
            resultsGA25.loc[len(resultsGA25)] = [cm_size, 'GA-25', plan, makespan, reactive, expected, makespan - expected, reactive - expected, toc-tic]

            del planner1, planner2, planner3, planner4, planner5, planner6

    resultsHEFT.to_csv('../Data/heft/StHomoCampaigns_4DynHomoResourcesHEFT_new.csv', index=False)
    resultsGA50.to_csv('../Data/ga/perc_050/StHomoCampaigns_4DynHomoResourcesGA50_new.csv', index=False)
    resultsGA25.to_csv('../Data/ga/perc_075/StHomoCampaigns_4DynHomoResourcesGA25_new.csv', index=False)
    resultsGA00.to_csv('../Data/ga/perc_100/StHomoCampaigns_4DynHomoResourcesGA00_new.csv', index=False)
    resultsL2FF.to_csv('../Data/l2ff/StHomoCampaigns_4DynHomoResourcesL2FF_new.csv', index=False)
    resultsRAND.to_csv('../Data/random/StHomoCampaigns_4DynHomoResourcesRAND_new.csv', index=False)
