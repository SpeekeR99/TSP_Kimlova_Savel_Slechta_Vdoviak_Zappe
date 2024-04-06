import random

from ai.src.bubble_sheet_generator import generate_bubble_sheet
from ai.src.question_paper_generator import generate_question_paper


class Student:
    def __init__(self, id, name, student_number):
        self.id = id
        self.name = name
        self.student_number = student_number


class Question:
    def __init__(self, question_id, question_text, options, correct_answer):
        self.question_id = question_id
        self.question_text = question_text
        self.options = options
        self.correct_answer = correct_answer


def preprocess_data(json_data):
    students_data = json_data['students']
    questions_data = json_data['questions']

    students = [Student(student['id'], student['name'], student['student_number']) for student in students_data]
    questions = [
        Question(question['id'], question['question_text'], question['options'], question['correct_answer']) for
        question in questions_data]

    return students, questions


def shuffled_questions(questions_list, test_length):
    shuffled_list = questions_list.copy()
    random.shuffle(shuffled_list)
    return shuffled_list[:test_length]


def generate_sheets(json_data):
    students, questions = preprocess_data(json_data)

    # number of questions in each test
    test_length = 5
    for student in students:

        # generate bubble sheet with unique id for every student
        generate_bubble_sheet(test_length, student.id)

        # generate question paper with unique set of questions
        student_questions = shuffled_questions(questions, test_length)
        questions_text = [question.question_text for question in student_questions]
        generate_question_paper(questions_text, student.id)
