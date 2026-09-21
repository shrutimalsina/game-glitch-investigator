def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    raise NotImplementedError("Refactor this function from app.py into logic_utils.py")


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    raise NotImplementedError("Refactor this function from app.py into logic_utils.py")


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    # FIX: Refactored this function out of app.py into logic_utils.py using
    # Claude in agent mode. I asked the AI to find the buggy functions first,
    # and it correctly spotted that the hint messages were swapped, so
    # "Too High" was telling the player to go HIGHER.
    # FIX: The old version also had a try/except TypeError branch that compared
    # the guess and the secret as strings, where "9" > "42" is True. Casting
    # both to int here removes that whole branch.
    guess = int(guess)
    secret = int(secret)

    if guess == secret:
        return "Win", "🎉 Correct!"

    if guess > secret:
        return "Too High", "📉 Go LOWER!"

    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """
    Update score based on outcome and attempt number.

    attempt_number is 1-based: the first guess of a game is attempt 1.
    A win pays 100 points on the first attempt, 10 fewer for each attempt
    after that, with a floor of 10. A wrong guess costs 5 points in either
    direction.
    """
    # FIX: Also moved here from app.py with Claude in agent mode. Two bugs.
    # First an off by one: the old formula was 100 - 10 * (attempt_number + 1),
    # but app.py already counts the attempt before calling, so a first attempt
    # win paid only 80.
    # FIX: Second, "Too High" used to ADD 5 points on even numbered attempts,
    # which rewarded the player for guessing wrong. Both wrong directions now
    # cost the same 5 points.
    if outcome == "Win":
        points = 100 - 10 * (attempt_number - 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score
