# TRIVIA API GAME - Full Stack Web Developer Nanodegree

In this game, users can play answering random trivia questions. This is part of the `API Course` from Udacity's `Full Stack Web Developer Nanodegree` and the goal here was to create an API w/tests for implementing the following functionality:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

## Before Playing: Installation Instructions

### Installing Dependencies

To properly use this project, you should already have `Python3`, `pip`, `node`, and `npm` installed. To avoid compatibility issues with the backend scripts, I recommend to use `python 3.7.0` version.

#### Frontend Dependencies

This project uses NPM to manage software dependencies. NPM Relies on the `package.json` file located in the `frontend` directory of this repository. Once you clone this project, open your terminal and run:

```bash
npm install
```

> _tip_: **npm i** is shorthand for **npm install**

If there are some troubles in the npm installation process, just follow the directions given in the terminal:

```bash
npm audit fix --force
```

#### Backend Dependencies

As a general recommendation, every time you try a third-party python code, I recommend the use of virtual environments to avoid compatibility issues regarding to inconsistencies with you own package versions. Here is a clear reference on how to install, activate and deactivate your virtual environments:

[Python's Virtual Environments](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/#:~:text=The%20virtual%20environment%20is%20a,them%20in%20the%20virtual%20environment)

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

or

```bash
pip3 install -r requirements.txt
```

#### Database

This project uses a LOCAL PostgreSQL database named "trivia" and there is also some default information provided in the trivia.psql file file. To incorporate this information to your local database, execute the following commands:

```
dropdb trivia
createdb trivia
psql trivia < trivia.psql
```

`Note:` Omit the `dropdb` command the first time you run tests (Because there's no trivia DB yet!).

## Running the Frontend in Dev Mode

The frontend app was built using `create-react-app`. In order to run the app in development mode use `npm start`. You can change the script in the `package.json` file.

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.<br>

```bash
npm start
```

## Running the Server

Go to the `backend` directory first. Activate your previously created virtual environment:

If you run on `Windows 10`, to run the server, execute from the terminal:

```bash
set FLASK_APP=flaskr
set FLASK_ENV=development
flask run
```

If you run on `Linux` or `Mac`, to run the server, execute from the terminal:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

## Testing your API

This project includes a testing script to check that all the endpoints are running accordingly. From the terminal, execute:

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

`Note:` Omit the `dropdb` command the first time you run tests (Because there's no trivia_test DB yet!).

## API Reference

### Getting Started

- This application is for local use ONLY. (i.e.: the backend is hosted at `http://127.0.0.1:5000/`)
- There is no authentication needed to use this API keys.

### Error Handling

Errors are returned as JSON in the following format:<br>

    {
        "success": False,
        "error": 404,
        "message": "resource not found"
    }

The API will return three types of errors:

- 400 – bad request
- 404 – resource not found
- 422 – unprocessable

### Endpoints

#### GET /categories

- General: Returns a list categories.
- Sample: `curl http://127.0.0.1:5000/categories`<br>

        {
            "categories": {
                "1": "Science",
                "2": "Art",
                "3": "Geography",
                "4": "History",
                "5": "Entertainment",
                "6": "Sports"
            },
            "success": true
        }

#### GET /questions

- General:
  - Returns a list questions.
  - Results are paginated in groups of 10 (as default).
  - Also returns list of categories and total number of questions.
- Sample: `curl http://127.0.0.1:5000/questions`<br>

        {
            "categories": {
                "1": "Science",
                "2": "Art",
                "3": "Geography",
                "4": "History",
                "5": "Entertainment",
                "6": "Sports"
            },
            "questions": [
                {
                    "answer": "Maya Angelou",
                    "category": 4,
                    "difficulty": 2,
                    "id": 5,
                    "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
                },
                {
                    "answer": "Muhammad Ali",
                    "category": 4,
                    "difficulty": 1,
                    "id": 9,
                    "question": "What boxer's original name is Cassius Clay?"
                },
                {
                    "answer": "Apollo 13",
                    "category": 5,
                    "difficulty": 4,
                    "id": 2,
                    "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
                },
                {
                    "answer": "Brazil",
                    "category": 6,
                    "difficulty": 3,
                    "id": 10,
                    "question": "Which is the only team to play in every soccer World Cup tournament?"
                },
                {
                    "answer": "Uruguay",
                    "category": 6,
                    "difficulty": 4,
                    "id": 11,
                    "question": "Which country won the first ever soccer World Cup in 1930?"
                },
                {
                    "answer": "George Washington Carver",
                    "category": 4,
                    "difficulty": 2,
                    "id": 12,
                    "question": "Who invented Peanut Butter?"
                },
                {
                    "answer": "Lake Victoria",
                    "category": 3,
                    "difficulty": 2,
                    "id": 13,
                    "question": "What is the largest lake in Africa?"
                },
                {
                    "answer": "The Palace of Versailles",
                    "category": 3,
                    "difficulty": 3,
                    "id": 14,
                    "question": "In which royal palace would you find the Hall of Mirrors?"
                },
                {
                    "answer": "Agra",
                    "category": 3,
                    "difficulty": 2,
                    "id": 15,
                    "question": "The Taj Mahal is located in which Indian city?"
                },
                {
                    "answer": "Escher",
                    "category": 2,
                    "difficulty": 1,
                    "id": 16,
                    "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
                }
            ],
            "success": true,
            "total_questions": 18
        }

#### DELETE /questions/\<int:id\>

- General:
  - Deletes a question by id using url parameters.
  - Returns id of deleted question upon success.
- Sample: `curl http://127.0.0.1:5000/questions/4 -X DELETE`<br>

        {
            "deleted": 4,
            "success": true
        }

#### POST /questions

This endpoint is designed either to create a new question or to return search results.

1. If searchTerm is not included in request:

- General:
  - Creates a new question using JSON request parameters.
  - Returns JSON object with newly created question, as well as paginated questions.
- Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{ "question": "Which year was America discovered by Columbus?", "answer": "1492", "difficulty": 1, "category": "4" }'`<br>

        {
            "created": 23,
            "question_created": "Which year was America discovered by Columbus?",
            "questions": [
                {
                    "answer": "Maya Angelou",
                    "category": 4,
                    "difficulty": 2,
                    "id": 5,
                    "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
                },
                {
                    "answer": "Muhammad Ali",
                    "category": 4,
                    "difficulty": 1,
                    "id": 9,
                    "question": "What boxer's original name is Cassius Clay?"
                },
                {
                    "answer": "Apollo 13",
                    "category": 5,
                    "difficulty": 4,
                    "id": 2,
                    "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
                },
                {
                    "answer": "Brazil",
                    "category": 6,
                    "difficulty": 3,
                    "id": 10,
                    "question": "Which is the only team to play in every soccer World Cup tournament?"
                },
                {
                    "answer": "Uruguay",
                    "category": 6,
                    "difficulty": 4,
                    "id": 11,
                    "question": "Which country won the first ever soccer World Cup in 1930?"
                },
                {
                    "answer": "George Washington Carver",
                    "category": 4,
                    "difficulty": 2,
                    "id": 12,
                    "question": "Who invented Peanut Butter?"
                },
                {
                    "answer": "Lake Victoria",
                    "category": 3,
                    "difficulty": 2,
                    "id": 13,
                    "question": "What is the largest lake in Africa?"
                },
                {
                    "answer": "The Palace of Versailles",
                    "category": 3,
                    "difficulty": 3,
                    "id": 14,
                    "question": "In which royal palace would you find the Hall of Mirrors?"
                },
                {
                    "answer": "Agra",
                    "category": 3,
                    "difficulty": 2,
                    "id": 15,
                    "question": "The Taj Mahal is located in which Indian city?"
                },
                {
                    "answer": "Escher",
                    "category": 2,
                    "difficulty": 1,
                    "id": 16,
                    "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
                }
            ],
            "success": true,
            "total_questions": 19
        }

2. If searchTerm is included in request:

- General:
  - Searches for questions using search term in JSON request parameters.
  - Returns JSON object with paginated matching questions.
- Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "which"}'`<br>

        {
            "questions": [
                {
                    "answer": "Brazil",
                    "category": 6,
                    "difficulty": 3,
                    "id": 10,
                    "question": "Which is the only team to play in every soccer World Cup tournament?"
                },
                {
                    "answer": "Uruguay",
                    "category": 6,
                    "difficulty": 4,
                    "id": 11,
                    "question": "Which country won the first ever soccer World Cup in 1930?"
                },
                {
                    "answer": "The Palace of Versailles",
                    "category": 3,
                    "difficulty": 3,
                    "id": 14,
                    "question": "In which royal palace would you find the Hall of Mirrors?"
                },
                {
                    "answer": "Agra",
                    "category": 3,
                    "difficulty": 2,
                    "id": 15,
                    "question": "The Taj Mahal is located in which Indian city?"
                },
                {
                    "answer": "Escher",
                    "category": 2,
                    "difficulty": 1,
                    "id": 16,
                    "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
                },
                {
                    "answer": "Jackson Pollock",
                    "category": 2,
                    "difficulty": 2,
                    "id": 19,
                    "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
                },
                {
                    "answer": "Scarab",
                    "category": 4,
                    "difficulty": 4,
                    "id": 23,
                    "question": "Which dung beetle was worshipped by the ancient Egyptians?"
                },
                {
                    "answer": "Michigan",
                    "category": 3,
                    "difficulty": 3,
                    "id": 173,
                    "question": "Which US state contains an area known as the Upper Penninsula?"
                }
            ],
            "success": true,
            "total_questions": 18
        }

#### GET /categories/\<int:id\>/questions

- General:
  - Gets questions by category id using url parameters.
  - Returns JSON object with paginated matching questions.
- Sample: `curl http://127.0.0.1:5000/categories/2/questions`<br>

        {
            "current_category": "Art",
            "questions": [
                {
                    "answer": "Escher",
                    "category": 2,
                    "difficulty": 1,
                    "id": 16,
                    "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
                },
                {
                    "answer": "Mona Lisa",
                    "category": 2,
                    "difficulty": 3,
                    "id": 17,
                    "question": "La Giaconda is better known as what?"
                },
                {
                    "answer": "One",
                    "category": 2,
                    "difficulty": 4,
                    "id": 18,
                    "question": "How many paintings did Van Gogh sell in his lifetime?"
                }
                {
                    "answer": "Jackson Pollock",
                    "category": 2,
                    "difficulty": 2,
                    "id": 19,
                    "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
                }
            ],
            "success": true,
            "total_questions": 19
        }

#### POST /quizzes

- General:
  - Allows users to play the quiz game.
  - Uses JSON request parameters of category and previous questions.
  - Returns JSON object with random question not among previous questions.
- Sample: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [20, 21], "quiz_category": {"type": "Science", "id": "1"}}'`<br>

        {
            "question": {
                "answer": "Blood",
                "category": 1,
                "difficulty": 4,
                "id": 22,
                "question": "Hematology is a branch of medicine involving the study of what?"
            },
            "success": true
        }

## Authors and Owners

Adjustments to the following files are authored by Jorge Villarroel Bryndzová: `__init__.py`, `test_flaskr.py`, and `README.md`.<br>
The default template for backend and frontend were created by [Udacity](https://www.udacity.com/) and was taken as a kick-off for the oresented project.
