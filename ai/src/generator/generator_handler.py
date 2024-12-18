import os
import fitz
import uuid
import numpy as np
import copy

from ai.src.generator.bubble_sheet_generator import generate_bubble_sheet
from ai.src.generator.question_paper_generator import generate_question_paper


class Student:
    """
    Class representing a student
    """
    def __init__(self, id, name, surname, student_number, username, email):
        """
        Initialize the student
        :param id: Our internal ID
        :param name: Name of the student
        :param surname: Surname of the student
        :param student_number: Student number (os_cislo)
        """
        self.id = id
        self.name = name
        self.surname = surname
        self.student_number = student_number
        self.username = username
        self.email = email
        self.shuffle = []

    def to_dict(self):
        """
        Convert the student to a dictionary
        :return: Dictionary representation of the student
        """
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "student_number": self.student_number,
            "username": self.username,
            "email": self.email,
            "shuffle": self.shuffle,
        }


class Question:
    """
    Class representing a question
    """
    def __init__(self, question_id, type, name, text, answers, default_grade=None, penalty=None):
        """
        Initialize the question
        :param question_id: Question ID
        :param type: Type of the question
        :param name: Name of the question
        :param text: Text of the question
        :param answers: Answers to the question
        :param default_grade: Default grade
        :param penalty: Penalty
        """
        self.question_id = question_id
        self.type = type
        self.name = name
        self.text = text
        self.answers = answers
        self.default_grade = default_grade
        self.penalty = penalty

    def to_dict(self):
        """
        Convert the question to a dictionary
        :return: Dictionary representation of the question
        """
        return {
            "question_id": self.question_id,
            "type": self.type,
            "name": self.name,
            "text": self.text,
            "answers": self.answers,
            "default_grade": self.default_grade,
            "penalty": self.penalty
        }


def preprocess_data(students_json, questions_json):
    """
    Preprocess the data from the JSON files from the request
    :param students_json: Students JSON
    :param questions_json: Questions JSON
    :return: Students and questions (as objects)
    """
    student_id = 0
    students = []
    for student in students_json:
        students.append(Student(student_id, student["jmeno"], student["prijmeni"], student["osCislo"], student["userName"], student["email"]))
        student_id += 1

    questions = []
    for question in questions_json:
        questions.append(Question(question["id"], question["type"], question["name"][0], question["text"], question["answers"], question["defaultGrade"], question["penalty"]))

    return students, questions


def shuffled_questions(questions_list):
    """
    Shuffle the questions
    :param questions_list: List of questions
    :return: Shuffler and shuffled list
    """
    # Shuffle the questions
    shuffled_list = copy.deepcopy(questions_list)
    shuffler = np.random.permutation(len(shuffled_list))
    shuffled_list = [shuffled_list[i] for i in shuffler]

    # Shuffle the answers as well
    answer_shufflers = []
    for question in shuffled_list:
        answer_shuffler = np.random.permutation(len(question.answers))
        question.answers = [question.answers[i] for i in answer_shuffler]
        answer_shufflers.append(answer_shuffler)

    shuffle = []
    for i in range(len(shuffler)):
        shuffle.append({"question": shuffler[i].tolist(), "answers": answer_shufflers[i].tolist()})

    return shuffle, shuffled_list


def generate_sheets(collection, questions_json, students_json, date, gc=False):
    """
    Generate bubble sheets and question papers for the students
    :param collection: DB collection
    :param questions_json: Questions JSON (from the request)
    :param students_json: Students JSON (from the request)
    :param date: Date of the test
    """
    students, questions = preprocess_data(students_json, questions_json)
    test_id = uuid.uuid4().hex
    test_length = len(questions)

    for student in students:
        student_name = student.name + " " + student.surname

        # generate bubble sheet with unique id for every student
        generate_bubble_sheet(test_id, student.id, test_length, date, student_name)

        # generate question paper with unique set of questions
        shuffle, student_questions = shuffled_questions(questions)
        student.shuffle = shuffle

        questions_text = [f"({int(float(question.default_grade))}b) {question.name}\n{question.text}" for question in student_questions]
        answers_text = []
        for question in student_questions:
            answers_text.append([answer["text"] for answer in question.answers])

        generate_question_paper(student.id, questions_text, answers_text, date, student_name)

    # Save the data to the database
    collection.insert_one(
        {
            "test_id": test_id,
            "gc": gc,
            "num_of_questions": test_length,
            "students": [student.to_dict() for student in students],
            "questions": [question.to_dict() for question in questions]
        }
    )

    # Generate one student-less bubble sheet
    generate_bubble_sheet(test_id, "empty", test_length, date, "")

    if not os.path.exists("generated_pdfs"):
        os.makedirs("generated_pdfs")

    pdfs_q = [f"generated_pdfs/{student.id}_question_paper.pdf" for student in students]
    pdfs_a = ["generated_pdfs/empty_bubble_sheet.pdf"] + [f"generated_pdfs/{student.id}_bubble_sheet.pdf" for student in students]

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
