"""
Image Stitching Problem
(Due date: Oct. 23, 3 P.M., 2019)
The goal of this task is to stitch two images of overlap into one image.
To this end, you need to find feature points of interest in one image, and then find
the corresponding ones in another image. After this, you can simply stitch the two images
by aligning the matched feature points.
For simplicity, the input two images are only clipped along the horizontal direction, which
means you only need to find the corresponding features in the same rows to achieve image stiching.

Do NOT modify the code provided to you.
You are allowed use APIs provided by numpy and opencv, except “cv2.findHomography()” and
APIs that have “stitch”, “Stitch”, “match” or “Match” in their names, e.g., “cv2.BFMatcher()” and
“cv2.Stitcher.create()”.
"""
import cv2
import numpy as np



def solution(left_img, right_img):
    """
    :param left_img:
    :param right_img:
    :return: you need to return the result image which is stitched by left_img and right_img
    """
    #get grayscale images
    right_img_gray = cv2.cvtColor(right_img, cv2.COLOR_BGR2GRAY)
    left_img_gray = cv2.cvtColor(left_img, cv2.COLOR_BGR2GRAY)

    #find keypoints and descriptors for a gray image with sift
    sift = cv2.xfeatures2d.SIFT_create()
    kp_right, d1 = sift.detectAndCompute(right_img_gray, None)
    
    sift = cv2.xfeatures2d.SIFT_create()
    kp_left, d2 = sift.detectAndCompute(left_img_gray, None)
    
    #finds the best matches in two lists of feature descriptors  
    bf=cv2.BFMatcher()
    matches = bf.knnMatch(d1, d2, k=2)
    matches = np.asarray([m for m in matches if m[0].distance < 0.5 * m[1].distance])
    # threshold distance between 2 feature points = 0.5
    

    # coordinates  in the original image plane
    source = np.float32([kp_right[m.queryIdx].pt for m in matches[:,0]]).reshape(-1,1,2)

    # coordinates in the target image plane
    target = np.float32([kp_left[m.trainIdx].pt for m in matches[:,0]]).reshape(-1,1,2)

    H, _ = cv2.findHomography(source, target, cv2.RANSAC, 5.0)
    #  threshold distance between 2 points for  RANSAC = 5.0

    # warp right image to target image plane
    result = cv2.warpPerspective(right_img, H, (left_img.shape[1] + right_img.shape[1], left_img.shape[0]))

    # stitch the two images together
    result[0:left_img.shape[0], 0: left_img.shape[1]] = left_img
    
    return result


    #raise NotImplementedError

if __name__ == "__main__":
    left_img = cv2.imread('left.jpg')
    right_img = cv2.imread('right.jpg')
    result_image = solution(left_img, right_img)
    cv2.imwrite('results/task2_result.jpg',result_image)


