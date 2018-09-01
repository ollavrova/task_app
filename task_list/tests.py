# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase, LiveServerTestCase
from selenium import webdriver
from task_list.models import Task


class ProjectSeleniumTests(LiveServerTestCase):
    """
    set of selenium tests
    """
    fixtures = ['initial.json']

    def setUp(self):
        self.browser = webdriver.PhantomJS()
        self.auth = {"username": "admin", "password": "adminadmin"}
        self.task1 = Task.objects.create(
            name="first task",
            description="this is a very important task",
            status="False",
        )
        self.task2 = Task.objects.create(
            name="second task",
            description="this is another very important task",
            status="False",
        )

    def tearDown(self):
        self.browser.quit()

    def test_check_if_home_page_closed(self):
        """
        testing auth to page
        """
        self.browser.get(self.live_server_url)
        login = self.browser.find_element_by_link_text('Login')
        self.assertTrue(login.is_displayed())
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Task list', body.text)
        self.assertIn('Login', body.text)

    def test_login(self):
        """
        testing login procedure
        """
        self.browser.get(self.live_server_url)
        login = self.browser.find_element_by_link_text('Login')
        self.assertTrue(login.is_displayed())
        login.click()
        username = self.browser.find_element_by_id("id_username")
        password = self.browser.find_element_by_id("id_password")

        username.send_keys("admin")
        password.send_keys("adminadmin")
        self.browser.find_element_by_name("submit").click()
        self.browser.get(self.live_server_url)
        body = self.browser.find_element_by_tag_name('body')
        self.assertNotIn('Login', body.text)
        self.assertIn('Logout', body.text)
        self.browser.get(self.live_server_url)

    def test_hide_completed_tasks_button(self):
        """
        testing button for hide/show completed tasks from task list on home page
        """
        self.test_login()
        hide = self.browser.find_element_by_id('hide-completed-tasks')
        done_task = self.browser.find_elements_by_css_selector('tr[data-status="1"]')
        self.assertTrue(len(done_task) == 1)
        hide.click()
        done_task = self.browser.find_elements_by_css_selector('tr[data-status="1"]')
        self.assertTrue(len(done_task) == 0)
        hide.click()
        done_task = self.browser.find_elements_by_css_selector('tr[data-status="1"]')
        self.assertTrue(len(done_task) == 1)

    def test_create_task(self):
        self.test_login()
        self.assertTrue(len(self.browser.find_elements_by_link_text('task new description')) == 0)
        add_button = self.browser.find_element_by_css_selector('button[title="Add new task"]')
        add_button.click()
        self.browser.find_element_by_id('id_name').send_keys('task new')
        self.browser.find_element_by_id('id_description').send_keys('task new description')
        self.browser.find_element_by_name('submit').click()
        self.browser.get(self.live_server_url)
        new = self.browser.find_element_by_link_text('task new description')
        self.assertTrue(new.is_displayed())


class ProjectTests(TestCase):
    """
    test check info on main page
    """
    fixtures = ['initial.json']

    def setUp(self):
        self.auth = {"username": "admin", "password": "adminadmin"}
        self.task1 = Task.objects.create(
            name="first task",
            description="this is a very important task",
            status="False",
        )
        self.task2 = Task.objects.create(
            name="second task",
            description="this is another very important task",
            status="False",
        )
        self.user = User.objects.first()

    def tearDown(self):
        self.client.post(reverse('logout'))

    def test_show_pages(self):
        """
        test check if show info about only person1 on main page
        """
        self.client.post(reverse('login'), self.auth)
        response = self.client.get(reverse('home'))
        self.assertContains(response, "Task list", status_code=200)
        self.assertContains(response, "Name", status_code=200)
        self.assertContains(response, "Assigned", status_code=200)
        self.assertContains(response, "Created", status_code=200)
        self.assertContains(response, "Description", status_code=200)
        self.assertContains(response, "Status", status_code=200)
        self.assertContains(response, "Actions", status_code=200)
        self.assertContains(response, self.task1.name, status_code=200)
        self.assertContains(response, self.task1.description[:50], status_code=200)
        self.assertContains(response, self.task1.name, status_code=200)
        self.assertContains(response, self.task2.name, status_code=200)
        self.assertContains(response, self.task2.description[:50], status_code=200)
        self.assertContains(response, self.task2.name, status_code=200)
        self.assertContains(response, self.task2.name, status_code=200)

    def test_show_empty_page(self):
        """
        testing what if database is empty
        """
        Task.objects.all().delete()
        self.client.post(reverse('login'), self.auth)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.task1.name, status_code=200)
        self.assertNotContains(response, self.task1.description[:50], status_code=200)
        self.assertContains(response, 'Sorry, no tasks for now.', status_code=200)


class TestEditForm(TestCase):

    def setUp(self):
        self.user, _ = User.objects.get_or_create(username='admin')
        self.client.force_login(User.objects.get_or_create(username='admin')[0])

        self.task1 = Task.objects.create(
            name="first task for update",
            description="this is a very important task too",
            status="False",
            assigned=self.user,
        )
        self.task2 = Task.objects.create(
            name="first task for update",
            description="this is a very important task too",
            status="False",
            assigned=None,
        )

    def tearDown(self):
        self.client.logout()

    def test_update_task(self):
        """
        test edit task
        """
        data = dict(
            name="updated task",
            description="this is not a task for now",
        )
        get_response = self.client.get(reverse('task-edit', kwargs={'pk': self.task2.id}))
        self.assertEqual(get_response.status_code, 404)  # user can edit own task only
        get_response = self.client.get(reverse('task-edit', kwargs={'pk': self.task1.id}))
        self.assertEqual(get_response.status_code, 200)
        self.assertContains(get_response, 'Edit task:')
        self.assertContains(get_response, self.task1.name)
        self.assertContains(get_response, self.task1.description)
        self.assertContains(get_response, 'Is Task Done?')
        response = self.client.post(reverse('task-edit', kwargs={'pk': self.task1.id}), data=data)
        self.assertEqual(response.status_code, 302)

        self.assertEqual(self.client.get(reverse('task-edit', kwargs={'pk': self.task1.pk})).status_code, 200)
        task1 = Task.objects.get(pk=self.task1.pk)
        self.assertTrue(task1.name == "updated task")
        self.assertTrue(task1.description == "this is not a task for now")

    def test_create_task(self):
        """
        test create task
        """
        self.assertEqual(self.client.get(reverse('task-create')).status_code, 200)
        data = dict(
            name="new task",
            description="this is a task for future",
            status="False",
        )
        response = self.client.post(reverse('task-create'), data=data)
        self.assertEqual(response.status_code, 302)
        task = Task.objects.filter(name="new task")[0]
        self.assertTrue(task)
        self.assertTrue(task.description == data['description'])

        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "new task", status_code=200)
        self.assertIn("this is a task for future", str(response.content))
        self.assertIn("undone", str(response.content))

    def test_mark_done_task(self):
        """
        testing mark done for task and writing info about user who did it.
        check if any logged user can make mark done any task.
        """
        self.assertEqual(self.client.get(reverse('task-done', kwargs={'pk': self.task1.pk})).status_code, 200)
        get_response = self.client.get(reverse('task-done', kwargs={'pk': self.task1.pk}))
        self.assertContains(get_response, 'Mark Task Done task:')
        self.assertContains(get_response, 'Is Task Done?')

        # check if user can mark done own tasks
        self.assertTrue(self.task1.assigned == self.user)
        data = dict(
            status="True",
        )
        response = self.client.post(reverse('task-done', kwargs={'pk': self.task1.pk}), data=data)
        self.assertEqual(response.status_code, 302)

        task1 = Task.objects.get(pk=self.task1.pk)
        self.assertTrue(task1.status is True)
        self.assertTrue(task1.done_by == self.user)

        # check if user can mark done not only own tasks
        self.assertTrue(self.task2.assigned != self.user)
        response = self.client.post(reverse('task-done', kwargs={'pk': self.task2.pk}), data=data)
        task2 = Task.objects.get(pk=self.task2.pk)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(task2.status is True)
        self.assertTrue(task1.done_by == self.user)

    def test_delete_task(self):
        """
        test delete a task
        """
        admin_task = Task.objects.filter(assigned=self.user)[0]
        self.assertTrue(admin_task)
        get_response = self.client.get(reverse('task-delete', kwargs={'pk': admin_task.pk}), follow=True)
        self.assertContains(get_response, 'Task delete')
        self.assertContains(get_response, 'Are you sure to remove this task')
        post_response = self.client.post(reverse('task-delete', kwargs={'pk': admin_task.pk}), follow=True)
        self.assertRedirects(post_response, reverse('home'), status_code=302)  # check if success url working
        self.assertFalse(Task.objects.filter(assigned=self.user).exists())  # own task is deleted

        another_task = Task.objects.exclude(assigned=self.user)[0]
        self.assertTrue(another_task)
        self.client.post(reverse('task-delete', kwargs={'pk': another_task.pk}))
        self.assertTrue(Task.objects.exclude(assigned=self.user).exists())  # not own task is not deleted
