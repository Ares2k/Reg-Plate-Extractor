import cv2
from matplotlib import pyplot as plt
import numpy as np
import easygui
import imutils
import easyocr


def read_in_image():
    """
    Function that reads a user selected image
    :return: image that was selected
    """
    easygui.msgbox(
        "Select an image with a registration plate to begin...",
        title="License Plate Extractor",
        ok_button="Select Image")

    # Read in the path (will be used later to identify image)
    return cv2.imread(easygui.fileopenbox())


def edge_detection(img):
    """
    Function that detects edges in an image
    :param img: Takes in original user selected image
    :return: image with highlighted edges and a grayscale version of the original image
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    pixel_diameter = 11
    sigmaColor, sigmaSpace = 17, 17
    threshold1 = 30
    threshold2 = 200

    filtered_image = cv2.bilateralFilter(gray, pixel_diameter, sigmaColor, sigmaSpace)  # Noise reduction
    edged = cv2.Canny(filtered_image, threshold1, threshold2)  # Edge detection
    # plt.imshow(cv2.cvtColor(edged, cv2.COLOR_BGR2RGB))

    return edged, gray


def find_contours(edged_image):
    """
    Function to detect contours from the provided edged image
    :param edged_image: Image with highlighted edges
    :return: Sorted contours array
    """
    contours = cv2.findContours(edged_image.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    return sorted(contours, key=cv2.contourArea, reverse=True)[:10]


def identify_polygonal_curves(contours):
    """
    Function that detects polygonal curves in the contoured image
    :param contours: Contoured image
    :return: Location of the polygonal curves where length of it is 4 (e.g square or rectangle)
    """
    for contour in contours:
        polygonal_curves = cv2.approxPolyDP(contour, 10, True)
        if len(polygonal_curves) == 4:
            location = polygonal_curves
            break
    return location, polygonal_curves


def identify_and_mask_contours(location, gray, img):
    """
    Function that identifies contours and creates a mask from it
    :param location: location array which contains the polygonal curves (forming rectangle)
    :param gray: grayscale version of originally selected image
    :param img: original image selected by user
    :return: reverse mask of the contoured image
    """
    h, w = gray.shape
    mask = np.zeros((h, w), np.uint8)
    new_image = cv2.drawContours(mask, [location], 0,255, -1)
    new_image = cv2.bitwise_and(img, img, mask=mask)
    return mask


def extract_x_y(mask, gray):
    white_pixels = mask == 255

    x, y = np.where(white_pixels)
    x1 = y1 = float("inf")
    x2 = y2 = 0

    # Get the lowest x1, x2 values
    for val in x:
        x1 = min(x1, val)
        x2 = max(x2, val)

    # Get the lowest y1, y2 values
    for val in y:
        y1 = min(y1, val)
        y2 = max(y2, val)

    return gray[x1:x2+1, y1:y2+1]


def extract_text_from_plate(cropped_image):
    """
    Extracts english text from the image using easyOCR library
    :param cropped_image: cropped license plate of the grayscaled image
    :return: license plate number as a string
    """
    reader = easyocr.Reader(['en'])
    result = reader.readtext(cropped_image)

    license_plate = ''
    for item in result:
        print(str(item[1]) + '\n')
        license_plate += str(item[1]) + ' '
    return license_plate


def draw_rect_text_on_img(img, license_plate, polygonal_curves):
    """
    Function that draws a rectangle around the license plate and the plate's number
    :param img: original image selected by user
    :param license_plate: registration plate number
    :param polygonal_curves:
    """
    font = cv2.FONT_HERSHEY_SIMPLEX
    text_location = (polygonal_curves[0][0][0], polygonal_curves[1][0][1])
    color = (0, 255, 0)  # Green font
    offset = 60

    rectangle_location = (polygonal_curves[0][0], polygonal_curves[2][0])

    # Draw a rectangle on the image where the license plate is located
    paint_image = cv2.rectangle(img, rectangle_location[0], rectangle_location[1], color, 5)
    paint_image = cv2.putText(img, text=license_plate, org=(text_location[0], text_location[1] + offset), fontFace=font, fontScale=1, color=color, thickness=2, lineType=cv2.LINE_AA)
    plt.imshow(cv2.cvtColor(paint_image, cv2.COLOR_BGR2RGB))
    plt.show()


# Read in image
img = read_in_image()

# Detect the edges in the image
edged_image, gray = edge_detection(img)

# Locate the contours in the edged image
contours = find_contours(edged_image)

# Identify the polygonal curves in the contour locations
location, polygonal_curves = identify_polygonal_curves(contours)

# Identify the contours, draw them and create a reverse mask
masked_img = identify_and_mask_contours(location, gray, img)

# Extract coordinates of the license plate and crop it
cropped = extract_x_y(masked_img, gray)

# Extract text from the cropped license plate
license_plate = extract_text_from_plate(cropped)

# Draw rectangle and license plate's contents onto the image
draw_rect_text_on_img(img, license_plate, polygonal_curves)