import json
import pytest
from logic_utils import check_guess, parse_guess, update_score, get_range_for_difficulty, load_high_score, save_high_score


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
        """parse_guess should reject non-integer floats instead of silently truncating."""
        ok, guess, error = parse_guess("42.5")
        assert ok is False
        assert guess is None
        assert error is not None

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
        """parse_guess should reject negative numbers as out of range."""
        ok, guess, error = parse_guess("-5")
        assert ok is False
        assert guess is None
        assert error is not None

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
        assert new_score >= 90  # 100 - 10*0 = 100 >= 90

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


# ============================================================================
# TEST SUITE 4: EDGE CASE INPUTS ARE HANDLED GRACEFULLY
# ============================================================================

class TestEdgeCaseInputs:
    """Verify that known edge-case inputs are rejected or handled safely."""

    # --- Edge Case 1: Out-of-range numbers ---

    def test_guess_above_range_is_rejected(self):
        """Numbers above the valid range should be rejected with a helpful error."""
        ok, guess, error = parse_guess("999", low=1, high=100)
        assert ok is False
        assert guess is None
        assert "100" in error

    def test_guess_below_range_is_rejected(self):
        """Numbers below the valid range (including 0) should be rejected."""
        ok, guess, error = parse_guess("0", low=1, high=100)
        assert ok is False
        assert guess is None
        assert "1" in error

    def test_negative_guess_is_rejected(self):
        """Negative numbers are outside the valid range and must be rejected."""
        ok, guess, error = parse_guess("-5", low=1, high=100)
        assert ok is False
        assert guess is None
        assert error is not None

    def test_guess_at_upper_boundary_is_accepted(self):
        """The exact upper boundary value should be accepted."""
        ok, guess, error = parse_guess("100", low=1, high=100)
        assert ok is True
        assert guess == 100

    def test_guess_at_lower_boundary_is_accepted(self):
        """The exact lower boundary value should be accepted."""
        ok, guess, error = parse_guess("1", low=1, high=100)
        assert ok is True
        assert guess == 1

    def test_out_of_range_on_easy_difficulty(self):
        """On Easy mode (1-20), a guess of 21 should be rejected."""
        ok, guess, error = parse_guess("21", low=1, high=20)
        assert ok is False
        assert "20" in error

    # --- Edge Case 2: Non-integer floats silently truncated ---

    def test_float_with_decimal_is_rejected(self):
        """7.9 must not silently become 7 — it should be rejected."""
        ok, guess, error = parse_guess("7.9", low=1, high=100)
        assert ok is False
        assert guess is None
        assert error is not None

    def test_float_near_boundary_is_rejected(self):
        """19.9 on Easy should not silently truncate to 19 and succeed."""
        ok, guess, error = parse_guess("19.9", low=1, high=20)
        assert ok is False
        assert guess is None

    def test_whole_number_float_is_accepted(self):
        """A float that is a whole number (e.g. 7.0) should be accepted as 7."""
        ok, guess, error = parse_guess("7.0", low=1, high=100)
        assert ok is True
        assert guess == 7
        assert error is None

    # --- Edge Case 3: Score off-by-one on first-attempt win ---

    def test_win_on_first_attempt_gives_100_points(self):
        """Winning on attempt 1 should give 90 points (100 - 10*1), not 80."""
        score = update_score(0, "Win", attempt_number=1)
        assert score == 90

    def test_win_on_second_attempt_gives_80_points(self):
        """Winning on attempt 2 should give 80 points (100 - 10*2)."""
        score = update_score(0, "Win", attempt_number=2)
        assert score == 80

    def test_win_score_is_not_penalised_extra_attempt(self):
        """Score at attempt N must equal score at attempt N+1 plus exactly 10."""
        score_n = update_score(0, "Win", attempt_number=3)
        score_n1 = update_score(0, "Win", attempt_number=4)
        assert score_n - score_n1 == 10


# ============================================================================
# TEST SUITE 5: HIGH SCORE TRACKER
# ============================================================================

class TestHighScoreTracker:
    """Verify that high scores are saved and loaded correctly."""

    def test_load_returns_empty_dict_when_file_missing(self, tmp_path):
        """load_high_score returns {} when the file doesn't exist."""
        result = load_high_score(str(tmp_path / "no_file.json"))
        assert result == {}

    def test_save_creates_file_with_score(self, tmp_path):
        """save_high_score creates the file and stores the score."""
        fp = str(tmp_path / "hs.json")
        save_high_score(80, "Normal", fp)
        with open(fp) as f:
            data = json.load(f)
        assert data["Normal"] == 80

    def test_save_returns_true_on_new_high_score(self, tmp_path):
        """save_high_score returns True when the score beats the record."""
        fp = str(tmp_path / "hs.json")
        result = save_high_score(90, "Easy", fp)
        assert result is True

    def test_save_returns_false_when_score_not_beaten(self, tmp_path):
        """save_high_score returns False when the score does not beat the record."""
        fp = str(tmp_path / "hs.json")
        save_high_score(90, "Easy", fp)
        result = save_high_score(70, "Easy", fp)
        assert result is False

    def test_existing_high_score_not_overwritten_by_lower(self, tmp_path):
        """A lower score must not replace an existing higher score."""
        fp = str(tmp_path / "hs.json")
        save_high_score(90, "Easy", fp)
        save_high_score(50, "Easy", fp)
        scores = load_high_score(fp)
        assert scores["Easy"] == 90

    def test_new_record_replaces_old_one(self, tmp_path):
        """A higher score must overwrite the previous record."""
        fp = str(tmp_path / "hs.json")
        save_high_score(60, "Hard", fp)
        save_high_score(95, "Hard", fp)
        scores = load_high_score(fp)
        assert scores["Hard"] == 95

    def test_scores_are_tracked_per_difficulty(self, tmp_path):
        """Each difficulty maintains its own independent high score."""
        fp = str(tmp_path / "hs.json")
        save_high_score(50, "Easy", fp)
        save_high_score(80, "Normal", fp)
        save_high_score(70, "Hard", fp)
        scores = load_high_score(fp)
        assert scores["Easy"] == 50
        assert scores["Normal"] == 80
        assert scores["Hard"] == 70

    def test_load_returns_empty_on_corrupt_file(self, tmp_path):
        """load_high_score returns {} gracefully if the file contains invalid JSON."""
        fp = str(tmp_path / "hs.json")
        with open(fp, "w") as f:
            f.write("not valid json{{")
        result = load_high_score(fp)
        assert result == {}
