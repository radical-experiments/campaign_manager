from radical.cm.planner import L2FFPlanner, HeftPlanner, GAPlanner, RandomPlanner
from random import gauss, uniform, randint
import pandas as pd
import numpy as np
import sys
from time import time


def df_to_lists(cmp, size):

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

def resdf_to_dict(res_df, size):

    tmp_resources = list()
    for i in range(size):
        point = res_df.loc[randint(0,3)]
        tmp_res = {'id': i + 1,
                   'performance': point['PFlops Mean']}
        tmp_resources.append(tmp_res)
    return tmp_resources

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
    dyn_resources = np.load('../Data/homogeneous_resources_dyn.npy')
    total_resources = pd.read_csv('../Data/heterogeneous_resources.csv')
    total_cmp = pd.read_csv('../Data/heterogeneous_campaign.csv')
    num_resources = [4, 8, 16, 32, 64, 128, 256]
    resultsHEFT = pd.DataFrame(columns=['size', 'planner', 'plan', 'makespan', 'reactive', 'expected', 'mpn_snt', 'rect_snt', 'time'])
    resultsGA50 = pd.DataFrame(columns=['size', 'planner', 'plan', 'makespan', 'reactive', 'expected', 'mpn_snt', 'rect_snt', 'time'])
    resultsL2FF = pd.DataFrame(columns=['size', 'planner', 'plan', 'makespan', 'reactive', 'expected', 'mpn_snt', 'rect_snt', 'time'])
    resultsRAND = pd.DataFrame(columns=['size', 'planner', 'plan', 'makespan', 'reactive', 'expected', 'mpn_snt', 'rect_snt', 'time'])
    campaign, num_oper = df_to_lists(cmp=total_cmp, size=1024)
    resources = None
    for res_num in num_resources:
        print('Number of resources: %d' % res_num)
        for _ in range(repetitions):
            resources = resdf_to_dict(res_df=total_resources, size=res_num)
            planner1 = HeftPlanner(campaign=campaign, resources=resources, num_oper=num_oper, sid='heft_exp')
            planner2 = GAPlanner(campaign=campaign, resources=resources, num_oper=num_oper, sid='ga50', random_init=0.5)
            planner3 = L2FFPlanner(campaign=campaign, resources=resources, num_oper=num_oper, sid='l2ff')
            planner4 = RandomPlanner(campaign=campaign, resources=resources, num_oper=num_oper, sid='random')

            tic = time()
            plan = planner1.plan()
            toc = time()
            makespan, reactive, expected = get_makespan(plan, res_num, workflow_inaccur=workflow_inaccur)
            resultsHEFT.loc[len(resultsHEFT)] = [res_num, 'HEFT', plan, makespan, reactive, expected, makespan - expected, reactive - expected, toc-tic]

            tic = time()
            plan = planner2.plan()
            toc = time()
            makespan, reactive, expected = get_makespan(plan, res_num, workflow_inaccur=workflow_inaccur)
            resultsGA50.loc[len(resultsGA50)] = [res_num, 'GA-50', plan, makespan, reactive, expected, makespan - expected, reactive - expected, toc-tic]

            tic = time()
            plan = planner3.plan()
            toc = time()
            makespan, reactive, expected = get_makespan(plan, res_num, workflow_inaccur=workflow_inaccur)
            resultsL2FF.loc[len(resultsL2FF)] = [res_num, 'L2FF', plan, makespan, reactive, expected, makespan - expected, reactive - expected, toc-tic]

            tic = time()
            plan = planner4.plan()
            toc = time()
            makespan, reactive, expected = get_makespan(plan, res_num, workflow_inaccur=workflow_inaccur)
            resultsRAND.loc[len(resultsRAND)] = [res_num, 'RANDOM', plan, makespan, reactive, expected, makespan - expected, reactive - expected, toc-tic]

            del planner1, planner2, planner3, planner4

    resultsHEFT.to_csv('../Data/heft/StHeteroResources_StHeteroCampaignsHEFT_inaccr%d_new.csv' % sys.argv[2], index=False)
    resultsGA50.to_csv('../Data/ga/perc_050/StHeteroResources_StHeteroCampaignsGA50_inaccr%d_new.csv' % sys.argv[2], index=False)
    resultsL2FF.to_csv('../Data/l2ff/StHeteroResources_StHeteroCampaignsL2FF_inaccr%d_new.csv' % sys.argv[2], index=False)
    resultsRAND.to_csv('../Data/random/StHeteroResources_StHeteroCampaignsRAND_inaccr%d_new.csv' % sys.argv[2], index=False)
