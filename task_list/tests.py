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

    def test_chack_if_home_page_closed(self):
        """
        testing auth to page
        """
        self.browser.get(self.live_server_url)
        login = self.browser.find_element_by_link_text('Login')
        self.assertTrue(login.is_displayed())
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Task list', body.text)
        self.assertIn('Login', body.text)


class ProgectTest(TestCase):
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
        self.user = User.objects.create(username='admin', password='adminadmin').save()
        self.auth = {"username": self.user.username, "password": "adminadmin"}
        self.task1 = Task.objects.create(
            name="first task 1222",
            description="this is a very important task too",
            status="False",
        )

    def tearDown(self):
        self.client.post(reverse('logout'))

    def test_update_task(self):
        """
        test edit task
        """
        self.client.post(reverse('login'), self.auth)
        # self.assertEqual(self.client.get(reverse('task-edit', kwargs={'pk': self.task1.id})).status_code, 200)
        data = dict(
            name="first task 1222",
            description="this is not a task for now",
        )
        response = self.client.post(reverse('task-edit', kwargs={'pk': self.task1.id}), data=data)
        self.assertEqual(response.status_code, 302)
        data1 = dict(
            name="third task",
        )
        response = self.client.post(reverse('task-edit', kwargs={'pk': self.task1.id}), data=data1)
        self.assertEqual(response.status_code, 302)

        self.assertEqual(self.client.get(reverse('task-edit', kwargs={'pk': self.task1.id})).status_code, 302)
        self.assertEqual(self.task1.name, "third task")
        self.assertEqual(self.task1.description, "this is not a task for now")

    def test_create_task(self):
        """
        test create task
        """
        self.client.post(reverse('login'), self.auth)
        self.assertEqual(self.client.get(reverse('task-create')).status_code, 302)
        data = dict(
            name="new task",
            description="this is a task for future",
            status="False",
        )
        response = self.client.post(reverse('task-create'), data)
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "new task", status_code=200)
        self.assertContains(response, "this is a task for future", status_code=200)
        self.assertContains(response, "undone", status_code=200)

    def test_mark_done_task(self):
        """
        test mark done for task and writing info about user who did it
        """
        self.assertEqual(self.client.post(reverse('login'), self.auth).status_code, 200)
        self.assertEqual(self.client.get(reverse('task-done', kwargs={'pk': self.task1.pk})).status_code, 302)
        data = dict(
            status="True",
        )
        response = self.client.post(reverse('task-done', kwargs={'pk': self.task1.pk}), data=data)
        self.assertEqual(response.status_code, 302)

        self.assertEqual(self.task1.status, "True")
        self.assertEqual(self.task1.done_by, User.objects.get(username='admin'))

    def test_delete_task(self):
        """
        test delete a task
        """
        self.client.post(reverse('login'), self.auth)
        self.assertEqual(self.client.get(reverse('task-delete', kwargs={'pk': self.task1.pk})).status_code, 302)
        response = self.client.post(reverse('task-delete', kwargs={'pk': self.task1.pk}), {})
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Logout')
        self.assertEqual(response.status_code, 302)
        self.assertNotContains(response, self.task1.name, status_code=200)
        self.assertNotContains(response, self.task1.description[50:], status_code=200)
        self.assertNotContains(response, self.task1.assigned, status_code=200)
        self.assertFalse(Task.objects.get(pk=self.task1.pk))
