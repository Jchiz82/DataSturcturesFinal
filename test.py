import unittest
from main import Leaderboard
from main import Scorecard

class TestLeaderboard(unittest.TestCase):
    def test_add_scorecard(self):
        # Test adding scorecards to the leaderboard
        leaderboard = Leaderboard()
        scorecard1 = Scorecard("Course1", 72, 70)
        leaderboard.add_scorecard(scorecard1)
        self.assertEqual(leaderboard.leaderboard.qsize(), 1)

        scorecard2 = Scorecard("Course2", 72, 75)
        leaderboard.add_scorecard(scorecard2)
        self.assertEqual(leaderboard.leaderboard.qsize(), 2)

    def test_remove_worst_score(self):
        # Test removing the worst score from the leaderboard
        leaderboard = Leaderboard()
        scorecard1 = Scorecard("Course1", 72, 70)
        scorecard2 = Scorecard("Course2", 72, 75)
        leaderboard.add_scorecard(scorecard1)
        leaderboard.add_scorecard(scorecard2)

        leaderboard.remove_worst_score()
        self.assertEqual(leaderboard.leaderboard.qsize(), 1)

        leaderboard.remove_worst_score()
        self.assertEqual(leaderboard.leaderboard.qsize(), 0)

    def test_get_top_scores(self):
        # Test getting the top scores from the leaderboard
        leaderboard = Leaderboard()
        scorecard1 = Scorecard("Course1", 72, 70)
        scorecard2 = Scorecard("Course2", 72, 75)
        scorecard3 = Scorecard("Course3", 72, 68)
        scorecard4 = Scorecard("Course4", 72, 65)
        scorecard5 = Scorecard("Course5", 72, 79)
        scorecard6 = Scorecard("Course6", 72, 81)
        leaderboard.add_scorecard(scorecard1)
        leaderboard.add_scorecard(scorecard2)
        leaderboard.add_scorecard(scorecard3)
        leaderboard.add_scorecard(scorecard4)
        leaderboard.add_scorecard(scorecard5)
        leaderboard.add_scorecard(scorecard6)

        top_scores = leaderboard.get_top_scores(5)
        self.assertEqual(len(top_scores), 5)


class TestScorecard(unittest.TestCase):
    def test_scorecard_init(self):
        # Test initializing a scorecard
        scorecard = Scorecard("Course1", 72, 70)
        self.assertEqual(scorecard.course_name, "Course1")
        self.assertEqual(scorecard.course_par, 72)
        self.assertEqual(scorecard.actual_score, 70)
        self.assertEqual(scorecard.relative_score, -2)

    def test_scorecard_lt(self):
        # Test the less than comparison between scorecards
        scorecard1 = Scorecard("Course1", 72, 70)
        scorecard2 = Scorecard("Course2", 72, 75)
        self.assertTrue(scorecard1 < scorecard2)
        self.assertFalse(scorecard2 < scorecard1)


if __name__ == '__main__':
    unittest.main()

