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


def find_contours(image):
    """
    Find contours in the image
    :param image: thresholded image
    :return: list of contours
    """
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours



def find_edges(image):
    """
    Find edges in the image
    :param image: grayscale image
    :return: edges
    """
    edges = cv2.Canny(image, 100, 200)
    return edges


generated_sheet = load_pdf(f'{IMG_FOLDER}/vygenerovany.pdf')[0]
scanned_empty = load_pdf(f'{IMG_FOLDER}/naskenovany_prazdny.pdf')[0]
scanned_filled = load_pdf(f'{IMG_FOLDER}/naskenovany_vyplneny.pdf')[0]
print(generated_sheet.shape)
# show_images(['generated_sheet', 'scanned_empty', 'scanned_filled'], [generated_sheet, scanned_empty, scanned_filled])


# plot histogram of the filled image
gray_filled = cv2.cvtColor(scanned_filled, cv2.COLOR_RGB2GRAY)
threshed_filled = threshold_OTSU(gray_filled)
# show_images(['scanned_filled', 'threshed_filled'], [scanned_filled, threshed_filled])

contours = find_contours(threshed_filled)
print(len(contours))
# pick k largest contours
k = 4
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:k]
# draw contours
contour_image = cv2.drawContours(scanned_filled.copy(), contours, -1, (0, 255, 0), 2)
show_images(['scanned_filled', 'contour_image'], [scanned_filled, contour_image])

subimages = []
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    print(x, y, w, h)
    x += 20
    y += 20
    w -= 40
    h -= 40
    subimage = scanned_filled[y:y+h, x:x+w]
    subimages.append(subimage)

show_images(['subimage1', 'subimage2', 'subimage3', 'subimage4'], subimages)

how_many_circles = [100, 100, 100, 40]
for i, subimage in enumerate(subimages):
    # for each image, find circles
    gray = cv2.cvtColor(subimage, cv2.COLOR_RGB2GRAY)
    threshed = threshold_OTSU(gray)
    contours = find_contours(threshed)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:how_many_circles[i] + 1]
    circle_image = cv2.drawContours(subimage.copy(), contours, -1, (0, 255, 0), 2)
    show_images([f'subimage{i+1}', f'circle_image{i+1}'], [subimage, circle_image])
