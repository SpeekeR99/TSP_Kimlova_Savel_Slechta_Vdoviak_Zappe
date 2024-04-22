import fitz
import numpy as np
import cv2


def load_pdf(file_path):
    """
    Load pdf file and return list of images
    If nessesary, rotate images
    :param file_path: Path to pdf file
    :return: List of (rotated) images
    """
    pdf = fitz.open(file_path)
    images = []
    for page_num in range(len(pdf)):  # Iterate over all pages
        page = pdf[page_num]
        image = page.get_pixmap(dpi=300)
        if image.h > image.w:
            image = np.frombuffer(image.samples, dtype=np.uint8).reshape(image.h, image.w, 3)  # Convert to numpy array
            image = np.rot90(image) # Rotate image 90 degrees
        else:
            image = np.frombuffer(image.samples, dtype=np.uint8).reshape(image.h, image.w, 3)
        # Check if there is a rectangle in the top right corner
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)[1]
        height, width, _ = image.shape
        rect = gray[:int(height*0.1), int(width*0.9):]
        # find rectangular contours
        contours, _ = cv2.findContours(
            rect, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        rotate = True
        for contour in contours[1:]:
            approx = cv2.approxPolyDP( # Approximate polygonal curves with a specific precision
                contour, 0.01 * cv2.arcLength(contour, True), True)
            if len(approx) == 4:
                rotate = False
        if rotate:
            image = np.rot90(image, 2)  # Rotate image 180 degrees

        images.append(image)
    return images