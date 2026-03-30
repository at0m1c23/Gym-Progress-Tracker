from Final import Workout, Session
import tkinter as tk
from tkinter import messagebox

class WorkoutApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Workout App")
        self.root.geometry("450x600")
        self.root.configure(bg="#F5F5F7")

        # Temporary storage for workouts
        self.workouts = []

        # ---- DES Frame ----
        self.des_frame = tk.Frame(root, bg="white")
        self.des_frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=500)

        tk.Label(self.des_frame, text="Enter Your Workouts:", font=("Helvetica", 16, "bold"), bg="white", fg="black").pack(pady=10)

        # Entry fields
        self.entries = {}
        fields = ["Name", "Sets", "Reps", "Weight (kg)", "Rest (s)"]
        for field in fields:
            frame = tk.Frame(self.des_frame, bg="white")
            frame.pack(pady=5, fill="x", padx=20)
            tk.Label(frame, text=field+":", width=12, anchor="w", bg="white", fg="black").pack(side="left")
            entry = tk.Entry(frame)
            entry.pack(side="left", fill="x", expand=True)
            self.entries[field] = entry

        # Add Workout Button
        self.add_button = tk.Button(self.des_frame, text="Add Workout", bg="#007AFF", fg="black", command=self.add_workout)
        self.add_button.pack(pady=15)

        # Workout list display
        self.workout_list_label = tk.Label(self.des_frame, text="No workouts added", bg="white", fg="black", justify="left")
        self.workout_list_label.pack(pady=10)

        # Start Session Button
        self.start_button = tk.Button(self.des_frame, text="Start Session", bg="#34C759", fg="black", command=self.start_session)
        self.start_button.pack(pady=20)

    # Add workout from DES to list
    def add_workout(self):
        try:
            name = self.entries["Name"].get()
            sets = int(self.entries["Sets"].get())
            reps = int(self.entries["Reps"].get())
            weight = int(self.entries["Weight (kg)"].get())
            rest = int(self.entries["Rest (s)"].get())

            if not name:
                messagebox.showerror("Error", "Workout name cannot be empty")
                return
            if sets <= 0 or reps <= 0 or weight <= 0 or rest <= 0:
                messagebox.showerror("Error", "Sets, Reps, Weight, and Rest must all be greater than 0.")
                return

            workout = Workout(name, sets, reps, weight, rest)
            self.workouts.append(workout)
            self.update_workout_list()
            self.clear_entries()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for sets, reps, weight, and rest")

    # Update the workout list display
    def update_workout_list(self):
        if not self.workouts:
            self.workout_list_label.config(text="No workouts added")
        else:
            text = "Workouts Added:\n"
            for i, w in enumerate(self.workouts, start=1):
                text += f"{i}. {w.name} ({w.sets}x{w.reps}, {w.weight}kg, rest {w.rest_time}s)\n"
            self.workout_list_label.config(text=text)

    # Clear entries after adding
    def clear_entries(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    # Launch the session screen
    def start_session(self):
        if not self.workouts:
            messagebox.showerror("Error", "Add at least one workout to start session")
            return
        # Hide DES
        self.des_frame.destroy()
        # Initialize session
        self.session = Session(self.workouts)
        self.launch_session_screen()

    # Session GUI
    def launch_session_screen(self):
        self.session_frame = tk.Frame(self.root, bg="white")
        self.session_frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=500)

        self.title_label = tk.Label(self.session_frame, text="Workout Session", font=("Helvetica", 16, "bold"), bg="white", fg="black")
        self.title_label.pack(pady=10)

        self.display_label = tk.Label(self.session_frame, text="", font=("Helvetica", 14), bg="white", fg="black", justify="left")
        self.display_label.pack(pady=20)

        self.action_button = tk.Button(self.session_frame, text="Complete Set", bg="#007AFF", fg="black",
                                       command=self.complete_set_action)
        self.action_button.pack(pady=30)

        self.update_display()

    # Update display during session
    def update_display(self):
        current = self.session.get_current_workout()
        if current:
            info = current.get_display_info()
            progress = self.session.session_progress()
            self.display_label.config(text=f"{progress}\n\n{info}")
        else:
            self.display_label.config(text="🎉 Session Completed!")
            self.action_button.config(state="disabled")

    def next_workout_action(self):
        self.session.next_workout()
        if self.session.is_session_completed():
            self.display_label.config(text="🎉 Session Completed!")
            self.action_button.config(state="disabled")
        else:
            self.action_button.config(text="Complete Set", command=self.complete_set_action)
            self.update_display()

    # Button logic
    def complete_set_action(self):
        current = self.session.get_current_workout()
        if not current:
            return
        
        status = current.complete_set()

        self.update_display()

        if status == "rest":
            current.start_rest(self.display_label, self.action_button)
            return
        
        if status == "done":
            self.action_button.config(text="Next Workout", command=self.next_workout_action)


if __name__ == "__main__":
    root = tk.Tk()
    app = WorkoutApp(root)
    root.mainloop()
    