import cv2
import matplotlib.pyplot as plt
import fitz
import numpy as np
import skimage.filters.thresholding as th

IMG_FOLDER = 'tsp_zaznamove_archy'

def load_pdf(file_path):
    """
    Load pdf file and return list of images
    :param file_path:  path to pdf file
    :return:  list of images
    """
    pdf = fitz.open(file_path)
    images = []
    for page_num in range(len(pdf)): # iterate over all pages
        page = pdf[page_num]
        image = page.get_pixmap(dpi=300)
        image = np.frombuffer(image.samples, dtype=np.uint8).reshape(image.h, image.w, 3) # convert to numpy array
        images.append(image)
    return images


def show_images(titles, images):
    """
    Display images in a row with titles
    :param titles:  list of titles
    :param images:  list of images
    """
    fig, axs = plt.subplots(1, len(images), figsize=(len(images)*10, 10))
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
    :param image: grayscale image
    :param threshold: threshold value
    :return: thresholded image
    """
    _, thresh = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh


def threshold_to_zero(image, threshold):
    """
    Apply thresholding to zero to the image
    :param image: grayscale image
    :param threshold: threshold value
    :return: thresholded image
    """
    _, thresh = cv2.threshold(image, threshold, 255, cv2.THRESH_TOZERO)
    return thresh

def threshold_yen(image, threshold):
    """
    Apply Yen thresholding to the image
    :param image: grayscale image
    :param threshold: threshold value (not used)
    :return: thresholded image
    """
    thresh = th.threshold_yen(image)
    return image > thresh

def threshold_mean(image, threshold):
    """
    Apply mean thresholding to the image
    :param image: grayscale image
    :param threshold: threshold value (not used)
    :return: thresholded image
    """
    thresh = th.threshold_mean(image)
    return image > thresh


generated_sheet = load_pdf(f'{IMG_FOLDER}/vygenerovany.pdf')[0]
scanned_empty = load_pdf(f'{IMG_FOLDER}/naskenovany_prazdny.pdf')[0]
scanned_filled = load_pdf(f'{IMG_FOLDER}/naskenovany_vyplneny.pdf')[0]


gray_filled = cv2.cvtColor(scanned_filled, cv2.COLOR_RGB2GRAY)
gray_filled = cv2.GaussianBlur(gray_filled, (5, 5), 0)

threshold = 170
threshold_opts = [threshold_OTSU, threshold_to_zero, threshold_yen, threshold_mean]
thresh_images = [threshold_fun(gray_filled, threshold) for threshold_fun in threshold_opts]
show_images([f'{threshold.__name__}' for threshold in threshold_opts], thresh_images)
