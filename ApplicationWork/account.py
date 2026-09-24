import json

# Class for storing an account
class Account:
    def __init__(self, username, password,  admin=False, locked=False, failedAttempts = 0):
        self.username = username
        self.password = password
        self.admin = admin
        self.locked = locked
        self.failedAttempts = failedAttempts
        self.workoutHistory = []

# Class for storing a single workout session
class Workout:
    def __init__(self, exercise, weight, sets, reps, rest, accuracy, date):
        self.exercise = exercise
        self.weight = weight
        self.sets = sets
        self.reps = reps
        self.rest = rest
        self.accuracy = accuracy
        self.date = date 

#Method for saving all account data to the accounts.json file
def saveAccounts(accounts):
    data = []

    for account in accounts:
        accountData = {
            "username": account.username,
            "password": account.password,
            "admin": account.admin,
            "locked": account.locked,
            "failed attempts":account.failedAttempts,
            "workoutHistory": []
        }

        for workout in account.workoutHistory:
            workoutData = {
                "exercise": workout.exercise,
                "weight": workout.weight,
                "sets": workout.sets,
                "reps": workout.reps,
                "rest": workout.rest,
                "accuracy": workout.accuracy,
                "date": workout.date
            }

            accountData["workoutHistory"].append(workoutData)

        data.append(accountData)

    with open("accounts.json", "w") as file:
        json.dump(data, file, indent=4)

#Method for loading all account data from accounts.json
def loadAccounts():
    try:
        with open("accounts.json", "r") as file:
            data = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        return []

    accounts = []

    for accountData in data:
        account = Account(
            accountData["username"],
            accountData["password"],
            accountData["admin"],
            accountData["locked"],
            accountData["failed attempts"]
        )

        for workoutData in accountData["workoutHistory"]:
            workout = Workout(
                workoutData["exercise"],
                workoutData["weight"],
                workoutData["sets"],
                workoutData["reps"],
                workoutData["rest"],
                workoutData["accuracy"],
                workoutData["date"]
            )

            account.workoutHistory.append(workout)

        accounts.append(account)

    return accounts

