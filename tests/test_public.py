from datetime import datetime
from datetime import timedelta
import math
import unittest

from src.app import public


class TestYieldInterval(unittest.TestCase):
    def setUp(self):
        self.now = datetime.utcnow()

    def test_yield_interval_first_interation(self):
        yesterday, today = next(public.yield_interval(self.now, 1, 86400))
        self.assertEqual(self.now - timedelta(days=1), yesterday)
        self.assertEqual(self.now, today)

    def test_yield_interval_length(self):
        self.times = [t for t in public.yield_interval(self.now, 10, 3600)]
        self.assertEqual(10*24, len(self.times))


class TestYieldBatch(unittest.TestCase):
    def setUp(self):
        self.now = datetime.utcnow()

    def test_yield_batch_first_iteration(self):
        two_weeks_ago, one_week_ago = next(public.yield_batch(self.now, 14, 86400, 7))
        self.assertEqual(self.now - timedelta(days=14), two_weeks_ago)
        self.assertEqual(self.now - timedelta(days=7), one_week_ago)

    def test_yield_batch_length(self):
        batch_size = 100
        self.times = [t for t in public.yield_batch(self.now, 10, 3600, batch_size)]
        self.assertEqual(math.ceil((10*24) / batch_size), len(self.times))
