from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


def draw_labels(labels, student_id, filename):
    c = canvas.Canvas(filename, pagesize=letter)

    # set font
    pdfmetrics.registerFont(TTFont("Arial", "arial.ttf"))
    c.setFont("Arial", 12)  # Set the font and size

    # Define label dimensions and spacing
    label_height = 20
    x_margin = 50
    y_margin = 50
    y_spacing = 10

    # Draw student_id labels
    x = x_margin
    y = letter[1] - y_margin
    c.drawString(x, y, str(student_id))
    y -= (label_height + y_spacing)

    # draw questions labels
    for label in labels:
        c.drawString(x, y, label)
        y -= (label_height + y_spacing)

        # if questions does not fit one page
        if y - (label_height + y_spacing) < 0:
            y = letter[1] - y_margin
            c.showPage()

    c.showPage()
    c.save()


def generate_question_paper(student_questions, student_id):
    file_path = '../generated_pdfs/' + str(student_id) + '_question_paper.pdf'
    draw_labels(student_questions, student_id, file_path)
