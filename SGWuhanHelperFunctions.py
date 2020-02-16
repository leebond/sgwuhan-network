# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 14:04:58 2020

@author: david
"""
import networkx
import networkx as nx
import matplotlib.pyplot as plt


def add_node_to_graph(g, case, more_nodes_to_ignore):
    '''
    Graph.add_node(node_for_adding, **attr)

    Add a single node node_for_adding and update node attributes.

    Graph.add_nodes_from(nodes_for_adding, **attr)

    Add multiple nodes.
    '''
    nodes_to_ignore = ['', 'no info by moh']
    
    case = [c.strip() for c in case.split(',')]
    case = [c for c in case if c.lower() not in nodes_to_ignore]
    case = [c for c in case if not any(w in c.lower() for w in more_nodes_to_ignore)]
    
    if len(case) != 0:
        g.add_node(case[0])
#             else:
#                 for node in case:
#                     g.add_node(node)

    return g

def add_edge_to_graph(g, case, relatedCaseNo, more_nodes_to_ignore):
    '''
    Graph.add_edge(u_of_edge, v_of_edge, **attr)

    Add an edge between u and v.

    Graph.add_edges_from(ebunch_to_add, **attr)

    Add all the edges in ebunch_to_add.
    '''
    nodes_to_ignore = ['', 'no info by moh'] + more_nodes_to_ignore

    case = [c.strip() for c in case.split(',')]
    case = [c for c in case if c.lower() not in nodes_to_ignore]
    case = [c for c in case if not any(w in c.lower() for w in more_nodes_to_ignore)]

    relatedCaseNo = [rc.strip() for rc in relatedCaseNo.split(',')]
    relatedCaseNo = [rc for rc in relatedCaseNo if rc.lower() not in nodes_to_ignore]
    relatedCaseNo = [rc for rc in relatedCaseNo if not any(w in rc.lower() for w in more_nodes_to_ignore)]

    if len(case) != 0 and len(relatedCaseNo) != 0:
        g.add_edge(case[0], relatedCaseNo[0])
#         else:
#             for rc in relatedCaseNo:
#                 g.add_edge(case[0], rc)
    return g

def loadGraph(g:networkx.classes.graph.Graph, data_dict, more_nodes_to_ignore):
    for d in data_dict['data']:
        case = d['caseNo']
        relatedCaseNo = d['relatedCaseNo']
        from_ = d['from']
        stayed = d['stayed']
        visited = d['visited']
        links = d['relatedArrayNo']

        g = add_node_to_graph(g, case, more_nodes_to_ignore)
        g = add_node_to_graph(g, relatedCaseNo, more_nodes_to_ignore)
        
        if 'china' in from_.lower() or 'wuhan' in from_.lower(): ## rename nodes that come from 'china' or 'wuhan' as 'imported case'
            from_ = 'imported case'
#         if 'singapore' not in from_.lower(): ## not adding nodes with 'singapore' in the text 
        g = add_node_to_graph(g, from_, more_nodes_to_ignore)
        g = add_node_to_graph(g, stayed, more_nodes_to_ignore)
#         if 'hospital' not in visited.lower() and 'gp clinic' not in visited.lower(): ## not adding nodes with 'hospital' and 'gp clinic' in the text 
        g = add_node_to_graph(g, visited, more_nodes_to_ignore)

        g = add_edge_to_graph(g, case, relatedCaseNo, more_nodes_to_ignore)
#         if 'singapore' not in from_.lower(): ## not adding nodes with 'singapore' in the text 
        g = add_edge_to_graph(g, case, from_, more_nodes_to_ignore)
        g = add_edge_to_graph(g, case, stayed, more_nodes_to_ignore)
#         if 'hospital' not in visited.lower() and 'gp clinic' not in visited.lower():  ## not adding edges with 'hospital' and 'gp clinic' in the text
        g = add_edge_to_graph(g, case, visited, more_nodes_to_ignore)
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