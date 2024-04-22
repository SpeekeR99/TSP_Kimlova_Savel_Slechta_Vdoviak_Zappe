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

        question_number = "Otázka " + str(i + 1)
        c.drawString(x, y, question_number + ": " + question)
        y -= (label_height + y_spacing / 2)

        for i, answer in enumerate(answers):
            x_answer = x + 20
            question_letter = chr(65 + i) + "."
            c.drawString(x_answer, y, question_letter + " " + answer)
            y -= (label_height + y_spacing / 5)

        # if questions do not fit one page
        if y - (label_height + y_spacing) < 0:
            # Draw page number before starting a new page
            c.drawString(letter[0] / 2, y_margin / 2, str(c.getPageNumber()))
            y = letter[1] - y_margin
            c.showPage()

    # Draw page number on the last page
    c.drawString(letter[0] / 2, y_margin / 2, str(c.getPageNumber()))

    c.showPage()
    c.save()


def generate_question_paper(student_id, student_questions, question_answers):
    file_path = '../generated_pdfs/' + str(student_id) + '_question_paper.pdf'
    draw_labels(student_id, student_questions, question_answers, file_path)
