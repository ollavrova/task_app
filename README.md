## Task application management on Django

### Features:
- users can login to their accounts;
- then they see a list of everyones tasks;
- available buttons: add, edit(owner only), mark done, delete(owner only), hide completed tasks;
- after add task it will assigned to creator;
- tests for code.

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
