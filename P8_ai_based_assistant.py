import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Example tasks and decisions
tasks = [
    "I am hungry and need food",
    "I have an exam and need to study",
    "I am tired and need rest",
    "I need to travel somewhere",
    "I have a job interview",
    "I need to manage my money"
]

actions = [
    "Find food or prepare a meal",
    "Prepare a study plan",
    "Take some rest",
    "Plan a travel route",
    "Prepare for the job interview",
    "Prepare a budget"
]

# Learn task patterns
model = TfidfVectorizer()
task_data = model.fit_transform(tasks)

# Get a new task
user_task = input("Enter your task: ")

# Compare the new task with known tasks
user_data = model.transform([user_task])
scores = cosine_similarity(user_data, task_data)[0]

best = scores.argmax()

# Make a decision
if scores[best] > 0:
    decision = actions[best]
else:
    decision = "Please provide more details about your task"

print("AI Decision:", decision)

# Display the decision
plt.figure(figsize=(8, 4))
plt.axis("off")

plt.text(0.5, 0.8, "AI TASK ASSISTANT",
         ha="center", fontsize=16, fontweight="bold")

plt.text(0.5, 0.6, "Task: " + user_task,
         ha="center", wrap=True,
         bbox=dict(boxstyle="round", facecolor="lightblue"))

plt.text(0.5, 0.3, "Decision: " + decision,
         ha="center", wrap=True,
         bbox=dict(boxstyle="round", facecolor="lightgreen"))

plt.show()