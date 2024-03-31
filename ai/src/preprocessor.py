import numpy as np
import cv2
import matplotlib.pyplot as plt
import fitz
import skimage.filters.thresholding as th
import pythreshold.utils as putils
import imutils.contours

IMG_FOLDER = 'tsp_zaznamove_archy'


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
        ax.imshow(image, cmap='gray' if len(image.shape) == 2 else None)
        ax.set_title(title)
        ax.axis('off')
    plt.show()


def threshold_OTSU(image, threshold):
    """
    Apply OTSU thresholding to the image
    :param image: Grayscale image
    :param threshold: Threshold value
    :return: Thresholded image
    """
    _, threshed = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return threshed


def threshold_to_zero(image, threshold):
    """
    Apply thresholding to zero to the image
    :param image: Grayscale image
    :param threshold: Threshold value
    :return: Thresholded image
    """
    _, threshed = cv2.threshold(image, threshold, 255, cv2.THRESH_TOZERO)
    return cv2.bitwise_not(threshed)


def threshold_yen(image, threshold):
    """
    Apply Yen thresholding to the image
    :param image: Grayscale image
    :param threshold: Threshold value (not used)
    :return: Thresholded image
    """
    thresh = th.threshold_yen(image)
    threshed = putils.apply_threshold(image, thresh)
    return cv2.bitwise_not(np.array(threshed, dtype=np.uint8))


def threshold_mean(image, threshold):
    """
    Apply mean thresholding to the image
    :param image: Grayscale image
    :param threshold: Threshold value (not used)
    :return: Thresholded image
    """
    thresh = th.threshold_mean(image)
    threshed = putils.apply_threshold(image, thresh)
    return cv2.bitwise_not(np.array(threshed, dtype=np.uint8))


def threshold_kapur(image, threshold):
    """
    Apply Kapur thresholding to the image
    :param image: Grayscale image
    :param threshold: Threshold value (not used)
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


generated_sheet = load_pdf(f'{IMG_FOLDER}/vygenerovany.pdf')[0]
scanned_empty = load_pdf(f'{IMG_FOLDER}/naskenovany_prazdny.pdf')[0]
scanned_filled = load_pdf(f'{IMG_FOLDER}/naskenovany_vyplneny.pdf')[0]
# print(generated_sheet.shape)
# show_images(['generated_sheet', 'scanned_empty', 'scanned_filled'], [generated_sheet, scanned_empty, scanned_filled])


# plot histogram of the filled image
gray_filled = cv2.cvtColor(scanned_filled, cv2.COLOR_RGB2GRAY)
threshed_filled = threshold_OTSU(gray_filled, 170)
# show_images(['scanned_filled', 'threshed_filled'], [scanned_filled, threshed_filled])

contours = find_contours(threshed_filled)
# pick k largest contours
k = 4
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:k]
# draw contours
contour_image = cv2.drawContours(scanned_filled.copy(), contours, -1, (0, 255, 0), 2)
# show_images(['scanned_filled', 'contour_image'], [scanned_filled, contour_image])

subimages = []
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    # print(x, y, w, h)
    x += 20
    y += 20
    w -= 40
    h -= 40
    subimage = scanned_filled[y:y+h, x:x+w]
    subimages.append(subimage)

# show_images(['subimage1', 'subimage2', 'subimage3', 'subimage4'], subimages)

answers = []

how_many_circles = [100, 100, 100, 40]
for i, subimage in enumerate(subimages):
    answers.append([])
    # for each image, find circles
    gray = cv2.cvtColor(subimage, cv2.COLOR_RGB2GRAY)
    threshed = threshold_OTSU(gray, 170)
    contours = find_contours(threshed)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:how_many_circles[i]]
    contours = imutils.contours.sort_contours(contours, method="top-to-bottom")[0]
    circle_image = cv2.drawContours(subimage.copy(), contours, -1, (0, 255, 0), 2)

    threshed_subimage = cv2.GaussianBlur(subimage, (5, 5), 0)
    threshed_subimage = threshold_mean(threshed_subimage, 170)

    if i != len(subimages) - 1:
        num_col = 5
    else:
        num_col = 4

    for (q, j) in enumerate(np.arange(0, len(contours), num_col)):
        subcontours = imutils.contours.sort_contours(contours[j:j + num_col])[0]
        answers[i].append([])

        for bubble in subcontours:
            (x, y, w, h) = cv2.boundingRect(bubble)
            cv2.rectangle(circle_image, (x, y), (x+w, y+h), (255, 0, 0), 2)

            bubble_subimage = threshed_subimage[y:y+h, x:x+w]
            one_channel = cv2.cvtColor(bubble_subimage, cv2.COLOR_RGB2GRAY)

            pixels = cv2.countNonZero(one_channel)
            num_pixels = w * h

            # print(pixels, num_pixels)

            if pixels > 0.75 * num_pixels:
                answers[i][q].append(1)
            else:
                answers[i][q].append(0)

    show_images([f'subimage{i+1}', f'threshed_subimage{i+1}', f'circle_image{i+1}'], [subimage, threshed_subimage, circle_image])

    print(answers[i])
