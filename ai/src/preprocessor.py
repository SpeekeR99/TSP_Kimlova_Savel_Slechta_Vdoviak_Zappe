import cv2
import matplotlib.pyplot as plt
import fitz
import numpy as np

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


def threshold_OTSU(image):
    """
    Apply OTSU thresholding to the image
    :param image: grayscale image
    :return: thresholded image
    """
    _, thresh = cv2.threshold(image, 170, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return thresh

generated_sheet = load_pdf(f'{IMG_FOLDER}/vygenerovany.pdf')[0]
scanned_empty = load_pdf(f'{IMG_FOLDER}/naskenovany_prazdny.pdf')[0]
scanned_filled = load_pdf(f'{IMG_FOLDER}/naskenovany_vyplneny.pdf')[0]
print(generated_sheet.shape)
show_images(['generated_sheet', 'scanned_empty', 'scanned_filled'], [generated_sheet, scanned_empty, scanned_filled])


# plot histogram of the filled image
gray_filled = cv2.cvtColor(scanned_filled, cv2.COLOR_RGB2GRAY)
threshed_filled = threshold_OTSU(gray_filled)
show_images(['scanned_filled', 'threshed_filled'], [scanned_filled, threshed_filled])