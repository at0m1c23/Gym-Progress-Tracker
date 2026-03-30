class Workout:
    #Initializing atrributes for workout class
    def __init__(self, name, sets, reps, weight, rest_time): 
        self.name = name
        self.sets = sets
        self.reps = reps
        self.weight = weight
        self.rest_time = rest_time
        self.current_set = 0
    
    #Creating a set complete function to check if a set is done within a workout
    def complete_set(self): 
        if self.current_set < self.sets:
            self.current_set += 1
            print(f"Completed set {self.current_set} of {self.sets}.")

            #Checking if the workout sets are done
            if self.current_set < self.sets:
                print(f"Rest for {self.rest_time} seconds until the next set")
                return "rest"   
            else:
                print(f"You've completed {self.sets} out of {self.sets} sets for {self.name}.")
                return "done" 
        else:  
            print(f"All sets already completed for {self.name}")
            return "done"
        
    #To create a function that allows for rest to occur via button 
    def start_rest(self,label,button): 
        button.config(state="disabled")
        remaining = self.rest_time

        #To count and create a display for time
        def countdown(): 
            nonlocal remaining
            minutes = remaining // 60
            seconds = remaining % 60
            label.config(text=f"Rest: {minutes}:{seconds:02d}")

            if remaining > 0:
                remaining -= 1
                label.after(1000, countdown)
            else:
                label.config(text="Rest Done!")
                button.config(state="normal")
        countdown()

    #To make sure that sets of a workout are finished/completed
    def is_completed(self):
        return self.current_set >= self.sets
    
    #To transfer the data collected by previous functions are displayed properly and orderly
    def get_display_info(self):
        minutes = self.rest_time // 60
        seconds = self.rest_time % 60
        info = (
            f"Workout: {self.name}\n"
            f"Set: {self.current_set} / {self.sets}\n"
            f"Reps {self.reps}\n"
            f"Weight {self.weight}kg\n"
            f"Rest: {minutes}:{seconds:02d}"
        )
        return info

class Session:
    #Initializing for session class, which is used to track over multiple workouts
    def __init__(self,workouts):
        self.workouts = workouts
        self.current_index = 0

    #To double check the validity of pairs, index to the workout
    def get_current_workout(self):
        if self.current_index < len(self.workouts):
            return self.workouts[self.current_index]
        return None
    
    #To double check validity of the pair, first checking if its valid within parameters, then updating self.current_index by 1 to move to next workout
    def next_workout(self):
        if self.current_index < len(self.workouts) - 1:
            self.current_index += 1
            print(f"Now doing: {self.get_current_workout().name}")
        else:
            self.current_index += 1
            print("All workouts completed!")

    #To check the current workout out of all workouts
    def session_progress(self):
        total = len(self.workouts)
        return f"Workout {self.current_index + 1} of {total}"
    
    #Returns a boolean (state checker)
    def is_session_completed(self):
        return self.current_index >= len(self.workouts)
    
def get_positive_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            else:
                print("Input a value larger than 0.")
        except ValueError:
            print("Please input a valid number.")


def run_cli_session():
    num_workouts = int(input("How many workouts are going to be in this session? "))
    workouts = []

    for i in range(num_workouts):
        name = input("Name: ")
        sets = get_positive_int("Sets: ")
        reps = get_positive_int("Reps: ")
        weight = get_positive_int("Weight (kg): ")
        rest_time = get_positive_int("Rest time (seconds): ")

        workout = Workout(name, sets, reps, weight, rest_time)
        workouts.append(workout)

    session = Session(workouts)

    while not session.is_session_completed():
        current = session.get_current_workout()
        print("\n=== Current Workout ===")
        print(current.get_display_info())

        while not current.is_completed():
            input("Press Enter to complete a set...\n")
            status = current.complete_set()
            print(current.get_display_info())
            if status == "rest":
                print(f"Rest for {current.rest_time} seconds\n")
                import time
                time.sleep(1)

        session.next_workout()

    print("\nSession completed! All workouts done")

if __name__ == "__main__":
    run_cli_session()