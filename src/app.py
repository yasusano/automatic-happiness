"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Practice teamwork and compete in soccer matches",
        "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["alex@mergington.edu", "lucas@mergington.edu"]
    },
    "Basketball Club": {
        "description": "Develop shooting, passing, and defensive skills",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 14,
        "participants": ["noah@mergington.edu", "mia@mergington.edu"]
    },
    "Tennis Club": {
        "description": "Improve your serve, volleys, and court strategy",
        "schedule": "Tuesdays and Thursdays, 4:30 PM - 5:30 PM",
        "max_participants": 12,
        "participants": ["harper@mergington.edu", "jack@mergington.edu"]
    },
    "Swimming Team": {
        "description": "Build endurance and technique in competitive swimming",
        "schedule": "Mondays and Wednesdays, 3:45 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["isabella@mergington.edu", "logan@mergington.edu"]
    },
    "Drama Club": {
        "description": "Explore acting, stagecraft, and performance techniques",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["ava@mergington.edu", "liam@mergington.edu"]
    },
    "Art Workshop": {
        "description": "Create paintings, sketches, and mixed media projects",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["ella@mergington.edu", "grace@mergington.edu"]
    },
    "Photography Club": {
        "description": "Learn composition, lighting, and digital editing techniques",
        "schedule": "Fridays, 3:00 PM - 4:30 PM",
        "max_participants": 14,
        "participants": ["charlotte@mergington.edu", "henry@mergington.edu"]
    },
    "Dance Team": {
        "description": "Practice choreography and perform at school events",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["amelia@mergington.edu", "leo@mergington.edu"]
    },
    "Math Olympiad": {
        "description": "Solve advanced math problems and prepare for competitions",
        "schedule": "Wednesdays, 3:30 PM - 4:30 PM",
        "max_participants": 10,
        "participants": ["ben@mergington.edu", "zoe@mergington.edu"]
    },
    "Science Club": {
        "description": "Conduct experiments and explore scientific concepts",
        "schedule": "Fridays, 2:30 PM - 4:00 PM",
        "max_participants": 20,
        "participants": ["nora@mergington.edu", "ethan@mergington.edu"]
    },
    "Robotics Club": {
        "description": "Design, build, and program robots for competitions",
        "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["mila@mergington.edu", "owen@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Thursdays, 3:30 PM - 4:45 PM",
        "max_participants": 12,
        "participants": ["sarah@mergington.edu", "elijah@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_participant(activity_name: str, email: str):
    """Remove a student from an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]
    normalized_email = email.strip().lower()
    current_participants = [participant.strip().lower() for participant in activity["participants"]]

    if normalized_email not in current_participants:
        raise HTTPException(status_code=404, detail="Student is not registered for this activity")

    activity["participants"] = [
        participant for participant in activity["participants"]
        if participant.strip().lower() != normalized_email
    ]

    return {
        "message": f"Removed {email} from {activity_name}",
        "participants": activity["participants"],
    }
