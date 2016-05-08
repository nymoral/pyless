from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from .models import Game, Team
from .views.validation import *

from datetime import datetime, timezone


class GameTest(TestCase):
    def setUp(self):
        Team.objects.create(short='LT', full_name='Lithuania')
        Team.objects.create(short='LV', full_name='Latvia')
        Game.objects.create(team1_id='LT', team2_id='LV', time=datetime(2016, 7, 1, 21, 00, tzinfo=timezone.utc))

    def test_auto_close(self):
        g = Game.objects.get(team1_id='LT', team2_id='LV')
        g.ended = datetime.now(tz=timezone.utc)
        g.result1 = 2
        g.result2 = 1
        g.full_clean()
        g.save()

        g = Game.objects.get(team1_id='LT', team2_id='LV')
        self.assertIsNotNone(g.closed)

    def test_close_no_result(self):
        g = Game.objects.get(team1_id='LT', team2_id='LV')
        g.ended = datetime.now(tz=timezone.utc)
        with self.assertRaises(ValidationError):
            g.result1 = None
            g.result2 = 1
            g.full_clean()
            g.save()
        with self.assertRaises(ValidationError):
            g.result1 = 1
            g.result2 = None
            g.full_clean()
            g.save()


class UserTest(TestCase):
    def test_autocreate_points(self):
        u = User(username='test', password='hunter2')
        u.save()
        u = User.objects.get(username='test')
        self.assertIsNotNone(u.points)
        self.assertEqual(u.points.points, 0)


class ValidationTest(TestCase):
    def test_check_len(self):
        self.assertFalse(check_len(None, 0))
        self.assertFalse(check_len(None, 1))
        self.assertFalse(check_len(None, 4))
        self.assertFalse(check_len('', 1))
        self.assertTrue(check_len('', 0))
        self.assertFalse(check_len('123', 4))
        self.assertTrue(check_len('123', 3))
        self.assertTrue(check_len('123', 2))

    def test_require_missing(self):
        form = {'empty': '', 'required': 'required', 'non_required': 'non_required'}
        r = required_missing(form, [])
        self.assertEqual(len(r), 0)
        r = required_missing(form, ['empty', 'required', 'required_not_presend'])
        self.assertFalse('non_required' in r)
        self.assertFalse('required' in r)
        self.assertTrue('empty' in r)
        self.assertTrue('required_not_presend' in r)

    def too_long_fields(self):
        form = {'1': '1', '2': '12', '3': '123', '4': '1234', '5': '12345'}
        fields = ['1', '2', '3', '4', '5', '6']
        r = too_long_fields(form, fields, 1)
        self.assertFalse('1' in r)
        self.assertFalse('6' in r)
        self.assertTrue('2' in r)
        self.assertTrue('5' in r)
        r = too_long_fields(form, fields, 5)
        self.assertFalse('5' in r)
        self.assertFalse('6' in r)
        self.assertFalse('2' in r)
        r = too_long_fields(form, fields, 3)
        self.assertTrue('4' in r)
        self.assertTrue('5' in r)

    def test_is_email(self):
        self.assertTrue(is_email('user@hostname.com'))
        self.assertTrue(is_email('user@hostname.co.uk'))
        self.assertTrue(is_email('long.user@hostname.co.uk'))
        self.assertTrue(is_email('long.user@long.hostname.co.uk'))
        self.assertFalse(is_email('justUsername'))
        self.assertFalse(is_email('user@invalid$host.com'))
        self.assertFalse(is_email('invalid$user@hostname.com'))
