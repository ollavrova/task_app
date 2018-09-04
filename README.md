## Task management application

 - deployed to https://fierce-brook-54192.herokuapp.com/ and http://krocozabr.pythonanywhere.com/ 
 
### Features:
- users can login to their accounts;
- then they see a list of everyones tasks;
- available actions: add, edit(owner only), mark done, delete(owner only), hide completed tasks;
- after adding task it can be assigned to anyone or it will assigned to creator by system;
- tests for code included(Selenium and unit tests).

### Requirements:
- django 2.1
- python 3.5
- bootstrap 3.3.7
- jquery 3.3.1

Also there is provided a test user and test data in fixtures. 
For log in to the site you can use next credentials(from fixtures)
- login - admin, password - 'adminadmin'
- login - developer1, password - 'dev12345'
- login - developer2, password - 'dev12345'


###Instructions:

Clone the project and go to the project folder. You can use next commands:

```bash
 $ pip install -r requirements.txt
 $ python manage.py migrate
 $ python manage.py runserver
```

Run tests:

```bash
 $ python manage.py test
```