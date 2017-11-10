#%%
#importing some useful packages
import numpy as np
import cv2
#import math
#%matplotlib inline
#%%
def grayscale(img):
    """Applies the Grayscale transform
    This will return an img with only one color channel
    but NOTE: to see the returned img as grayscale
    you should call plt.imshow(gray, cmap='gray')"""
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # Or use BGR2GRAY if you read an img with cv2.imread()
    # return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#%%    
def canny(img, low_threshold, high_threshold):
    """Applies the Canny transform"""
    return cv2.Canny(img, low_threshold, high_threshold)
#%%
def gaussian_blur(img, kernel_size):
    """Applies a Gaussian Noise kernel"""
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)
#%%
def RoI(img, vertices):
    """
    Applies an img mask.
    Only keeps the region of the img defined by the polygon
    formed from `vertices`. The rest of the img is set to black.
    """
#defining a blank mask to start with
    mask = np.zeros_like(img)   
#defining a 3 channel or 1 channel color to fill the mask with depending on the input img
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your img
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255
    #filling pixels inside the polygon defined by "vertices" with the fill color    
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    #returning the img only where mask pixels are nonzero
    masked_img = cv2.bitwise_and(img, mask)
    return masked_img
#%%
def draw_lines(img, lines, color=[255, 0, 0], thickness=10):
    """
    NOTE: this is the function you might want to use as a starting point once you want to 
    average/extrapolate the line segments you detect to map out the full
    extent of the lane (going from the result shown in raw-lines-example.mp4
    to that shown in P1_example.mp4).  
    Think about things like separating line segments by their 
    slope ((y2-y1)/(x2-x1)) to decide which segments are part of the left
    line vs. the right line.  Then, you can average the position of each of 
    the lines and extrapolate to the top and bottom of the lane.
    This function draws `lines` with `color` and `thickness`.    
    Lines are drawn on the img inplace (mutates the img).
    If you want to make the lines semi-transparent, think about combining
    this function with the weighted_img() function below
    """
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), color, thickness)
#%%
def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    """
    `img` should be the output of a Canny transform.
    Returns an img with hough lines drawn.
    """
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    line_img = np.zeros((*img.shape, 3), dtype=np.uint8)
    draw_lines(line_img, lines)
    return line_img
#%%
# Python 3 has support for cool math symbols.
def weighted_img(img, initial_img, α=0.8, β=1., λ=0):
    """
    `img` is the output of the hough_lines(), An img with lines drawn on it.
    Should be a blank img (all black) with lines drawn on it.
    `initial_img` should be the img before any processing.
    The result img is computed as follows:
        initial_img * α + img * β + λ
        NOTE: initial_img and img must be the same shape!
    """
    return cv2.addWeighted(initial_img, α, img, β, λ)
#%%
#Removing outlier slopes from the averaging performed below in lane_lines
def remove_outliers(slopes, m = 2):
    med = np.mean(slopes)
    stand_dev = np.std(slopes)
    for slope in slopes:
        if abs(slope - med) > (m * stand_dev):
           slopes.remove(slope)
    return slopes
#%%
def extrapolaing_lines(line_img, lines):
    left_lines = []
    left_slopes = []
    right_lines = []
    right_slopes = []
    for line in lines:
            for x1,y1,x2,y2 in line:
                slope = (y2-y1)/(x2-x1)
                if slope < 0:
                    left_lines.append(line)
                    left_slopes.append(slope)
                else:
                    right_lines.append(line)
                    right_slopes.append(slope)
        
    #Average line positions
    avg_left_pos = [sum(col)/len(col) for col in zip(*left_lines)]
    avg_right_pos = [sum(col)/len(col) for col in zip(*right_lines)]
    
    #Remove slope outliers, and take the average
    avg_left_slope = np.mean(remove_outliers(left_slopes))
    avg_right_slope = np.mean(remove_outliers(right_slopes))
    
    #Extrapolate to our mask boundaries - up to 325, down to 539
    avg_left_line = []
    for x1,y1,x2,y2 in avg_left_pos:
        x = int(np.mean([x1, x2])) #Midpoint x
        y = int(np.mean([y1, y2])) #Midpoint y
        slope = avg_left_slope
        b = -(slope * x) + y #Solving y=mx+b for b
        avg_left_line = [int((325-b)/slope), 325, int((539-b)/slope), 539] #Line for the img 
    
    #Same thing for the right side
    avg_right_line = []
    for x1,y1,x2,y2 in avg_right_pos:
        x = int(np.mean([x1, x2]))
        y = int(np.mean([y1, y2]))
        slope = avg_right_slope
        b = -(slope * x) + y
        avg_right_line = [int((325-b)/slope), 325, int((539-b)/slope), 539]
    
    lines = [[avg_left_line], [avg_right_line]]
    
    draw_lines(line_img, lines)
    return line_img

    # Transparent lines
#%%
#Importing the imgs, and let's take a look at what we have!
#The below function tries to combine the helper functions as necessary
#Gray-scale, smoothing, canny edge, masking, hough-transform
#Then take the resulting lines and slopes, remove outliers
#Finally, extrapolate the lines based on the average slope and midpoint of the average lane line on each side
def lane_lines(img):
    #Gray-scale it
    gray = grayscale(img)
    
    #Smooth it a bit with Gaussian Blur
    kernel_size = 9
    blur_gray = gaussian_blur(gray, kernel_size)
    
    #Add in the canny edge detection
    low_threshold = 90
    high_threshold = 180
    edges = canny(blur_gray, low_threshold, high_threshold)
    
    # Now the masking
    imshape = img.shape
    vertices = np.array([[(0,imshape[0]),(450, 325), (550, 325), (imshape[1],imshape[0])]], dtype=np.int32)  
    masked_edges = RoI(edges, vertices)

    # Define the Hough transform parameters
    # Make a blank the same size as our img to draw on
    rho = 5 # distance resolution in pixels of the Hough grid
    theta = np.pi/30 # angular resolution in radians of the Hough grid
    threshold = 50     # minimum number of votes (intersections in Hough grid cell)
    min_line_len = 25 #minimum number of pixels making up a line
    max_line_gap = 25    # maximum gap in pixels between connectable line segments

    # Run Hough on edge detected img
    # Output "lines" is an array containing endpoints of detected line segments
    lines = cv2.HoughLinesP(masked_edges, rho, theta, threshold, np.array([]), min_line_len, max_line_gap)
    #Make lists of the lines and slopes for averaging        
    line_img = np.copy(img)*0 # creating a blank to draw lines on

    extrapolaing_lines(line_img, lines)
    line_edges = weighted_img(img = line_img, initial_img = img, α=0.8, β=1, λ=0)
    
    return line_edges
