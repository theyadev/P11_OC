from utils import getCompetition, getClubByEmail
competitions = [
    {
        'name': 'Test Competition',
        'date': '2019-01-01 00:00:00',
        'places': 10
    }
]
clubs = [
    {
        'name': 'Test Club',
        'email': 'test@club.com',
        'places': 10
    }
]


def test_get_club():
    club = getClubByEmail(clubs, 'test@club.com')

    assert club['name'] == 'Test Club'


def test_get_club_returns_none():
    club = getClubByEmail(clubs, 'g')

    assert club == None


def test_get_competition():
    competition = getCompetition(competitions, 'Test Competition')

    assert competition['name'] == 'Test Competition'


def test_get_competition_returns_none():
    competition = getCompetition(competitions, 'Test Competition 2')

    assert competition == None
