# CS50xFinal
Final project for CS50x offered by Harvard. This project was created in December 2020. This program is a website, similar to BaseballReference.com, where a user can search for any baseball player from the beginning of baseball through 2019. The SQL database used in this program is the property of Sean Lahman.

For my final project I was able to make anything I wanted. My brother introduced me to Sean Lahman's baseball database. I love baseball and thought using this database would be a great way to learn how websites like BaseballReference.com work.

This project uses Flask to run the web application. The user has many search options. He/She can search for the statistics of a specific player or search for all players that fall under a certain category (throwing handedness, batting handedness, first name, last name, birth year). Based on the types of search, SQL queries are made from Python to retrieve information from the database. After all the information is gathered and sorted by player and type of statistic (batting average, homeruns, ERA, etc...) an HTML template, styled with CSS, is rendered and presented to the user with the information about the player(s).

Video demonstration: https://youtu.be/-TpEdycWINQ
