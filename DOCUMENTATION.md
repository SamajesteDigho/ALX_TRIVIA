# DOCUMENTATION (TRIVIA API)

## 1. INTRODUCTION
Welcome to the TRIVIA ALX API. This API is a that of the second project of the Full Stack Course presented by ALX in
Nanodege. It is and API which gives access to data in relation with questions classified in different categories.
It gives us the possibility of storing, retrieving and managing question data grouped by thier category. 

## 1. GETTING STARTED
### Base URL
Since we are working on our local environment (while waiting to hoist the project online), the base default url is :
http://127.0.0.1:5000/. 

### API keys / Authentication
This version of the API does not support authentication or API keys.

## 3. ERRORS
Errors are returned as a JSON object and all have the same format, but different messages associated to them.
````json
{
    "success": "False",
    "error": "<Error code>",
    "message": "<message>"
}
````
Four errors are being taken into consideration here:
* 400: Bad Request
* 404: Resource Not Found
* 422: Not Processable
* 500: Internal Server Error

## 4. RESOURCE ENDPOINTS LIBRARY
<b> GET /categories</b><br>

* General:
    * Returns the list of all the available categories.
* Example: <b> curl http://127.0.0.1:5000/categories </b>
````json
{
    "categories": {
        "1": "Science",  
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment"
    }
}
````

<b> GET /questions</b>

* General:
    * Returns the list of 10 questions, the total number of question, the list of the categories.
    * The result is paginated with 10 questions per page.
    * It takes an optional parameter <b><i>page</i></b>, which returns the questions on the page number.
    When this parameter is not precised, it returns the first 10 questions i.e default page is 1.
* Example: curl http://127.0.0.1:5000/questions?page=2
````json
{
    "categories": {
        "1": "Science",
        "2": "Art",
        ...
    },
    "currentCategory": null,
    "questions": [
        {
            "answer": "The Palace of Versailles",
            "category": "3",
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
        },
        ...
    ],
    "totalQuestions": 19
}
````

<b> DELETE /questions/{id}</b>

* General:
    * Takes in the URL the id of the question to delete.
    * Returns a JSON object with the id of the deleted question.
* Example: curl -X DELETE http://127.0.0.1:5000/questions/2
````json
{
  "status_code": 200,
  "deleted_id": 2
}
````

<b> POST /questions</b> (Create a new Question)

* General:
    * Take a JSON object in the post body. This object should have as attributes <i>question, answer, category, difficulty</i>.
    * If none of the below attribute is given, the request is redirected to the search term method where it is treated
    accordingly.
    * If some of the parameters are given and some not, the request is considered as a BAD REQUEST.
    * If the request is successful, it returns nothing.
* Example: <b> curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d
'{"question":"question", "answer":"answer", "category":2, "difficulty":3}' <b>
    * On windows, try this if above doesn't function <br>
    <b> curl --request POST --header "Content-Type: application/json"
    --data "{\\"question\\":\\"question\\", \\"answer\\":\\"answer\\", \\"category\\":2, \\"difficulty\\":3}" http://127.0.0.1:5000/questions </b>
````json
````

<b> POST /questions</b> (Search Question by Term)

* General:
    * Take a JSON object in the post body. This JSON object should have the attribute <i>searchTerm</i>.
    * It returns all the questions which have the searchTerm as a substring, the total number of these questions and the
    current category.
* Example: curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d
'{"searchTerm":"what is"}'
    * On windows, try this if above doesn't function <br>
    <b> curl --request POST --header "Content-Type: application/json"
    --data "{\\"searchTerm\\":\\"what is\\"}" http://127.0.0.1:5000/questions </b>
````json
{
    "currentCategory": null,
    "questions": [
        {
            "answer": "Muhammad Ali",
            "category": "4",
            "difficulty": 1,
            "id": 9,
            "question": "What boxers original name is Cassius Clay?"
        },
        {
            "answer": "Apollo 13",
            "category": "5",
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        ...
    ],
    "totalQuestions": 12
}
````

<b> GET /categories/{id}/questions</b>

* General:
    * Returns the list of all the questions found in a given category along side with total number of those questions
    and the current category.
    * The id given for the category should be a valid id.
* Example: curl -X GET http://127.0.0.1:5000/categories/2/questions
````json
{
    "currentCategory": "Art",
    "questions": [
        {
            "answer": "Escher",
            "category": "2",
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
        },
      ...
    ],
    "totalQuestions": 4
}
````

<b> POST /quizzes</b>

* General:
    * Take a JSON object in the post body. This JSON object should have the attributes <i>previous_questions, quiz_category</i>.
    * It returns a random question in the given category whose id is not in the list of the previous questions.
* Example: curl -X POST http://127.0.0.1:5000/quizzes -H "Content-Type: application/json" -d
'{"previous_questions": [1,2,8,6], "quiz_category": "Science"}'
    * On windows, try this if above doesn't function <br>
    <b> curl --request POST --header "Content-Type: application/json"
    --data "{\\"previous_questions\\":[1,2,8,6], \\"quiz_category\\":\\"Science\\"}" http://127.0.0.1:5000/quizzes </b>
````json
{
    "question": {
        "answer": "The Liver",
        "category": "1",
        "difficulty": 4,
        "id": 20,
        "question": "What is the heaviest organ in the human body?"
    }
}
````