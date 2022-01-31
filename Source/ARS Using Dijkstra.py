# Airline Recommendation System Using Bucket Dijkstra Algorithm
import os
from posixpath import commonpath
import sys
import heapq
import math

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
cities_name = os.path.join(THIS_FOLDER, 'cities_name.txt')
cities_code = os.path.join(THIS_FOLDER, 'cities_code.txt')
cities_distance = os.path.join(THIS_FOLDER, 'cities_distance.txt')

# Read Txt File


def readFileArr(txtFile):

    with open(txtFile, mode='rt') as f:
        array = [[int(x) for x in line.split()] for line in f]
        return array


def readFileLst(txtFile):

    with open(txtFile, mode='rt') as f:
        data = f.read().splitlines()
    return data


citiesDistance = readFileArr(cities_distance)
citiesCode = readFileLst(cities_code)
citiesName = readFileLst(cities_name)
adjacencyMatrix = citiesDistance

undirected_graph = {}

for i in range(len(citiesCode)):
    undirected_graph[citiesCode[i]] = adjacencyMatrix[i]
# print(undirected_graph)


def vertexWithWeight(graph, givenCity):
    cityGraph = {}
    cityData = graph[givenCity]
    combData = list(zip(citiesCode, cityData))

    valueIndx = [i for i, tupl in enumerate(combData) if (tupl[1] == 0)]
    for Indx in sorted(valueIndx, reverse=True):
        del combData[Indx]
    cityGraph[givenCity] = list()
    cityGraph[givenCity].extend(combData)
    return cityGraph


def Weighted_grpah(graph):
    final_graph = vertexWithWeight(graph, 'AZ')
    for i in citiesCode:
        final_graph.update(vertexWithWeight(graph, i))
    return final_graph
# print(Weighted_grpah(undirected_graph))


# Dijkstra Baalti Algo
def baltiDijkstra(graph, root):
    distance = {root: math.inf for root in graph}
    distance[root] = 0
    parent = {root: None for root in graph}
    parent[root] = root
    Q = [(0, root)]
    bucket = {}
    # tempDst=[]
    # Nextroot=[]
    # Wght=[]
    # CurRoot=[]
    while Q:
        # print('Q:', Q, 'B:', bucket)
        current_distance, current_root = heapq.heappop(Q)
        # print(current_root, current_distance)
        for next_root, weight in graph[current_root]:

            temp_distance = current_distance + weight
            print(current_root, distance[current_root], next_root,
                  distance[next_root], current_distance, weight, temp_distance, end='\n ')
            # tempDst.append(temp_distance)
            # Nextroot.append(next_root)
            # Wght.append(weight)
            # CurRoot.append(current_root)

            if temp_distance < distance[next_root]:
                distance[next_root] = temp_distance
                parent[next_root] = current_root
                parent[next_root] = current_root
                heapq.heappush(Q, (temp_distance, next_root))

            bucket[current_root] = current_distance
    # newDistance=list(zip(CurRoot,Nextroot,Wght, tempDst))
    return parent, distance, bucket


# Distance Between Two Cities
def DistanceBTWTwoCities(graph, start_city, end_city):

    f_distance = {node: float('inf') for node in graph}
    f_distance[start_city] = 0
    g_distance = {node: float('inf') for node in graph}
    g_distance[start_city] = 0
    parent = {node: None for node in graph}
    parent[start_city] = start_city
    queue = [(0, start_city)]
    while queue:
        current_f_distance, current_node = heapq.heappop(queue)
        if current_node == end_city:
            finalDistance = dict(
                sorted(f_distance.items(), key=lambda item: item[1]))
            return finalDistance, parent
        for next_node, weights in graph[current_node]:
            temp_g_distance = g_distance[current_node]+weights
            if temp_g_distance < g_distance[next_node]:
                g_distance[next_node] = temp_g_distance
                heuristic = weights
                f_distance[next_node] = temp_g_distance+heuristic
                parent[next_node] = current_node
                heapq.heappush(queue, (f_distance[next_node], next_node))
    finalDistance = dict(sorted(f_distance.items(), key=lambda item: item[1]))
    return finalDistance, parent


def update_in_alist(alist, key, value):
    return [(k, v) if (k != key) else (key, value) for (k, v) in alist]


def update_in_alist_inplace(alist, key, value):
    alist[:] = update_in_alist(alist, key, value)


def remove_direct_route(graph, givenCity, remDirRouCity):
    cityData = graph[givenCity]

    first_tuple_elements = [a_tuple[0] for a_tuple in cityData]
    for val in first_tuple_elements:
        if val == remDirRouCity:
            update_in_alist_inplace(cityData, val, 0)
            print(val, ', Direct Route is removed Successfully')
            print(
                'In Following Record The Desired City Route Is Destroyed Against The Selected City:', '\n')
    valueIndx = [i for i, tupl in enumerate(cityData) if (tupl[1] == 0)]
    for Indx in sorted(valueIndx, reverse=True):
        del cityData[Indx]
    graph[givenCity] = list()
    graph[givenCity].extend(cityData)
    return graph


def shortestCityPathInfo(graph, city):

    visited = {}
    parent, distance, Binfo = baltiDijkstra(graph, city)
    unvisited = Binfo.copy()
    Binfo.clear()
    unvisited.pop(city)
    minKeys = shortestDistanceCity(graph, city)
    combinedInfo = {}

    for i in range(len(minKeys)):

        if minKeys:
            for key in minKeys:
                pass

            delete = [i for i in minKeys if i == key]
            for i in delete:
                del minKeys[key]

            if delete[0] not in visited:
                parent, distance, Binfo = baltiDijkstra(graph, delete[0])
                combinedInfo[delete[0]] = Binfo
            visited[delete[0]] = unvisited[delete[0]]
            unvisited.pop(delete[0])
    return visited, unvisited, combinedInfo


def shortestDistanceAndPath(graph, givenCity):
    updateShrtestDst = {}
    visited, unvisited, combinedInfo = shortestCityPathInfo(graph, givenCity)

    for key in visited:
        updateShrtestDst[key] = visited[key]
        del visited[key]
        break
    minKeys = {}
    for key in unvisited:

        for city in combinedInfo:
            if city not in updateShrtestDst:
                minKeys[city] = shortestDistanceCity(graph, city)

        for minKey in minKeys:
            # print(minKey)
            if minKey not in updateShrtestDst:
                print(minKeys)
                dicval = sum(updateShrtestDst.values())

                minVal = sum(minKeys[minKey].values())

                # print(dicval,minVal)
                distance = dicval + minVal
                updateShrtestDst[minKey] = distance
        minKeys.clear()
        visited, unvisited, combinedInfo = shortestCityPathInfo(graph, key)

    return updateShrtestDst


def shortestDistanceCity(graph, city):
    parent, distance, Binfo = baltiDijkstra(graph, city)
    unvisited = Binfo.copy()
    Binfo.clear()
    unvisited.pop(city)
    minKeys = {}
    min_keys = [k for k, x in unvisited.items() if not any(
        y < x for y in unvisited.values())]
    for key in min_keys:
        minKeys[key] = unvisited[key]

    return minKeys


def longestDistanceCity(graph, city):
    parent, distance, Binfo = baltiDijkstra(graph, city)
    unvisited = Binfo.copy()
    Binfo.clear()
    unvisited.pop(city)
    maxKeys = {}
    max_keys = [k for k, x in unvisited.items() if not any(
        y > x for y in unvisited.values())]
    for key in max_keys:
        maxKeys[key] = unvisited[key]

    return maxKeys


graph = Weighted_grpah(undirected_graph)


# print(remove_direct_route(graph,'AZ','BD'))


def AirlineRecommendationSystem():
    print('Following Data Shows the Adjacency List Of Airline Operation:')
    print()
    print(graph)

    while True:
        print('Menu to Perform Operations using this Program:')
        print('a. Best Distance or Route From the given City: ')
        print('b. Best Route From the Given city to the other city with minimum Cost:  ')
        print('c. Longest Distance of other city From the Given City: ')
        print('d. Smallest Distance of other city From the Given City: ')
        print('e. Removed Direct Route From Any Given City: ')
        print('f. After Removing Direct Route Find Distance Between Two Cities: ')
        print('g. Best Route From the Given city to all others cities with minimum Cost: ')
        print('h. Exit The Program')
        print()
        Command = input('Enter any above alphabet to perform operations: ')
        print()
        if Command == 'a':
            print(' '.join(map(str, citiesCode)))
            print()
            givenCity = input('Enter Any Above City Code To Find Near Route: ')

            print('Nearest Route To The Given City Is The Following:')
            print()
            parent, distance, bucket = baltiDijkstra(graph, givenCity)
            print('Following is the Parent Along with Distance', '\n')
            print(parent, '\n')
            print(distance, '\n')
            print(bucket)
            print()
        if Command == 'b':
            print(' '.join(map(str, citiesCode)))
            print()
            givenCity1 = input('Enter Any Above "From" City Code : ')
            givenCity2 = input('Enter Any Above "To" City Code : ')
            print()
            print('Best Route From the Given city with minimum Cost is Following :')
            distance, route = DistanceBTWTwoCities(
                graph, givenCity1, givenCity2)
            print('From City', givenCity1, ':',
                  distance[givenCity1], 'To The Given City With Cost Is ', ':', distance[givenCity2])
            print('Following Is The Route')
            print(givenCity2, ':', route[givenCity1],
                  ', Indirect Route If Available Otherwise Show Same: ', givenCity1, ':', route[givenCity2])
            print()

        if Command == 'c':
            print(' '.join(map(str, citiesCode)))
            print()
            givenCity = input(
                'Enter Any Above City Code To Find Longest Distance City: ')
            print('Longest Distance of other city From the Given City Is Following:')
            print()
            print(longestDistanceCity(graph, givenCity))
            print()
        if Command == 'd':
            print(' '.join(map(str, citiesCode)))
            print()
            givenCity = input(
                'Enter Any Above City Code To Find Smallest Distance City: ')
            print('Smallest Distance of other city From the Given City Is Following:')
            print()
            print(shortestDistanceCity(graph, givenCity))
            print()

        if Command == 'e':
            print(' '.join(map(str, citiesCode)))
            print()
            givenCity = input(
                'Enter Any Above City Code: ')
            givenCity1 = input(
                'Again Enter Any Above City Code In Order To Remove Its Direct Link With Previous City: ')

            print()
            print(remove_direct_route(graph, givenCity, givenCity1), '\n')
            print('Scroll Above In Order To See Changes')

            print('After Removing Direct Edges Following Is The Ditance Between These Two Cities, We Can Say Alternate Route Is: ')
            distance, route = DistanceBTWTwoCities(
                graph, givenCity, givenCity1)
            
            print('From City', givenCity, ':',
                  distance[givenCity], 'To The Given City With Minimum Cost Is ', ':', distance[givenCity1])
            print('Following Is The Route')
            print(givenCity1, ':', route[givenCity],'Deleted',
                  ', Now The Alternative Route Is: ', givenCity, ':', route[givenCity1])
            print()

            # print(graph)
        if Command == 'f':
            print(' '.join(map(str, citiesCode)))
            print()
            givenCity1 = input('Enter Any Above "From" City Code : ')
            givenCity2 = input('Enter Any Above "To" City Code : ')
            print()
            print('Best Route From the Given city with minimum Cost is Following :')
            distance, route = DistanceBTWTwoCities(
                graph, givenCity1, givenCity2)
            print('From City', givenCity1, ':',
                  distance[givenCity1], 'To The Given City With Cost Is ', ':', distance[givenCity2])
            print('Following Is The Route')
            print(givenCity2, ':', route[givenCity1],
                  ', Indirect Route If Available Otherwise Show Same: ', givenCity1, ':', route[givenCity2])
            print()

        if Command == 'g':
            print(' '.join(map(str, citiesCode)))
            print()
            givenCity = input(
                'Enter Any Above City Code To Find Longest Distance City: ')
            print()
            print(
                'Best Route From the Given city to all other cities with minimum Cost is Following :')
            print('It may not Work Properly Because It is under Maintenance..........')
            print(shortestDistanceAndPath(graph, givenCity))
            print()

        if Command == 'h':
            print('Program Exit Successfully')
            return quit()


AirlineSystem = AirlineRecommendationSystem()
