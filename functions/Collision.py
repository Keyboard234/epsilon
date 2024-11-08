import math

#point = (x, y)
#circle = (point, radius)
#rect = (x, y, xsize, ysize)
#line = (point, point)

def dist(p1, p2):
    distx = p2[0]-p1[0]
    disty = p2[1]-p1[1]
    return math.sqrt((distx**2) + (disty**2))

def linepoint(line, point):
    linelength = dist(line[0], line[1])
    pointdist1 = dist(point, line[0])
    pointdist2 = dist(point, line[1])
    
    buf = 0.1
    return ((pointdist1 + pointdist2) >= linelength-buf and (pointdist1 + pointdist2) <= linelength+buf)

def circlepoint(circle, point):
    return (dist(point, circle[0]) < circle[1])

def lineline(line1, line2):
    point1 = line1[0]
    point2 = line1[1]
    point3 = line2[0]
    point4 = line2[1]

    uAn = ((point4[0]-point3[0])*(point1[1]-point3[1]) - (point4[1]-point3[1])*(point1[0]-point3[0]))
    uAd = ((point4[1]-point3[1])*(point2[0]-point1[0]) - (point4[0]-point3[0])*(point2[1]-point1[1]))
    uA = uAn/uAd

    uBn = ((point2[0]-point1[0])*(point1[1]-point3[1]) - (point2[1]-point1[1])*(point1[0]-point3[0]))
    uBd = ((point4[1]-point3[1])*(point2[0]-point1[0]) - (point4[0]-point3[0])*(point2[1]-point1[1]))
    if uBd == 0:
        uBd = 0.000001
    uB = uBn/uBd
    
    if uA >= 0 and uA <= 1 and uB >= 0 and uB <= 1:
        intersectionx = point1[0] + (uA * (point2[0]-point1[0]))
        intersectiony = point1[1] + (uA * (point2[1]-point1[1]))
        return True, (intersectionx, intersectiony)
    return False, False

def linerect(line, rect):

    rectsize = rect[2:]
    rectpos = rect[:2]
    
    posx2 = rectpos[0] + rectsize[0]
    posy2 = rectpos[1] + rectsize[1]
    
    line1 = ((rectpos[0], rectpos[1]), (posx2, rectpos[1])) #top
    line2 = ((rectpos[0], rectpos[1]), (rectpos[0], posy2)) #left

    line3 = ((posx2, posy2),           (posx2, rectpos[1])) #right
    line4 = ((posx2, posy2),           (rectpos[0], posy2)) #bottom

    points = []

    result1, p = lineline(line, line1)
    if result1 is not False:
        points.append(p)

    result2, p = lineline(line, line2)
    if result2 is not False:
        points.append(p)

    result3, p = lineline(line, line3)
    if result3 is not False:
        points.append(p)

    result4, p = lineline(line, line4)
    if result4 is not False:
        points.append(p)

    return (result1 or result2 or result3 or result4), points

def circleline(circle, line, debug=False):
    point1 = line[0]
    point2 = line[1]
    
    inside1 = circlepoint(circle, point1)
    inside2 = circlepoint(circle, point2)
    
    linelength = dist(point1, point2)
    
    x1 = point1[0]
    y1 = point1[1]
    
    x2 = point2[0]
    y2 = point2[1]

    cx = circle[0][0]
    cy = circle[0][1]

    dot = (((cx-x1)*(x2-x1)) + ((cy-y1)*(y2-y1))) / linelength**2
    closestx = x1 + (dot * (x2-x1))
    closesty = y1 + (dot * (y2-y1))
    closestpoint = (closestx, closesty)

    onsegment = linepoint(line, closestpoint)

    if debug:
        print("inside: ", (inside1 or inside2))
        print(line, closestpoint, onsegment)
        

    if inside1 or inside2: return True, closestpoint  
    
    if not onsegment: return False, closestpoint

    closestdist = dist(circle[0], closestpoint)
    
    return (closestdist < circle[1]), closestpoint

def circlerect(circle, rect):
    rectsize = rect[2:]
    rectpos = rect[:2]

    circlepos = circle[0]

    posx2 = rectpos[0] + rectsize[0]
    posy2 = rectpos[1] + rectsize[1]

    line1 = ((rectpos[0], rectpos[1]), (posx2, rectpos[1])) #top
    line2 = ((rectpos[0], rectpos[1]), (rectpos[0], posy2)) #left

    line3 = ((posx2, posy2),           (posx2, rectpos[1])) #right
    line4 = ((posx2, posy2),           (rectpos[0], posy2)) #bottom
    
    result1 = False
    result2 = False
    result3 = False
    result4 = False

    if circlepos[1] < rectpos[1]: #above
        result1 = circleline(circle, line1)[0]
    elif circlepos[1] > rectsize[1]: #below
        result2 = circleline(circle, line4)[0]
    
    if circlepos[0] < rectpos[0]: #left
        result3 = circleline(circle, line2)[0]
    elif circlepos[0] > rectsize[0]: #right
        result4 = circleline(circle, line3)[0]

    return (result1 or result2 or result3 or result4)
