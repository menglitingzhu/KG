import math

import numpy as np
from py2neo import Record

from app import get_profile
from neo_db.config import graph, CA_LIST, similar_words
import codecs
import os
import json
import base64

def query(name):
    data = graph.run(
    # match(p{name: '朱文生'})-[r]->(n)return p.name, r.property1, n.name, p.label, n.label
    "match(p)-[r]->(n{name:'%s'}) return  p.name,r.property1,n.name,p.label,n.label\
        Union all\
    match(p{Name:'%s'}) -[r]->(n) return p.name, r.property1, n.name, p.label, n.label" % (name,name)
    )
    data = list(data)
    return get_json_data(data)
def get_json_data(data):
    json_data={'data':[],"links":[]}
    d=[]


    for i in data:
        # print(i["p.Name"], i["r.relation"], i["n.Name"], i["p.cate"], i["n.cate"])
        d.append(i['p.name']+"_"+i['p.label'])
        d.append(i['n.name']+"_"+i['n.label'])
        d=list(set(d))
    name_dict={}
    count=0
    for j in d:
        j_array=j.split("_")
    
        data_item={}
        name_dict[j_array[0]]=count
        count+=1
        data_item['name']=j_array[0]
        data_item['category']=CA_LIST[j_array[1]]
        json_data['data'].append(data_item)
    for i in data:
   
        link_item = {}
        
        link_item['source'] = name_dict[i['p.name']]
        
        link_item['target'] = name_dict[i['n.name']]
        link_item['value'] = i['r.property1']
        json_data['links'].append(link_item)

    return json_data
# f = codecs.open('./static/test_data.json','w','utf-8')
# f.write(json.dumps(json_data,  ensure_ascii=False))
def get_KGQA_answer(array):
    data_array=[]
    print(array)
    k = len(array)
    for i in range(5):
        if i==0:
            name=array[0]
        else:
            if i < k:
                name = array[i]
            # else:
            #     break
            # name=data_array[i]['p.name']
        data = graph.run(
            # "match(p{name:'%s'})-[r]->(n) return  p.name,n.name,r.property1,p.label,n.label" % (
            #     name)
        "match(p)-[r]->(n{name:'%s'}) return  p.name,r.property1,n.name,p.label,n.label\
                Union all\
            match(p{name:'%s'}) -[r]->(n) return p.name, r.property1, n.name, p.label, n.label" % (name, name)
        )
        # array.append(data[i].name)
        # data2 = data['p.name']
        data = list(data)
        data_array.extend(data)
        if data:
            for j in range(len(data)):
                array.append(data[j]['n.name'])
        # else:
        #     break
        k = len(array)
        print("==="*36)
    # with open("./spider/images/"+"%s.jpg" % (str(data_array[-1]['p.name'])), "rb") as image:
    #         base64_data = base64.b64encode(image.read())
    #         b=str(base64_data)

    return get_json_data(data_array)
    # return [get_json_data(data_array), get_profile(str(data_array[0]['p.name']))]
def get_answer_profile(name):
    with open("./spider/images/"+"%s.jpg" % (str(name)), "rb") as image:
        base64_data = base64.b64encode(image.read())
        b = str(base64_data)
    return [get_profile(str(name)), b.split("'")[1]]
        
def get_KGQA_answer2(array):
    data_array=[]
    print(array)
    k = len(array)
    for i in range(5):
        if i==0:
            name=array[0]
        else:
            if i < k:
                name = array[i]
            else:
                break
            # name=data_array[i]['p.name']
        data = graph.run(
             "match(p{name:'%s'})-[r]->(n) return  p.name,n.name,r.property1,p.label,n.label" % (
                 name)
        )
        # array.append(data[i].name)
        # data2 = data['p.name']
        data = list(data)
        data_array.extend(data)
        if data:
            for j in range(len(data)):
                array.append(data[j]['n.name'])
        else:
            break
        k = len(array)
        print("==="*36)
    # with open("./spider/images/"+"%s.jpg" % (str(data_array[-1]['p.name'])), "rb") as image:
    #         base64_data = base64.b64encode(image.read())
    #         b=str(base64_data)

    return get_json_data(data_array)

def Neo4j_Search_Entity(self, Str,SearchObj):  # Fuzzy Search,search entities, SearchObj could be "PubCompany" or"NonPubCompany" or "Person" or ""
    if len(SearchObj) == 0:
        cypher = "match (n) where n.CompanyName =~'.*" + Str + ".*' or n.Shortname =~'.*" + Str + \
            ".*' or n.Stock_Code =~'.*" + Str + ".*' or n.PersonName =~'.*" + Str + ".*' Return n"
    else:
        cypher = "match (n:" + SearchObj + ") where n.CompanyName =~'.*" + Str + ".*' or n.Shortname =~'.*" \
            + Str + ".*' or n.Stock_Code =~'.*" + Str + ".*' or n.PersonName =~'.*" + Str + ".*' Return n"

        with self._driver.session() as session:
            with session.begin_transaction() as tx:
                data = []
                for record in tx.run(cypher).records():
                    data.append(record)
    return data

def Neo4j_SearchByRe(self, ModelN, direction, *list):
        # args means a list of 5 elements which have been known for searching
        # direction = 0 or 1, 0 means forward relation, 1 means backward relation
        # ModelN from 0 to 2, represents which element of tenary relation is absence
        # for example: Neo4j_SearchByRe(2,1, [":Person{PersonName:'王石'}", ":Manage|:Holder"]) means search entities
        #  N which meet the relation (王石) manages N or has share of, refers to (:Person{PersonName:'王石'}) <-[:Manage|:Horlder]- (which entities)
    args = list[0]
    if len(args) != 2:
        print("the number of parameters is error\n")
        return None
    if ModelN > 2 or ModelN < 0:
        print("Wrong ModelN number\n")
        return None
    if direction > 1 or direction < 0:
        print("Wrong direction number\n")

    if ModelN == 0:
        if direction == 0:
             cypher = "match(result)-[" + args[0] + "]->(" + args[1] + ") return result"
        else:
            cypher = "match(result)<-[" + args[0] + "]-(" + args[1] + ") return result"
    elif ModelN == 1:
        if direction == 0:
            cypher = "match(" + args[0] + ")-[result]->(" + args[1] + ") return result"
        else:
            cypher = "match(" + args[0] + ")<-[result]-(" + args[1] + ") return result"
    else:
        if direction == 0:
            cypher = "match(" + args[0] + ")-[" + args[1] + "]->(result) return result"
        else:
            cypher = "match(" + args[0] + ")<-[" + args[1] + "]-(result) return result"
    with self._driver.session() as session:
        with session.begin_transaction() as tx:
            data = []
            for record in tx.run(cypher).records():
                # print(type(tx.run(cypher).records()))
                print(type(record[0]._properties))
                data.append(record)
    return data

def Neo4j_SearchByOneEntity(self, ModelN, direction, SearchObj):
        # Meaning of direction is same as that of Neo4j_SearchByRe
        # ModelN is 0 or 1, 0 refers to function will return set of entities, 1 refers set of relations
        # SearchObj is a string similar with *list of Neo4j_SearchByRe
        if ModelN == 0:
            if direction == 0:
                cypher = "MATCH (" + SearchObj + ")-->(result) return result"
            else:
                cypher = "MATCH (result)-->(" + SearchObj + ") return result"
        else:
            if direction == 0:
                cypher = "MATCH (" + SearchObj + ")-[r]->(result) return r"
            else:
                cypher = "MATCH (result)-[r]->(" + SearchObj + ") return r"
        with self._driver.session() as session:
            with session.begin_transaction() as tx:
                data = []
                for record in tx.run(cypher).records():
                    # print(type(tx.run(cypher).records()))
                    print(type(record[0]._properties))
                    data.append(record)
        return data

def SortByLD(self, str, args):  # designed for sorting entities
    if type(args[0]) != Record:
            print("Only could sort the class of neo4j.Records")
            return None
    LDtemp = []
    for record in args:
        Tmp = []
        for pros in record[0]._properties.keys():
            Tmp.append(self.auto_distance(str, record[0]._properties[pros]))
        LDtemp.append(sum(Tmp))
    NewRank = []
    RankScore = []
    for i in args:
        Site = LDtemp.index(max(LDtemp))
        RankScore.append(LDtemp[Site])
        LDtemp[Site] = -1
        NewRank.append(args[Site])
    return NewRank, RankScore

def auto_distance(Exa_str1, Exa_str2):  # LD
    global result
    n1 = len(Exa_str1)
    n2 = len(Exa_str2)
    Exa_M = np.zeros((n1 + 1, n2 + 1))
    for i in range(n1 + 1):
        Exa_M[i][0] = i
    for j in range(n2 + 1):
            Exa_M[0][j] = j
    for i in range(1, n1 + 1):
        for j in range(1, n2 + 1):
            Exa_M[i][j] = min(Exa_M[i - 1][j - 1] + (1 - (Exa_str1[i - 1] == Exa_str2[j - 1])), Exa_M[i][j - 1] + 1,
                                Exa_M[i - 1][j] + 1)
            result = 1 - 1 / (1 + math.log(Exa_M[i][j] + 1, math.e))
    return result
