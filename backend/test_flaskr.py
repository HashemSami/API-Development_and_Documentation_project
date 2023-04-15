import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import Question, Category, db


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""

        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            "student", "student", "localhost:5432", self.database_name
        )

        self.app = create_app({"SQLALCHEMY_DATABASE_URI": self.database_path})

        self.client = self.app.test_client

        # binds the app to the current context
        with self.app.app_context():
            db.create_all()

        self.new_question = {
            "question": "What is the diameter of Earth?",
            "answer": "12756 km",
            "category": 3,
            "difficulty": 5,
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_all_getegories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["categories"]))

    def test_get_all_getegories_not_valid_method(self):
        res = self.client().post("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")

    def test_get_valid_questions_page(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["questions"]))

    def test_get_beyond_valid_questions_page(self):
        res = self.client().get("/questions?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_create_new_question(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_create_new_question_failure(self):
        res = self.client().post("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")

    def test_delete_question(self):
        # get the question to make sure the we deleted an existing data
        res = self.client().post("/questions", json={"searchTerm": "diameter"})
        data = json.loads(res.data)["questions"][0]

        res = self.client().delete("/questions/{}".format(data["id"]))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_delete_question_not_valid(self):
        res = self.client().delete("/questions/550")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_get_question_search_with_results(self):
        res = self.client().post("/questions", json={"searchTerm": "royal"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])

    def test_get_question_search_without_results(self):
        res = self.client().post(
            "/questions", json={"searchTerm": "applejacks"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["total_questions"], 0)

    def test_get_questions_by_category(self):
        res = self.client().get("/categories/6/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["current_category"], "Sports")

    def test_get_questions_by_category_not_valid(self):
        res = self.client().get("/categories/500/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_get_next_quizzes(self):
        res = self.client().post(
            "/quizzes",
            json={"previous_questions": [19, 17], "quiz_category": {"id": 2}},
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["question"]["category"], 2)

    def test_get_next_quizzes_not_valid(self):
        res = self.client().post(
            "/quizzes",
            json={
                "previous_questions": [19, 17],
                "quiz_category": {"id": 500},
            },
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
