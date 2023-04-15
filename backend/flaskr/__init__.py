from flask import Flask, request, abort, jsonify, Request
from flask_cors import CORS
import random
import sys

from models import Question, Category, db, database_path
from utils import paginate_questions


def current_category():
    current_category = "All"

    def get_current_category():
        return current_category

    def set_current_category(category):
        nonlocal current_category
        current_category = category

    return get_current_category, set_current_category


get_current_category, set_current_category = current_category()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    # bind production database
    app.config.from_mapping(SQLALCHEMY_DATABASE_URI=database_path)

    # if in testing, bind test config
    if test_config is not None:
        app.config.from_mapping(test_config)

    # binding thr app with the database
    db.init_app(app)

    with app.app_context():
        db.create_all()

    CORS(app, origins=["*"])

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    @app.route("/categories")
    def retrieve_catagory():
        error = False
        try:
            categories = Category.query.order_by(Category.type).all()
            formated_categories = {
                c["id"]: c["type"] for c in [c.format() for c in categories]
            }

            return jsonify(
                {
                    "success": True,
                    "categories": formated_categories,
                    "total_categories": len(formated_categories),
                }
            )

        except Exception:
            error = True
            db.session.rollback()
            print(sys.exc_info())

        finally:
            db.session.close()
            if error is True:
                abort(400)

    @app.route("/questions")
    def retrieve_questions():
        error = False
        current_questions = []
        total_questions = 0

        try:
            categories = Category.query.order_by(Category.type).all()
            formated_categories = {
                c["id"]: c["type"] for c in [c.format() for c in categories]
            }

            questions = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, questions)

            total_questions = len(questions)

            return jsonify(
                {
                    "success": True,
                    "questions": current_questions,
                    "total_questions": total_questions,
                    "categories": formated_categories,
                    "current_category": get_current_category(),
                }
            )

        except Exception:
            error = True
            db.session.rollback()
            print(sys.exc_info())

        finally:
            db.session.close()

            if len(current_questions) == 0:
                abort(404)

            if error is True:
                abort(400)

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        error = False
        question: Question | None = None
        try:
            question = Question.query.filter(
                Question.id == question_id
            ).one_or_none()

            if question is not None:
                question.delete()

        except Exception:
            error = True
            db.session.rollback()
            print(sys.exc_info())

        finally:
            db.session.close()

            if question is None:
                abort(404)

            if error is True:
                abort(400)

            else:
                return jsonify(
                    {
                        "success": True,
                        "deleted_id": question_id,
                    }
                )

    @app.route("/questions", methods=["POST"])
    def create_question():
        body: Request = request.get_json()

        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_category = body.get("category", None)
        new_difficulty = body.get("difficulty", None)
        search = body.get("searchTerm", None)

        error = False
        # question: Question | None
        try:
            if search is not None:
                selection = Question.query.order_by(Question.id).filter(
                    Question.question.ilike("%{}%".format(search))
                )

                current_questions = paginate_questions(request, selection)

                return jsonify(
                    {
                        "success": True,
                        "questions": current_questions,
                        "total_questions": len(selection.all()),
                        "current_category": get_current_category(),
                    }
                )

            else:
                question = Question(
                    question=new_question,
                    answer=new_answer,
                    category=new_category,
                    difficulty=new_difficulty,
                )

                question.insert()

                return jsonify(
                    {
                        "success": True,
                    }
                )

        except Exception:
            error = True
            db.session.rollback()
            print(sys.exc_info())

        finally:
            db.session.close()

            if error is True:
                abort(422)

    @app.route("/categories/<int:category_id>/questions")
    def retrieve_questions_by_catagory(category_id):
        error = False
        formated_questions = []
        category: Category | None = None
        try:
            category: Category = Category.query.filter(
                Category.id == category_id
            ).one_or_none()

            if category is not None:
                questions = Question.query.filter_by(
                    category=category_id
                ).all()

                formated_questions = [q.format() for q in questions]

                set_current_category(category.format()["type"])

                return jsonify(
                    {
                        "success": True,
                        "questions": formated_questions,
                        "total_questions": len(formated_questions),
                        "current_category": get_current_category(),
                    }
                )

        except Exception:
            error = True
            db.session.rollback()
            print(sys.exc_info())

        finally:
            db.session.close()

            if category is None:
                abort(404)

            if error is True:
                abort(400)

    @app.route("/quizzes", methods=["POST"])
    def retrieve_quiz_question():
        body: Request = request.get_json()

        previous_questions = body.get("previous_questions", None)
        quiz_category = body.get("quiz_category", None)

        error = False
        category: Category | None = None
        try:
            category = Category.query.filter(
                Category.id == quiz_category["id"]
            ).one_or_none()

            questions: Question = Question.query.filter(
                db.and_(
                    Question.category == category.id,
                    Question.id.notin_([q for q in previous_questions]),
                )
                if category is not None
                else Question.id.notin_([q for q in previous_questions])
            ).all()

            random_question = None

            if len(questions) > 0:
                formated_questions = [q.format() for q in questions]
                random_question = random.choice(formated_questions)

            return jsonify(
                {
                    "success": True,
                    "question": random_question,
                }
            )

        except Exception:
            error = True
            db.session.rollback()
            print(sys.exc_info())

        finally:
            db.session.close()

            if category is None and quiz_category["id"] != 0:
                abort(404)

            if error is True:
                abort(400)

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 404,
                    "message": "resource not found",
                }
            ),
            404,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify(
                {"success": False, "error": 400, "message": "bad request"}
            ),
            400,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify(
                {"success": False, "error": 422, "message": "unprocessable"}
            ),
            422,
        )

    @app.errorhandler(500)
    def server_error(error):
        return (
            jsonify(
                {"success": False, "error": 500, "message": "server error"}
            ),
            500,
        )

    @app.errorhandler(405)
    def method_not_allowed(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 405,
                    "message": "method not allowed",
                }
            ),
            405,
        )

    return app
