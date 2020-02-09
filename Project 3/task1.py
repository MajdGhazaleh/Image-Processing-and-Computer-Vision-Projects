"""
K-Means Segmentation Problem
(Due date: Nov. 25, 11:59 P.M., 2019)
The goal of this task is to segment image using k-means clustering.

Do NOT modify the code provided to you.
Do NOT import ANY library or API besides what has been listed.
Hint: 
Please complete all the functions that are labeled with '#to do'. 
You are allowed to add your own functions if needed.
You should design you algorithm as fast as possible. To avoid repetitve calculation, you are suggested to depict clustering based on statistic histogram [0,255]. 
You will be graded based on the total distortion, e.g., sum of distances, the less the better your clustering is.
"""


import utils
import numpy as np
import json
import time

class Center():
    def __init__(self, value):
        self.value = value
        self.sum = 0
        self.points_count = 0

    def add(self, val, quantity):
        self.sum += val * quantity
        self.points_count += quantity

    def reset(self):
        self.sum = 0
        self.points_count = 0

    def eval_center(self):
        if self.points_count == 0:
            return
        self.value = int(self.sum / self.points_count)



def closest_center(pixel, centers):
    closest = centers[0]
    index = 0
    for i in range(1, len(centers)):
        if abs(pixel - centers[i].value) < abs(pixel - closest.value):
            closest = centers[i]
            index = i
    return closest, index



def kmeans(img, k):
    """
    Implement kmeans clustering on the given image.
    Steps:
    (1) Random initialize the centers.
    (2) Calculate distances and update centers, stop when centers do not change.
    (3) Iterate all initializations and return the best result.
    Arg: Input image;
         Number of K. 
    Return: Clustering center values;
            Clustering labels of all pixels;
            Minimum summation of distance between each pixel and its center.  
    """
    # TODO: implement this function.
    img_height, img_width = np.shape(img)
    min_intensity = np.amin(img)
    max_intensity = np.amax(img)
    histo_map = {}
    for row in img:
        for pixel in row:
            val = histo_map.get(pixel)
            if val is None:
                histo_map[pixel] = 0
            histo_map[pixel] += 1
            
    # Randomly initialize centers
    centers = []
    partitions = (max_intensity - min_intensity) // k
    for j in range(k):
        low = min_intensity + (j * partitions)
        hi = low + partitions
        c = np.random.randint(low,hi+1)
        centers.append(Center(c))
        
    # Update center locations 
    while True:
        old_vals = [c.value for c in centers]
        for intensity, count in histo_map.items():
            closest, _ = closest_center(intensity, centers)
            closest.add(intensity, count)
        for center in centers:
            center.eval_center()
            center.reset()  # Reset sum and point count for next iteration
        new_vals = [c.value for c in centers]
    
        if old_vals == new_vals:
                break       


    # Find closest center for each pixel and calculate total inner-cluster distance    
    distance_sum = 0
    labels = np.zeros((img_height, img_width), dtype=np.uint8)
    for i in range(img_height):
        for j in range(img_width):
            closest, index = closest_center(img[i, j], centers)
            labels[i, j] = index
            distance_sum += int(abs(img[i, j] - closest.value))
    

    center_vals = [c.value for c in centers]
    return center_vals, labels, distance_sum



def visualize(centers,labels):
    """
    Convert the image to segmentation map replacing each pixel value with its center.
    Arg: Clustering center values;
         Clustering labels of all pixels. 
    Return: Segmentation map.
    """
    # TODO: implement this function.

    height, width = np.shape(labels)
    seg_map = np.zeros((height, width), dtype = np.uint8)
    for i in range(height):
        for j in range(width): 
            seg_map[i, j] = centers[labels[i, j]]
    return seg_map
    
     
if __name__ == "__main__":
    img = utils.read_image('lenna.png')
    k = 2

    start_time = time.time()
    centers, labels, sumdistance = kmeans(img,k)
    result = visualize(centers, labels)
    end_time = time.time()

    running_time = end_time - start_time
    print(running_time)

    centers = list(centers)
    with open('results/task1.json', "w") as jsonFile:
        jsonFile.write(json.dumps({"centers":centers, "distance":sumdistance, "time":running_time}))
    utils.write_image(result, 'results/task1_result.jpg')
