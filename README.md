# neighboring_nodes

===========

## Using Docker:

1. Create the container image:
'''     docker build . -t neighboring_nodes '''

2. Run the container 
'''     docker run -p 8000:8000 neighboring_nodes '''

3. Go to 127.0.0.1:8000/controller 


## Running Manually:

If you want to run manually then you should 
1. Create a virtualenv and activate it
'''     python -m venv env
        . env/bin/activate'''
2. Install the requirements 
'''     pip install -r requirements.txt '''
3. Run app
'''     python manage.py runserver '''
4. To run unit tests check the file neighboring_nodes/tests.py
'''     python manage.py test '''

## Note:
- If you want to review the logic itself for the solution of the problem then you should review the neighboring_nodes/views.py file.
- If you want to review unit tests then you should review the neighboring_nodes/tests.py file.
- There are many additional files that are included in order to have a web app where you don't need to manually or locally interact with the code.
- The longest_consecutive_days.sql file corresponds to task 3 of the challenge.