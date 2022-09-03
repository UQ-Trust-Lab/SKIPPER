# -*- coding: utf-8 -*-

import pandas
import utilities
import os
import argparse
import noncompliance_check as vc
import json

def Alexa_response_yes(str):
    string = str.lower()
    with open('Alexa_response_pattern.txt') as f:
        # lines = f.readlines()
        lines = [line.rstrip() for line in f]
    f.close()
    for l in range(len(lines)):
        if lines[l] in string:
            return True
        if l == len(lines) - 1:
            return False

def test_case_yes(str):
    string = str.lower()
    with open('test_cases.txt') as f:
        # lines = f.readlines()
        lines = [line.rstrip() for line in f]
    f.close()
    for l in range(len(lines)):
        if lines[l] in string:
            return True
        if l == len(lines) - 1:
            return False

def test_case_repeat_yes(str):
    return test_case_yes(str)

def data_type_pattern_query_list(str):
    string = str.lower()
    list = []
    with open('location_keywords.txt') as f:
        locationKey = f.readlines()
        for loc in locationKey:
            if loc.rstrip() in string:
                list.append('location')

    with open('phoneno_keywords.txt') as f:
        phoneKey = f.readlines()
        for phone in phoneKey:
            if phone.rstrip() in string:
                list.append('phone number')

    with open('birthday_keywords.txt') as f:
        birthKey = f.readlines()
        for birth in birthKey:
            if birth.rstrip() in string:
                list.append('birthday')

    with open('email_keywords.txt') as f:
        emailKey = f.readlines()
        for email in emailKey:
            if email.rstrip() in string:
                list.append('email')

    with open('postcode_keywords.txt') as f:
        postcodeKey = f.readlines()
        for postcode in postcodeKey:
            if postcode.rstrip() in string:
                list.append('postcode')

    with open('name_keywords.txt') as f:
        nameKey = f.readlines()
        for name in nameKey:
            if name.rstrip() in string:
                list.append('name')

    with open('age_keywords.txt') as f:
        ageKey = f.readlines()
        for age in ageKey:
            if age.rstrip() in string:
                list.append('age')

    if len(list) != 0:
        return list

def data_type_pattern_answer_list(str):
    str = str.lower()
    list = data_type_pattern_query_list(str)
    if list is None:
        list = []

    # check keyword repeated in query
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

    if len(list) != 0:
        return list

def derive_behavior_profiles(file_dir):
    for root, dirs, files in os.walk(file_dir):
        count = 1
        files_dict= {}
        for file in files:
            if file.endswith(".xlsx"):  # check is xlsx file
                print('processing file: ' + str(file))
                df = pandas.read_excel(file_dir+file, engine='openpyxl',usecols=[0], names=['colA'])
                values = df['colA'].values.tolist()
                flag = 0
                dt_list = [] #data-type list
                for i in range(0, len(values)-1):
                    if type(values[i+1]) != type('str') or type(values[i]) != type('str'):
                        continue
                    if ('found a few' in values[i+1]) or ('having trouble accessing' in values[i+1]) or ('not available'in values[i+1]) \
                            or ('some technical difficulties' in values[i+1]) or ('a few skills' in values[i+1]) \
                            or ('have a few' in values[i+1]) or ('I don\'t know' in values[i+1]) \
                            or ('<Short audio>' in values[i+1]): # break here if not able to correctly open skills at the first time
                        break

                # check query
                    if 'alexa open' in values[i]:
                        if not (Alexa_response_yes(values[i+1]) or test_case_repeat_yes(values[i+1])):
                            dt = data_type_pattern_query_list(values[i + 1])
                            if file not in files_dict and dt is not None:
                                flag +=1
                                typo = 'query : ' + str(dt) +' : ' + values[i+1]
                                if 'location' in dt:
                                    bool = utilities.checkLocation(values[i+1])
                                    if not bool:
                                        continue
                                elif 'email' in dt:
                                    bool = utilities.checkEmail(values[i+1])
                                    if not bool:
                                        continue
                                elif 'phone number' in dt:
                                    bool = utilities.checkNumber(values[i+1])
                                    if not bool:
                                        continue
                                dt_list.append(typo)

                # check answer
                    if test_case_yes(values[i]):
                        if not (Alexa_response_yes(values[i+1]) or test_case_repeat_yes(values[i+1])):
                            dt = data_type_pattern_answer_list(values[i + 1])
                            if True:
                                if file not in files_dict and dt is not None:
                                    flag+=1
                                    typo = 'answer : '+ str(dt) +' : ' + values[i+1]
                                    if not utilities.check_an_mood(values[i+1]):
                                        continue
                                    dt_list.append(typo)

                if flag > 1 and len(dt_list) != 0:
                    files_dict.update({file: dt_list})
                count += 1

        count1 = 0
        print('\nderived behavior profiles: ')
        for k in files_dict:
            print(k+' : '+str(files_dict.get(k)))
            print('\n')
            count1 += 1
        print("The number of derived behavior profiles is: " + str(len(files_dict)))
        return files_dict


def getArgsCategory():
    parser = argparse.ArgumentParser(description='enter the CATEGORY of violation cases you want to check')
    parser.add_argument('--t', type=str, help='check violations in TYPE category (V1)')
    parser.add_argument('--c', type=str, help='check violations in CHILDREN category (V2)')
    parser.add_argument('--regions', type=str, help='check violations in REGIONS category (V3)')
    parser.add_argument('--retention', type=str, help='check violations in retention category (V4)')
    args = parser.parse_args()
    if args.t is not None:
        return 'TYPES'
    elif args.c is not None:
        return 'CHILDREN'
    elif args.regions is not None:
        return 'REGIONS'
    elif args.retention is not None:
        return 'RETENTION'


if __name__ == '__main__':

    ViolationCheckCategory = getArgsCategory()

    if ViolationCheckCategory == 'TYPES':
        logFileDir = '../../example/TYPES_example/behavior_logs/'
        ppDir = '../../example/TYPES_example/pp_process_results/pp_process_TYPE.xlsx'
        # logFileDir = '../../benchmark/benchmark_log_type/behavior_logs/'
        # ppDir = '../../benchmark/benchmark_log_type/pp_processing_results/benchmark_type_pp.xlsx'


        data_log = derive_behavior_profiles(logFileDir)
        # Write behavior profiles into data array format
        behavior_dict = {}
        for log in data_log:
            result = [0, 0, 0, 0, 0, 0, 0]
            connect = data_log.get(log)
            skill = log.split('_')[0]
            if 'location' in json.dumps(connect):
                result[0] = 1
            if 'name' in json.dumps(connect):
                result[1] = 1
            if 'phone number' in json.dumps(connect):
                result[2] = 1
            if 'email' in json.dumps(connect):
                result[3] = 1
            if 'birthday' in json.dumps(connect):
                result[4] = 1
            if 'age' in json.dumps(connect):
                result[5] = 1
            if 'postcode' in json.dumps(connect):
                result[6] = 1
            behavior_dict.update({int(skill):result})
        for file in os.listdir(logFileDir):
            if file.endswith('.xlsx'):
                index = file.split('_')[0]
                if int(index) not in behavior_dict:
                    behavior_dict.update({int(index): [0, 0, 0, 0, 0, 0, 0]})
        vc.check_types(behavior_dict, ppDir)

    elif ViolationCheckCategory == 'CHILDREN':
        file_dir = '../../example/CHILDREN_example/behavior_logs/'
        # file_dir = '../../benchmark/benchmark_log_child/'
        vc.check_children(file_dir)

    elif ViolationCheckCategory == 'REGIONS':
        file_dir = '../../example/REGIONS_example/behavior_logs/'
        # file_dir = '../../benchmark/benchmark_log_region/'
        vc.check_regions(file_dir)

    elif ViolationCheckCategory == 'RETENTION':
        file_dir = '../../example/RETENTION_example/behavior_logs/'
        # file_dir = '../../benchmark/benchmark_log_retention/'
        vc.check_retention(file_dir)







