import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import fitz
import qrcode
import json

from ai.src.utils import load_config, get_A4_size, get_max_num_of_rects_in_page, get_num_of_rects_per_page


# Use Agg backend for matplotlib
matplotlib.use("Agg")
# Question number (global across all rectangles and sheets)
question_number = 1


def draw_header(ax, config, rect_x, rect_y, date, student_name):
    """
    Draw the header of the bubble sheet
    :param ax: The axis to draw the rectangle on
    :param config: Configuration dictionary
    :param rect_x: The x-coordinate of the rectangle top left corner
    :param rect_y: The y-coordinate of the rectangle top left corner
    :param date: Date of the test
    :param student_name: Student name
    """
    PIXELS_PER_INCH = 96

    # Configuration
    header_title = config["header"]["title"]
    header_date = config["header"]["date"] + date
    header_name = config["header"]["name"] + student_name
    font_size = config["header"]["font_size"]
    font_size_relative = font_size / (ax.figure.get_figheight() * PIXELS_PER_INCH)
    font = config["header"]["font"]
    text_color = config["colors"]["main_color"]

    # Draw the header
    rect_y -= font_size_relative
    rect_x -= font_size_relative
    ax.text(rect_x, rect_y, header_title, ha='left', va='bottom', fontsize=font_size + 5, fontname=font,
            color=text_color, weight='bold')
    font_size_offset = font_size_relative * 2
    ax.text(rect_x, rect_y - font_size_offset, header_name, ha='left', va='bottom', fontsize=font_size, fontname=font,
            color=text_color)
    font_size_offset = font_size_relative * 4
    ax.text(rect_x, rect_y - font_size_offset, header_date, ha='left', va='bottom', fontsize=font_size, fontname=font,
            color=text_color)


def gray_out(ax, config, rect_x, rect_y, rect_type="answer_rect", gray_columns=False):
    """
    Gray out every other column or row
    :param ax: The axis to draw the rectangle on
    :param config: Configuration dictionary
    :param rect_x: The x-coordinate of the rectangle top left corner
    :param rect_y: The y-coordinate of the rectangle top left corner
    :param rect_type: Type of the rectangle (Student ID or Answers)
    :param gray_columns: If true every other column will be grayed out, otherwise every other row
    """
    # Configuration
    off_color = config["colors"]["off_color"]

    rect_width = config["rect_settings"]["rect_line_width"]

    width = config[rect_type]["width"]
    height = config[rect_type]["height"]

    cols = config[rect_type]["grid"]["cols"]
    rows = config[rect_type]["grid"]["rows"]

    # Width and Height of grid cell
    grid_width = width / cols
    grid_height = height / rows

    # Gray out every other column
    if gray_columns:
        for i in range(cols):
            x = rect_x + grid_width * i
            if i % 2 == 0:
                rect = patches.Rectangle((x, rect_y), grid_width, height, edgecolor=off_color,
                                         facecolor=off_color, linewidth=rect_width)
                ax.add_patch(rect)
    # Gray out every other row
    else:
        for i in range(rows):
            y = rect_y + grid_height * i
            if i % 2 == 0:
                rect = patches.Rectangle((rect_x, y), width, grid_height, edgecolor=off_color,
                                         facecolor=off_color, linewidth=rect_width)
                ax.add_patch(rect)


def draw_bubbles(ax, config, rect_x, rect_y, rect_type, last_rect_q, student_id):
    """
    Draw the bubbles in the rectangle
    :param ax: The axis to draw the rectangle on
    :param config: Configuration dictionary
    :param rect_x: The x-coordinate of the rectangle top left corner
    :param rect_y: The y-coordinate of the rectangle top left corner
    :param rect_type: Type of the rectangle (Student ID or Answers)
    :param last_rect_q: Number of questions in the last rectangle
    :param student_id: Student ID
    """
    # Configuration
    rect_color = config["colors"]["main_color"]

    rect_width = config["rect_settings"]["rect_line_width"]

    width = config[rect_type]["width"]
    height = config[rect_type]["height"]

    cols = config[rect_type]["grid"]["cols"]
    rows = config[rect_type]["grid"]["rows"]

    # Width and Height of grid cell
    grid_width = width / cols
    grid_height = height / rows

    for i in range(cols):
        for j in range(rows):
            # Skip the bubbles if this is the last rectangle and the question number is less than the last_rect_q
            if last_rect_q is not None and j >= last_rect_q:
                continue

            # Calculate the position of the bubble
            x = rect_x + grid_width * i
            y = rect_y + height - (grid_height * (j + 1))

            # If this is the student ID rectangle, fill the bubbles according to the student ID
            face_color = "none"
            if rect_type == "student_id_rect":
                y = rect_y + height - (grid_height * (j + 1))
                if student_id != "empty" and student_id[i] == str(j):
                    face_color = rect_color

            # Draw the bubble
            circle = patches.Circle((x + grid_width / 2, y + grid_height / 2), grid_width / 3,
                                    edgecolor=rect_color, facecolor=face_color, linewidth=rect_width)
            ax.add_patch(circle)


def setup_labels(config, rect_type, last_rect_q=None):
    """
    Set up the question label and answer label correctly
    :param config: Configuration dictionary
    :param rect_type: Type of the rectangle (Student ID or Answers)
    :param last_rect_q: Number of questions in the last rectangle
    :return: Question label and Answer label
    """
    # Configuration
    cols = config[rect_type]["grid"]["cols"]
    rows = config[rect_type]["grid"]["rows"]

    q_label = config[rect_type]["label"]["rows"]
    a_label = config[rect_type]["label"]["cols"]

    # Set up the question label and answer label correctly
    if rect_type == "answer_rect":
        global question_number  # Global question number counter

        # If this is the last rectangle, that could have less questions
        if last_rect_q is not None:
            q_label = [str(i + question_number) for i in range(last_rect_q)]
            question_number += last_rect_q
        # Else normal rectangle
        else:
            q_label = [str(i + question_number) for i in range(rows)]
            question_number += rows

        # If the answer labels are alphabetic use ABCD... else if numeric use 1234...
        if a_label == "alphabetic":
            a_label = [chr(65 + i) for i in range(cols)]
        elif a_label == "numeric":
            a_label = [str(i + 1) for i in range(cols)]

    # Set up the student ID label correctly
    if rect_type == "student_id_rect":
        q_label = [str(i) for i in range(rows)]

    return q_label, a_label


def draw_labels(ax, config, rect_x, rect_y, rect_type, last_rect_q=None):
    """
    Draw the labels of questions and answers
    :param ax: The axis to draw the rectangle on
    :param config: Configuration dictionary
    :param rect_x: The x-coordinate of the rectangle top left corner
    :param rect_y: The y-coordinate of the rectangle top left corner
    :param rect_type: Type of the rectangle (Student ID or Answers)
    :param last_rect_q: Number of questions in the last rectangle
    """
    # Configuration
    text_color = config["colors"]["text_color"]

    width = config[rect_type]["width"]
    height = config[rect_type]["height"]

    label = config[rect_type]["label"]["main"]

    cols = config[rect_type]["grid"]["cols"]
    rows = config[rect_type]["grid"]["rows"]

    label_offset = config[rect_type]["label_offset"]["main"]
    q_offset = config[rect_type]["label_offset"]["rows"]
    a_offset = config[rect_type]["label_offset"]["cols"]

    label_font_size = config[rect_type]["label_font_size"]["main"]
    q_label_fontsize = config[rect_type]["label_font_size"]["rows"]
    a_label_fontsize = config[rect_type]["label_font_size"]["cols"]

    # Set up the question label and answer label correctly (or student ID label)
    q_label, a_label = setup_labels(config, rect_type, last_rect_q=last_rect_q)

    # Width and Height of grid cell
    grid_width = width / cols
    grid_height = height / rows

    if label != "":
        ax.text(rect_x + width / 2, rect_y + height + label_offset, label,
                ha='center', va='center', fontsize=label_font_size)

    # Draw the labels of answers (columns)
    for i, label in enumerate(a_label):
        ax.text(rect_x + grid_width * i + grid_width / 2, rect_y + height + a_offset, label,
                ha='center', va='center', fontsize=a_label_fontsize, color=text_color)

    # Draw the labels of questions (rows)
    for i, label in enumerate(q_label):
        ax.text(rect_x - q_offset, rect_y + height - (grid_height * i + grid_height / 2), label,
                ha='center', va='center', fontsize=q_label_fontsize, color=text_color)


def draw_rect(ax, config, rect_x, rect_y, rect_type="answer_rect", gray_columns=False, last_rect_q=None, student_id=0):
    """
    Draws a rectangle including circles to be filled in the final bubble sheet
    :param ax: The axis to draw the rectangle on
    :param config: Configuration dictionary
    :param rect_x: The x-coordinate of the rectangle top left corner
    :param rect_y: The y-coordinate of the rectangle top left corner
    :param rect_type: Type of the rectangle (Student ID or Answers)
    :param gray_columns: If true every other column will be grayed out, otherwise every other row
    :param last_rect_q: Number of questions in the last rectangle
    :param student_id: Student ID
    """
    # Configuration
    rect_color = config["colors"]["main_color"]

    rect_width = config["rect_settings"]["rect_line_width"]

    width = config[rect_type]["width"]
    height = config[rect_type]["height"]

    # Rounded corners rectangle
    round_rect = patches.FancyBboxPatch((rect_x, rect_y), width, height, edgecolor=rect_color, facecolor="none",
                                        linewidth=rect_width, boxstyle="round,pad=0.01")
    ax.add_patch(round_rect)

    # Gray out every other column or row
    gray_out(ax, config, rect_x, rect_y, rect_type=rect_type, gray_columns=gray_columns)

    # Draw the bubbles
    if student_id == "empty":
        draw_bubbles(ax, config, rect_x, rect_y, rect_type, last_rect_q, student_id)
    else:
        draw_bubbles(ax, config, rect_x, rect_y, rect_type, last_rect_q, str(student_id).zfill(4))

    # Draw labels
    draw_labels(ax, config, rect_x, rect_y, rect_type, last_rect_q=last_rect_q)


def draw_page(ax, config, test_id, student_id, page, num_of_pages, num_of_rects_in_page, offset_between_rect, last_rect_q, date, student_name):
    """
    Draw a page of the bubble sheet
    :param ax: Axis to draw the page on
    :param config: Configuration dictionary
    :param test_id: Test ID
    :param student_id: Student ID
    :param page: Current page number
    :param num_of_pages: Number of pages
    :param num_of_rects_in_page: Number of rectangles in each page
    :param offset_between_rect: Offset between rectangles
    :param last_rect_q: Number of questions in the last rectangle
    :param date: Date of the test
    :param student_name: Student name
    """
    # Define the Student ID field
    x = config["student_id_rect"]["x"]
    y = config["student_id_rect"]["y"]
    draw_rect(ax, config, x, y, rect_type="student_id_rect", gray_columns=True, student_id=student_id)

    # Draw QR code to the top right corner serving as pdf rotation indicator also
    qr_data = {"test_id": test_id, "page": page}
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(json.dumps(qr_data))
    qr.make(fit=True)
    qr = qr.make_image(fill_color="black", back_color="white")
    qr = qr.resize((100, 100))
    ax_in_ax = ax.inset_axes([0.87, 0.85, 0.2, 0.2], transform=ax.transAxes)
    ax_in_ax.imshow(qr)
    ax_in_ax.axis('off')

    # Draw the header
    draw_header(ax, config, x, 1 - y, date, student_name)

    # Define answers fields
    x += config["student_id_rect"]["width"] + 2 * offset_between_rect

    num_of_rects_this_page = num_of_rects_in_page[page]
    for i in range(num_of_rects_this_page):
        # Last rectangle has less questions (maybe)
        if i == num_of_rects_this_page - 1 and last_rect_q != 0 and page == num_of_pages - 1:
            draw_rect(ax, config, x, y, last_rect_q=last_rect_q)
        # Normal rectangle
        else:
            draw_rect(ax, config, x, y)

        # Move to the next rectangle
        x += config["answer_rect"]["width"] + 1.5 * offset_between_rect


def generate_bubble_sheet(test_id, student_id, num_of_q, date, student_name):
    """
    Main function to generate the bubble sheet
    :param test_id: Test ID
    :param student_id: Student ID (number from 0 to 9999)
    :param num_of_q: Number of questions
    :param date: Date of the test
    :param student_name: Student name
    """
    global question_number
    question_number = 1

    # Load the configuration file
    config = load_config()

    # A4 paper size in inches
    A4 = get_A4_size()

    # Offset between rectangles
    offset_between_rect = config["rect_settings"]["rect_space_between"]

    # Number of questions
    num_of_q_per_rect = config["answer_rect"]["grid"]["rows"]
    num_of_rect = int(np.ceil(num_of_q / num_of_q_per_rect))
    last_rect_q = num_of_q % num_of_q_per_rect

    # Calculate the number of rectangles that can fit in the figure
    num_of_rects_per_page = get_max_num_of_rects_in_page(config, A4)

    # Calculate the number of pages needed
    num_of_pages = int(np.ceil(num_of_rect / num_of_rects_per_page))

    # Calculate the number of rectangles in each page
    num_of_rects_in_page = get_num_of_rects_per_page(num_of_rect, num_of_pages, num_of_rects_per_page)

    # Generate the bubble sheet for each page
    sub_pdfs = []
    for page in range(num_of_pages):
        # Create a figure
        fig, ax = plt.subplots(figsize=A4, dpi=300)

        # Set the aspect of the plot to be equal
        ax.set_aspect('equal', adjustable='datalim')

        draw_page(ax, config, test_id, student_id, page, num_of_pages, num_of_rects_in_page, offset_between_rect, last_rect_q, date, student_name)

        # Turn off the axis but keep the frame
        ax.axis("off")
        # Save the figure as a PDF file
        file_name = f"generated_pdfs/{student_id}_bubble_sheet_page_{page + 1}.pdf"
        sub_pdfs.append(file_name)
        plt.savefig(file_name, format='pdf', bbox_inches='tight', pad_inches=0)

        # Cleanup
        plt.close()
        fig.clf()

    # Merge the PDFs now
    merged_pdf = fitz.open()
    for pdf in sub_pdfs:
        with fitz.open(pdf) as pdf_file:
            merged_pdf.insert_pdf(pdf_file)

    # Save the final PDF
    final_pdf = f"generated_pdfs/{student_id}_bubble_sheet.pdf"
    merged_pdf.save(final_pdf)
    merged_pdf.close()

    # Remove the sub PDFs
    for pdf in sub_pdfs:
        os.remove(pdf)
