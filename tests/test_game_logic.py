# FIX: The three original tests compared check_guess() to a plain string, but
# the function returns an (outcome, message) tuple that app.py unpacks, so they
# failed on shape even though the logic was right. I had Claude unpack them and
# also assert the hint direction, since a backwards message was the actual bug.
from logic_utils import check_guess, update_score

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert "Correct" in message

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    # and the message must point the player DOWN.
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    # and the message must point the player UP.
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message


def test_hint_direction_is_not_inverted():
    # The original bug: "Too High" told the player to go HIGHER.
    _, high_message = check_guess(60, 50)
    _, low_message = check_guess(40, 50)
    assert "HIGHER" not in high_message
    assert "LOWER" not in low_message


def test_string_secret_compares_numerically():
    # app.py passes the secret as a str on even attempts. The old code fell
    # back to lexicographic comparison, where "9" > "42" was True.
    assert check_guess(9, "42")[0] == "Too Low"
    assert check_guess(90, "42")[0] == "Too High"
    assert check_guess(42, "42")[0] == "Win"


def test_win_on_first_attempt_pays_full_points():
    # Off-by-one bug: the old formula was 100 - 10 * (attempt_number + 1),
    # which paid only 80 for a first-attempt win.
    assert update_score(0, "Win", 1) == 100


def test_win_payout_drops_by_ten_per_attempt():
    # Attempt 2 should be one 10-point step below attempt 1, not two.
    assert update_score(0, "Win", 2) == 90
    assert update_score(0, "Win", 3) == 80


def test_win_payout_floors_at_ten():
    # The floor should bite at attempt 10, not two attempts early:
    # under the old off-by-one, attempt 9 was already clamped to 10.
    assert update_score(0, "Win", 9) == 20
    assert update_score(0, "Win", 10) == 10
    assert update_score(0, "Win", 99) == 10


def test_too_high_on_even_attempt_loses_points():
    # Parity bug: an even-numbered "Too High" used to ADD 5 points,
    # rewarding the player for guessing wrong.
    assert update_score(50, "Too High", 2) == 45


def test_wrong_guess_penalty_is_symmetric():
    # Too High and Too Low should cost the same, on any attempt number.
    for attempt in range(1, 6):
        assert update_score(50, "Too High", attempt) == update_score(50, "Too Low", attempt)


def test_wrong_guess_never_increases_score():
    for attempt in range(1, 11):
        for outcome in ("Too High", "Too Low"):
            assert update_score(50, outcome, attempt) < 50
