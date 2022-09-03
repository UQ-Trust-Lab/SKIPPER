import os

from bs4 import BeautifulSoup

from find_subtitle import find_title_Label
from get_text import write_text
from types_pp_processing import caculateSim
from children_pp_processing import process_specialGroup
from region_pp_processing import get_alifornia
from retention_pp_processing import retention_process
from clean_txt import cleaning_txt
if __name__ == '__main__':
    INPUT = "../../example/pp_example/"
    for file in os.listdir(INPUT):
        pathName = os.path.basename(file)
        if pathName == ".DS_Store":
            continue
        path = INPUT+pathName
        label = find_title_Label(path)
        print("The current file is:" + pathName)

        soup = BeautifulSoup(open(path), features="html.parser")
        title_list = soup.find_all(label)
        cleaning_txt()
        write_text(title_list)
        # types
        all_types = caculateSim("./txt/data_types.txt")
        # print("The matrix of the data type is:")
        print(" D.TYPES :" + str(all_types))

        #children
        age , rule, childUse, specialGroup = process_specialGroup("./txt/children.txt")
        # print("children age is :")
        print("D.CHILDREN.age : " + str(age))
        if childUse == 1:
            print(" the skill’s privacy policy states that it does not collect any information from children")
            print("D.CHILDREN.[CTypes] = [ ]")
        else:
            print("D.CHILDREN.[CTypes] :" + str(all_types))
        #region
        specialArea,california = get_alifornia("./txt/region.txt")
        if california == 1:
            print("D.REGIONS.region :California")
            print("D.REGIONS.delete : Yes")
        else:
            print("D.REGIONS.region :No mention")
            print("D.REGIONS.delete : No")

        #retention
        time, text = retention_process("./txt/data_retention.txt")
        print("D.RETENTION.period :"+ time)
        cleaning_txt()
        print("-------------------------------------------------------")

        # region
