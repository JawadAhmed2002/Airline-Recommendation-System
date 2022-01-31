
import heapq
import math


def baltiDijkstra(graph,root):

    distance= {root: math.inf for root in graph}
    distance[root]=0  
    
    parent= {root: None for root in graph}
    Q = [(0,root)]

    bucket={}
    # tempDst=[]
    # Nextroot=[]
    # Wght=[]
    # CurRoot=[]
    while Q:
        # print('Q:', Q, 'B:', bucket)
        current_distance, current_root = heapq.heappop(Q)
        # print(current_root,current_distance)

        if current_distance > distance[current_root]:
            continue

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
                heapq.heappush(Q,(temp_distance,next_root))

            bucket[current_root] = current_distance
    # newDistance=list(zip(CurRoot,Nextroot,Wght, tempDst))

    return bucket, distance