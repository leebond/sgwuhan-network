# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 14:04:58 2020

@author: david
"""
import networkx
import networkx as nx
import matplotlib.pyplot as plt

def add_node_to_graph(g, case):
    '''
    Graph.add_node(node_for_adding, **attr)

    Add a single node node_for_adding and update node attributes.

    Graph.add_nodes_from(nodes_for_adding, **attr)

    Add multiple nodes.
    '''
    case = [c.strip() for c in case.split(',')]
    
    if case != [] and '' not in case and 'No info by MOH' not in case:
        if len(case) == 1:
            g.add_node(case[0])
        else:
            for node in case:
                g.add_node(node)

    return g

def add_edge_to_graph(g, case, relatedCaseNo):
    '''
    Graph.add_edge(u_of_edge, v_of_edge, **attr)

    Add an edge between u and v.

    Graph.add_edges_from(ebunch_to_add, **attr)

    Add all the edges in ebunch_to_add.
    '''
    case = [c.strip() for c in case.split(',')]
    relatedCaseNo = [rc.strip() for rc in relatedCaseNo.split(',')]

    if case != [] and '' not in case and 'No info by MOH' not in case and \
    relatedCaseNo != [] and '' not in relatedCaseNo and 'No info by MOH' not in relatedCaseNo:
        if len(relatedCaseNo) == 1:
            g.add_edge(case[0], relatedCaseNo[0])
        else:
            for rc in relatedCaseNo:
                g.add_edge(case[0], rc)
    return g

def loadGraph(g:networkx.classes.graph.Graph, data_dict):
    for d in data_dict['data']:
        case = d['caseNo']
        relatedCaseNo = d['relatedCaseNo']
        stayed = d['stayed']
        visited = d['visited']
        links = d['relatedArrayNo']

        g = add_node_to_graph(g, case)
        g = add_node_to_graph(g, relatedCaseNo)
        g = add_node_to_graph(g, stayed)
        if 'hospital' not in visited.lower():
            g = add_node_to_graph(g, visited)

        g = add_edge_to_graph(g, case, relatedCaseNo)
        g = add_edge_to_graph(g, case, stayed)
        if 'hospital' not in visited.lower():
            g = add_edge_to_graph(g, case, visited)
    return g

def getNodeCentrality(g, func):
    myDict = func(g)
    myDict_sort = sorted(myDict, key=myDict.get, reverse=True)
    return myDict_sort

def showGraph(g):
    plt.figure(figsize=(16,12))
    nx.draw(g, with_labels=True, node_size=200, style = 'dotted', font_color = 'Black'\
            , node_color = '#ffb64f')
    plt.show()

def showSubGraph(g, metric, size):
    plt.figure(figsize=(16,12))
    edgelist = [e for e in list(g.edges()) if e[0] in  metric[:size] or e[1] in  metric[:size]]
    nx.draw(g, with_labels=True, node_size=200, style = 'dotted', font_color = 'Black'\
            , node_color = '#ffb64f', nodelist = metric[:size], edgelist = edgelist\
            , labels = dict(list(zip(metric[:size],metric[:size]))) )
    plt.show()