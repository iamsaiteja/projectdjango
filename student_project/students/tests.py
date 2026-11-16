from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Student

class StudentSafetyTests(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user('staff', password='test-password', is_staff=True)
        self.student = Student.objects.create(name='Sample', roll_no='1', branch='Civil', year=2)

    def test_anonymous_and_nonstaff_cannot_read_or_delete(self):
        for user in [None, User.objects.create_user('ordinary')]:
            if user:
                self.client.force_login(user)
            for name in ['edit_student', 'delete_student']:
                response = self.client.post(reverse(name, args=[self.student.pk]), {'name': 'Changed'})
                self.assertEqual(response.status_code, 302)
            self.assertTrue(Student.objects.filter(pk=self.student.pk).exists())

    def test_delete_requires_post_and_csrf(self):
        self.client.force_login(self.staff)
        url = reverse('delete_student', args=[self.student.pk])
        self.assertEqual(self.client.get(url).status_code, 405)
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.force_login(self.staff)
        self.assertEqual(csrf_client.post(url).status_code, 403)
        self.assertEqual(self.client.post(url).status_code, 302)
        self.assertFalse(Student.objects.exists())

    def test_invalid_form_and_missing_id(self):
        self.client.force_login(self.staff)
        self.client.post(reverse('add_student'), {'name': 'A', 'roll_no': '2', 'branch': 'Civil', 'year': 99})
        self.assertEqual(Student.objects.count(), 1)
        self.assertEqual(self.client.get(reverse('edit_student', args=[99999])).status_code, 404)

    def test_valid_create_and_edit(self):
        self.client.force_login(self.staff)
        data = {'name': 'New', 'roll_no': '2', 'branch': 'Civil', 'year': 3}
        self.assertEqual(self.client.post(reverse('add_student'), data).status_code, 302)
        data['name'] = 'Updated'
        self.assertEqual(self.client.post(reverse('edit_student', args=[self.student.pk]), data).status_code, 302)
        self.student.refresh_from_db()
        self.assertEqual(self.student.name, 'Updated')
