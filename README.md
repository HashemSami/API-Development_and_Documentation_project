## Overview

This project is for Udacity full stack developer Nanodegree. Student can create an API (Application Programing Interface) to manage a pre-built web Trivia web app that can play a Game that can ask a trivia question for users and display their score.

## Trivia App

The applications has the following features:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

## Motivation

This trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.

## About the Stack

The full stack application is designed with some key functional areas:

### Backend

The [backend](./backend/README.md) directory contains a completed Flask and SQLAlchemy server with defined endpoints and can referencing models.py for DB and SQLAlchemy setup.

> View the [Backend README](./backend/README.md) for more details.

### Frontend

The [frontend](./frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server. If you have prior experience building a frontend application, you should feel free to edit the endpoints as you see fit for the backend you design. If you do not have prior experience building a frontend application, you should read through the frontend code before starting and make notes regarding:

1. What are the end points and HTTP methods the frontend is expecting to consume?
2. How are the requests from the frontend formatted? Are they expecting certain parameters or payloads?

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API. The places where you may change the frontend behavior, and where you should be looking for the above information, are marked with `TODO`. These are the files you'd want to edit in the frontend:

1. `frontend/src/components/QuestionView.js`
2. `frontend/src/components/FormView.js`
3. `frontend/src/components/QuizView.js`

By making notes ahead of time, you will practice the core skill of being able to read and understand code and will have a simple plan to follow to build out the endpoints of your backend API.

> View the [Frontend README](./frontend/README.md) for more details.
