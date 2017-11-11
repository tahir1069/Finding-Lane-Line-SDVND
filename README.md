# Project: **Finding Lane Lines on the Road** 
***
## Overview
When we drive a car, we use our eyes to see on the road. One of the first thing we need to drive is to keep track of lane lines on the road. Coming up to self-driving cars or driving assistance systems we need the system should track the lane lines to stay on its track. 
Our job is to teach the car how to drive itself in order to do that we have to teach the car how to perceive the world around it now when we drive we figure out how fast to drive where the lane lines are? And where to turn?  
The goals steps of this project are the following:

•	Make a pipeline that finds lane lines on the road

A car doesn’t have eyes but in self-driving cars we use cameras and other sensors to achieve a similar function. Now let’s see what the cameras sees around them. We can see the things automatically. So here our goal is to teach the car to identify and track the position of the lane lines in a series of images.
Here are some of the features we can identify on the road in order to find lane lines on the road: 

•	Color

•	Shape

•	Orientation 

•	Position in Image
<figure>
 <img src="Original_Image_1.png" width="380" alt="Combined Image" />
 <figcaption>
 <p></p> 
 <p style="text-align: center;"> This is a sample image to detect road lines on. </p> 
</figcaption>

## Color Selection
 
For starting point, now Let’s try finding the lane lines using the color. The lane lines are usually white. To select a color, We actually sees, need to identify what it means in digital image. In digital domain images are made up of stack of three images: 

•	Red 

•	Green 

•	Blue
<figure>
 <img src="RGB Image.png" width="380" alt="Combined Image" />
 <figcaption>
 <p></p> 
 <p style="text-align: center;">RGB Image</p> 
 </figcaption>
The images are sometime called color channels. Each of these color have values from 0-255 where 0 is the darkest possible value and 255 is the brightest possible values. If zero is dark and brightest is 255 than white will be [255,255,255]. Now getting this we define threshold for RGB image for white.
<figure>
 <img src="Color Selection.png" width="380" alt="Combined Image" />
 <figcaption>
 <p></p> 
 <p style="text-align: center;">RGB Image after Color Thresholding</p> 
 </figcaption>
Now let’s focus on the region of the image which interests us. Namely the regions where the lane lines are. In this case we can assume the camera is mounted in front of the image and it took the image and region stays the same for every single image taken.
<figure>
 <img src="Masking.png" width="380" alt="Combined Image" />
 <figcaption>
 <p></p> 
 <p style="text-align: center;"> Masking the image to get some region of interest</p> 
</figcaption>
Now we've seen how to mask out a region of interest in an image. Next, let's combine the mask and color selection to pull only the lane lines out of the image.
<figure>
 <img src="Color Selection and Masking.png" width="380" alt="Combined Image" />
 <figcaption>
 <p></p> 
 <p style="text-align: center;"> Color Selction and Masking Combined</p> 
 </figcaption>
As it happens, lane lines are not always the same color, and even lines of the same color under different lighting conditions (day, night, etc.) may fail to be detected by our simple color selection.
What we need is to take our algorithm to the next level to detect lines of any color using sophisticated computer vision methods.
We will be using Python with OpenCV for computer vision work. OpenCV stands for Open-Source Computer Vision. 
*You can download the files following instructions at the end of this document.
<figure>
 <img src="OpenCV and Python.png" width="380" alt="Combined Image" />
 <figcaption>
 <p></p> 
 <p style="text-align: center;"> </p> 
 </figcaption>
OpenCV contains extensive libraries of functions that you can use. The OpenCV libraries are well documented, so if you’re ever feeling confused about what the parameters in a particular function are doing, or anything else, you can find a wealth of information at opencv.org.

With edge detection our goal is to identify the boundaries of an image. So to do that first we convert to gray scale. And next we compute the gradient. In gradients the brightness of each pixels corresponds to the strength of the gradient at that point we will define edges by tracing out the pixels that follows the strongest gradient. By identifying edges we can even more easily detect object with their shapes.
<figure>
 <img src="Original Image 2.png" width="380" alt="Combined Image" />
 <figcaption>
 <p></p> 
 <p style="text-align: center;"> Example Image</p> 
</figcaption>
<figure>
 <img src="Gray_Scale.png" width="380" alt="Combined Image" />
 <figcaption>
 <p></p> 
 <p style="text-align: center;"> Gray Scale</p> 
 </figcaption>
<figure>
 <img src="Gradient.png" width="380" alt="Combined Image" />
 <figcaption>
 <p></p> 
 <p style="text-align: center;"> Gradient Image</p> 
 </figcaption>
After doing edge detection the function gives edges in the form of dots. And these dots represents edges. Now it’s time to connect the dots. We could connect the dots with any kind of shapes in the image. For in this case we are interested in lane lines. To find lines we need to adapt a model of a line to the assortment of dots in our edge detected image keeping in mind image is a mathematical function we can apply equation of line.
