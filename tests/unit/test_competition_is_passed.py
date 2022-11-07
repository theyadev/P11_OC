from utils import competitionIsPassed


def test_competition_is_passed():
    competition = {
        'name': 'Test Competition',
        'date': '2019-01-01 00:00:00',
        'places': 10
    }

    assert competitionIsPassed(competition) == True


def test_competition_is_not_passed():
    competition = {
        'name': 'Test Competition',
        'date': '2123-01-01 00:00:00',
        'places': 10
    }

    assert competitionIsPassed(competition) == False
