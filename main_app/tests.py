from django.test import TestCase
from django.contrib.auth.models import User
from main_app.models import Session, Space, Task
from datetime import datetime

class SessionModelTests(TestCase):
    def setUp(self):
        # Create user
        self.user = User.objects.create_user(username='alanoud', password='12345')

        # Create session
        self.session = Session.objects.create(
            title='Focus Session',
            duration=10,
            image='image-data',
            sound='sound.mp3',
            user=self.user
        )

        self.space1 = Space.objects.create(
            session=self.session,
            type='star',
            x=50,
            y=100,
            image='https://example.com/star.png'
        )
        self.space2 = Space.objects.create(
            session=self.session,
            type='planet',
            x=200,
            y=300,
            image='https://example.com/planet.png'
        )

        self.task1 = Task.objects.create(
            session=self.session,
            title='Read Article',
            duration=5
        )
        self.task2 = Task.objects.create(
            session=self.session,
            title='Write Summary',
            duration=15
        )



    def test_user_str(self):
        self.assertEqual(str(self.user), 'alanoud')

    def test_session_str(self):
        self.assertEqual(str(self.session), 'Focus Session')

    def test_space_str(self):
        self.assertEqual(str(self.space1), 'star from session Focus Session')

    def test_task_str(self):
        self.assertEqual(str(self.task1), 'Read Article (5 min)')


    # -------------------
    def test_session_user_relationship(self):
        self.assertEqual(self.session.user, self.user)

    def test_space_session_relationship(self):
        self.assertEqual(self.space1.session, self.session)
        self.assertEqual(self.space2.session, self.session)

    def test_task_session_relationship(self):
        self.assertEqual(self.task1.session, self.session)
        self.assertEqual(self.task2.session, self.session)

    def test_session_space_count(self):
        self.assertEqual(self.session.spaces.count(), 2)

    def test_session_task_count(self):
        self.assertEqual(self.session.tasks.count(), 2)


    # -------------------
    def test_deleting_session_deletes_spaces_and_tasks(self):
        self.session.delete()
        self.assertEqual(Space.objects.count(), 0)
        self.assertEqual(Task.objects.count(), 0)

    def test_deleting_user_deletes_sessions(self):
        self.user.delete()
        self.assertEqual(Session.objects.count(), 0)