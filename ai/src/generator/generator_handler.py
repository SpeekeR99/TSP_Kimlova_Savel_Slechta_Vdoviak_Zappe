import os
import fitz
import random
import uuid
import numpy as np

from ai.src.generator.bubble_sheet_generator import generate_bubble_sheet
from ai.src.generator.question_paper_generator import generate_question_paper


class Student:
    def __init__(self, id, name, surname, student_number):
        self.id = id
        self.name = name
        self.surname = surname
        self.student_number = student_number
        self.shuffle = []

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "student_number": self.student_number,
            "shuffle": self.shuffle
        }


class Question:
    def __init__(self, question_id, type, text, answers, default_grade=None, penalty=None):
        self.question_id = question_id
        self.type = type
        self.text = text
        self.answers = answers
        self.default_grade = default_grade
        self.penalty = penalty

    def to_dict(self):
        return {
            "question_id": self.question_id,
            "type": self.type,
            "text": self.text,
            "answers": self.answers,
            "default_grade": self.default_grade,
            "penalty": self.penalty
        }


def preprocess_data(students_json, questions_json):
    student_id = 0
    students = []
    for student in students_json:
        students.append(Student(student_id, student["jmeno"], student["prijmeni"], student["os_cislo"]))
        student_id += 1

    questions = []
    for question in questions_json:
        questions.append(Question(question["id"], question["type"], question["text"], question["answers"], question["defaultGrade"], question["penalty"]))

    return students, questions


def shuffled_questions(questions_list):
    shuffled_list = questions_list.copy()
    shuffler = np.random.permutation(len(shuffled_list))
    shuffled_list = [shuffled_list[i] for i in shuffler]
    return shuffler, shuffled_list


def generate_sheets(collection, questions_json, students_json):
    students, questions = preprocess_data(students_json, questions_json)
    test_id = uuid.uuid4().hex
    test_length = len(questions)

    for student in students:
        # generate bubble sheet with unique id for every student
        generate_bubble_sheet(test_id, student.id)

        # generate question paper with unique set of questions
        shuffler, student_questions = shuffled_questions(questions)
        student.shuffle = shuffler.tolist()

        questions_text = [question.text for question in student_questions]
        answers_text = []
        for question in student_questions:
            answers_text.append([answer["text"] for answer in question.answers])

        generate_question_paper(student.id, questions_text, answers_text)

    collection.insert_one(
        {
            "test_id": test_id,
            "num_of_questions": test_length,
            "students": [student.to_dict() for student in students],
            "questions": [question.to_dict() for question in questions]
        }
    )

    pdfs_q = [f"generated_pdfs/{student.id}_question_paper.pdf" for student in students]
    pdfs_a = [f"generated_pdfs/{student.id}_bubble_sheet.pdf" for student in students]

    merged_pdf_q = fitz.open()
    merged_pdf_a = fitz.open()

    for pdf_q in pdfs_q:
        merged_pdf_q.insert_pdf(fitz.open(pdf_q))
    for pdf_a in pdfs_a:
        merged_pdf_a.insert_pdf(fitz.open(pdf_a))

    merged_pdf_q.save("generated_pdfs/question_papers.pdf")
    merged_pdf_a.save("generated_pdfs/bubble_sheets.pdf")

    for pdf in pdfs_q + pdfs_a:
        os.remove(pdf)
