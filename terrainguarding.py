import os

def ith_element(l, i):
    return l[i-1]


def union(a, b):
    u = a + [member for member in b if member not in a]
    return u


def intersect(a, b):
    i = [member for member in a if member in b]
    return i

#################################################################################
#  THIS FUNCTION GIVES A FULL FILE PATH AND RETURNS A LIST OF THE POINTS IN IT  #
#                                    BEGIN                                      #
#################################################################################
fpath = '/Users/grack/Downloads/instances/concavevalleys/concavevalleys-500000-10.terrain'
fname = os.path.basename(fpath)
newfname = fname + '_solution.txt'


def make_list_from_file(fname):
    with open(fname) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    lines = [x.strip() for x in content]
    number = lines[0]
    iterations_count = int(number)
    new_list = []
    while iterations_count > 0:
        line = lines[iterations_count]
        line = line.split(' ')
        line = map(float, line)
        new_list.append(line)
        iterations_count -= 1
    return new_list
#################################################################################
#  THIS FUNCTION GIVES A FULL FILE PATH AND RETURNS A LIST OF THE POINTS IN IT  #
#                                      END                                      #
#################################################################################

##############################################################################
#  INPUT OF THE PROBLEM; SHOULD BE ASSIGNED TO THE VARIABLE 'points' - BEGIN #
#  NOTE : THERE IS NO NEED FOR THE POINTS TO BE SORTED                       #
#  THE APPLICATION DOES SORTING ITSELF                                       #
##############################################################################
a = [1, 10]
b = [2, 1]
c = [3, 12]
d = [4, 4]
e = [5, 7]
f = [6, 5]
g = [7, 9]
h = [8, 3]
i = [9, 8]
j = [10, 6]
k = [11, 12]
l = [12, 2]
m = [13, 11]
points = [b, c, d, e, f, g, h, i, j, k, l, m, a]
points = make_list_from_file(fpath)
points = sorted(points)
points.reverse()
##############################################################################
#  INPUT OF THE PROBLEM; SHOULD BE ASSIGNED TO THE VARIABLE 'points' - END   #
##############################################################################


#############################################################################
#  UPPER CONVEX HULL - GRAHAM METHOD - BEGIN                                #
#  INPUT : AN ARRAY OF POINTS                                               #
#  A POINT IS A MEMBER OF THE INPUT ARRAY                                   #
#  EACH POINT HAS TWO ELEMENTS. E.G. [5,0]                                  #
#  OUTPUT : AN ARRAY INCLUDING UPPER CONVEX HULL'S POINTS                   #
#  THIS FUNCTION (upper_convex_hull) IS SAFE (DOESN'T CHANGE THE INPUT)     #
#############################################################################
TURN_LEFT, TURN_RIGHT, TURN_NONE = (1, -1, 0)


def turn(p, q, r):
    return cmp((q[0] - p[0])*(r[1] - p[1]) - (r[0] - p[0])*(q[1] - p[1]), 0)


def _keep_left(hull, r):
    while len(hull) > 1 and (turn(hull[-2], hull[-1], r) == TURN_RIGHT):
            hull.pop()
    if not len(hull) or hull[-1] != r:
        hull.append(r)
    return hull


def upper_convex_hull(points):
    u = reduce(_keep_left, points, [])
    return u
#############################################################################
#  UPPER CONVEX HULL - GRAHAM METHOD - END                                  #
#############################################################################

###################################################################################################
#  ONION PEELING - BEGIN                                                                          #
#  INPUT : A SET OF POINTS                                                                        #
#  OUTPUT : A LIST OF LISTS EACH CONTAINING THE POINTS OF A LAYER IN THE ONION PEELING            #
#  FOR EXAMPLE, ONE CAN GET THE FIRST LAYER (WHICH IS AN ARRAY OF POINTS) USING 'onion_layers[0]' #
###################################################################################################


def onion_peeling(point_set):
    onion_layers = []
    working_set = point_set[:]
    while len(working_set) >= 3:
        uch = upper_convex_hull(working_set)
        onion_layers.append(uch)
        working_set = [point for point in working_set if point not in uch]
    return onion_layers

###################################################################################################
#  ONION PEELING - END                                                                            #
###################################################################################################

######################################################################
#  POINTS BETWEEN TWO POINTS IN THE GIVEN SET - BEGIN                #
#  OUTPUT WILL BE A LIST OF POINTS INCLUDING THE GIVEN POINTS        #
#  THERE IS NO NEED FOR THE TERRAIN OR POINTS TO BE SORTED           #
######################################################################


def points_between(terrain, a, b):
    t = terrain[:]
    t = sorted(t)
    if a[0] <= b[0]:
        result = [point for point in t if point[0] >= a[0]]
        result = [point for point in result if point[0] <= b[0]]
    else:
        result = [point for point in t if point[0] >= b[0]]
        result = [point for point in result if point[0] <= a[0]]
    return result


######################################################################
#  POINTS BETWEEN TWO POINTS IN THE GIVEN SET - END                  #
######################################################################

#########################################
#  ITH EDGE OF A CONVEX HULL (OR LAYER) #
#                BEGIN                  #
#########################################
def ith_edge(convex_hull_vertices, i):
    c = sorted(convex_hull_vertices)
    edge = [c[i-1], c[i]]
    return edge
#########################################
#  ITH EDGE OF A CONVEX HULL (OR LAYER) #
#                  END                  #
#########################################

##########################################################################################
#                                     E(LAYER_L_I)  BEGIN                                #
##########################################################################################


def elayeril(layers, bags, l, i):
    the_number_of_edges_in_layer_l = len(ith_element(layers,l))-1
    edges = []
    for x in range(the_number_of_edges_in_layer_l):
        edge = ith_edge(ith_element(layers, l), x+1)
        intersection = [point for point in edge if point in bags[i-1]]
        if len(intersection) > 0:
            edges.append(edge)
    return edges

##########################################################################################
#                                     E(LAYER_L_I)  END                                  #
##########################################################################################
pockets = [[]]


def td_construction(l, layers, terrain):
    global pockets
    number_of_nodes = len(tree_decompositions[l-1])
    td_new = []
    for i in range(1, number_of_nodes+1):
        #####
        pockets.append([])
        #####
        edges = elayeril(layers,tree_decompositions[l-1], l, i)
        m = len(edges)
        for o in range(1, m+1):
            edge = edges[o-1]
            terrain_vertices = points_between(terrain, edge[0], edge[1])
            x_i = tree_decompositions[l-1][i-1]
            #####
            e_0 = edges[0]
            v_p = e_0[0]
            v_q = e_0[1]
            x_i_temp = x_i[:]
            x_i_temp.reverse()
            if v_p in x_i_temp:
                pockets[i].append([v_p, x_i_temp[x_i_temp.index(v_p)+1]])
            if v_q in x_i_temp:
                pockets[i].append([x_i_temp[x_i_temp.index(v_q)-1], v_q])
            # print '-----'
            # print pockets
            # print '-----'
            #####
            second_intersection = intersect(terrain_vertices, x_i)
            first_intersection = []
            for j in range(1, l+1):
                inner_intersection = intersect(ith_element(layers, j), x_i)
                first_intersection = union(first_intersection, inner_intersection)
            new_bag = union(first_intersection, second_intersection)
            td_new.append(new_bag)
    return td_new

layers = onion_peeling(points)
tree_decompositions = [[points]]
k = len(layers)
#####
all_pockets = []
#####
for l in range(1, k+1):
    all_pockets.append(pockets)
    pockets = [[]]
    tree_decompositions.append(td_construction(l, layers, points))

output = ''
output += (str(len(layers)) + ' layers in onion peeling: \n')
layer_counter = 1

for layer in layers:
    output += ('Layer ' + str(layer_counter) + '\n')
    # output = output, 'Layer', layer_counter, '\n'
    for point in layer:
        output = output + '(' + str(point[0]) + ',' + str(point[1]) + ') '
    output += '\n'
    layer_counter += 1
output += '---------------------------------------------------------------------------------------\n'

td_counter = 0
for td in tree_decompositions:
    output += ('TD ' + str(td_counter) + ' :\n')
    td_counter += 1
    for bag in td:
        # print bag
        for point in bag:
            output += ('(' + str(point[0]) + ',' + str(point[1]) + ') ')
        output += '\n'

layer_pocket_counter = 0
for layer_pocket in all_pockets:
    output += ('Pocket ' + str(layer_pocket_counter) + ' :\n')
    temp = layer_pocket[1:]
    output += '('
    if len(temp)>0:
        for pocket in temp:
                for edge in pocket:
                    output += '{ '
                    first_end = edge[0]
                    second_end = edge[1]
                    output += (' (' + str(first_end[0]) + ',' + str(first_end[1]) + ') ,' + '(' + str(second_end[0]) + ',' + str(second_end[1]) + ') ')
                    output += '} '
    output += ')\n'
    layer_pocket_counter += 1

print '------------------------------------------------------'
with open('/Users/grack/Documents/tgpilsolutions/concavevalleys/' + newfname, 'w') as f:
    f.write(output)
# print output