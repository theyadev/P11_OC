import json

from flask import Flask, render_template, request, redirect, flash, url_for
from utils import withPassedCompetitions, competitionIsPassed, getClubByEmail, getClubByName, getCompetition


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    club = getClubByEmail(clubs, request.form['email'])

    if not club:
        flash('No club found with that email address')

        return redirect(url_for('index'), 404)

    return render_template('welcome.html', club=club, competitions=withPassedCompetitions(competitions))


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = getClubByName(clubs, club)
    foundCompetition = getCompetition(competitions, competition)

    if not foundClub or not foundCompetition:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=withPassedCompetitions(competitions))

    return render_template('booking.html', club=foundClub, competition=foundCompetition)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = getCompetition(competitions, request.form['competition'])
    club = getClubByName(clubs, request.form['club'])

    if not competition or not club:
        flash("Something went wrong-please try again")
        return render_template('booking.html', club=club, competition=competition)

    placesRequired = int(request.form['places'])
    numberOfPlaces = int(competition['numberOfPlaces'])

    if competitionIsPassed(competition):
        flash("Sorry, you cannot book for a competition in the past")
        return render_template('booking.html', club=club, competition=competition)

    points = int(club['points'])

    if placesRequired < 0:
        flash("You cannot book a negative number of places")
        return render_template('booking.html', club=club, competition=competition)

    if placesRequired > numberOfPlaces:
        flash("Sorry, there are not enough places available")
        return render_template('booking.html', club=club, competition=competition)

    if placesRequired > 12:
        flash("You cannot book more than 12 places")
        return render_template('booking.html', club=club, competition=competition)

    if points < placesRequired:
        flash("Sorry, you do not have enough points to book this number of places")
        return render_template('booking.html', club=club, competition=competition)

    competition['numberOfPlaces'] = numberOfPlaces - placesRequired
    club['points'] = points - placesRequired

    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=withPassedCompetitions(competitions))


@app.route("/clubs")
def list_clubs():
    return render_template(
        "clubs.html",
        clubs=clubs,
    )


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
