import re

import bs4

from paragraph_bayesian import clf,tf
from bs4 import BeautifulSoup

mark_txt = {'0':"./txt/data_types.txt",'1':"./txt/data_types.txt",'2':"./txt/personal_information_type.txt",
            '3':"./txt/share_information.txt",'4':"./txt/protect_information.txt",
            '5':"./txt/advertising.txt",'6':"./txt/user_right.txt",'7':"./txt/children.txt",
            '8':"./txt/region.txt",'9':"./txt/update.txt",'10':"./txt/way_to_collect.txt",
            '11':"./txt/provider.txt",'12':"./txt/data_retention.txt",'13':"./txt/data_types.txt",'14':"./txt/thrid_party.txt",'15':"./txt/data_types.txt"}
def write_text(title_list):
    type = 0
    security = 0
    right = 0
    specialGroup = 0
    specialArea = 0
    update = 0
    retention = 0
    useData = 0
    clean_title_list = []
    for title in title_list:
        if title.text != "•":
            clean_title_list.append(title)
    lastMark = ""
    for title in clean_title_list:
        title_Str = re.sub(r'\s+', ' ',str(title))
        title_Str = re.sub(r'<[^<]+?>', '', title_Str).replace('\n','').strip()
        if title is None:
            continue
        try:
            mark = clf.predict(tf.transform([title_Str]))
        except Exception as e:
            continue
        # print(mark)
        if mark == "1":
            type = 1
        if mark == "4":
            security = 1
        if mark == "6":
            right = 1
        if mark == "13":
            useData = 1
        if mark == "8":
            specialArea = 1
        if mark == "9":
            update = 1
        if mark == "12":
            retention = 1

        if mark == "7":
            specialGroup = 1
        if mark == "0":
            if lastMark != "":
                mark = lastMark
        lastMark = mark
        for sibling in title.next_elements:
            try:
                if clean_title_list[clean_title_list.index(title) + 1] == sibling:
                        break
            except Exception:
                continue
            if isinstance(sibling, bs4.element.Tag):
                continue
            if str(sibling) == '\n':
                continue
            if sibling == title.string:
                continue

            if clean_title_list.index(title) == len(clean_title_list) - 1:
                with open(mark_txt.get(mark[0]),"a") as f:
                    currentSibing = str(sibling)
                    if currentSibing[-1].isalpha() or currentSibing[-1] == ")":
                        currentSibing = currentSibing + "."
                    f.write(currentSibing)
                    f.close()
            else:
                with open(mark_txt.get(mark[0]),"a") as g:
                    currentSibing = str(sibling)
                    if currentSibing[-1].isalpha() or currentSibing[-1] == ")":
                        currentSibing = currentSibing + "."
                    g.write(currentSibing)
                    g.write("\n")
                    g.close()
    return type,security,right,specialArea,specialGroup,update,retention,useData
