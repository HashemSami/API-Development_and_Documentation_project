from flask import Request
from typing import List
from models import Question

QUESTIONS_PER_PAGE = 10


def paginate_questions(request_obj: Request, selection: List[Question]):
    page = request_obj.args.get("page", 1, type=int)

    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    books: List[Question] = [question.format() for question in selection]

    current_questions = books[start:end]
    return current_questions
