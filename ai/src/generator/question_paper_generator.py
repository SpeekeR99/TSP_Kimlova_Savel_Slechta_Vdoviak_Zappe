import os
import datetime
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import SvgFormatter
import fitz
from PIL import Image
import numpy as np
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup


def latex_to_img(latex_str, font_size=12):
    # Create a new figure and axis
    fig, ax = plt.subplots(figsize=(1, 1))

    # Set the axis off
    ax.axis("off")

    # Add the latex to the axis
    ax.text(0.5, 0.5, "$%s$" % latex_str, size=font_size, va="center", ha="center")

    # Save the figure to a temporary file
    temp_file = "temp" + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + ".png"
    fig.savefig(temp_file, bbox_inches='tight', pad_inches=0.1, transparent=True)

    # Close the figure
    plt.close(fig)

    return temp_file


def wrap_text(text, max_width, font, font_size, first_width=None):
    paragraphs = text.split('\n')
    lines = []
    for paragraph in paragraphs:
        words = paragraph.split(' ')
        current_line = []
        current_width = 0

        is_comment = "#" in paragraph

        for word in words:
            word_width = pdfmetrics.stringWidth(word, font, font_size)
            line_width = max_width - first_width if (first_width is not None and len(lines) == 0) else max_width
            if current_width + word_width <= line_width:
                current_line.append(word)
                current_width += word_width
            else:
                # If the line is a comment, add it to the line
                lines.append(' '.join(current_line))
                current_line = [word]
                if is_comment:
                    current_line.insert(0, "# ")
                current_width = word_width

        lines.append(' '.join(current_line))
    return lines


def html_strip(html):
    # Remove HTML tags
    soup = BeautifulSoup(html, "html.parser")
    stripped = soup.get_text()

    stripped = replace_html_entities(stripped)
    stripped = stripped.encode("utf-8").decode("utf-8")

    return stripped


def replace_html_entities(text):
    text = text.replace("&nbsp;", " ")
    text = text.replace("&lt;", "<")
    text = text.replace("&gt;", ">")
    text = text.replace("&amp;", "&")
    text = text.replace("&quot;", "\"")
    text = text.replace("&apos;", "'")
    text = text.replace("&#8221;", "\"")
    text = text.replace("&#8220;", "\"")
    text = text.replace("&#8211;", "-")
    text = text.replace("&#8212;", "-")
    text = text.replace("&#8230;", "...")
    text = text.replace("&#8216;", "'")
    text = text.replace("&#8217;", "'")
    text = text.replace("&#39;", "'")
    return text


def contains_code(text):
    code_start = text.find("<pre>")
    code_end = text.find("</pre>")
    return code_start != -1 and code_end != -1


def get_code_substring(text):
    code_start = text.find("<pre>")
    code_end = text.find("</pre>")
    return text[code_start:code_end + len("</pre>")]


def upscale_svg(svg_file_path, scale_factor):
    # Parse the SVG file
    tree = ET.parse(svg_file_path)
    root = tree.getroot()

    # Get the current width and height
    current_width = float(root.attrib['width'])
    current_height = float(root.attrib['height'])

    # Calculate the new width and height
    new_width = current_width * scale_factor
    new_height = current_height * scale_factor

    # Update the width and height attributes
    root.attrib['width'] = str(new_width)
    root.attrib['height'] = str(new_height)

    # Apply a scaling transform to the root <svg> element
    transform = 'scale({})'.format(scale_factor)
    if 'transform' in root.attrib:
        root.attrib['transform'] += ' ' + transform
    else:
        root.attrib['transform'] = transform

    # Write the modified SVG back to the file
    tree.write(svg_file_path)


def draw_labels(student_id, student_questions, question_answers, filename, date, student_name):
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
    c.drawString(x, y, "Jméno: " + student_name)
    y -= label_height
    c.drawString(x, y, "Datum: " + date)
    y -= label_height
    c.drawString(x, y, "ID studenta: " + str(student_id))
    y -= (label_height + y_spacing)

    # draw questions labels
    for i in range(len(student_questions)):
        question = student_questions[i]
        answers = question_answers[i]

        question = question.replace("<br>", "\n")
        code_part = None

        if contains_code(question):
            code_part = get_code_substring(question)
            question = question.replace(code_part, "*CODE*")
            code_part = html_strip(code_part)
            code_part = wrap_text(code_part, letter[0] - 3 * x_margin, "Arial", 12)
            code_part = "\n".join(code_part)

        question = html_strip(question)

        for j in range(len(answers)):
            answers[j] = answers[j].replace("<br>", "")
            answers[j] = html_strip(answers[j])

        c.line(x, y + 10, letter[0] - x_margin, y + 10)
        y -= y_spacing

        # If question with answers does not fit in the page
        lines = wrap_text(question, letter[0] - 3 * x_margin, "Arial", 12)
        overall_height = len(lines) * label_height
        if code_part:
            code_lines = wrap_text(code_part, letter[0] - 3 * x_margin, "Arial", 12)
            overall_height += len(code_lines) * label_height

        if y - overall_height < y_margin / 2:
            # Draw page number before starting a new page
            c.drawString(letter[0] / 2, y_margin / 2, str(c.getPageNumber()))
            y = letter[1] - y_margin
            c.showPage()
            c.setFont("Arial", 12)
            c.line(x, y + 10, letter[0] - x_margin, y + 10)
            y -= y_spacing

        question_number = "Otázka " + str(i + 1)
        question = question_number + ": " + question.replace("$$", "$")

        # Question may have code in it
        if code_part:
            # Draw the text so far
            question_text = question.split("*CODE*")[0]
            lines = wrap_text(question_text, letter[0] - 3 * x_margin, "Arial", 12)
            for line in lines:
                c.drawString(x, y, line)
                y -= label_height
                x = x_margin

            # Highlight the code
            highlighted_code = highlight(code_part, PythonLexer(), SvgFormatter())
            header_utf_8 = '<?xml version="1.0" encoding="UTF-8"?>'
            highlighted_code = highlighted_code.split("\n", 1)[1]
            highlighted_code = header_utf_8 + highlighted_code

            # Set font to Arial 12
            highlighted_code = highlighted_code.replace("font-family=\"monospace\"", "font-family=\"Arial\"")
            highlighted_code = highlighted_code.replace("font-size=\"14px\"", "font-size=\"12\"")

            # Find any <text> tags and set the font to Arial 12
            highlighted_code = highlighted_code.replace("<text", "<text font-family=\"Arial\" font-size=\"12\"")

            # Add size to the svg
            height_overall = len(code_part.split("\n")) * label_height
            width_max = 1.05 * np.max([pdfmetrics.stringWidth(line, "Arial", 12) for line in code_part.split("\n")])
            highlighted_code = highlighted_code.replace("<svg", f"<svg width='{width_max}' height='{height_overall}'")

            filename = "temp" + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + ".svg"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(highlighted_code)

            # Upscale the SVG so the text is readable
            scale_factor = 5
            upscale_svg(filename, scale_factor)

            # Get the dimensions of the image
            img = fitz.open(filename)
            # Upscale the image when in the PDF
            img = img[0].get_pixmap()
            img = Image.frombytes("RGB", (img.w, img.h), img.samples)
            filename_png = filename.replace(".svg", ".png")
            img.save(filename_png)
            os.remove(filename)

            # # Draw the image
            x = x_margin
            new_width = img.width / scale_factor
            new_height = img.height / scale_factor
            c.drawImage(filename_png, x, y - new_height, width=new_width, height=new_height)
            os.remove(filename_png)

            y -= new_height

            # Draw the remaining text
            question_text = question.split("<CODE>")
            if len(question_text) > 1:
                question_text = question_text[1]
                lines = wrap_text(question_text, letter[0] - 3 * x_margin, "Arial", 12)
                for line in lines:
                    c.drawString(x, y, line)
                    y -= label_height
                    x = x_margin

            y -= label_height
        # Normal text
        else:
            # Question may have LaTeX math in it
            char_index = 0
            question_text = ""
            # Char stream
            x_so_far = x
            while char_index < len(question):
                current_char = question[char_index]
                if current_char == "$":
                    # First draw the text so far
                    lines = wrap_text(question_text, letter[0] - 3 * x_margin, "Arial", 12, first_width=x_so_far)
                    for line in lines:
                        c.drawString(x_so_far, y, line)
                        y -= label_height
                        x_so_far = x_margin
                    y += label_height
                    x_so_far += c.stringWidth(lines[-1], "Arial", 12)
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

                    # Draw the image
                    c.drawImage(latex, x_so_far, y - new_height / 4, width=new_width, height=new_height)
                    os.remove(latex)

                    x_so_far += new_width
                    if x_so_far > letter[0] - 3 * x_margin:
                        x_so_far = x_margin
                        y -= label_height

                    # Update the char index
                    char_index = end_index + 1
                else:
                    question_text += current_char
                    char_index += 1

            # Draw the remaining text
            lines = wrap_text(question_text, letter[0] - 3 * x_margin, "Arial", 12, first_width=x_so_far)
            for line in lines:
                c.drawString(x_so_far, y, line)
                y -= label_height
                x = x_margin
                x_so_far = x

        answers_height = 0
        for j, answer in enumerate(answers):
            answer_letter = chr(65 + j) + "."
            lines = wrap_text(answer_letter + " " + answer, letter[0] - 3 * x_margin, "Arial", 12)
            answers_height += len(lines) * label_height

        if y - answers_height < y_margin / 2:
            # Draw page number before starting a new page
            c.drawString(letter[0] / 2, y_margin / 2, str(c.getPageNumber()))
            y = letter[1] - y_margin
            c.showPage()
            c.setFont("Arial", 12)
            c.line(x, y + 10, letter[0] - x_margin, y + 10)
            y -= y_spacing

        for j, answer in enumerate(answers):
            x_answer = x + 20
            answer_letter = chr(65 + j) + "."
            answer = answer_letter + " " + answer.replace("$$", "$")

            # Answer may have LaTeX math in it
            char_index = 0
            answer_text = ""
            x_so_far = x_answer

            # Char stream
            while char_index < len(answer):
                current_char = answer[char_index]
                if current_char == "$":
                    # First draw the text so far
                    lines = wrap_text(answer_text, letter[0] - 3 * x_margin, "Arial", 12, first_width=x_so_far)
                    for line in lines:
                        c.drawString(x_so_far, y, line)
                        y -= label_height
                        x_so_far = x_answer
                    y += label_height
                    x_so_far += c.stringWidth(lines[-1], "Arial", 12)
                    answer_text = ""

                    # Find the end of the math expression
                    answer_substr = answer[char_index:]
                    end_index = answer_substr.find("$", 1) + char_index
                    # Add the math expression to the answer text
                    latex_text = answer[char_index + 1:end_index]
                    latex = latex_to_img(latex_text, font_size=120)

                    # Get the dimensions of the image
                    img = plt.imread(latex)
                    height, width = img.shape[:2]
                    new_height = height / 14
                    new_width = width / 14

                    # Draw the image
                    c.drawImage(latex, x_so_far, y - new_height / 4, width=new_width, height=new_height)
                    os.remove(latex)

                    x_so_far += new_width
                    if x_so_far > letter[0] - 3 * x_margin:
                        x_so_far = x_answer
                        y -= label_height

                    # Update the char index
                    char_index = end_index + 1
                else:
                    answer_text += current_char
                    char_index += 1

            # Draw the remaining text
            lines = wrap_text(answer_text, letter[0] - 3 * x_margin, "Arial", 12, first_width=x_so_far)
            for line in lines:
                c.drawString(x_so_far, y, line)
                y -= label_height
                x_answer = x + 20
                x_so_far = x_answer

    # Draw page number on the last page
    c.drawString(letter[0] / 2, y_margin / 2, str(c.getPageNumber()))
    c.showPage()

    # Check if the last page was even or odd (if odd, add a blank page)
    if c.getPageNumber() % 2 == 0:
        c.showPage()

    c.save()


def generate_question_paper(student_id, student_questions, question_answers, date, student_name):
    file_path = 'generated_pdfs/' + str(student_id) + '_question_paper.pdf'
    draw_labels(student_id, student_questions, question_answers, file_path, date, student_name)
