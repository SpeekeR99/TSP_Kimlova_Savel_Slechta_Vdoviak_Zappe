import json
import numpy as np

# Config filepath
CONFIG_FILE = "config.json"


def load_config(config_file_path=CONFIG_FILE):
    """
    Load the configuration file
    :param config_file_path: Path to the configuration file
    :return: Configuration as a dictionary
    """
    try:
        with open(config_file_path, "r", encoding="utf-8") as fp:
            config = json.load(fp)
    except FileNotFoundError:
        print("ERROR: Config file not found! Please create a config file.")
        exit(1)
    except json.JSONDecodeError:
        print("ERROR: Config file is not a valid JSON file!")
        exit(1)
    except Exception as e:
        print(f"ERROR: {e}")
        exit(1)

    return config


def get_A4_size():
    """
    Get the A4 paper size in inches
    :return: A4 paper size in inches
    """
    cm = 1 / 2.54  # Centimeters in inches
    A4 = (29.7 * cm, 21.0 * cm)
    
    return A4


def get_max_num_of_rects_in_page(config, A4):
    """
    Calculate the maximum number of rectangles that can fit in a page
    :param config: Configuration dictionary
    :param A4: A4 paper size in inches
    :return: Maximum number of rectangles that can fit in a page
    """
    # Offset between rectangles
    offset_between_rect = config["rect_settings"]["rect_space_between"]

    # Calculate the number of rectangles that can fit in the figure
    num_of_rects_per_page = 0
    aspect_ratio = A4[0] / A4[1]
    width_so_far = config["student_id_rect"]["width"] + 2 * offset_between_rect  # Every page has student ID field

    while width_so_far < aspect_ratio - config["answer_rect"]["width"] - 1.5 * offset_between_rect:
        width_so_far += config["answer_rect"]["width"] + 1.5 * offset_between_rect
        num_of_rects_per_page += 1

    return num_of_rects_per_page


def get_num_of_rects_per_page(num_of_rect, num_of_pages, num_of_rects_per_page):
    """
    Calculate the number of rectangles in each page
    :param num_of_rect: Total number of rectangles
    :param num_of_pages: Total number of pages
    :param num_of_rects_per_page: Number of rectangles that can fit in a page
    :return: List of number of rectangles in each page
    """
    # Calculate the number of rectangles in each page
    num_of_rects_in_page = []
    for page in range(num_of_pages):
        # If it is the last page and the last rectangle has fewer questions than the rest
        if page == num_of_pages - 1 and num_of_rect % num_of_rects_per_page != 0:
            num_of_rects_in_page.append(num_of_rect % num_of_rects_per_page)
        # Otherwise, add the maximum number of rectangles that can fit in a page
        else:
            num_of_rects_in_page.append(num_of_rects_per_page)

    return num_of_rects_in_page


def transform_eval_output_to_moodle(json_data, db_data):
    """
    Transform the evaluation output to a Moodle happy output
    :param json_data: Evaluation output
    :param db_data: Data from the database
    :return: JSON response containing the student ID and answers
    """
    student_id = int(json_data["student_id"])
    questions = db_data["questions"]
    student_answers = json_data["answers"]
    student_dict = {}
    for student in db_data["students"]:
        if student["id"] == student_id:
            student_dict = student

    result = {
        "lastname": student_dict["surname"],
        "firstname": student_dict["name"],
        "emailaddress": "-",
        "state": "Finished",
        "startedon": "-",
        "completed": "-",
        "timetaken": "-",
        "grade1000": "-"
    }

    shuffle = student_dict["shuffle"]
    undo_shuffler = np.argsort(shuffle)
    unshuffled_answers = [student_answers[i] for i in undo_shuffler]

    for i, question in enumerate(questions):
        answers = question["answers"]
        student_answers = unshuffled_answers[i]
        for j, answer in enumerate(answers):
            student_answer = student_answers[j]
            if student_answer == 1:
                answer_value = answer["text"]
                if answer_value == "true":
                    answer_value = "Pravda"
                elif answer_value == "false":
                    answer_value = "Nepravda"
                result[f"response{i + 1}"] = answer_value

    return [[result]]
