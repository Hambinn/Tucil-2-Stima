import math
# main function, untuk menkonversi numpy array ke array biasa, mencari min max, mencari titik hull dan dipasangkan menjadi garis
def myConvexHull(unconv):
    solution = []
    solutionPair = []
    points = convertToArr(unconv)
    minimum,maximum = findExtreme(points)
    solution.append(minimum)
    solution.append(maximum)

    kiri,kanan = divide(points,minimum,maximum)
    hullSet1(kiri,minimum,maximum,solution)
    hullSet2(kanan,minimum,maximum,solution)

    x = sum(point[0] for point in solution)/len(solution)
    y = sum(point[1] for point in solution)/len(solution)
    solution.sort(key = lambda point: math.atan2(point[0]-x,point[1]-y))
    
    for i in range(len(solution)):
        if i == len(solution)-1:
            solutionPair.append([solution[i],solution[0]])
        else:
            solutionPair.append([solution[i],solution[i+1]])
    return solutionPair

# untuk mengkonversi numpy array ke array biasa
def convertToArr(points):
    arr = []
    for i in range(len(points)):
        arr.append([float(points[i][0]),float(points[i][1])])
    return arr

# untuk mencari determinan
def determinan(x1,x2,x3):
    return(x1[0]*x2[1]) + (x1[1]*x3[0]) + (x2[0]*x3[1]) - (x3[0]*x2[1]) - (x3[1]*x1[0]) - (x2[0]*x1[1])

# untuk mencari titik maksimum dan minimum
def findExtreme(points):
    minimum = points[0]
    maximum = points[0]

    for point in points:
        if point[0] <= minimum[0]:
            minimum = point
        if point[0] >= maximum[0]:
            maximum = point
    return minimum, maximum

# untuk membagi hull menjadi set 1 dan set 2 sesuai besar determinan (+ atau -)
def divide(points,minimum,maximum):
    set1 = []
    set2 = []

    for point in points:
        if point!=minimum and point!=maximum:
            if(determinan(minimum,maximum,point) > 0):
                set1.append(point)
            if(determinan(minimum,maximum,point) < 0):
                set2.append(point)
    return set1,set2

# untuk mencari titik terjauh dari garis
def pointDistace(points,minimum,maximum):
    jarak = 0
    index = 0

    for i in range(len(points)):
        jaraktmp = abs((points[i][0]-minimum[0])*(maximum[1]-minimum[1]) - (maximum[0]-minimum[0])*(points[i][1]-minimum[1]))
        if jaraktmp > jarak:
            jarak = jaraktmp
            index = i
    
    return points[index]

# untuk mencari titik hull dari set 1(atas) secara rekursif setelah di divide
def hullSet1(points,minimum,maximum,solution):
    if(len(points) == 0):
        return
    else:
        pointmax = pointDistace(points,minimum,maximum)
        points.remove(pointmax)
        solution.append(pointmax)
        x1,a = divide(points,minimum,pointmax)
        x2,b = divide(points,pointmax,maximum)
        hullSet1(x1,minimum,pointmax,solution)
        hullSet1(x2,pointmax,maximum,solution)

# untuk mencari titik hull dari set 2(bawah) secara rekursif setelah di divide 
def hullSet2(points,minimum,maximum,solution):
    if(len(points) == 0):
        return
    else:
        pointmax = pointDistace(points,minimum,maximum)
        points.remove(pointmax)
        solution.append(pointmax)
        a,x1 = divide(points,minimum,pointmax)
        b,x2 = divide(points,pointmax,maximum)
        hullSet2(x1,minimum,pointmax,solution)
        hullSet2(x2,pointmax,maximum,solution)