import tkinter as tk
from account import Account, saveAccounts, loadAccounts, Workout
from tkinter import messagebox

# section that will contain the entire interface for the trainer application
class RaiderTrainer(tk.Tk):
    def __init__(self):
        super().__init__()

        # setting up GUI window
        self.title("RaiderTrainer")
        self.geometry("1000x850")
        self.resizable(False, False)

        # tracks current user
        self.current_user = None

        # account list
        self.accounts = loadAccounts()

        # placeholder set of user information for workouts
        self.exercise = ""
        self.weight = ""
        self.reps = 10
        self.rest = 30
        self.sets = 3
        self.accuracy = "95%"

        # sets up the main container for GUI
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # sets up a list of all different pages
        self.frames = {}

        # sets up each different page in the interface
        for page in (LoginPage, AccountCreation, UserMenu, ExerciseSelection, WorkoutSetup, WorkoutPage, WorkoutSummary, WorkoutHistory, AdminMenu):
            # assign each page on application its own frame
            frame = page(self.container, self)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # makes login page the landing
        self.show_frame(LoginPage)

    # method that allows user to change across different pages/frames
    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()

# section of the application that is the landing page where user logs in
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # creates the main title of the login page 
        title = tk.Label(self, text="RaiderTrainer", font=("Impact", 32, "bold"), fg="green")
        title.pack(pady=(100, 10))
        # creates subtitle below main title
        subtitle = tk.Label(self, text="Strength Training/Exercise Assistant", font=("Arial", 16), fg="gold")
        subtitle.pack(pady=(0, 40))

        # sets up username login prompt
        tk.Label(self, text="Username:", font=("Arial", 14)).pack()
        self.usernameInput = tk.Entry(self, font=("Arial", 14), width=25)
        self.usernameInput.pack(pady=10)

        # sets up password login prompt
        tk.Label(self,text="Password:", font=("Arial", 14)).pack()
        self.passwordInput = tk.Entry(self, font=("Arial", 14), width=25, show="*")
        self.passwordInput.pack(pady=10)

        # sets up button to login into account
        loginButton = tk.Button(self, text="Login", font=("Arial", 14), width=20, command=self.login)
        loginButton.pack(pady=20)

        # sets up button to create new account
        createButton = tk.Button(self, text="Create Account", font=("Arial", 14), width=20, command=lambda: self.controller.show_frame(AccountCreation))
        createButton.pack(pady=20)

    # method set up to actually login a user
    def login(self):
        # takes in username and password
        username = self.usernameInput.get()
        password = self.passwordInput.get()

        # Locates the account with the given username
        usernameFound = False
        for account in self.controller.accounts:
            if account.username == username:
                usernameFound = True
                break

        incorrectPasswordCount = 0

        #Admin login, will be replaced later
        if username == "Admin":
            self.controller.show_frame(AdminMenu)

        #user login
        elif username != "":

            if usernameFound == True:

                if password != "":

                    # Prevents login if account is locked
                    if account.locked == True:
                            messagebox.showerror("Login Error", 
                                                "Account Locked")

                    # logs user in if password is correct
                    elif password == account.password:
                        account.failedAttempts = 0
                        self.controller.current_user = username
                        self.controller.show_frame(UserMenu)

                    # locks account after 3 failed login attempts
                    else:
                        account.failedAttempts += 1
                        if account.failedAttempts >= 3:
                            account.locked = True
                            saveAccounts(self.controller.accounts)
                            messagebox.showerror("Login Error", 
                                                "3 Failed login attempts, account is now locked")
                        else:
                            messagebox.showerror("Login Error", 
                                                "Password Incorrect")
                else:
                    messagebox.showerror("Login Error", 
                                        "Please enter a password")                    
            else:
                messagebox.showerror("Login Error", 
                                    "Account not Found")              
        else:
            messagebox.showerror("Login Error", 
                                 "Please enter a username.")

# page of the application that displays account creation
class AccountCreation(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # creates the main title of the login page 
        title = tk.Label(self, text="RaiderTrainer", font=("Impact", 32, "bold"), fg="green")
        title.pack(pady=(100, 10))
        # creates subtitle below main title
        subtitle = tk.Label(self, text="Strength Training/Exercise Assistant", font=("Arial", 16), fg="gold")
        subtitle.pack(pady=(0, 40))

        # sets up username creation prompt
        tk.Label(self, text="Create a username: ", font=("Arial", 14)).pack()
        self.usernameInput = tk.Entry(self, font=("Arial", 14), width=25)
        self.usernameInput.pack(pady=10)

        # sets up password creation prompt
        tk.Label(self,text="Create a password: ", font=("Arial", 14)).pack()
        self.passwordInput = tk.Entry(self, font=("Arial", 14), width=25, show="*")
        self.passwordInput.pack(pady=10)

        # sets up button to create account
        createButton = tk.Button(self, text="Create Account", font=("Arial", 14), width=20, command=self.createAccount)
        createButton.pack(pady=20)

        # sets up button to go back to login page
        backButton = tk.Button(self, text="Back to Login", font=("Arial", 14), width=20, command=lambda: self.controller.show_frame(LoginPage))
        backButton.pack(pady=20)

    # method to create new account
    def createAccount(self):
        # takes in username and password
        username = self.usernameInput.get()
        password = self.passwordInput.get()

        #checks if username is already in use
        usernameTaken = False
        for account in self.controller.accounts:
            if account.username == username:
                usernameTaken = True

        if usernameTaken == True:
            messagebox.showerror("Account Creation Error", 
                                 "Username is taken.")

        # checks if username consists of 8 lowercase characters
        elif (len(username) == 8 
              and username.isalpha() 
              and username.islower()):

            # checks if password is 12 characters, including 1 uppercase and 1 lowercase letter, 1 number, and 1 special character
            if (len(password) == 12 
                and any(c.isupper() for c in password) 
                and any(c.islower() for c in password)
                and any(c.isdigit() for c in password)
                and any(not c.isalnum() for c in password)):

                # Creates new account and logs the user in
                self.controller.current_user = username
                newAccount = Account(username, password)
                self.controller.accounts.append(newAccount)
                saveAccounts(self.controller.accounts)
                self.controller.show_frame(UserMenu)

            else:
                messagebox.showerror("Account Creation Error",
                                     "Password must be exactly 12 characters and contain "
                                     "at least 1 uppercase letter, 1 lowercase letter, "
                                     "1 number, and 1 special character.")
                
        else:
            messagebox.showerror("Account Creation Error", 
                                 "Username must be exactly 8 lowercase letters.")

# page of the application that is the regular user menu for the raider trainer
class UserMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # title of the user screen
        tk.Label(self, text="User Menu", font=("Impact", 28, "bold"), fg="green").pack(pady=40)

        # subtitle of user screen to welcome in the specific user
        self.welcomeLabel = tk.Label(self, text="", font=("Arial", 16), fg="gold")
        self.welcomeLabel.pack(pady=10)

        # button to go to the exercise selection page for the user
        tk.Button(self, text="Select Workout", font=("Arial", 14), width=25, command=lambda: controller.show_frame(ExerciseSelection)).pack(pady=15)

        # button to go to the workout history page for the user
        tk.Button(self, text="View History", font=("Arial", 14), width=25, command=lambda: controller.show_frame(WorkoutHistory)).pack(pady=15)

        # button to go return to the login page
        tk.Button(self, text="Logout", font=("Arial", 14), width=25, command=lambda: controller.show_frame(LoginPage)).pack(pady=15)

    # method to implement username in the welcome subtitle of the user page
    def tkraise(self, *args, **kwargs):
        self.welcomeLabel.config(text="Welcome, " + self.controller.current_user + "!")
        super().tkraise(*args, **kwargs)

# page of the application that provides the user selection of exercises available
class ExerciseSelection(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # title label for user exercise selection
        tk.Label(self, text="Choose an Exercise", font=("Impact", 28, "bold"), fg="green").pack(pady=50)

        # button to select first workout
        tk.Button(self, text="Bicep Curl", font=("Arial", 16), width=25, command=lambda: self.selectExercise("Bicep Curl")).pack(pady=15)

        # button to select second workout
        tk.Button(self, text="Lateral Raise", font=("Arial", 16), width=25, command=lambda: self.selectExercise("Lateral Raise")).pack(pady=15)

        # button to return to user menu
        tk.Button(self, text="Back", font=("Arial", 14), width=15, command=lambda: controller.show_frame(UserMenu)).pack(pady=30)

    # method to initialize the two different exercises for selection and display
    def selectExercise(self, exercise):
        self.controller.exercise = exercise
        self.controller.show_frame(WorkoutSetup)

# page of the application that displays the selected workout exercise information and selections for sets/reps/intervals
class WorkoutSetup(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # title label for the workout set up page
        tk.Label(self, text="Workout Setup", font=("Impact", 28, "bold"), fg="green").pack(pady=35)

        # subtitle label to display the selected workout user is setting up
        self.exerciseLabel = tk.Label(self, text="Exercise:", font=("Arial", 16), fg="gold")
        self.exerciseLabel.pack(pady=10)

        # sets up option menu for user to select weight from listed options
        tk.Label(self, text="Weight", font=("Arial", 14)).pack()
        self.selectedWeight = tk.StringVar()
        self.selectedWeight.set("5 lbs")
        tk.OptionMenu(self, self.selectedWeight, "5 lbs", "10 lbs", "15 lbs").pack(pady=10)

        # sets up user sets input for workout
        tk.Label(self, text="Sets", font=("Arial", 14)).pack()
        self.setsInput = tk.Entry(self, font=("Arial", 14), width=10)
        self.setsInput.insert(0, "3")
        self.setsInput.pack(pady=10)

        # sets up user reps input for workout
        tk.Label(self, text="Reps", font=("Arial", 14)).pack()
        self.repsInput = tk.Entry(self,font=("Arial", 14), width=10)
        self.repsInput.insert(0, "10")
        self.repsInput.pack(pady=10)

        # sets up user rest intervals input for workout
        tk.Label(self, text="Rest Interval (Seconds)", font=("Arial", 14)).pack()
        self.restInput = tk.Entry(self, font=("Arial", 14), width=10)
        self.restInput.insert(0, "30")
        self.restInput.pack(pady=10)

        # button for starting the workout 
        tk.Button(self, text="Start Workout", font=("Arial", 14), width=20, command=self.start_workout).pack(pady=25)
        # button for returning back to exercise selection page
        tk.Button(self, text="Back", font=("Arial", 14), width=15, command=lambda: controller.show_frame(ExerciseSelection)).pack()

    # method to define which workout is being displayed
    def tkraise(self, *args, **kwargs):
        self.exerciseLabel.config(text="Exercise: " + self.controller.exercise)
        super().tkraise(*args, **kwargs)

    # method to move to the workout page and setup the workout duration 
    def start_workout(self):
        # transfer the following selected data from the setup page onto the actual workout page
        try:
            self.controller.weight = self.selectedWeight.get()
            self.controller.reps = int(self.repsInput.get())
            self.controller.rest = int(self.restInput.get())
            self.controller.sets = int(self.setsInput.get())
            self.controller.show_frame(WorkoutPage)
        # catches any input errors if any fields are left empty 
        except ValueError:
            messagebox.showerror("Input Error", "Please fill out every input field.")

# page of the application that will contain the active workout session of an exercise
class WorkoutPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # title label for the active workout session
        tk.Label(self, text="Active Workout Session", font=("Impact", 28, "bold"), fg="green").pack(pady=30)

        # subtitle label for the selected workout and weights
        self.exerciseLabel = tk.Label(self, text="", font=("Arial", 18), fg="gold")
        self.exerciseLabel.pack(pady=10)

        # temporary placeholder for where the camera posetracker will be displayed for the workout
        cameraGrid = tk.Frame(self, width=600, height=300, relief="solid", borderwidth=2)
        cameraGrid.pack(pady=20)
        cameraGrid.pack_propagate(False)
        tk.Label(cameraGrid, text="CAMERA GOES HERE", font=("Arial", 18)).pack(expand=True)

        # set display
        self.setLabel = tk.Label(self, text="SET: 1 / 3", font=("Arial", 20, "bold"))
        self.setLabel.pack(pady=5)

        # rep display
        self.repLabel = tk.Label(self, text="REP: 0 / 10", font=("Arial", 20, "bold"))
        self.repLabel.pack(pady=5)

        # display to track the users form during workout
        self.formLabel = tk.Label(self, text="FORM: WAITING", font=("Arial", 18))
        self.formLabel.pack(pady=10)

        # placeholder button to represent tracking a workout
        tk.Button(self, text="Simulate Correct Rep", font=("Arial", 12), command=self.simulateRep).pack(pady=10)

        # button to end a workout and head to summary page
        tk.Button(self, text="End Workout", font=("Arial", 14), width=20, command=lambda: controller.show_frame(WorkoutSummary)).pack(pady=10)

    # method that defines the starting values for all the workout information (sets, reps, intervals) to track workout progress
    def tkraise(self, *args, **kwargs):
        self.exerciseLabel.config(text=self.controller.exercise + " - " + self.controller.weight)
        self.setLabel.config(text="SET: 1 / " + str(self.controller.sets))
        self.repLabel.config(text="REP: 0 / " + str(self.controller.reps))
        self.formLabel.config(text="FORM: WAITING")
        self.currentRep = 0
        super().tkraise(*args, **kwargs)

    # method to carry out the completion of a singular rep
    def simulateRep(self):
        # condition to track rep count
        if self.currentRep < self.controller.reps:
            self.currentRep += 1
            self.repLabel.config(text="REP: " + str(self.currentRep) + " / " + str(self.controller.reps))
            self.formLabel.config(text="FORM: CORRECT")

# page of the application that provides the user their workout summary
class WorkoutSummary(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # title label to display completed workout
        tk.Label(self, text="Workout Complete!", font=("Impact", 28, "bold"), fg="green").pack(pady=50)

        # label that will list all the details of the completed and selected workout
        self.summaryLabel = tk.Label(self, text="", font=("Arial", 16), fg="gold", justify="left")
        self.summaryLabel.pack(pady=20)

        # button to return back to the user menu
        tk.Button(self, text="Back to User Menu", font=("Arial", 14), width=25, command=lambda: controller.show_frame(UserMenu)).pack(pady=15)
        # button to return to the users workout history
        tk.Button(self, text="View History", font=("Arial", 14), width=25,command=lambda: controller.show_frame(WorkoutHistory)).pack(pady=15)

    # method that lists all the exercise workout summary in the given order as well as saves the workout
    def tkraise(self, *args, **kwargs):
       # Create the completed workout
        newWorkout = Workout(
            self.controller.exercise,
            self.controller.weight,
            self.controller.sets,
            self.controller.reps,
            self.controller.rest,
            self.controller.accuracy,
            "2026-09-23"
        )

        # Add workout to current user's history
        for account in self.controller.accounts:
            if account.username == self.controller.current_user:
                account.workoutHistory.append(newWorkout)
                saveAccounts(self.controller.accounts)
                break
 
        self.summaryLabel.config(text= "Exercise: " + self.controller.exercise + "\nWeight: " + self.controller.weight 
        + "\nSets: " + str(self.controller.sets) + "\nReps: " +
        str(self.controller.reps) + " seconds" + "\nRest Intervals: " + str(self.controller.rest) + "\nAccuracy: " + self.controller.accuracy)
        super().tkraise(*args, **kwargs)

# page of the website that tracks and lists the workout history of a user
class WorkoutHistory(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # title label for the history page/list
        tk.Label(self, text="Workout History", font=("Impact", 28, "bold"), fg="green").pack(pady=40)

        # label that lists all the content of a users workout history      
        self.historyLabel = tk.Label(self, text="", font=("Arial", 14), fg="gold", justify="left")
        self.historyLabel.pack(pady=20)

        # button to return to the user home back
        tk.Button(self,text="Return", font=("Arial", 14), width=20, command=lambda: controller.show_frame(UserMenu)).pack(pady=30)

    #method that lists the current users workout history
    def tkraise(self, *args, **kwargs):

        historyList = ""

        for account in self.controller.accounts:

            if account.username == self.controller.current_user:

                #Displays Workout History
                for workout in account.workoutHistory:
                    historyList += (
                        workout.date + "\n" +
                        workout.exercise +
                        " - Weight: " + workout.weight +
                        " lbs | Sets: " + str(workout.sets) +
                        " | Reps: " + str(workout.reps) +
                        " | Accuracy: " + str(workout.accuracy) +
                        "%\n\n"
                    )

        self.historyLabel.config(text=historyList)

        super().tkraise(*args, **kwargs)

# page of the application that holds the admin menu
class AdminMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # title label of the admin menu display
        tk.Label(self, text="Admin Menu", font=("Impact", 28, "bold"), fg="green").pack(pady=40)
        # subtitle label of the list of user accounts within the raider trainer interface/database
        tk.Label(self, text="User Accounts", font=("Arial", 18, "bold"), fg="gold").pack(pady=10)

        # placeholder list of usernames that the admin will have access to
        users = ["AdamHamdan       LOCKED", "WilliamBurson      ACTIVE", "GavinLemoine       ACTIVE"]

        # displays the user list onto the screen
        for user in users:
            tk.Label(self, text=user, font=("Courier", 14)).pack(pady=5)

        # placeholder button to represent the action of an admin fixing a user account
        tk.Button(self, text="Unlock Account", font=("Arial", 14), width=25, command=self.unlockAccount).pack(pady=20)
        # button to logout of admin account and return to login page
        tk.Button(self, text="Logout", font=("Arial", 14), width=20, command=lambda: controller.show_frame(LoginPage)).pack(pady=10)

    # method to represent the action of a users account being unlocked
    def unlockAccount(self):
        messagebox.showinfo("Account Unlocked", "Account has been unlocked.\n\n" "New Password: temporaryTesting123!")

# main function of code to run the GUI
if __name__ == "__main__":
    app = RaiderTrainer()
    app.mainloop()
