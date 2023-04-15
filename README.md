# uTrack-Gym-Tracker

uTrack is a project designed to solve the problem of tracking and verifying the number of hours spent in Active-Living facilities at the University of Calgary. Many sports teams and school programs require participants to record a certain number of hours in the gym or performing other athletic activities, but the facilities at the university do not provide a simple way for participants to verify these hours.

To solve this problem, a two-way hour tracking system has been proposed, where participants can enter their gym hour goals, track the cost of rented equipment, and see which facilities they used. The front attendants at the gym will verify themselves and log participants into the system to record their verified hours upon request.

The project primarily produces a web interface with multiple sections corresponding to the types of users (e.g. attendants versus student athletes). The interface includes forms that allow users to input different Active-Living facilities, equipment used, user names, student IDs, check-in, and check-out times. Different roles and information are granted to the different types of users in the system.

This solution is especially useful for student athletes and coaches to verify that individuals have gone to a facility for the required number of hours. The web interface also makes it easy for individuals to view their activity time and make changes to their goals and activity types.


## Installation
1. Clone the repository using `git clone https://github.com/your_username/utrack.git`.
2. Change into the project directory with `cd utrack`.
3. Create a virtual environment with `python3 -m venv venv`.
4. Activate the virtual environment with `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows).
5. Install the Python dependencies with `pip install -r requirements.txt`.
6. Change into the `djangoStruct` directory with `cd djangoStruct`.
7. Install the Node dependencies with `npm install`.

## Django server setup
1. Open the `djangoStruct` directory in the terminal.
2. Activate the virtual environment with `source env/bin/activate` (for Linux/Mac) or `env\Scripts\activate` (for Windows).
3. Run `python manage.py runserver` to start the Django server.

## React development server setup
1. Open the `uTrack/djangoStruct/utrackfront` directory in the terminal.
2. Run `npm start` to start the development server.

Note: Make sure the Django server is running before starting the React development server.

## Features
1. Allows participants to enter a goal for gym hours and track the cost of rented equipment.
2. Allows front-attendants at the gym to verify users and log their verified hours.
3. Provides a web interface for end-users to input different Active-Living facilities, equipment used at the facilities, user name, student IDs, check-in, and check-out times.
4. Different roles and information will be granted to the different types of users in the system.

## Tools and Technologies
- The backend was developed using Django, a high-level Python web framework that allows for rapid development of secure and maintainable websites.
- The frontend was created using React, a popular JavaScript library for building user interfaces.
- A REST API was developed with various endpoints to provide communication between the frontend and backend.
- A Postgres database was used to store user information, facility information, and activity logs.


