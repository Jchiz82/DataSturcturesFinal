'''
Joe Chizek - jchizek1@dmacc.edu
Data Structures - Python
12/8/2023
Program Description: The program is a GUI-based golf score tracker that allows users to input their golf scores.
Following multiple entries, the program calculates and displays the top five scores, organizes all scorecards
alphabetically by course name, and provides users with high score, low score, and average score.
'''
import tkinter as tk
from tkinter import messagebox
from queue import PriorityQueue

# Represents a golf scorecard
class Scorecard:
    def __init__(self, course_name, course_par, actual_score):
        # Initializes the scorecard with course information and scores
        self.course_name = course_name
        self.course_par = course_par
        self.actual_score = actual_score
        self.relative_score = actual_score - course_par

    def __lt__(self, other):
        # Defines comparison for sorting in priority queue
        return self.actual_score < other.actual_score

    def __str__(self):
        # String method for scorecard
        sign = "+" \
        if self.relative_score >= 0 else ""
        return f"Course: {self.course_name}, Par: {self.course_par}, Actual Score: {self.actual_score}, Relative Score: {sign}{self.relative_score}"


# Represents a leaderboard for tracking top golf scores
class Leaderboard:
    def __init__(self):
        # Initializes a priority queue
        self.leaderboard = PriorityQueue()

    def add_scorecard(self, scorecard):
        # Adds a scorecard to the leaderboard, keeping only the top 5 scores
        if self.leaderboard.qsize() < 5:
            self.leaderboard.put((scorecard.relative_score, scorecard))
        else:
            # Checks if the new score is better than the worst score in the top 5
            worst_score = self.leaderboard.queue[0][1]
            if scorecard.relative_score < worst_score.relative_score:
                self.leaderboard.get()
                self.leaderboard.put((scorecard.relative_score, scorecard))

    def remove_worst_score(self):
        # Removes the worst score from the leaderboard
        if not self.leaderboard.empty():
            self.leaderboard.get()

    def get_top_scores(self, n=5):
        # Gets the top 5 scores from the leaderboard
        top_scores = []
        for _ in range(min(n, self.leaderboard.qsize())):
            _, scorecard = self.leaderboard.get()
            top_scores.append(scorecard)
        return top_scores

# Represents a results page for displaying golf scores
class ResultsPage(tk.Toplevel):
    def __init__(self, master, app_instance, top_scores, high_score, low_score, average_score, sorted_scorecard_by_alphabet):
        # Initializes the results page
        super().__init__(master)
        self.app_instance = app_instance
        self.title("Results")
        self.geometry("800x400")

        self.result_text = tk.Text(self, height=20, width=70)
        self.result_text.pack()
        self.sorted_by_alpha = sorted_scorecard_by_alphabet
        self.show_results(top_scores, high_score, low_score, average_score)

    def show_results(self, top_scores, high_score, low_score, average_score):
        # Displays all the results on the results page
        result_str = "\nTop 5 scores:\n"
        for i, scorecard in enumerate(top_scores, 1):
            result_str += f"{i}. {str(scorecard)}\n"

        result_str += "\nAll Score Cards Sorted Alphabetically\n"
        for i, scorecard in enumerate(self.sorted_by_alpha, 1):
            result_str += f"{i}. {str(scorecard)}\n"

        result_str += f"\nLow Score: {low_score.actual_score if low_score else 'N/A'}\n"
        result_str += f"High Score: {high_score.actual_score if high_score else 'N/A'}\n"
        result_str += f"Average Score: {average_score}\n"

        self.result_text.insert(tk.END, result_str)

        # Disables the Show Results button in the main app after showing results
        self.app_instance.disable_show_results_button()

# Main application for tracking golf scores
class GolfApp:
    def __init__(self, master):
        # Initializes the main application
        self.master = master
        self.master.title("Golf Score Tracker")

        self.leaderboard = Leaderboard()
        self.scorecards_list = []

        self.create_widgets()

    def create_widgets(self):
        # Creates GUI widgets for entering golf scores
        self.label_course_name = tk.Label(self.master, text="Enter course name:")
        self.label_course_name.pack()

        self.entry_course_name = tk.Entry(self.master)
        self.entry_course_name.pack()

        self.label_course_par = tk.Label(self.master, text="Enter course par:")
        self.label_course_par.pack()

        self.entry_course_par = tk.Entry(self.master)
        self.entry_course_par.pack()

        self.label_actual_score = tk.Label(self.master, text="Enter your actual score:")
        self.label_actual_score.pack()

        self.entry_actual_score = tk.Entry(self.master)
        self.entry_actual_score.pack()

        self.submit_button = tk.Button(self.master, text="Submit", command=self.submit_scorecard)
        self.submit_button.pack()

        self.show_results_button = tk.Button(self.master, text="Show Results", command=self.show_results, state=tk.DISABLED)
        self.show_results_button.pack()

        self.quit_button = tk.Button(self.master, text="Quit", command=self.quit)
        self.quit_button.pack()

    def submit_scorecard(self):
        # Submits a golf scorecard and update the leaderboard
        course_name = self.entry_course_name.get()
        course_par = self.entry_course_par.get()
        actual_score = self.entry_actual_score.get()
        try:
            # Validates the user enters data correctly
            course_par = int(course_par)
            actual_score = int(actual_score)
            if course_par < 0 or actual_score < 0:
                messagebox.showerror("Error", "Course par or actual score must be greater than 0.")
                return
        except ValueError:
            messagebox.showerror("Error", "Course par and actual score must be integers.")
            return

        scorecard = Scorecard(course_name, course_par, actual_score)
        self.leaderboard.add_scorecard(scorecard)
        self.scorecards_list.append(scorecard)

        if self.leaderboard.leaderboard.qsize() > 5:
            self.leaderboard.remove_worst_score()

        # Clears entry fields after submitting a scorecard
        self.entry_course_name.delete(0, tk.END)
        self.entry_course_par.delete(0, tk.END)
        self.entry_actual_score.delete(0, tk.END)

        #Enables the show results button
        self.show_results_button.config(state=tk.NORMAL)

    def sort_score_cards(self, scorecards_list):
        # Sorts golf scorecards alphabetically by course name
        for i in range(len(scorecards_list)):
            for j in range(0, len(scorecards_list)-i-1):
                if scorecards_list[j].course_name > scorecards_list[j+1].course_name:
                    scorecards_list[j], scorecards_list[j+1] = scorecards_list[j+1], scorecards_list[j]
        return scorecards_list

    def show_results(self):
        #Helps display results including top scores, high score, low score, and average score
        top_scores = self.leaderboard.get_top_scores()
        high_score = max(self.scorecards_list, key=lambda x: x.actual_score, default=None)
        low_score = min(self.scorecards_list, key=lambda x: x.actual_score, default=None)
        average_score = int(sum(scorecard.actual_score for scorecard in self.scorecards_list) / len(self.scorecards_list))

        # Sort scorecards alphabetically
        sorted_scorecard_by_alphabet = self.sort_score_cards(self.scorecards_list)

        # Creates and shows the results page
        ResultsPage(self.master, self, top_scores, high_score, low_score, average_score, sorted_scorecard_by_alphabet)

        # Disables the Submit button after showing results
        self.submit_button.config(state=tk.DISABLED)

    # Disables the Submit button after showing results
    def disable_show_results_button(self):
        self.show_results_button.config(state=tk.DISABLED)

    #Quits/Destroys the application
    def quit(self):
        self.master.destroy()

if __name__ == "__main__":
    # Creates the main Tkinter window and GolfApp
    root = tk.Tk()
    app = GolfApp(root)
    root.mainloop()
