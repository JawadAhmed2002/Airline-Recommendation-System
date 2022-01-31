import heapq
import math

# def balti_Dijkstra(graph,root):
    # bucket=[]
    # Q = []
    # parent= {}
    # BFSTree = {} # to keep track of levels
    # BFSTree[root]= 0
    # parent[root]= ''
    # bucket.append(root)
    # Q.extend(graph[root])

    # for v in graph[root]:
    #     BFSTree[v]= BFSTree[root] + 1 
    #     parent[v] = root
    
    # while len(Q) != 0:
    #     print('Q:', Q, 'B:', bucket)
    #     adjVertex=Q.pop(0) 
    #     if adjVertex not in bucket:
    #         bucket.append(adjVertex)
    #         Q.extend(graph[adjVertex])

    #         for v in graph[adjVertex]:
    #             if v not in BFSTree.keys():
    #                 BFSTree[v]= BFSTree[adjVertex] + 1 
    #                 parent[v] = adjVertex


    # return bucket, BFSTree, parent   

    # visited=[]
    # unvisited=[]
    # Q=[]
    # for key in graph.keys() :
    #     unvisited.append(key)
    # parent={}
    # shortest_dist_from_root={root: math.inf for root in graph}
    # shortest_dist_from_root[root]=0
    # visited.append(root)
    # Q.extend(graph[root])

    # print(visited)
    # print()
    # # print(unvisited)
    # print(Q)
    # print()
    # print(shortest_dist_from_root)
    # distance={}
    # distance[root]=graph[root]
    # print(distance)

    # unvisited.pop(0)
    # while unvisited:
    #     graph_key= unvisited.pop(0)
    #     print(graph_key)


def baltiDijkstra(graph,root):

    distance= {root: math.inf for root in graph}
    distance[root]=0  
    
    parent= {root: None for root in graph}
    parent[root]=root
    Q = [(0,root)]
    

    while Q:
        current_distance, current_root = heapq.heappop(Q)
        # print()
        # print(current_root,current_distance)
       
        for next_root, weight in graph[current_root]:    
            # print(parent[current_root])
            temp_distance= current_distance + weight
            # print(current_root,distance[current_root],next_root, distance[next_root],current_distance, weight, temp_distance,end='\n ')
            # tempDst.append(temp_distance)
            # Nextroot.append(next_root)
            # Wght.append(weight)
            # CurRoot.append(current_root)

            if temp_distance < distance[next_root]:                
                distance[next_root]= temp_distance
                parent[next_root] = current_root
                parent[next_root]=current_root
                heapq.heappush(Q,(temp_distance,next_root))
                

    # newDistance=list(zip(CurRoot,Nextroot,Wght, tempDst))

    return parent, distance
    
def DistanceBTWTwoCities(graph,start_city,end_city):

    f_distance={node:float('inf') for node in graph}
    f_distance[start_city]=0
    g_distance={node:float('inf') for node in graph}
    g_distance[start_city]=0
    parent={node:None for node in graph}
    parent[start_city]=start_city
    queue=[(0,start_city)]
    while queue:
        current_f_distance,current_node=heapq.heappop(queue)
        if current_node == end_city:
            finalDistance=dict(sorted(f_distance.items(), key=lambda item: item[1]))
            return finalDistance, parent
        for next_node,weights in graph[current_node]:
            temp_g_distance=g_distance[current_node]+weights
            if temp_g_distance<g_distance[next_node]:
                g_distance[next_node]=temp_g_distance
                heuristic=weights
                f_distance[next_node]=temp_g_distance+heuristic
                parent[next_node]=current_node
                heapq.heappush(queue,(f_distance[next_node],next_node))
    finalDistance=dict(sorted(f_distance.items(), key=lambda item: item[1]))
    return finalDistance, parent

graph = {'a': [('b',6),('d',1)], 
        'b': [('c',5),('d',2),('e',2),('a',6)],
         'c': [('b',5),('e',5)], 
         'd': [('b',2),('a',1),('e',1)],
         'e': [('d',1),('b',2),('c',5)]

          }



graph1={'a':[('b',2),('c',1),('d',6)],
        'b':[('a',2),('c',5),('d',4)],
        'c':[('b',5),('a',1),('d',3)],
        'd': [('b',4),('a',6),('c',3)]

}
root= 'a'
# print(graph)
BaltiD = DistanceBTWTwoCities(graph1, root,'d')
print(BaltiD)
# print('Traversed Tree', myBucket)
# print('Traversed Tree with Level', treeLevel)
# print('Parent Information', parent)
