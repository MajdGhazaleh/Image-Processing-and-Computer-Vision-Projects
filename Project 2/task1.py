"""
RANSAC Algorithm Problem
(Due date: Oct. 23, 3 P.M., 2019)
The goal of this task is to fit a line to the given points using RANSAC algorithm, and output
the names of inlier points and outlier points for the line.

Do NOT modify the code provided to you.
Do NOT use ANY API provided by opencv (cv2) and numpy (np) in your code.
Do NOT import ANY library (function, module, etc.).
You can use the library random
Hint: It is recommended to record the two initial points each time, such that you will Not 
start from this two points in next iteration.
"""
import random


def distance(p1,p2,p0) :
    """
    return square of perpendicular distance between two lines from point p0
    """
    x1, y1 = p1['value']
    x2, y2 = p2['value']
    x0, y0 = p0['value']
    
    return ((y2-y1)*x0 -(x2-x1)*y0 + x2*y1 - y2*x1)**2 / ((y2-y1)**2 + (x2-x1)**2)
    

    
def solution(input_points, t, d, k):
    """
    :param input_points:
           t: t is the perpendicular distance threshold from a point to a line
           d: d is the number of nearby points required to assert a model fits well, you may not need this parameter
           k: k is the number of iteration times
           Note that, n for line should be 2
           (more information can be found on the page 90 of slides "Image Features and Matching")
    :return: inlier_points_name, outlier_points_name
    inlier_points_name and outlier_points_name is two list, each element of them is str type.
    For example: If 'a','b' is inlier_points and 'c' is outlier_point.
    the output should be two lists of ['a', 'b'], ['c'].
    Note that, these two lists should be non-empty.
    """
    input_size = len(input_points)
    least_error_inliers = []
    least_error_outliers = []
    previous_pairs = []
    least_error = 10000
    permutations = input_size*(input_size-1)
    

    for i in range(k):
        # choose starting points
        if len(previous_pairs) >= permutations:
            break
        while True:
            starting_pts = random.sample(input_points, 2)
            if starting_pts not in previous_pairs:
                previous_pairs.append(starting_pts)
                break

        # compute the line that defines the given points
        dist_sq = [distance(*starting_pts, pt) for pt in input_points]

        error_total=0;
        inliers=[]
        outliers=[]
        
        for i,p in enumerate(input_points):
            if dist_sq[i]>t**2:
                outliers.append(p)
            else:
                inliers.append(p)
                error_total += dist_sq[i]
        if len(inliers)==2:
            mean_error =10000
        else:
            mean_error = error_total/(len(inliers)-2) #minus 2 for starting points
            

        if len(inliers) < d:
            continue

        if (mean_error < least_error or
                mean_error == least_error and len(inliers) > len(least_error_inliers)):
            least_error = mean_error
            least_error_outliers = outliers
            least_error_inliers = inliers
            
    return [n['name'] for n in least_error_inliers], [n['name'] for n in least_error_outliers] 
  


if __name__ == "__main__":
    input_points = [{'name': 'a', 'value': (0.0, 1.0)}, {'name': 'b', 'value': (2.0, 1.0)},
                    {'name': 'c', 'value': (3.0, 1.0)}, {'name': 'd', 'value': (0.0, 3.0)},
                    {'name': 'e', 'value': (1.0, 2.0)}, {'name': 'f', 'value': (1.5, 1.5)},
                    {'name': 'g', 'value': (1.0, 1.0)}, {'name': 'h', 'value': (1.5, 2.0)}]
    t = 0.5
    d = 3
    k = 100
    inlier_points_name, outlier_points_name = solution(input_points, t, d, k)  # TODO
    assert len(inlier_points_name) + len(outlier_points_name) == 8  
    f = open('./results/task1_result.txt', 'w')
    f.write('inlier points: ')
    for inliers in inlier_points_name:
        f.write(inliers + ',')
    f.write('\n')
    f.write('outlier points: ')
    for outliers in outlier_points_name:
        f.write(outliers + ',')
    f.close()


