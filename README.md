# Final-Project-Pathfinder-2e

![RPG App Demonstration](/RPG_App_Demo.gif)

#### Description:
This app allows the user to create custom RPG characters in the style of the Pathfinder Second Edition system. The app is designed to let users log in and access their existing characters, create new characters, edit existing characters, and roll virtual dice. Characters and users are stored in sql databases. 

The app consists of multiple webpages linked together with a python flask app:
* A registration page to add new users
* A login page to log users in based on the store users in the database
* A home page that displays a welcome message
* An error page that displays error messages related to logging in, for example
* A list of characters page that allows users to view all of their characters and open any of them, or create a new character
* A page to view a character and also edit the fields of the character (javascript to show/hide the edit fields)
* A new character page to create a new character from scratch

I chose to develop my app in a virtual environment, to keep the packages and setup separate from any other projects in the future. URLs are dynamically routed in flask to redirect to various characters. I chose to use the sqlite python library to manipulate a local database. This requires connection and cursor objects to create, read, update, and delete. The dynamic queries also need to be SQL-injection resistant. The "?" syntax is not always supported with this library so another helper function was required to "scrub" user inputs of most special characters. 

Some other interesting features include the scripting to make the nav links "active". This required checking the current url to format the nav links correctlty. I also added navbar collapsing for mobile devices and messages with icons for login.

## How to Run Locally

`pip install -r requirements.txt`

`flask run`
