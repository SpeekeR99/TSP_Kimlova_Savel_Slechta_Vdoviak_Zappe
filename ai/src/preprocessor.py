import json

import numpy as np
import cv2
import matplotlib.pyplot as plt
import skimage.filters.thresholding as th
import pythreshold.utils as putils
import imutils.contours
from utils import load_config
from pdf_rotator import load_pdf


def show_images(titles, images):
    """
    Display images in a row with titles
    :param titles: List of titles
    :param images: List of images
    """
    fig, axs = plt.subplots(1, len(images), figsize=(len(images) * 10, 10))
    fig.tight_layout()
    if len(images) == 1:
        axs = [axs]
    for ax, title, image in zip(axs, titles, images):
        ax.imshow(image, cmap="gray" if len(image.shape) == 2 else None)
        ax.set_title(title)
        ax.axis("off")
    plt.show()


def threshold_otsu(image, threshold=170):
    """
    Apply OTSU thresholding to the image
    :param image: Grayscale image
    :param threshold: Threshold value
    :return: Thresholded image
    """
    _, threshed = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return threshed


def threshold_to_zero(image, threshold=170):
    """
    Apply thresholding to zero to the image
    :param image: Grayscale image
    :param threshold: Threshold value
    :return: Thresholded image
    """
    _, threshed = cv2.threshold(image, threshold, 255, cv2.THRESH_TOZERO)
    return cv2.bitwise_not(threshed)


def threshold_yen(image):
    """
    Apply Yen thresholding to the image
    :param image: Grayscale image
    :return: Thresholded image
    """
    thresh = th.threshold_yen(image)
    threshed = putils.apply_threshold(image, thresh)
    return cv2.bitwise_not(np.array(threshed, dtype=np.uint8))


def threshold_mean(image):
    """
    Apply mean thresholding to the image
    :param image: Grayscale image
    :return: Thresholded image
    """
    thresh = th.threshold_mean(image)
    threshed = putils.apply_threshold(image, thresh)
    return cv2.bitwise_not(np.array(threshed, dtype=np.uint8))


def threshold_kapur(image):
    """
    Apply Kapur thresholding to the image
    :param image: Grayscale image
    :return: Thresholded image
    """
    th = putils.kapur_threshold(image)
    threshed = putils.apply_threshold(image, th)
    return cv2.bitwise_not(threshed)


def find_contours(image):
    """
    Find contours in the image
    :param image: Thresholded image
    :return: List of contours
    """
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def find_edges(image):
    """
    Find edges in the image
    :param image: Grayscale image
    :return: Edges
    """
    edges = cv2.Canny(image, 100, 200)
    return edges


def preprocess_image(path_to_image):
    """
    Preprocess the image and detect filled bubbles
    :param path_to_image: Path to the image
    :return: JSON output with student ID and answers
    """

    # Load the configuration file
    config = load_config()

    num_rows = config["answer_rect"]["grid"]["rows"]
    num_cols = config["answer_rect"]["grid"]["cols"]

    scanned_filled_images = load_pdf(path_to_image)

    # A4 paper size in inches
    cm = 1 / 2.54  # Centimeters in inches
    A4 = (29.7 * cm, 21.0 * cm)

    # Offset between rectangles
    offset_between_rect = config["rect_settings"]["rect_space_between"]

    # Number of questions
    num_of_q = config["number_of_questions"]
    num_of_q_per_rect = config["answer_rect"]["grid"]["rows"]
    num_of_rect = int(np.ceil(num_of_q / num_of_q_per_rect))
    last_rect_q = num_of_q % num_of_q_per_rect

    # Calculate the number of rectangles that can fit in the figure
    num_of_rects_per_page = 0
    aspect_ratio = A4[0] / A4[1]
    width_so_far = config["student_id_rect"]["width"] + 2 * offset_between_rect  # Every page has student ID field

    while width_so_far < aspect_ratio - config["answer_rect"]["width"] - 1.5 * offset_between_rect:
        width_so_far += config["answer_rect"]["width"] + 1.5 * offset_between_rect
        num_of_rects_per_page += 1

    # Calculate the number of pages needed
    num_of_pages = len(scanned_filled_images)

    # Calculate the number of rectangles in each page
    num_of_rects_in_page = []
    for page in range(num_of_pages):
        if page == num_of_pages - 1 and last_rect_q != 0 and num_of_rect % num_of_rects_per_page != 0:
            num_of_rects_in_page.append(num_of_rect % num_of_rects_per_page)
        else:
            num_of_rects_in_page.append(num_of_rects_per_page)


    # Create subimages from the big boxes
    subimages = []
    answers = []
    how_many_circles = []
    for indx, scanned_filled in enumerate(scanned_filled_images):
        subimages.append([])
        # Convert the image to grayscale and threshold it
        gray_filled = cv2.cvtColor(scanned_filled, cv2.COLOR_RGB2GRAY)
        threshed_filled = threshold_otsu(gray_filled, 170)

        # Find the big boxes around the answer bubbles
        contours = find_contours(threshed_filled)
        # Pick k largest contours
        k = num_of_rects_in_page.pop(0) + 1  # +1 for student id
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:k]
        contours = imutils.contours.sort_contours(contours, method="left-to-right")[0]

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)

            # Throw away 1% of the border of the image
            diff = w // 100 if w > h else h // 100
            x += diff
            y += diff
            w -= 2 * diff
            h -= 2 * diff

            subimage = scanned_filled[y:y + h, x:x + w]
            subimages[-1].append(subimage)

        # Number of circles in each subimage
        student_id_grid = config["student_id_rect"]["grid"]["rows"] * config["student_id_rect"]["grid"][
            "cols"]  # rows * cols
        if indx == 0:
            answer_grid = [student_id_grid]
        else:
            answer_grid = []
        max_grid = num_rows * num_cols
        answer_grid += [max_grid] * (k - 2)  # previous bubble grids are always full
        if num_of_pages == indx + 1 and last_rect_q != 0: # last page
            answer_grid.append(last_rect_q * num_cols)
        else:
            answer_grid.append(num_rows * num_cols)

        how_many_circles += answer_grid
    # For each big box
    for page in range(num_of_pages):
        for s in range(len(subimages[page])):
            subimage = subimages[page][s]
            i = page * num_of_rects_per_page + s
            # Skip the student ID grid for every page except the first one
            if page != 0 and s == 0:
                continue
            # Create array for answers
            answers.append([])

            # Find contours of circles
            gray = cv2.cvtColor(subimage, cv2.COLOR_RGB2GRAY)
            threshed = threshold_otsu(gray, 170)
            contours = find_contours(threshed)
            # Find specified number of circles
            contours = sorted(contours, key=cv2.contourArea, reverse=True)[:how_many_circles[i]]
            # Sort them top to bottom, for easier processing
            contours = imutils.contours.sort_contours(contours, method="top-to-bottom")[0]

            # Just for showcase purposes
            circle_image = cv2.drawContours(subimage.copy(), contours, -1, (0, 255, 0), 2)

            # Threshold the subimage
            threshed_subimage = cv2.GaussianBlur(subimage, (5, 5), 0)
            threshed_subimage = threshold_mean(threshed_subimage)

            if i != 0:
                num_col = num_cols  # it is an answer grid
            else:
                num_col = config["student_id_rect"]["grid"]["cols"]  # it is a student id grid

            # Iterate over the circles
            for (q, j) in enumerate(np.arange(0, len(contours), num_col)):
                # Sort the contours from left to right
                subcontours = imutils.contours.sort_contours(contours[j:j + num_col])[0]
                # Create array for answers
                answers[i].append([])

                # Iterate over the subcontours
                for bubble in subcontours:
                    # Find the bounding box of the bubble
                    (x, y, w, h) = cv2.boundingRect(bubble)

                    # Just for showcase purposes
                    cv2.rectangle(circle_image, (x, y), (x + w, y + h), (255, 0, 0), 2)

                    # Find the bubble subimage and convert it to grayscale
                    bubble_subimage = threshed_subimage[y:y + h, x:x + w]
                    one_channel = cv2.cvtColor(bubble_subimage, cv2.COLOR_RGB2GRAY)
                    # Close the image using morphological operations
                    closed = cv2.morphologyEx(one_channel, cv2.MORPH_CLOSE,
                                              cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))

                    # Count the number of white pixels and the total number of pixels
                    pixels = cv2.countNonZero(closed)
                    num_pixels = w * h

                    # We found out that the circle often takes up around 40-50% of the area
                    # So if the whole area is at least 75% filled, the student probably tried to at least fill the circle
                    if pixels > 0.75 * num_pixels:
                        answers[i][q].append(1)
                    else:
                        answers[i][q].append(0)

            # Show the images (just for showcase purposes)
            # show_images([f'subimage{i + 1}', f'threshed_subimage{i + 1}', f'circle_image{i + 1}'],
            #             [subimage, threshed_subimage, circle_image])

    output = {"student_id": ''.join(str(column.index(1)) for column in zip(*answers[0]) if 1 in column),
              "answers": [item for sublist in answers[1:] for item in sublist]}

    return output
