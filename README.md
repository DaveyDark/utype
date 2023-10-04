# U-Type
My Final Project submission for the CS50x course by Harvard. It uses Flask for the backend and jinja/html/css/js for frontend along with a SQLite database.

Demo Video:

[![YouTube Video](https://img.youtube.com/vi/59wK5EDarWs/0.jpg)](https://www.youtube.com/watch?v=59wK5EDarWs)

## About
uType is a typing practice and testing platform that offers features like customizable tests, stat tracking and leaderboards. It also uses a score system to rank users and tests. The score of a test is calculated using a formula that involves numerous parameters like CPM, WPM, Average word length, time taken etc. It is intended to give a fair assesment of a user's performance independant of the options they chose for the test.

## Setup
1) Clone this repositiory
  ```git clone https://github.com/DaveyDark/utype```
2) Install dependencies
   ```pip install -r requirements.txt```
3) Run server
   - To run for development:
     ```flask run --debug```
   - To run for production:
     ```gunicorn -w 4 -b 0.0.0.0:80 app:app```
