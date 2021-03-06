from radical.cm.planner import HeftPlanner
import pandas as pd
import sys
from time import time
from random import gauss

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
                       #'performance': 1.0}
                       'performance': point['PFlops Mean']}
                       #'performance': gauss(point['PFlops Mean'], point['Pflops STD'])}
            tmp_resources.append(tmp_res)
        return prev_set + tmp_resources

def get_makespan(curr_plan):

    checkpoints = [0]

    for work in curr_plan:
        if work[2] not in checkpoints:
            checkpoints.append(work[2])
        if work[3] not in checkpoints:
            checkpoints.append(work[3])

    checkpoints.sort()
    return checkpoints[-1]


if __name__ == "__main__":

    repetitions = int(sys.argv[1])
    num_resources = [4, 8, 16, 32, 64, 128]
    total_resources = pd.read_csv('../../Data/heterogeneous_resources.csv')
    total_cmp = pd.read_csv('../../Data/heterogeneous_campaign.csv')
    campaign, num_oper = df_to_lists(cmp=total_cmp, size=1024)
    results = pd.DataFrame(columns=['size','planner','plan','makespan', 'time'])
    resources = None
    for res_num in num_resources:
        print('Number of resources: %d' % res_num)
        resources = resdf_to_dict(res_df=total_resources, size=res_num, prev_set=resources)
        for _ in range(repetitions):
            planner = HeftPlanner(campaign=campaign, resources=resources, num_oper=num_oper, sid='heft_exp')
            tic = time()
            plan = planner.plan()
            toc = time()
            makespan = get_makespan(plan)
            results.loc[len(results)]= [res_num, 'HEFT', plan, makespan, toc - tic]
            del planner

    results.to_csv('../../Data/heft/SpHeteroResources_StHeteroCampaignsHEFT.csv', index=False)
