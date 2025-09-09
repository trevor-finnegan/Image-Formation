import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

# Read in the image.
img = cv.imread('..\\images\\transformed_image.jpeg')
assert img is not None, "file could not be read, check with os.path.exists()"

# Get the images rows, columns 
rows,cols,ch = img.shape

# First step: Translate image back to original frame of view:
# --------------------------------------------------------
# Here, I try to move the board so its top-left corner is at the origin (0,0).
# I use a 2x3 translation matrix, T, which shift the pixels
# of the image 93 columns to the left and 20 rows up.
T = np.float32([
    [1,0,-93],  # 93 columns to left
    [0,1,-20]]) # 20 rows up

# I then use OpenCV's warpAffine function to apply this 
# transformation to every pixel:
translated_img = cv.warpAffine(img,T,(cols,rows))

# Second step: Affine transformation.
# --------------------------------------------------------
# Now that the top left of the board is aligned
# I can use a affine transformation. The transformed image
# seems to maintain parallelism, so an affine transformation
# should be able to reproduce the original. I simply need to change
# the parallelogram back into a square.
rows,cols,ch = translated_img.shape # Get the rows, columns, and color of the outputed matrix (translated_img)

# OpenCV allows us to get a affine transformation matrix by
# providing three points on the input matrix that we want to
# be mapped to three different points on the output matrix.
# I decided to choose the top left corner (which should stay in the same place),
# the top right corner of the board (181, 125), which will move to the top right 
# corner of the frame (371, 0), and the bottom left corner of the board, which will 
# to a point near the bottom left corner (not exactly the bottom left some of 
# the bottom of the image has been chopped off).
pts1 = np.float32([
    [0,0],      # Top left corner
    [137,350],  # Bottom left corner
    [181,125]]) # Top right corner
pts2 = np.float32([
    [0,0],       # Top left corner
    [0,360],     # Bottom left corner
    [371,0]])    # Top right corner

# This function will give us a affine transfomation matrix 
# based on the points we have provided above:
Matrix2 = cv.getAffineTransform(pts1,pts2)

# Apply the transformation:
new_img = cv.warpAffine(translated_img,Matrix2,(371,371))

# Now we plot three images: The tranformed image which we
# used as input, the attempted recreation of the original
# matrix we outputted, and the original image which we are
# trying to replicate:
original_img = cv.imread('..\\images\\original_image.jpeg') # Read in the original image.
h, w = img.shape[:2] # Get the images height and width

dpi = 371
figsize = (3 * w / dpi, h / dpi)  # 3 images side by side
plt.figure(figsize=figsize, dpi=dpi)

plt.subplot(1, 3, 1)
plt.imshow(cv.cvtColor(original_img, cv.COLOR_BGR2RGB))
plt.title('Original Image', fontsize=4)
plt.axis('off')

plt.subplot(1, 3, 2)
plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
plt.title('Transformed Image', fontsize=4)
plt.axis('off')

plt.subplot(1, 3, 3)
plt.imshow(cv.cvtColor(new_img, cv.COLOR_BGR2RGB))
plt.title('Reverse Engineered Image', fontsize=4)
plt.axis('off')

plt.tight_layout()
plt.show()