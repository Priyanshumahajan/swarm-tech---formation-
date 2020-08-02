#import libs
from math import sin, cos, sqrt, atan2, radians
from sympy import Point, Line, Circle,Point2D,pi,Segment
from sympy.geometry import Ray
from geopy.distance import geodesic
'''will use geopy when we deal in lat long.
just replace the  function distance with :
def distance(a,b):
    d = geodesic(a,b)
    return d
'''

''' data set for the initial loc of drones
a1=(0,0)
a2=(1,2)
a3=(2,3)
a4=(2,1)
a4=(-1,5)
'''

n = 5    # no of drones
s = 2    # safety distance
#list of initial posi of drones
d = [Point2D(0,0),Point2D(1,2),Point2D(2,3),Point2D(2,1),Point2D(-1,5)]
#slope of the final lines
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
'''function formation is the main executable function .
here dl is list of initial loc of drones,num is no of drones,
safety is distance between 2 drones'''
def formation(dl,num,safety):
    x=[]
    y=[]
    for i in range(num):
        x.append(dl[i].x)
        y.append(dl[i].y)
    cenx=0
    ceny=0
    for i in range(num):
        cenx=cenx+x[i]
        ceny=ceny+y[i]
    cenx=cenx/num
    ceny=ceny/num
    center=(cenx,ceny)
    print(center)
    #plotting circle, calling radius function
    TheCircle=Circle(center,radius(num,safety))
    #creating points on circle,calling circpts for points
    points=circpts(num,TheCircle,center,finalln)
    #got output as nested list , flatting the list in next 4 lines
    circpt = []
    for sublist in points:
    	for val in sublist:
    		circpt.append(val)

    for i in range(n):
        dl[i] = assign(circpt,dl[i])
        remove = dl[i]
        if remove in circpt:
            circpt.pop(circpt.index(remove))

    print("###############################################")
    print("stage 1 initiate")
    print(dl)
    r = Line(center,slope=(finalln))
    f = TheCircle.intersection(r)
    f1 = (split(f[0],f[1],(n-1)))
    for i in range(num):
        dl[i] = assign(f1,dl[i])
        remove = dl[i]
        if remove in f1:
            f1.pop(f1.index(remove))

    print("############################################")
    print("stage 2 initiate")
    print(dl)
formation(d,n,s)
