# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 15:47:12 2021

@author: hoskim1
"""

import pandas as pd
import os
import xlrd

from answers import answers


def get_sheet_names(path : str) -> list:
        
    xls = xlrd.open_workbook(path, on_demand=True)
    participants = [sheet_name for sheet_name in xls.sheet_names() if sheet_name != 'Template']
    
    return participants


def add_name(data, name):
    
    data['Name'] = name
    
    return data


def get_participant_data(path, participant):
    
    prt_data = pd.read_excel(path, participant)
    
    prt_data = add_name(prt_data, participant)
    
    return prt_data


def get_all_participant_data(path, participants):
    
    base_data = {}
    
    for prt in participants:
        base_data[prt] = get_participant_data(path, prt)
    
    all_data = pd.concat(base_data.values())
    
    return all_data
   
    
def append_answers(all_data, answers):
    
    all_data = pd.merge(all_data, answers, how='left', on='Question')
    all_data['Correct'] = (all_data['Answer'] >= all_data['Lower Bound']) &\
                          (all_data['Answer'] <= all_data['Upper Bound'])
                          
    return all_data
    

def agg_values(data, agg_col, group_col, agg_func='sum'):
    """
    

    Parameters
    ----------
    data : pd.DataFrame
        Data to aggregate
    agg_col : str
        Column to apply agg_func to 
    group_col : str
        Column to group unique values off
    agg_func : str, optional
        Function to aggregate by. The default is 'sum'.

    Returns
    -------
    pd.DataFrame
        Aggregated data.

    """
    
    grouped_data = data.groupby(group_col)
    agged_data = grouped_data.agg({agg_col: agg_func})
    
    return agged_data
    
 #   return data.pivot_table(agg_col, group_col, aggfunc=agg_func).sort_values(agg_col, ascending=False)

def append_points(data, correct_point=1, bonus_point=3):
    
    correct = data[data['Correct'] == True]

    correct_mins = agg_values(correct, 'Range', 'Question', 'min')
    correct_mins.columns = ['min_range']
    
    data = pd.merge(data, correct_mins, how='left',
                    left_on='Question', right_index=True)
    
    data['Points'] = 0
    data['Points'] = data['Points'].where(data['Correct'] != True, 1)\
                                   .where(data['min_range'] != data['Range'], 3)\
                                   .where(data['Correct'] != False, 0)#leave existing value if condition passes

    

    # min_range = correct.loc[correct.groupby('Question').Range.idxmin()]
    # min_range['Min_Flag'] = 1
    
    # min_range = min_range[['Question', 'Name','Min_Flag']]
    
    # ########
    # data = pd.merge(data, min_range, how='left', on=['Question','Name'])
    
    # # 0 points by default. 
    # # 1(def) point if Correct
    # # 3(def) points if Min range
    # data['Points'] = 0
    # data['Points'] = data['Points'].where(data['Correct'] != True, 1)\
    #                                .where(data['Min_Flag'] != True, 3) #leave existing value if condition passes
        
    return data






def main(path):
    
    #all player names, based on sheet names
    participants = get_sheet_names(path)
    
    #read and combine all sheets
    all_data = get_all_participant_data(path, participants)
    
    #add answer info
    all_data = append_answers(all_data, answers)
    
    #find player with most correct answers
    total_correct = agg_values(all_data, 'Correct', 'Name')

    #add point values - more points for minimum range
    all_data = append_points(all_data)
    
    #find player with highest overall score
    total_score = agg_values(all_data, 'Points','Name')
    
    return total_correct, total_score

if __name__ == "__main__":
    
    path = "H:\\My Documents\\test_confidence.xlsx"

    tc, ts = main(path)
    
# path = "H:\\My Documents\\test_confidence.xlsx"

# confidence = xlrd.open_workbook(path, on_demand=True)
# participants = [sheet_name for sheet_name in confidence.sheet_names() if sheet_name != 'Template']
# participants

# answers = pd.DataFrame.from_dict({1:32,
#                                   2:42,
#                                   3:12,
#                                   4:434,
#                                   5:14,
#                                   6:1235,
#                                   7:12,
#                                   8:124,
#                                   9:69,
#                                   10:51}.items())

# answers.columns = ['Question','Answer']

# base_data = {}
# for prt in participants:
#     base_data[prt] = pd.read_excel(path, sheet_name = prt)
#     base_data[prt]['Name'] = prt
    
                           
# all_data = pd.concat(base_data.values())
# all_data = pd.merge(all_data, answers, how='left', on = 'Question')
# all_data['Correct'] = (all_data['Answer'] >= all_data['Lower Bound']) &\
#                       (all_data['Answer'] <= all_data['Upper Bound'])
                      

#get total number of correct answers                      
# total_correct = all_data.pivot_table('Correct', 'Name', aggfunc='sum').sort_values('Correct')
    

# correct = all_data[all_data['Correct'] == True]

# min_range = correct.loc[correct.groupby('Question').Range.idxmin()]
# min_range['Min_Flag'] = 1

# min_range = min_range[['Question', 'Name','Min_Flag']]

# ########
# all_data = pd.merge(all_data, min_range, how='left', on=['Question','Name'])

# all_data['Points'] = 0
# all_data['Points'] = all_data['Points'].where(all_data['Correct'] != True, 1)\
#                                         .where(all_data['Min_Flag'] != True, 3)

# total_score = all_data.pivot_table('Points','Name', aggfunc='sum').sort_values('Points')


