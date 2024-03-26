import matplotlib.pyplot as plt
import matplotlib.patches as patches


class BubbleSheet:
    """
    Bubble sheet class to generate
    """
    def __init__(self):
        # Constants
        self.MAIN_COLOR = "black"
        self.OFF_COLOR = "#eeeeee"
        self.TEXT_COLOR = "lightgray"
        self.RECT_WIDTH = 2

    def draw_rect(self, ax, rect_x, rect_y, width, height, grid_x, grid_y, rect_color=None,
                  rect_width=2, big_label=None, label_offset=0.1, label_fontsize=20, gray_columns=False):
        """
        Draws a rectangle including circles to be filled in the final bubble sheet
        :param ax: The axis to draw the rectangle on
        :param rect_x: The x-coordinate of the rectangle top left corner
        :param rect_y: The y-coordinate of the rectangle top left corner
        :param width: Width of the rectangle
        :param height: Height of the rectangle
        :param grid_x: Number of columns
        :param grid_y: Number of rows
        :param rect_color: Main color of the rectangle
        :param rect_width: Width of the rectangle border
        :param big_label: Label of the rectangle (above)
        :param label_offset: Offset of the big label
        :param label_fontsize: Font size of the big label
        :param gray_columns: If true every other column will be grayed out, otherwise every other row
        """
        # Set default colors if not provided
        if rect_color is None:
            rect_color = self.MAIN_COLOR

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
                    rect = patches.Rectangle((x, rect_y), grid_width, height, edgecolor=self.OFF_COLOR,
                                             facecolor=self.OFF_COLOR, linewidth=rect_width)
                    ax.add_patch(rect)
        # Gray out every other row
        else:
            for i in range(grid_y):
                y = rect_y + grid_height * i
                if i % 2 == 0:
                    rect = patches.Rectangle((rect_x, y), width, grid_height, edgecolor=self.OFF_COLOR,
                                             facecolor=self.OFF_COLOR, linewidth=rect_width)
                    ax.add_patch(rect)

        # Draw the big label
        if big_label:
            ax.text(rect_x + width / 2, rect_y + height + label_offset, big_label,
                    ha='center', va='center', fontsize=label_fontsize)

    def draw_grid(self, ax, rect_x, rect_y, width, height, grid_x, grid_y, q_label, a_label,
                  rect_color=None, label_color=None, q_offset=0.05, a_offset=0.05,
                  rect_width=2, q_label_fontsize=12, a_label_fontsize=12):
        """
        Draws a rectangle including circles to be filled in the final bubble sheet
        :param ax: The axis to draw the rectangle on
        :param rect_x: The x-coordinate of the rectangle top left corner
        :param rect_y: The y-coordinate of the rectangle top left corner
        :param width: Width of the rectangle
        :param height: Height of the rectangle
        :param grid_x: Number of columns
        :param grid_y: Number of rows
        :param q_label: List of labels for questions (rows)
        :param a_label: List of labels for answers (columns)
        :param rect_color: Main color of the rectangle
        :param label_color: Label color
        :param q_offset: Question label offset
        :param a_offset: Answer label offset
        :param rect_width: Width of the rectangle border
        :param q_label_fontsize: Font size of question labels
        :param a_label_fontsize: Font size of answer labels
        """
        # Set default colors if not provided
        if rect_color is None:
            rect_color = self.MAIN_COLOR
        if label_color is None:
            label_color = self.TEXT_COLOR

        # Width and Height of grid cell
        grid_width = width / grid_x
        grid_height = height / grid_y

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

        # Draw the labels of answers (columns)
        for i, label in enumerate(a_label):
            ax.text(rect_x + grid_width * i + grid_width / 2, rect_y + height + a_offset, label,
                    ha='center', va='center', fontsize=a_label_fontsize, color=label_color)

        # Draw the labels of questions (rows)
        for i, label in enumerate(q_label):
            ax.text(rect_x - q_offset, rect_y + grid_height * i + grid_height / 2, label,
                    ha='center', va='center', fontsize=q_label_fontsize, color=label_color)


def main():
    """
    Main function to generate the bubble sheet
    """
    # Create a new figure with size of A4 paper
    cm = 1 / 2.54  # Centimeters in inches
    fig, ax = plt.subplots(figsize=(29.7 * cm, 21.0 * cm), dpi=300)

    # Set the aspect of the plot to be equal
    ax.set_aspect('equal', adjustable='datalim')

    # Instantiate the BubbleSheet class
    bubble_sheet = BubbleSheet()

    # Define the Student ID field
    # THESE MAGIC NUMBERS SERVE AS EXAMPLES OF HOW THE USER MIGHT INPUT THIS FIELD
    x = -0.1
    y = 0.05
    width = 0.2
    height = 0.6
    grid_x = 4
    grid_y = 10
    q_label = [str(9 - i) for i in range(10)]
    a_label = []

    bubble_sheet.draw_rect(ax, x, y, width, height, grid_x, grid_y, big_label="Student ID",
                           label_offset=0.05, gray_columns=True)
    bubble_sheet.draw_grid(ax, x, y, width, height, grid_x, grid_y, q_label, a_label, q_offset=0.03)

    # Offset between rectangles
    offset_between_rect = 0.1

    # Define the first answer field
    # THESE MAGIC NUMBERS SERVE AS EXAMPLES OF HOW THE USER MIGHT INPUT THIS FIELD
    x = x + width + offset_between_rect * 2
    width = 0.15
    height = 0.8
    grid_x = 5
    grid_y = 20
    q_label = [str(20 - i) for i in range(20)]
    a_label = ["A", "B", "C", "D", "E"]

    bubble_sheet.draw_rect(ax, x, y, width, height, grid_x, grid_y)
    bubble_sheet.draw_grid(ax, x, y, width, height, grid_x, grid_y, q_label, a_label, q_offset=0.04, a_offset=0.03)

    # Define the second answer field
    # THESE MAGIC NUMBERS SERVE AS EXAMPLES OF HOW THE USER MIGHT INPUT THIS FIELD
    x = x + width + offset_between_rect * 1.5
    width += 0.05

    bubble_sheet.draw_rect(ax, x, y, width, height, grid_x + 2, grid_y, big_label="Answers")
    bubble_sheet.draw_grid(ax, x, y, width, height, grid_x + 2, grid_y, q_label, a_label + ["F", "G"])

    # Define the third answer field
    # THESE MAGIC NUMBERS SERVE AS EXAMPLES OF HOW THE USER MIGHT INPUT THIS FIELD
    x = x + width + offset_between_rect * 1.5
    width -= 0.05

    bubble_sheet.draw_rect(ax, x, y, width, height, grid_x, grid_y)
    bubble_sheet.draw_grid(ax, x, y, width, height, grid_x, grid_y, q_label, a_label, q_offset=0.04, a_offset=0.03)

    # Turn off the axis but keep the frame
    ax.axis('off')
    # Save the figure as a PDF file
    plt.savefig('output.pdf', format='pdf', bbox_inches='tight', pad_inches=0)


if __name__ == "__main__":
    # TODO: Take user input and make the bubble sheet customizable on user's demand
    main()
