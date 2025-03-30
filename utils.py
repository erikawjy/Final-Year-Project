import cv2

# load and preprocess the image
def preprocess_image(image, final_width=1280, final_height=720):
    """
    load image from path and convert to grayscale
    """
    resized_image = cv2.resize(image, (final_width, final_height))
    gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    return resized_image, gray_image

# subtract images
def subtract_images(image1, image2, binary_threshold=75):
    """
    does background substraction
    """
    abs_diff = cv2.absdiff(image1, image2)
    abs_diff_blurred = cv2.GaussianBlur(abs_diff, (5,5), 0)
    _, thresh_abs_diff = cv2.threshold(abs_diff_blurred, binary_threshold, 255, cv2.THRESH_BINARY)
    return abs_diff, thresh_abs_diff