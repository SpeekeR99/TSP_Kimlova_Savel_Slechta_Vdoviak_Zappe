from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def draw_labels(labels, filename):
    c = canvas.Canvas(filename, pagesize=letter)

    # Define label dimensions and spacing
    label_width = 100
    label_height = 50
    x_margin = 50
    y_margin = 50
    x_spacing = 10
    y_spacing = 10

    # Draw labels
    x = x_margin
    y = letter[1] - y_margin
    for label in labels:
        c.drawString(x, y, label)
        x += label_width + x_spacing
        if x + label_width + x_spacing > letter[0]:
            x = x_margin
            y -= label_height + y_spacing
            if y - y_spacing < 0:
                c.showPage()
                y = letter[1] - y_margin

    c.showPage()
    c.save()


def generate_question_paper(test_length, student_id):
    labels = ["Label 1", "Label 2", "Label 3", "Label 4", "Label 5"]
    draw_labels(labels, "labels.pdf")
