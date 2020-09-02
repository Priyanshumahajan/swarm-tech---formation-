#import libs
from math import sin, cos, sqrt, atan2, radians
from sympy import Point, Line, Circle,Point2D,pi,Segment
from sympy.geometry import Ray
from geopy.distance import geodesic
import matplotlib.pyplot as plt
'''will use geopy when we deal in lat long.
just replace the  function distance with :
def distance(a,b):
    d = geodesic(a,b)
    return d'''

onemtr = 1/111139
s = 5   # safety distance
s = s*onemtr
#list of initial posi of drones
d = [Point2D(21.285117,74.841746),Point2D(21.285070,74.841775),Point2D(21.285083,74.841814),Point2D(21.285110,74.841799),Point2D(21.285121,74.841759)]
n = len(d)
allloc=[[]for i in range(n)]
#slope of the final lines
finalln=0.5*pi
#function for calc for distance
def distance(a,b):
    d = geodesic(a,b)
    return d

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

#function to assign drones to points on the circle
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
def split(start, end, seg):
    x_delta = (end[0] - start[0]) / float(seg)
    y_delta = (end[1] - start[1]) / float(seg)
    points = []
    for i in range(1, seg):
        points.append(Point2D([start[0] + i * x_delta, start[1] + i * y_delta]))
    return [start] + points + [end]

############################################################################
'''function formation is the main executable function .
here dl is list of initial loc of drones,num is no of drones,
safety is distance between 2 drones'''
def formation(dl,num,safety,allloc):
    for i in range(n):
        allloc[i].append(dl[i])
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
    r = radius(num,safety)
    TheCircle=Circle(center,r)
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

    for i in range(n):
        allloc[i].append(d[i])

    circle = plt.Circle(center,radius(num,safety),fill = False)
    plt.gcf().gca().add_artist(circle)

    print("###############################################")
    print("stage 1 initiate")
    print(dl)
    x1=[]
    y1=[]
    for i in range(n):
        x1.append(dl[i].x)
        y1.append(dl[i].y)
    r = Line(center,slope=(finalln))
    f = TheCircle.intersection(r)
    f1 = (split(f[0],f[1],(n-1)))
    for i in range(num):
        dl[i] = assign(f1,dl[i])
        remove = dl[i]
        if remove in f1:
            f1.pop(f1.index(remove))
    finallinex = []
    finalliney = []
    for i in range(n):
        finallinex.append(dl[i].x)
        finalliney.append(dl[i].y)
    plt.plot(finallinex,finalliney,c='black')


    for i in range(n):
        allloc[i].append(d[i])

    print("############################################")
    print("stage 2 initiate")
    print(dl)

    print("all locations",allloc)

    segs=[[]for i in range(n)]
    for i in range(n):
        for j in range(3):
            if(j+1>2):
                continue
            else:
                segment = Segment(allloc[i][j],allloc[i][j+1])
                segs[i].append(segment)
    print(segs)

    x1 = []
    y1 = []
    for i in range(n):
        for j in range(3):
            x1.append(allloc[i][j].x)
            y1.append(allloc[i][j].y)
    plt.scatter(x1,y1)
    line = []
    for i in range(n):
        line1 = plt.plot(x1[0+3*i:3+3*i],y1[0+3*i:3+3*i])
        line.append(line1)

    plt.show()
formation(d,n,s,allloc)
