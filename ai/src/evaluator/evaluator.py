import numpy as np

from ai.src.utils import load_config


def transform_eval_output(json_data, db_data):
    """
    Transform the evaluation output to a Moodle happy output
    :param json_data: Evaluation output
    :param db_data: Data from the database
    :return: JSON response containing the student ID and answers
    """
    # Get the data from the JSON and the database
    student_id = int(json_data["student_id"])
    questions = db_data["questions"]
    student_answers = json_data["answers"]
    student_dict = {}
    for student in db_data["students"]:
        if student["id"] == student_id:
            student_dict = student

    # Check if the student was found in the database (most likely due to bad ID detection)
    if "name" not in student_dict.keys():
        return None, None

    # Check if the GC penalty is enabled (aka if the import used is Moodle or GC)
    gc_multiplier = 1
    if "gc" in db_data.keys() and db_data["gc"]:
        config = load_config()
        gc_multiplier = config["gc_multiplier"]

    # Prepare the result and log
    result = {
        "jmeno": student_dict["name"],
        "prijmeni": student_dict["surname"],
        "os_cislo": student_dict["student_number"],
        "login": student_dict["username"],
        "email": student_dict["email"],
        "result": []
    }

    log = f"Student: {student_dict['name']} {student_dict['surname']}; {student_dict['username']}; {student_dict['student_number']}\n"
    log += "Results: "
    for i, answers in enumerate(student_answers):
        log += f"{str(i + 1)}"
        for j, answer in enumerate(answers):
            if answer == 1:
                log += f"{chr(65 + j)}"
        log += "; "
    # Throw away the last "; "
    log = log[:-2]

    # Undo shuffle
    shuffle = student_dict["shuffle"]
    question_undo_shuffle = []
    answers_undo_shuffles = []
    # Shuffle is a list of dictionaries, where each dictionary contains the question number and shuffled answers
    for obj in shuffle:
        question_undo_shuffle.append(obj["question"])
        answers_undo_shuffles.append(obj["answers"])
    # Sort the questions and answers according to the shuffle
    question_undo_shuffle = np.argsort(question_undo_shuffle)
    answers_undo_shuffles = [np.argsort(answers) for answers in answers_undo_shuffles]

    # Undo the shuffle
    unshuffled_answer_arrays = [student_answers[i] for i in question_undo_shuffle]
    answers_undo_shuffles = [answers_undo_shuffles[i] for i in question_undo_shuffle]

    # Prepare the final answers
    final_answers = []
    for i, answer_array in enumerate(unshuffled_answer_arrays):
        unshuffled_answers = [answer_array[j] for j in answers_undo_shuffles[i]]
        final_answers.append(unshuffled_answers)

    # Calculate the points (evaluation starts here)
    points = 0
    overall_points = 0

    for i, question in enumerate(questions):
        # Get the question points and correct answers
        question_points = float(question["default_grade"])
        correct_answers = question["answers"]
        answers = final_answers[i]

        overall_points += question_points
        fraction = 0

        obj = {"question": {"name": question["name"], "text": question["text"]}, "answer": []}
        for j, answer in enumerate(answers):
            if answer == 1:
                try:
                    obj["answer"].append(chr(65 + j))
                    # obj["answer"].append(correct_answers[j]["text"])
                    fraction += float(correct_answers[j]["fraction"])
                except IndexError:
                    pass

        # GC penalty can be lowered, because the points are in range <-max; max> by default
        # if gc_multiplier is 1, it does not change anything, otherwise it scales accordingly (0 is the other extreme)
        fraction *= gc_multiplier

        # Fraction is in range <-100; 100>, so we need to scale it to <-1; 1>
        question_points *= np.round((fraction / 100), 2)
        points += question_points
        obj["points"] = question_points

        result["result"].append(obj)

    # Add the final points to the result
    result["body"] = np.round(points, 2)
    result["body_celkem"] = overall_points
    result["body_rel"] = np.round(points / overall_points, 2)

    return result, log
