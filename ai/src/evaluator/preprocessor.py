import numpy as np
import cv2
import matplotlib.pyplot as plt
import skimage.filters.thresholding as th
import pythreshold.utils as putils
import imutils.contours
import json
from PyPDF2 import PdfReader, PdfWriter
from qreader import QReader
from deskew import determine_skew
from concurrent.futures import ThreadPoolExecutor

from ai.src.evaluator.pdf_rotator import load_pdf
from ai.src.utils import load_config, get_A4_size, get_max_num_of_rects_in_page, get_num_of_rects_per_page


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


def rotate_img(image, angle):
    h, w = image.shape[:2]
    cX, cY = (w//2, h//2)
    M = cv2.getRotationMatrix2D((cX, cY), angle, 1)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_LINEAR)
    return rotated


def map_pages_to_students(collection, path_to_pdf):
    # Load the configuration file
    config = load_config()

    pdf = load_pdf(path_to_pdf)

    # A4 paper size in inches
    A4 = get_A4_size()

    # Find the QR code
    qreader = QReader(model_size='s')
    index = 0
    first_page = pdf[index]
    decoded_text = qreader.detect_and_decode(image=first_page, return_detections=False)
    # If the first page has bad QR quality, try the next one
    while (len(decoded_text) == 1 and decoded_text[0] is None) and index < len(pdf):
        index += 1
        next_page = pdf[index]
        decoded_text = qreader.detect_and_decode(image=next_page, return_detections=False)

    # If no QR code was found at all, return None (handled from the caller)
    if len(decoded_text) == 1 and decoded_text[0] is not None:
        qr_json = json.loads(decoded_text[0])
    else:
        return None, None

    # Get the test ID from the QR code
    test_id = qr_json["test_id"]

    # Calculate the number of rectangles that can fit in the figure
    num_of_rects_per_page = get_max_num_of_rects_in_page(config, A4)

    # Number of questions
    num_of_q = collection.find_one({"test_id": test_id})["num_of_questions"]
    num_of_q_per_rect = config["answer_rect"]["grid"]["rows"]
    num_of_rect = int(np.ceil(num_of_q / num_of_q_per_rect))

    # Calculate the number of pages needed
    num_of_pages = int(np.ceil(num_of_rect / num_of_rects_per_page))
    num_of_rects_in_page = get_num_of_rects_per_page(num_of_rect, num_of_pages, num_of_rects_per_page)

    student_page_ids = {}

    def process_page(page, pdf_page_index, num_of_rects_in_page, qreader):
        skew_detect_img = page[:int(page.shape[0] * 0.5), :int(page.shape[1] * 0.5)]
        angle = determine_skew(skew_detect_img)
        if angle != 0:
            page = rotate_img(page, angle)

        student_id = []

        decoded_text = qreader.detect_and_decode(image=page, return_detections=False)
        if len(decoded_text) == 1 and decoded_text[0] is not None:
            qr_json = json.loads(decoded_text[0])
        else:
            # Just skip the bad QR quality page, no need to return an error, it will be handled later
            return None
        page_num = qr_json["page"]

        k = num_of_rects_in_page[page_num] + 1  # +1 for student id

        # Convert the image to grayscale and threshold it
        gray_filled = cv2.cvtColor(page, cv2.COLOR_RGB2GRAY)
        threshed_filled = threshold_otsu(gray_filled, 170)

        # Find the big boxes around the answer bubbles
        contours = find_contours(threshed_filled)
        # Pick k largest contours

        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:k]
        contours = imutils.contours.sort_contours(contours, method="left-to-right")[0]

        student_contour = contours[0]
        x, y, w, h = cv2.boundingRect(student_contour)

        # Throw away 1% of the border of the image
        diff = w // 100 if w > h else h // 100
        x += diff
        y += diff
        w -= 2 * diff
        h -= 2 * diff

        student_subimage = page[y:y + h, x:x + w]

        # Find contours of circles
        gray = cv2.cvtColor(student_subimage, cv2.COLOR_RGB2GRAY)
        threshed = threshold_otsu(gray, 170)
        contours = find_contours(threshed)

        # Threshold the subimage
        threshed_subimage = cv2.GaussianBlur(student_subimage, (5, 5), 0)
        threshed_subimage = threshold_mean(threshed_subimage)

        # Find specified number of circles
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        temp_contours = []
        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)
            temp_image = threshed_subimage[y:y + h, x:x + w]
            blurred = cv2.medianBlur(temp_image, 5)
            gray = cv2.cvtColor(blurred, cv2.COLOR_RGB2GRAY)
            circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=5, param2=10, minRadius=10)

            if circles is not None:
                temp_contours.append(contour)
                if len(temp_contours) == 40:
                    break
        contours = temp_contours

        # Sort them top to bottom, for easier processing
        contours = imutils.contours.sort_contours(contours, method="top-to-bottom")[0]

        while len(contours) < 40:
            contours = list(contours)
            contours.append(contours[-1])
            contours = tuple(contours)

        # Iterate over the circles
        for (q, j) in enumerate(np.arange(0, len(contours), 4)):
            # Sort the contours from left to right
            subcontours = imutils.contours.sort_contours(contours[j:j + 4])[0]
            # Create array for answers
            student_id.append([])

            # Iterate over the subcontours
            for bubble in subcontours:
                # Find the bounding box of the bubble
                (x, y, w, h) = cv2.boundingRect(bubble)

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
                    student_id[q].append(1)
                else:
                    student_id[q].append(0)

        detected_student_id = ''.join(str(column.index(1)) for column in zip(*student_id) if 1 in column)

        return detected_student_id, page_num, pdf_page_index

    with ThreadPoolExecutor() as executor:
        # Create a list of futures
        futures = [executor.submit(process_page, page, pdf_page_index, num_of_rects_in_page, qreader)
                   for pdf_page_index, page in enumerate(pdf)]

        for future in futures:
            if future.result() is None:  # Skip from the original code (here returned None)
                continue
            page_result = future.result()
            if page_result:
                detected_student_id, page_num, pdf_page_index = page_result
                if detected_student_id not in student_page_ids:
                    student_page_ids[detected_student_id] = [{page_num: pdf_page_index}]
                else:
                    student_page_ids[detected_student_id].append({page_num: pdf_page_index})

    # Sort the pages by the page_num key
    result_student_page_ids = {}
    for student_id, pages in student_page_ids.items():
        result_student_page_ids[student_id] = sorted(pages, key=lambda x: list(x.keys())[0])

    # Throw away page_num keys
    for student_id, pages in result_student_page_ids.items():
        result_student_page_ids[student_id] = [list(page.values())[0] for page in pages]

    return result_student_page_ids, test_id


def create_temp_pdfs(student_page_ids, path_to_pdf):
    pdf_names = []

    # Create sub pdfs for each student (group by student ID over pages)
    reader = PdfReader(path_to_pdf)
    for student_id, page_ids in student_page_ids.items():
        try:
            _ = int(student_id)
        except ValueError:
            continue

        writer = PdfWriter()
        for page_id in page_ids:
            writer.add_page(reader.pages[page_id])
        pdf_name = f"temp_{student_id}.pdf"
        writer.write(pdf_name)
        pdf_names.append(pdf_name)

    return pdf_names


def preprocess_image(collection, path_to_image, test_id):
    """
    Preprocess the image and detect filled bubbles
    :param collection: DB collection
    :param path_to_image: Path to the image
    :return: JSON output with student ID and answers
    """
    # Load the configuration file
    config = load_config()

    num_rows = config["answer_rect"]["grid"]["rows"]
    num_cols = config["answer_rect"]["grid"]["cols"]

    scanned_filled_images = load_pdf(path_to_image)

    # A4 paper size in inches
    A4 = get_A4_size()

    # Calculate the number of rectangles that can fit in the figure
    num_of_rects_per_page = get_max_num_of_rects_in_page(config, A4)

    # Number of questions
    num_of_q = collection.find_one({"test_id": test_id})["num_of_questions"]
    num_of_q_per_rect = config["answer_rect"]["grid"]["rows"]
    num_of_rect = int(np.ceil(num_of_q / num_of_q_per_rect))
    last_rect_q = num_of_q % num_of_q_per_rect

    # Calculate the number of pages needed
    num_of_pages = len(scanned_filled_images)

    # Calculate the number of rectangles in each page
    num_of_rects_in_page = get_num_of_rects_per_page(num_of_rect, num_of_pages, num_of_rects_per_page)
    num_of_rects_in_page_copy = num_of_rects_in_page.copy()

    # Create subimages from the big boxes
    subimages = []
    answers = []
    how_many_circles = []

    for indx, scanned_filled in enumerate(scanned_filled_images):
        # Number of circles in each subimage
        # Rows * Cols
        student_id_grid = config["student_id_rect"]["grid"]["rows"] * config["student_id_rect"]["grid"]["cols"]

        if indx == 0:
            answer_grid = [student_id_grid]
        else:
            answer_grid = []

        # Pick k largest contours
        k = num_of_rects_in_page_copy.pop(0) + 1  # +1 for student id

        max_grid = num_rows * num_cols
        answer_grid += [max_grid] * (k - 2)  # Previous bubble grids are always full

        if num_of_pages == indx + 1 and last_rect_q != 0:  # Last page
            answer_grid.append(last_rect_q * num_cols)
        else:
            answer_grid.append(num_rows * num_cols)

        how_many_circles += answer_grid

    num_of_rects_in_page_copy = num_of_rects_in_page.copy()
    first_k = 0
    for indx, scanned_filled in enumerate(scanned_filled_images):
        subimages.append([])

        skew_detect_img = scanned_filled[:int(scanned_filled.shape[0] * 0.5), :int(scanned_filled.shape[1] * 0.5)]
        angle = determine_skew(skew_detect_img)
        if angle != 0:
            scanned_filled = rotate_img(scanned_filled, angle)

        # Convert the image to grayscale and threshold it
        gray_filled = cv2.cvtColor(scanned_filled, cv2.COLOR_RGB2GRAY)
        threshed_filled = threshold_otsu(gray_filled, 170)

        # Find the big boxes around the answer bubbles
        contours = find_contours(threshed_filled)
        # Pick k largest contours
        k = num_of_rects_in_page_copy.pop(0) + 1  # +1 for student id
        if indx == 0:
            first_k = k

        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:k]
        contours = imutils.contours.sort_contours(contours, method="left-to-right")[0]

        # Iterate over the big boxes
        for i, contour in enumerate(contours):
            x, y, w, h = cv2.boundingRect(contour)

            # Throw away 1% of the border of the image
            diff = w // 100 if w > h else h // 100
            x += diff
            y += diff
            w -= 2 * diff
            h -= 2 * diff

            # Modify height based on the number of questions
            if indx == 0 and i == 0:  # Student ID grid
                pass
            else:
                max_circles = num_rows * num_cols
                actual_circles = how_many_circles[indx * (first_k - 1) + i]
                h = int(h * actual_circles / max_circles)

            subimage = scanned_filled[y:y + h, x:x + w]
            subimages[-1].append(subimage)

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

            # Threshold the subimage
            threshed_subimage = cv2.GaussianBlur(subimage, (5, 5), 0)
            threshed_subimage = threshold_mean(threshed_subimage)

            # Find specified number of circles
            contours = sorted(contours, key=cv2.contourArea, reverse=True)
            temp_contours = []
            for contour in contours:
                (x, y, w, h) = cv2.boundingRect(contour)
                temp_image = threshed_subimage[y:y + h, x:x + w]
                blurred = cv2.medianBlur(temp_image, 5)
                gray = cv2.cvtColor(blurred, cv2.COLOR_RGB2GRAY)
                circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=5, param2=10, minRadius=10)

                if circles is not None:
                    temp_contours.append(contour)
                    if len(temp_contours) == how_many_circles[i]:
                        break
            contours = temp_contours
            # Sort them top to bottom, for easier processing
            contours = imutils.contours.sort_contours(contours, method="top-to-bottom")[0]

            while len(contours) < how_many_circles[i]:
                contours = list(contours)
                contours.append(contours[-1])
                contours = tuple(contours)

            # Just for showcase purposes
            circle_image = cv2.drawContours(subimage.copy(), contours, -1, (0, 255, 0), 2)

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
