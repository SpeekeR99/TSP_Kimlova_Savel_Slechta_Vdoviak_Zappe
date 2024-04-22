from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


def draw_labels(student_id, student_questions, question_answers, filename):
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
    for i in range(len(student_questions)):
        question = student_questions[i]
        answers = question_answers[i]

        c.drawString(x, y, question)
        y -= (label_height + y_spacing)

        for answer in answers:
            c.drawString(x, y, answer)
            y -= (label_height + y_spacing)

        # if questions does not fit one page
        if y - (label_height + y_spacing) < 0:
            y = letter[1] - y_margin
            c.showPage()

    c.showPage()
    c.save()


def generate_question_paper(student_id, student_questions, question_answers):
    file_path = '../generated_pdfs/' + str(student_id) + '_question_paper.pdf'
    draw_labels(student_id, student_questions, question_answers, file_path)
