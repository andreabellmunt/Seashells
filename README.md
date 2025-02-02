# Seashells

## Starting up 
To be able to work with it, we first need to ensure the requirements are satisfied: 
`pip install -r requirements.txt`

Then, we can run the code locally with: 
`uvicorn main:app --reload`

## API documentation 

Documentation can be found in the `/docs` path. For instance, when running the app locally, we can find it in `http://localhost:8000/docs`. It is supported by OpenAPI. 

As a summary, it offers the following functionality: 

- >**GET /seashells**: List all seashells in DB
- >**POST /seashells**: Add new seashell 
- >**PATCH /seashells/{seashell_id}**: Partially or completely edit a seashell with ID = seashell_id
- >**DELETE /seashells/{seashell_id}**: Delete seashell with ID = seashell_id  

