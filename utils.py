from datetime import datetime


def competitionIsPassed(competition):
    competitionDate = datetime.strptime(
        competition['date'], '%Y-%m-%d %H:%M:%S').date()
    today = datetime.today().date()

    return competitionDate < today


def withPassedCompetitions(competitions):
    competitionsWithIsPassed = [
        {**competition, 'isPassed': competitionIsPassed(competition)}
        for competition in competitions
    ]

    return competitionsWithIsPassed


def getClub(clubs, key, value):
    club = [club for club in clubs if club[key] == value]

    if len(club) == 0:
        return None

    return club[0]


def getClubByEmail(clubs, email):
    return getClub(clubs, 'email', email)


def getClubByName(clubs, name):
    return getClub(clubs, 'name', name)


def getCompetition(competitions, name):
    competition = [
        competition for competition in competitions if competition['name'] == name]

    if len(competition) == 0:
        return None

    return competition[0]
