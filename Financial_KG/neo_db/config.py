from py2neo import Graph
graph = Graph(
    "http://localhost:7474",
    username="neo4j",
    password="192425sxy"
)
CA_LIST = {"人":0,"行业":1,"概念":2,"股票":3}
similar_words = {
    "工作": "work",
    "职位": "work",
    "上班": "work",
    "属于": "belong",
    "属": "belong",
    "算": "belong",
}
