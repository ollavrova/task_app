## Task application on Django

Features:
- users can login to their accounts;
- then they see a list of everyones tasks;
- available buttons: add, edit(owner only), mark done, delete(owner only), hide completed tasks;
- after add task it will assigned to creator;

- tests for code.

Requirements:
- django 2.1
- python 3.5
- bootstrap 3.3.7
- jquery 3.3.1

Also there is provided a test user and test data in fixtures:
1. login - admin, password - 'adminadmin'
2. login - developer1, password - 'dev12345'
You can load it by command:
```bash
python manage.py loaddata task_list/fixtures/initial.json
```

Commands:
```
 $ python manage.py migrate
 $ python manage.py createsuperuser - if needed
 $ python manage.py runserver
 $ python manage.py test
```
