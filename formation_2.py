#import libs
from math import sin, cos, sqrt, atan2, radians
from sympy import Point, Line, Circle,Point2D,pi,Segment
from sympy.geometry import Ray
from geopy.distance import geodesic

''' data set for the initial loc of drones
a1=(0,0)
a2=(1,2)
a3=(2,3)
a4=(2,1)
'''

n = 4    # no of drones
s = 2    # safety distance
d1 = Point2D(0,0)
d2 = Point2D(1,2)
d3 = Point2D(2,3)
d4 = Point2D(2,1)
#list of initial posi of drones
d = [Point2D(0,0),Point2D(1,2),Point2D(2,3),Point2D(2,1)]
finalln=radians(pi/2)

#function for calc for distance
def distance(a,b):
    dist = sqrt((a.x-b.x)**2 + ((a.y-b.y)**2))
    return dist

# function for radius
def radius(n,s):
    r = s*(n-1)
    r = r/2
    return r

#function to generate points on the circle
def circpts(n,TheCircle,center,finalln):
    points=[]
    for i in range(n):
        rays = Ray(center,angle=(0+((2*pi/n)*i)))
        points.append(TheCircle.intersection(rays))
    return points

#function to assign drones to points on the circle !!!! ISSUE HERE !!!!
def assign(circpts,d):
    dist = distance(circpts[0],d)
    goto = circpts[0]
    for i in range(len(circpts)):
        dist1 = distance(circpts[i],d)
        if(dist1<dist):
            dist = dist1
            goto = circpts[i]
        else:
            continue
    return goto

#function to split required line and get points on the required line
def split(start, end, segments):
    x_delta = (end[0] - start[0]) / float(segments)
    y_delta = (end[1] - start[1]) / float(segments)
    points = []
    for i in range(1, segments):
        points.append(Point2D([start[0] + i * x_delta, start[1] + i * y_delta]))
    return [start] + points + [end]
############################################################################

# calc center for Circle
x = d1.x + d2.x + d3.x + d4.x
y = d1.y + d2.y + d3.y + d4.y
x = x/n
y = y/n
center = Point2D(x,y)

#plotting circle, calling radius function
TheCircle=Circle(center,radius(n,s))
#creating points on circle,calling circpts for points
points=circpts(n,TheCircle,center,finalln)
#got output as nested list , flatting the list in next 4 lines
circpts = []
for sublist in points:
	for val in sublist:
		circpts.append(val)
if(circpts[0].is_concyclic(circpts[1],circpts[2],circpts[3])==True):
    try:
        #calling assign function to assign points to drone
        d1 = assign(circpts,d1)
        #next 3 lines to remove selected loc from list same code after every call of assign
        remove = d1
        if remove in circpts:
            circpts.pop(circpts.index(remove))
            d2 = assign(circpts,d2)
            remove = d2
        if remove in circpts:
            circpts.pop(circpts.index(remove))
            d3 = assign(circpts,d3)
            remove = d3
        if remove in circpts:
            circpts.pop(circpts.index(remove))
            d4 = assign(circpts,d4)
            remove = d4
        if remove in circpts:
            circpts.pop(circpts.index(remove))
        print("###############################################")
        print("stage 1 initiate")
        print("drone 1 goto",d1)
        print("drone 2 goto",d2)
        print("drone 3 goto",d3)
        print("drone 4 goto",d4)
        r = Line(center,slope=(finalln))
        f = TheCircle.intersection(r)
        f1 = (split(f[0],f[1],(n-1)))
        d1 = assign(f1,d1)
        if remove in f1:
            f1.pop(f1.index(remove))
        d2 = assign(f1,d2)
        remove = d2
        if remove in f1:
            f1.pop(f1.index(remove))
        d3 = assign(f1,d3)
        remove = d3
        if remove in f1:
            f1.pop(f1.index(remove))
        d4 = assign(f1,d4)
        remove = d4
        if remove in f1:
            f1.pop(f1.index(remove))
        print("############################################")
        print("stage 2 initiate")
        print("drone 1 goto",d1,"in line")
        print("drone 2 goto",d2,"in line")
        print("drone 3 goto",d3,"in line")
        print("drone 4 goto",d4,"in line")
    except:
        print("not concyclic check prog or points")
