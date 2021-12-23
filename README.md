# Final-Project-Pathfinder-2e
#### Video Demo:  <URL HERE>
#### Description:
This app allows the use to create custom RPG characters in the style of the Pathfinder Second Edition system. The app is designed to let users log in and access their existing characters, create new characters, edit existing characters, and roll virtual dice. Characters and users are stored in sql databases. 

The app consists of multiple webpages linked together with a python flask app:
  A registration page to add new users
  A login page to log users in based on the store users in the database
  A home page that displays a welcome message
  An error page that displays messages related to errors logging in for example
  A list of characters page that allows users to view all of their characters and open any of them, or create a new character
  A page to view a character and also edit the fields of the character (javascript to show/hide the edit fields)
  A new character page to create a new character from scratch, filling in all fields

This project required that I learn some new techniques in order to execute this app. The first new experience for me was using VSCode, rather than CS50 IDE. The IDE is user friendly, but comes with lots more features and nuance to get used to. Additionally, I chose to develop my app in a virtual environment, to keep the packages and setup separate from any other projects in the future. I also needed to learn how to dynamically route URLs in flask to redirect to various characters without knowing the urls in advance. Because VSCode does not have CS50s libraries, I needed to find another way to execute sql commands on my database. I chose to use the sqlite python library. This requires connection and cursor objects and demanded some debugging due to the nature of these objects. One example of that required a workaround were the dynamic queries that needed to be SQL-injection resistant. The "?" syntax is not always supported with this library so another helper function was required to "scrub" user inputs of most special characters. 
  
Some other interesting features that took some time include the scripting to make the nav links "active" despite being in the layout. This required some checking of thr current url to format the nav links correctlty. I also added navbar collapsing for mobile devices and messages with icons for login.
  
While this project largely leveraged the flask Finance app layout from week 9, the work to recreate the databases, the appearance, and add features was still very time consuming.
  
 
  
