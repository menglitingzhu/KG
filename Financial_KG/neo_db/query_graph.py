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


