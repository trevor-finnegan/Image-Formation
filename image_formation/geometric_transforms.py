import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

# Read in the original image and make sure the file exists
img = cv.imread('..\\images\\original_image.jpg')
assert img is not None, "file could not be read"

# Get the images rows, columns (first two values returned by img.shape)
rows,cols = img.shape[1:]

# Method for reverse engineering: affine transformation.
# --------------------------------------------------------
# The transformed image seems to maintain parallelism, so an 
# affine transformation should be able to reproduce the original:

# OpenCV allows us to get a affine transformation matrix by
# providing three points on the input matrix that we want to
# be mapped to three different points on the output matrix.
# I decided to choose the top left corner of the board, 
# the top right corner of the board, and a point within the 
# board (I chose the corner of one of the black boxes)

# Points from original image
pts1 = np.float32([
    [0,0],          # Top left corner
    [1200,0],       # Top right corner
    [492,285]])     # Point within the grid

# Points from transformed image
pts2 = np.float32([
    [300,60],       # Top left corner
    [888,471],      # Top right corner
    [654,517]])     # Point within the grid

# This function will give us a 2x3 affine transfomation 
# matrix based on the points we have provided above:
Matrix2 = cv.getAffineTransform(pts1, pts2)

# Apply the transformation:
print(f"Applying one, all-encompassing affine transformation")
print("------------------------------------------------------")
print("This affine transformation matrix, as seen below, applies " \
      "a translation of tx = +300 and ty = +60 as well as a general" \
      "affine transformation which warps the original square into a non-square parallelogram:")
print(Matrix2)
print("------------------------------------------------------")
new_img = cv.warpAffine(img, Matrix2, (1200, 1200))

# Now we plot three images: The tranformed image which we
# used as input, the attempted recreation of the original
# matrix we outputted, and the original image which we are
# trying to replicate:
transformed_img = cv.imread('..\\images\\transformed_image.jpg') # Read in the transformed image.
h, w = img.shape[:2] # Get the images height and width (needed for plotting)

plt.figure(figsize=(10, 4), dpi = 100)

# Original image
plt.subplot(1, 3, 1)
plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
plt.title('Original Image', fontsize=12)
plt.axis('off')

# Transformed image
plt.subplot(1, 3, 2)
plt.imshow(cv.cvtColor(transformed_img, cv.COLOR_BGR2RGB))
plt.title('Transformed Image', fontsize=12)
plt.axis('off')

# Reverse engineered image
plt.subplot(1, 3, 3)
plt.imshow(cv.cvtColor(new_img, cv.COLOR_BGR2RGB))
plt.title('Reverse Engineered Image', fontsize=12)
plt.axis('off')

plt.tight_layout()
plt.show()