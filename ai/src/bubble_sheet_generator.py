import numpy as np
import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Config filepath
CONFIG_FILE = "config.json"

# Question number (global across all rectangles and sheets)
question_number = 0


def draw_rect(ax, config, rect_x, rect_y, rect_type="answer_rect", gray_columns=False):
    """
    Draws a rectangle including circles to be filled in the final bubble sheet
    :param ax: The axis to draw the rectangle on
    :param config: Configuration dictionary
    :param rect_x: The x-coordinate of the rectangle top left corner
    :param rect_y: The y-coordinate of the rectangle top left corner
    :param rect_type: Type of the rectangle (Student ID or Answers)
    :param gray_columns: If true every other column will be grayed out, otherwise every other row
    """
    # Set colors from the config
    rect_color = config["colors"]["main_color"]
    off_color = config["colors"]["off_color"]
    text_color = config["colors"]["text_color"]

    # Set the width of line of the rectangle
    rect_width = config["rect_settings"]["rect_line_width"]

    # Set the width and height of the rectangle and the grid inside
    width = config[rect_type]["width"]
    height = config[rect_type]["height"]
    grid_x = config[rect_type]["grid"]["cols"]
    grid_y = config[rect_type]["grid"]["rows"]

    # Set the labels and offsets and font sizes from the config
    label = config[rect_type]["label"]["main"]
    q_label = config[rect_type]["label"]["rows"]
    a_label = config[rect_type]["label"]["cols"]

    label_offset = config[rect_type]["label_offset"]["main"]
    q_offset = config[rect_type]["label_offset"]["rows"]
    a_offset = config[rect_type]["label_offset"]["cols"]

    label_font_size = config[rect_type]["label_font_size"]["main"]
    q_label_fontsize = config[rect_type]["label_font_size"]["rows"]
    a_label_fontsize = config[rect_type]["label_font_size"]["cols"]

    # Set up the question label and answer label correctly
    if rect_type == "answer_rect":
        global question_number
        q_label = [str(grid_y - i + question_number) for i in range(grid_y)]
        question_number += grid_y

        if a_label == "alphabetic":
            a_label = [chr(65 + i) for i in range(grid_x)]
        elif a_label == "numeric":
            a_label = [str(i + 1) for i in range(grid_x)]

    if rect_type == "student_id_rect":
        q_label = [str(grid_y - i) for i in range(grid_y)]

    # Rounded corners rectangle
    round_rect = patches.FancyBboxPatch((rect_x, rect_y), width, height, edgecolor=rect_color, facecolor="none",
                                        linewidth=rect_width, boxstyle="round,pad=0.01")
    ax.add_patch(round_rect)

    # Width and Height of grid cell
    grid_width = width / grid_x
    grid_height = height / grid_y

    # Gray out every other column
    if gray_columns:
        for i in range(grid_x):
            x = rect_x + grid_width * i
            if i % 2 == 0:
                rect = patches.Rectangle((x, rect_y), grid_width, height, edgecolor=off_color,
                                         facecolor=off_color, linewidth=rect_width)
                ax.add_patch(rect)
    # Gray out every other row
    else:
        for i in range(grid_y):
            y = rect_y + grid_height * i
            if i % 2 == 0:
                rect = patches.Rectangle((rect_x, y), width, grid_height, edgecolor=off_color,
                                         facecolor=off_color, linewidth=rect_width)
                ax.add_patch(rect)

    # Draw the bubbles
    for i in range(grid_x):
        for j in range(grid_y):
            # Calculate the position of the bubble
            x = rect_x + grid_width * i
            y = rect_y + grid_height * j
            # Draw the bubble
            circle = patches.Circle((x + grid_width / 2, y + grid_height / 2), grid_width / 3,
                                    edgecolor=rect_color, facecolor="none", linewidth=rect_width)
            ax.add_patch(circle)

    # Draw the big label
    if label != "":
        ax.text(rect_x + width / 2, rect_y + height + label_offset, label,
                ha='center', va='center', fontsize=label_font_size)

    # Draw the labels of answers (columns)
    for i, label in enumerate(a_label):
        ax.text(rect_x + grid_width * i + grid_width / 2, rect_y + height + a_offset, label,
                ha='center', va='center', fontsize=a_label_fontsize, color=text_color)

    # Draw the labels of questions (rows)
    for i, label in enumerate(q_label):
        ax.text(rect_x - q_offset, rect_y + grid_height * i + grid_height / 2, label,
                ha='center', va='center', fontsize=q_label_fontsize, color=text_color)


def main(config):
    """
    Main function to generate the bubble sheet
    """
    # Create a new figure with size of A4 paper
    cm = 1 / 2.54  # Centimeters in inches
    fig, ax = plt.subplots(figsize=(29.7 * cm, 21.0 * cm), dpi=300)

    # Set the aspect of the plot to be equal
    ax.set_aspect('equal', adjustable='datalim')

    # Define the Student ID field
    x = config["student_id_rect"]["x"]
    y = config["student_id_rect"]["y"]
    draw_rect(ax, config, x, y, rect_type="student_id_rect", gray_columns=True)

    # Offset between rectangles
    offset_between_rect = config["rect_settings"]["rect_space_between"]
    num_of_q = config["number_of_questions"]
    num_of_q_per_rect = config["answer_rect"]["grid"]["rows"]
    num_of_rect = np.ceil(num_of_q / num_of_q_per_rect)

    # Define the answer fields
    x += config["student_id_rect"]["width"] + 2 * offset_between_rect

    for i in range(int(num_of_rect)):
        draw_rect(ax, config, x, y)
        x += config["answer_rect"]["width"] + 1.5 * offset_between_rect

    # Turn off the axis but keep the frame
    ax.axis('off')
    # Save the figure as a PDF file
    plt.savefig('output.pdf', format='pdf', bbox_inches='tight', pad_inches=0)


if __name__ == "__main__":
    with open(CONFIG_FILE, "r", encoding="utf-8") as fp:
        config = json.load(fp)
    main(config)
