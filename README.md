# Seashells

Backend development - KONE interview for the Cloud Developer Summer Trainee position 

## Starting up 
To be able to work with it, we first need to ensure the requirements are satisfied: 
`pip install -r requirements.txt`
Then, we want to use a MongoDB Docker container to run the database. To be able to do that we execute: 
`docker run -d -p 27017:27017 -v ~/data:/data/db mongo`
This would ensure data persistence, as we are also mounting the data we have locally to the container. Also, if we were to remove the container, data would persist locally. 

## More information 
It is possible to run the code locally by using: 
`uvicorn main:app --reload`




