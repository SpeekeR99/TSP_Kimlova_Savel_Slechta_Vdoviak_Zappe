import numpy as np
import cv2
import matplotlib.pyplot as plt
import fitz
import skimage.filters.thresholding as th
import pythreshold.utils as putils
import imutils.contours
from ai.src.utils import load_config



def load_pdf(file_path):
    """
    Load pdf file and return list of images
    :param file_path: Path to pdf file
    :return: List of images
    """
    pdf = fitz.open(file_path)
    images = []
    for page_num in range(len(pdf)):  # Iterate over all pages
        page = pdf[page_num]
        image = page.get_pixmap(dpi=300)
        image = np.frombuffer(image.samples, dtype=np.uint8).reshape(image.h, image.w, 3)  # Convert to numpy array
        images.append(image)
    return images


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

    # Load the configuration file
    config = load_config()

    scanned_filled = load_pdf(path_to_image)[0]
    gray_filled = cv2.cvtColor(scanned_filled, cv2.COLOR_RGB2GRAY)
    threshed_filled = threshold_otsu(gray_filled, 170)

    # Find the big boxes around the answer bubbles
    contours = find_contours(threshed_filled)
    # Pick k largest contours
    k = np.ceil(config["number_of_questions"]/config["answer_rect"]["grid"]["rows"]).astype(int) + 1
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:k]

    # Create subimages from the big boxes
    subimages = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        # Throw away 1% of the border of the image
        diff = w // 100 if w > h else h // 100
        x += diff
        y += diff
        w -= 2 * diff
        h -= 2 * diff

        subimage = scanned_filled[y:y+h, x:x+w]
        subimages.append(subimage)

    # Detect filled bubbles
    answers = []

    # Number of circles in each subimage
    # TODO: this will probably be redone with a configure file in the future (connect to generator)
    num_questions = config["number_of_questions"]
    num_rows = config["answer_rect"]["grid"]["rows"]
    num_cols = config["answer_rect"]["grid"]["cols"]

    max_grid = num_rows * num_cols
    answer_grid = [max_grid] * (k-2)
    answer_grid.append(np.ceil(config["number_of_questions"] % config["answer_rect"]["grid"]["rows"]).astype(int) * config["answer_rect"]["grid"]["cols"])
    student_id_grid = config["student_id_rect"]["grid"]["rows"] * config["student_id_rect"]["grid"]["cols"]
    answer_grid.append(student_id_grid)
    print(answer_grid)
    how_many_circles = [100, 100, 100, 40]

    # For each big box
    for i, subimage in enumerate(subimages):
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

        # TODO: this will probably be redone with a configure file in the future (connect to generator)
        # But for now, ID has 4 columns, but answers have 5 columns
        if i != len(subimages) - 1:
            num_col = 5
        else:
            num_col = 4

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
                cv2.rectangle(circle_image, (x, y), (x+w, y+h), (255, 0, 0), 2)

                # Find the bubble subimage and convert it to grayscale
                bubble_subimage = threshed_subimage[y:y+h, x:x+w]
                one_channel = cv2.cvtColor(bubble_subimage, cv2.COLOR_RGB2GRAY)
                # Close the image using morphological operations
                closed = cv2.morphologyEx(one_channel, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))

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
        show_images([f'subimage{i+1}', f'threshed_subimage{i+1}', f'circle_image{i+1}'], [subimage, threshed_subimage, circle_image])
        # Print the answers (just for showcase purposes)
        print(answers[i])


IMG_FOLDER = "../tsp_zaznamove_archy"
INPUT_FILE = "naskenovany_vyplneny.pdf"
preprocess_image(f"{IMG_FOLDER}/{INPUT_FILE}")