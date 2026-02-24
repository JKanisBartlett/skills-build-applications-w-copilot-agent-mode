from django.core.management.base import BaseCommand
from django.conf import settings

from pymongo import MongoClient

# Sample data for superheroes, teams, activities, leaderboard, and workouts
def get_sample_data():
    users = [
        {"name": "Superman", "email": "superman@dc.com", "team": "DC"},
        {"name": "Batman", "email": "batman@dc.com", "team": "DC"},
        {"name": "Wonder Woman", "email": "wonderwoman@dc.com", "team": "DC"},
        {"name": "Iron Man", "email": "ironman@marvel.com", "team": "Marvel"},
        {"name": "Captain America", "email": "cap@marvel.com", "team": "Marvel"},
        {"name": "Black Widow", "email": "widow@marvel.com", "team": "Marvel"},
    ]
    teams = [
        {"name": "Marvel", "members": ["Iron Man", "Captain America", "Black Widow"]},
        {"name": "DC", "members": ["Superman", "Batman", "Wonder Woman"]},
    ]
    activities = [
        {"user": "Superman", "activity": "Flight", "duration": 60},
        {"user": "Batman", "activity": "Martial Arts", "duration": 45},
        {"user": "Iron Man", "activity": "Suit Training", "duration": 50},
    ]
    leaderboard = [
        {"user": "Superman", "score": 100},
        {"user": "Iron Man", "score": 95},
        {"user": "Batman", "score": 90},
    ]
    workouts = [
        {"name": "Strength Training", "suggested_for": ["Superman", "Wonder Woman"]},
        {"name": "Agility Drills", "suggested_for": ["Batman", "Black Widow"]},
    ]
    return users, teams, activities, leaderboard, workouts

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Connect to MongoDB using pymongo
        client = MongoClient("mongodb://localhost:27017/")
        db = client["octofit_db"]
        users, teams, activities, leaderboard, workouts = get_sample_data()

        # Drop collections if they exist
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Insert data
        db.users.insert_many(users)
        db.teams.insert_many(teams)
        db.activities.insert_many(activities)
        db.leaderboard.insert_many(leaderboard)
        db.workouts.insert_many(workouts)

        # Ensure unique index on email
        db.users.create_index("email", unique=True)

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data.'))
