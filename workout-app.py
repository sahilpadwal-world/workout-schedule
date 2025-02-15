import streamlit as st
import os

class Workout:
    def __init__(self, date, exercise_type, duration, calories_burned):
        self.date = date
        self.exercise_type = exercise_type
        self.duration = duration
        self.calories_burned = calories_burned

    def __str__(self):
        return f"{self.date}: {self.exercise_type} for {self.duration} minutes, {self.calories_burned} calories burned"

class User:
    def __init__(self, name, age, weight):
        self.name = name
        self.age = age
        self.weight = weight
        self.workouts = []

    def add_workout(self, workout):
        self.workouts.append(workout)

    def view_workouts(self):
        return "\n".join(str(workout) for workout in self.workouts) if self.workouts else "No workouts recorded yet."

    def save_data(self, filename):
        try:
            with open(filename, "w") as file:
                for workout in self.workouts:
                    file.write(f"{workout.date},{workout.exercise_type},{workout.duration},{workout.calories_burned}\n")
            return "Data saved successfully!"
        except Exception as e:
            return f"Error saving data: {e}"

    def load_data(self, filename):
        try:
            if not os.path.exists(filename):
                return "File not found!"
            self.workouts.clear()
            with open(filename, "r") as file:
                for line in file:
                    date, exercise_type, duration, calories_burned = line.strip().split(",")
                    self.workouts.append(Workout(date, exercise_type, int(duration), int(calories_burned)))
            return "Data loaded successfully!"
        except Exception as e:
            return f"Error loading data: {e}"

st.title("Workout Tracker")

if "user" not in st.session_state:
    st.session_state.user = None

with st.sidebar:
    st.header("User Profile")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, step=1)
    weight = st.number_input("Weight (kg)", min_value=1, step=1)
    if st.button("Create User"):
        st.session_state.user = User(name, age, weight)
        st.success(f"User {name} created!")

st.header("Add Workout")
date = st.text_input("Date (YYYY-MM-DD)")
exercise_type = st.text_input("Exercise Type")
duration = st.number_input("Duration (minutes)", min_value=1, step=1)
calories_burned = st.number_input("Calories Burned", min_value=1, step=1)
if st.button("Add Workout"):
    if st.session_state.user:
        workout = Workout(date, exercise_type, duration, calories_burned)
        st.session_state.user.add_workout(workout)
        st.success("Workout added successfully!")
    else:
        st.error("Please create a user first!")

st.header("View Workouts")
if st.button("Show Workouts"):
    if st.session_state.user:
        st.text(st.session_state.user.view_workouts())
    else:
        st.error("Please create a user first!")

st.header("Save/Load Data")
filename = st.text_input("Filename")
col1, col2 = st.columns(2)
with col1:
    if st.button("Save Data"):
        if st.session_state.user:
            st.success(st.session_state.user.save_data(filename))
        else:
            st.error("Please create a user first!")
with col2:
    if st.button("Load Data"):
        if st.session_state.user:
            st.success(st.session_state.user.load_data(filename))
        else:
            st.error("Please create a user first!")
