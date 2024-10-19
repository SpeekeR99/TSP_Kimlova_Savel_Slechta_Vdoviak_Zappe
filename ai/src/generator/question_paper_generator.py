import pdfkit
import fitz


def draw_labels(student_id, student_questions, question_answers, filename, date, student_name):
    # TODO: This dependency needs to be resolved in the future
    path_to_wkhtmltopdf = r"C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe"

    # Initialize the HTML string
    html_string = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            * { font-size: 14pt; font-family: Arial; }
        </style>
    </head>
    <script type="text/x-mathjax-config">
      MathJax.Hub.Config({tex2jax: {inlineMath: [['$', '$']]}, "HTML-CSS": {scale: 200}});
    </script>
    <script type="text/javascript"
      src="http://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
    </script>
    <body>
    """
    html_string += f"""
    <div style='word-wrap: break-word;'>
    <h1><b>Otázky k testu</b></h1>
    <b>Jméno</b>: {student_name}<br>
    <b>Datum</b>: {date}<br>
    <b>ID Studenta</b>: {student_id}<br>
    </div><hr>
    """

    # Add the questions and answers to the HTML string
    for i in range(len(student_questions)):
        question = student_questions[i]
        answers = question_answers[i]

        # Replace the $$ with $ for MathJax
        question = question.replace("$$", "$")

        html_string += f"""
        <div style='word-wrap: break-word;'>
        <b>Otázka {i + 1}</b>: {question}<br>
        <div style='margin-left: 50px;'>
        """

        for j, answer in enumerate(answers):
            # Replace the $$ with $ for MathJax
            answer = answer.replace("$$", "$").replace("<br>", "")

            answer_letter = chr(65 + j) + "."
            html_string += f"<b>{answer_letter}</b> {answer}<br>"

        html_string += "</div></div><hr>"

    html_string += "</body></html>"

    config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
    options = {
        "footer-center": "[page] / [topage]",
        "footer-font-size": 10,
        "javascript-delay": 1000,  # Wait for MathJax to render
    }

    # Generate the PDF
    pdfkit.from_string(html_string, filename, configuration=config, options=options)

    # Add a blank page if the number of pages is odd
    doc = fitz.open(filename)
    if doc.page_count % 2 != 0:
        doc.new_page()
        doc.saveIncr()
    doc.close()


def generate_question_paper(student_id, student_questions, question_answers, date, student_name):
    file_path = 'generated_pdfs/' + str(student_id) + '_question_paper.pdf'
    draw_labels(student_id, student_questions, question_answers, file_path, date, student_name)
