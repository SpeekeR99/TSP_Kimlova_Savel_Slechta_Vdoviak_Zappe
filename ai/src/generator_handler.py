import random

from ai.src.bubble_sheet_generator import generate_bubble_sheet
from ai.src.question_paper_generator import generate_question_paper
from ai.src.utils import load_config


class Student:
    def __init__(self, id, name, student_number):
        self.id = id
        self.name = name
        self.student_number = student_number


class Question:
    def __init__(self, question_id, type, text, answers, default_grade=None, penalty=None):
        self.question_id = question_id
        self.type = type
        self.text = text
        self.answers = answers
        self.default_grade = default_grade
        self.penalty = penalty


def prepare_mock_students():
    students = [
        Student(1, "Alice", "A20B0001P"),
        Student(2, "Bob", "A21N0001P"),
        Student(3, "Oskar", "A20B0002P"),
        Student(4, "Mock Student", "A20B0003P"),
    ]

    return students


def preprocess_data(json_data):
    # students_data = json_data['students']
    questions_data = json_data

    # students = [Student(student['id'], student['name'], student['student_number']) for student in students_data]
    students = prepare_mock_students()
    questions = []
    for question in questions_data:
        questions.append(Question(question["id"], question["type"], question["text"], question["answers"], question["defaultGrade"], question["penalty"]))

    return students, questions


def shuffled_questions(questions_list, test_length):
    shuffled_list = questions_list.copy()
    random.shuffle(shuffled_list)
    student_questions = shuffled_list[:test_length]
    for question in student_questions:
        random.shuffle(question.answers)
    return shuffled_list[:test_length]


def generate_sheets(json_data):
    # Load the configuration file
    config = load_config()

    students, questions = preprocess_data(json_data)

    # number of questions in each test
    test_length = config["number_of_questions"]
    for student in students:

        # generate bubble sheet with unique id for every student
        generate_bubble_sheet(student.id)

        # generate question paper with unique set of questions
        student_questions = shuffled_questions(questions, test_length)
        questions_text = [question.text for question in student_questions]
        answers_text = []
        for question in student_questions:
            answers_text.append([answer["text"] for answer in question.answers])
        generate_question_paper(student.id, questions_text, answers_text)
