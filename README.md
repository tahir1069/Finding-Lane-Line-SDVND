# Finding-Lane-Line-SDVND
## Lane Detection

This project uses Canny Edge Detection, Hough Transforms and Moving Averages for extrapolation to identify and mark lane lines on a road.

This repo was written with the hope that it would be easy to understand for someone not farmiliar with the project.

How it works

### How it works
***
 The steps for the pipeline are as follow:

    1. Color Selection
    2. Region Masking
    3. Canny Edge Detection
    4. Hough Tranform
    5. Extrapolating Lines

#### Now running the code blocks step by step:
The code is largely self explanotary.
The code has two files:
#### 1. Lane_Line_Finding
Here in all functions are defined according to all the steps above. lane_lines is the main function which is called with given in an image as an input. This manages all other function callings.
#### 2. main_file
This is the main file in which Lane_Line_Finding Library is called. All of the code is self explanatry.
**Note: If, at any point, you encounter frozen display windows or other confounding issues, you can always start again with a clean slate by going to the "Kernel" menu above and selecting "Restart & Clear Output".**

---


Requirements

    numpy
    matplotlib
    opencv
    python3
    imageio

Thank you to the Udacity mentors for the learning resources
