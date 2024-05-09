import os
import datetime
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


def latex_to_img(latex_str, font_size=12):
    # Create a new figure and axis
    fig, ax = plt.subplots(figsize=(1, 1))

    # Set the axis off
    ax.axis("off")

    # Add the latex to the axis
    ax.text(0.5, 0.5, "$%s$" % latex_str, size=font_size, va="center", ha="center")

    # Save the figure to a temporary file
    temp_file = "temp" + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + ".png"
    fig.savefig(temp_file, bbox_inches='tight', pad_inches=0.0, transparent=True)

    # Close the figure
    plt.close(fig)

    return temp_file


def wrap_text(text, max_width, font, font_size):
    paragraphs = text.split('\n')
    lines = []
    for paragraph in paragraphs:
        words = paragraph.split(' ')
        current_line = []
        current_width = 0

        for word in words:
            word_width = pdfmetrics.stringWidth(word, font, font_size)
            if current_width + word_width <= max_width:
                current_line.append(word)
                current_width += word_width
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_width = word_width

        lines.append(' '.join(current_line))
    return lines


def draw_labels(student_id, student_questions, question_answers, filename):
    c = canvas.Canvas(filename, pagesize=letter)

    font_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../res/fonts/arial", "Arial.ttf")
    # set font
    pdfmetrics.registerFont(TTFont("Arial", font_file))
    c.setFont("Arial", 12)  # Set the font and size

    # Define label dimensions and spacing
    label_height = 20
    x_margin = 50
    y_margin = 50
    y_spacing = 10

    # Draw title
    c.setFont("Arial", 20)
    c.drawString(x_margin, letter[1] - y_margin, "Otázky k testu")
    c.setFont("Arial", 12)

    # Draw student_id labels
    x = x_margin
    y = letter[1] - y_margin - 50
    c.drawString(x, y, "ID studenta: " + str(student_id))
    y -= (label_height + y_spacing)

    # draw questions labels
    for i in range(len(student_questions)):
        question = student_questions[i]
        answers = question_answers[i]

        c.line(x, y + 10, letter[0] - x_margin, y + 10)
        y -= y_spacing

        # If question with answers does not fit in the page
        lines = wrap_text(question, letter[0] - 3 * x_margin, "Arial", 12)
        overall_height = len(lines) * label_height
        for answer in answers:
            lines += wrap_text(answer, letter[0] - 3 * x_margin, "Arial", 12)
            overall_height += len(lines) * label_height
        if y - overall_height < y_margin / 2:
            # Draw page number before starting a new page
            c.drawString(letter[0] / 2, y_margin / 2, str(c.getPageNumber()))
            y = letter[1] - y_margin
            c.showPage()
            c.line(x, y + 10, letter[0] - x_margin, y + 10)
            y -= y_spacing

        question_number = "Otázka " + str(i + 1)
        c.drawString(x, y, question_number + ": ")
        x += c.stringWidth(question_number + ": ", "Arial", 12)

        # Question may have LaTeX math in it
        char_index = 0
        question_text = ""
        # Char stream
        x_so_far = c.stringWidth(question_number + ": ", "Arial", 12)
        while char_index < len(question):
            current_char = question[char_index]
            if current_char == "$":
                # First draw the text so far
                lines = wrap_text(question_text, letter[0] - 3 * x_margin, "Arial", 12)
                for line in lines:
                    c.drawString(x, y, line)
                    y -= label_height
                    x = x_margin
                if len(lines) == 1:
                    y += label_height
                    x_so_far += c.stringWidth(lines[0], "Arial", 12)
                    x += x_so_far
                else:
                    x_so_far = x
                question_text = ""

                # Find the end of the math expression
                question_substr = question[char_index:]
                end_index = question_substr.find("$", 1) + char_index
                # Add the math expression to the question text
                latex_text = question[char_index + 1:end_index]
                latex = latex_to_img(latex_text, font_size=120)

                # Get the dimensions of the image
                img = plt.imread(latex)
                height, width = img.shape[:2]
                new_height = height / 14
                new_width = width / 14
                x_so_far += new_width

                # Draw the image
                c.drawImage(latex, x, y - new_height / 2.5, width=new_width, height=new_height)
                x += new_width
                os.remove(latex)

                # Update the char index
                char_index = end_index + 1
            else:
                question_text += current_char
                char_index += 1

        # Draw the remaining text
        lines = wrap_text(question_text, letter[0] - 3 * x_margin, "Arial", 12)
        for line in lines:
            c.drawString(x, y, line)
            y -= label_height
            x = x_margin

        y -= y_spacing

        for j, answer in enumerate(answers):
            x_answer = x + 20
            question_letter = chr(65 + j) + "."
            lines = wrap_text(question_letter + " " + answer, letter[0] - 3 * x_margin, "Arial", 12)
            for line in lines:
                c.drawString(x_answer, y, line)
                y -= label_height

    # Draw page number on the last page
    c.drawString(letter[0] / 2, y_margin / 2, str(c.getPageNumber()))

    c.showPage()
    c.save()


def generate_question_paper(student_id, student_questions, question_answers):
    file_path = 'generated_pdfs/' + str(student_id) + '_question_paper.pdf'
    draw_labels(student_id, student_questions, question_answers, file_path)
