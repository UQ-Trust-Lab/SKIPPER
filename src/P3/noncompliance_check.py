# -*- coding: utf-8 -*-

import behavior_log_process as be
import pandas
import utilities
import os

def check_regions(filePath): # return True if violated
    dict = be.derive_behavior_profiles(filePath)
    for file in os.listdir(filePath):
        if file.endswith('.xlsx'):
            # print(file)
            if file in dict: # have data type collection behavior
                df = pandas.read_excel(filePath + file, engine='openpyxl', usecols=[0], names=['colA'])
                values = df['colA'].values.tolist()
                for i in range(0, len(values) - 1):
                    if ('erase my information' in values[i]) or ('delete my information' in values[i]) or \
                            ('delete personal information' in values[i]) or ('erase personal information' in values[i]):
                        # check confirmative response
                        if utilities.check_confirmative(values[i+1]):
                            print('the result of checking V3(REGIONS) on file ' + str(file) + ' is: FALSE')
                            break
                        else:
                            print('the result of checking V3(REGIONS) on file ' + str(file) + ' is: TRUE')
                            break
            else: # no data type collection behavior
                print('the result of checking V3(REGIONS) on file ' + str(file) + ' is: FALSE')
                continue

def check_children(filePath): # return True if violated
    dict = be.derive_behavior_profiles(filePath)
    for file in os.listdir(filePath):
        if file.endswith('.xlsx'):
            if file in dict:
                df = pandas.read_excel(filePath + file, engine='openpyxl', usecols=[0], names=['colA'])
                values = df['colA'].values.tolist()
                for i in range(0, len(values) - 1):
                    if be.test_case_repeat_yes(values[i]):
                        if be.Alexa_response_yes(values[i+1]): # if skill stop after test case return false
                            print('the result of checking V2(CHILDREN) on file ' + str(file) + ' is: FALSE')
                            break
                        else:
                            print('the result of checking V2(CHILDREN) on file ' + str(file) + ' is: TRUE')
                            break
            else:  # no data type collection behavior
                print('the result of checking V2(CHILDREN) on file ' + str(file) + ' is: FALSE')
                continue

def check_retention(filePath): # return True if violated
    for file in os.listdir(filePath):
        if file.endswith('.xlsx'):
            df = pandas.read_excel(filePath + file, engine='openpyxl', usecols=[0], names=['colA'])
            values = df['colA'].values.tolist()
            bool = False
            for i in range(0, len(values) - 1):
                if ('back' in values[i]) or ('continue' in values[i]) or ('again' in values[i]):
                    bool = True
                    list = check_test_case_repeat(values[i])
                    if len(list) != 0:
                        print('the result of checking V4(RETENTION) on file ' + str(file) + ' is: TRUE')
                        break
                    else:
                        if ('days until your' in values[i]) and ('birthday' in values[i]):
                            print('the result of checking V4(RETENTION) on file ' + str(file) + ' is: TRUE')
                            break
                        else:
                            print('the result of checking V4(RETENTION) on file ' + str(file) + ' is: FALSE')
                            break
            if not bool:
                print('the result of checking V4(RETENTION) on file ' + str(file) + ' is: FALSE')
                continue

def check_types(behavior_dict, filePath): # return True if violated
    b_is_subset = 0 # B is the subset of D when providing P
    b_minus_d_not_empty = 0 # the result of B - D is not empty set when providing PP
    b_is_empty = 0 # B is empty when not providing PP
    b_is_not_empty = 0 # B is not empty when not providing PP

    df_pp = pandas.read_excel(filePath, engine='openpyxl')
    pp_dict = dict(zip(df_pp['files'], df_pp['array']))
    pp_dict_clean = {}
    for index in pp_dict:
        pp_list = string_to_list(pp_dict.get(index))
        pp_list_clean = []
        pp_list_clean.append(pp_list[8]) # location
        pp_list_clean.append(pp_list[21]) # post address
        pp_list_clean.append(pp_list[0]) # name
        pp_list_clean.append(pp_list[2]) # phone no
        pp_list_clean.append(pp_list[1]) # email
        pp_list_clean.append(pp_list[4]) # birthday
        pp_list_clean.append(pp_list[5]) # age
        pp_list_clean.append(pp_list[22]) # postcode
        pp_dict_clean.update({index:pp_list_clean})

    print('behavior data array: ')
    print(behavior_dict)
    print('declared(pp) data array: ')
    print(pp_dict_clean)
    for index in behavior_dict:
        if index not in pp_dict_clean: # not providing PP
            if check_empty(behavior_dict.get(index)): # and B is empty
                b_is_empty += 1
                print('the result of checking V1(TYPES) on file ' + str(index) + ' is: FALSE')
            else: # B is not empty
                b_is_not_empty += 1
                print('the result of checking V1(TYPES) on file ' + str(index) + ' is: TRUE')
        else: # providing PP
            if check_empty(behavior_dict.get(index)): # B is empty, and is the subset of D
                b_is_subset += 1
                print('the result of checking V1(TYPES) on file ' + str(index) + ' is: FALSE')
            else:
                behavior_list = behavior_dict.get(index)
                pp_list = pp_dict_clean.get(index)

                if behavior_list[0] == 1:
                    if pp_list[0] == 0 and pp_list[1] == 0: # check location
                        b_minus_d_not_empty += 1 # break
                        print('the result of checking V1(TYPES) on file ' + str(index) + ' is: TRUE')
                        continue
                if behavior_list[1] == 1:
                    if pp_list[2] == 0:
                        b_minus_d_not_empty += 1  # break
                        print('the result of checking V1(TYPES) on file ' + str(index) + ' is: TRUE')
                        continue
                if behavior_list[2] == 1:
                    if pp_list[3] == 0:
                        b_minus_d_not_empty += 1  # break
                        print('the result of checking V1(TYPES) on file ' + str(index) + ' is: TRUE')
                        continue
                if behavior_list[3] == 1:
                    if pp_list[4] == 0:
                        b_minus_d_not_empty += 1  # break
                        print('the result of checking V1(TYPES) on file ' + str(index) + ' is: TRUE')
                        continue
                if behavior_list[4] == 1:
                    if pp_list[5] == 0:
                        b_minus_d_not_empty += 1  # break
                        print('the result of checking V1(TYPES) on file ' + str(index) + ' is: TRUE')
                        continue
                if behavior_list[5] == 1:
                    if pp_list[6] == 0:
                        b_minus_d_not_empty += 1  # break
                        print('the result of checking V1(TYPES) on file ' + str(index) + ' is: TRUE')
                        continue
                if behavior_list[6] == 1:
                    if pp_list[7] == 0:
                        b_minus_d_not_empty += 1  # break
                        print('the result of checking V1(TYPES) on file ' + str(index) + ' is: TRUE')
                        continue
                b_is_subset +=1
                print('the result of checking V1(TYPES) on file ' + str(index) + ' is: FALSE')

    print('B is the subset of D when providing PP: ' + str(b_is_subset))
    print('the result of B - D is not empty set when providing PP: ' + str(b_minus_d_not_empty))
    print('B is empty when not providing PP: ' + str(b_is_empty))
    print('B is not empty when not providing PP: ' + str(b_is_not_empty))

def string_to_list(str):
    list = str[1:-1].split(',')
    clean_list = []
    for s in list:
        clean_list.append(int(s.strip()))
    return clean_list

def check_empty(list):
    for i in list:
        if i == 1:
            return False
    return True

def check_test_case_repeat(str):
    list = []
    str = str.lower()
    if 'brisbane' in str:
        list.append('location')
    if ('4101' in str) or ('forty one oh one' in str) or ('04101' in str):
        list.append('postcode')
    if ('twenty fifth of december' in str) or ('25th of december' in str):
        list.append('birthday')
    if ('xxx at gmail dot com' in str) or ('xxx@gmail.com' in str):
        list.append('email')
    if ('oh four five oh four one nine nine nine nine' in str) or ('0450419999' in str) or ('450419999' in str):
        list.append('phone number')
    if ('james smith' in str) or ('james' in str) or ('smith' in str):
        list.append('name')
    return(list)









