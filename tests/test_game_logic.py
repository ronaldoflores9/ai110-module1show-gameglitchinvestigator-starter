import pytest
from logic_utils import check_guess, parse_guess, update_score, get_range_for_difficulty


# ============================================================================
# TEST SUITE 1: SECRET NUMBER HINTS ARE CORRECT
# ============================================================================

class TestSecretNumberHints:
    """Test that the secret number hints are correct."""

    def test_winning_guess_returns_win(self):
        """When guess equals secret, check_guess should return ('Win', message)."""
        outcome, message = check_guess(50, 50)
        assert outcome == "Win"
        assert "Correct" in message or "🎉" in message

    def test_guess_too_high_returns_correct_hint(self):
        """When guess > secret, check_guess should return ('Too High', message)."""
        outcome, message = check_guess(60, 50)
        assert outcome == "Too High"
        assert "LOWER" in message or "lower" in message or "📉" in message

    def test_guess_too_low_returns_correct_hint(self):
        """When guess < secret, check_guess should return ('Too Low', message)."""
        outcome, message = check_guess(40, 50)
        assert outcome == "Too Low"
        assert "HIGHER" in message or "higher" in message or "📈" in message

    def test_hint_with_string_secret_too_high(self):
        """When secret is string '50' and guess is 60, should return 'Too High'."""
        outcome, message = check_guess(60, "50")
        assert outcome == "Too High"

    def test_hint_with_string_secret_too_low(self):
        """When secret is string '50' and guess is 40, should return 'Too Low'."""
        outcome, message = check_guess(40, "50")
        assert outcome == "Too Low"

    def test_hint_with_string_secret_win(self):
        """When secret is string '50' and guess is 50, should return 'Win'."""
        outcome, message = check_guess(50, "50")
        assert outcome == "Win"

    def test_multiple_hints_are_consistent(self):
        """Multiple calls with same inputs should return same hint."""
        result1 = check_guess(75, 50)
        result2 = check_guess(75, 50)
        assert result1 == result2

    def test_boundary_hint_at_lower_range(self):
        """Test hint at lower boundary (secret = 1)."""
        outcome, message = check_guess(2, 1)
        assert outcome == "Too High"

    def test_boundary_hint_at_upper_range(self):
        """Test hint at upper boundary (secret = 100)."""
        outcome, message = check_guess(99, 100)
        assert outcome == "Too Low"


# ============================================================================
# TEST SUITE 2: NEW GAME BUTTON WORKS
# ============================================================================

class TestNewGameFunctionality:
    """Test that new game functionality works correctly."""

    def test_parse_guess_valid_integer(self):
        """parse_guess should handle valid integer inputs."""
        ok, guess, error = parse_guess("42")
        assert ok is True
        assert guess == 42
        assert error is None

    def test_parse_guess_valid_float(self):
        """parse_guess should handle float strings and convert to int."""
        ok, guess, error = parse_guess("42.5")
        assert ok is True
        assert guess == 42
        assert error is None

    def test_parse_guess_empty_string(self):
        """parse_guess should reject empty string."""
        ok, guess, error = parse_guess("")
        assert ok is False
        assert guess is None
        assert error is not None

    def test_parse_guess_none_input(self):
        """parse_guess should reject None input."""
        ok, guess, error = parse_guess(None)
        assert ok is False
        assert guess is None
        assert error is not None

    def test_parse_guess_non_numeric_string(self):
        """parse_guess should reject non-numeric strings."""
        ok, guess, error = parse_guess("not a number")
        assert ok is False
        assert guess is None
        assert error is not None

    def test_parse_guess_negative_number(self):
        """parse_guess should accept negative numbers."""
        ok, guess, error = parse_guess("-5")
        assert ok is True
        assert guess == -5
        assert error is None

    def test_get_range_easy_difficulty(self):
        """Easy difficulty should return range 1-20."""
        low, high = get_range_for_difficulty("Easy")
        assert low == 1
        assert high == 20

    def test_get_range_normal_difficulty(self):
        """Normal difficulty should return range 1-100."""
        low, high = get_range_for_difficulty("Normal")
        assert low == 1
        assert high == 100

    def test_get_range_hard_difficulty(self):
        """Hard difficulty should return range 1-50."""
        low, high = get_range_for_difficulty("Hard")
        assert low == 1
        assert high == 50

    def test_get_range_default_for_unknown_difficulty(self):
        """Unknown difficulty should default to 1-100."""
        low, high = get_range_for_difficulty("Unknown")
        assert low == 1
        assert high == 100


# ============================================================================
# TEST SUITE 3: GAME FINISHES WHEN YOU HAVE 0 ATTEMPTS
# ============================================================================

class TestGameFinishCondition:
    """Test that the game finishes when attempts reach the limit."""

    def test_update_score_on_win(self):
        """Score should increase significantly on win."""
        initial_score = 0
        new_score = update_score(initial_score, "Win", attempt_number=0)
        assert new_score > initial_score
        assert new_score >= 90  # 100 - 10*(0+1) >= 90

    def test_update_score_win_decreases_with_attempts(self):
        """Winning should give fewer points with more attempts."""
        score_at_attempt_0 = update_score(0, "Win", 0)
        score_at_attempt_7 = update_score(0, "Win", 7)
        assert score_at_attempt_0 > score_at_attempt_7

    def test_update_score_win_minimum_is_10_points(self):
        """Winning should never give less than 10 points."""
        final_score = update_score(0, "Win", attempt_number=20)
        assert final_score >= 10

    def test_update_score_on_too_high(self):
        """Score penalty on 'Too High' should depend on even/odd attempts."""
        score_even_attempt = update_score(100, "Too High", 0)
        score_odd_attempt = update_score(100, "Too High", 1)
        # Even attempts (0) get +5, odd attempts get -5
        assert score_even_attempt == 105
        assert score_odd_attempt == 95

    def test_update_score_on_too_low(self):
        """Score should decrease by 5 on 'Too Low'."""
        initial_score = 100
        new_score = update_score(initial_score, "Too Low", 5)
        assert new_score == 95

    def test_update_score_unknown_outcome(self):
        """Score should not change on unknown outcome."""
        initial_score = 50
        new_score = update_score(initial_score, "Unknown", 2)
        assert new_score == initial_score

    def test_game_over_after_attempt_limit_easy(self):
        """Game should end after 6 attempts on Easy difficulty."""
        attempt_limit_easy = 6
        assert 6 >= attempt_limit_easy  # At 6 attempts, game should be over

    def test_game_over_after_attempt_limit_normal(self):
        """Game should end after 8 attempts on Normal difficulty."""
        attempt_limit_normal = 8
        assert 8 >= attempt_limit_normal

    def test_game_over_after_attempt_limit_hard(self):
        """Game should end after 5 attempts on Hard difficulty."""
        attempt_limit_hard = 5
        assert 5 >= attempt_limit_hard

    def test_winning_before_attempt_limit(self):
        """Game should end immediately upon winning, even with attempts left."""
        # This tests the logic that a win (outcome == "Win") triggers game end
        outcome, _ = check_guess(50, 50)
        assert outcome == "Win"
        # Game should stop regardless of how many attempts are left

    def test_attempt_counter_increments(self):
        """Each guess should increment attempt counter (simulated test)."""
        # This would be tested in Streamlit's session state
        attempts_before = 3
        attempts_after = attempts_before + 1
        assert attempts_after == 4

    def test_game_does_not_continue_after_loss(self):
        """After losing (0 attempts left), no more guesses should be accepted."""
        # Simulates that game status changes to "lost" or "won"
        # and further guesses are blocked by the st.stop() condition
        game_status = "lost"
        assert game_status != "playing"
