# Web-Crawler
HOW TO RUN THE CODE :

STEP1:Open the terminal 
STEP2:Go to the particular program file location 
STEP3:Enter the command: make -f Makefile

Python version: python 3.0 or above
******************************************************************************************************************************************************************************************************

PROGRAM FLOW:

1. 10 movie genres will be displayed.

2. User will have to input any one out of the 10 movie genres that are displayed.

3. A list of 100 movies of the input genre will be displayed.

4. User will have to input name of any one movie from the shown list of movies.

5. A list of fields of the entered movie will be shown.

6. User will have to give input any one of the movie field (user will also have a option to exit from the program in the same list only).

7. Result for the entered field will be shown.

8. Program will Go to step (6)

******************************************************************************************************************************************************************************************************

ASSUMPTIONS MADE IN THE CODE:

1. Both tasks that is task1 and task2 are done in a single file named task1&2.py 

2. URLs of the 10 genres are saved in the code using a dictionary.

3. If any entered movie field is not present in the webpage of movie then user will be informed with a suitable message.

4. Only Cast with character name(NOT THE CREW NAME) will be shown name shown if user enters movie field 'Cast'.

5. All the genres, which would be present in the movie's html page, will be shown.

6. Entered genre's webpage will be downloaded as named '<genre>.html' in the same directory where programs are present.

7. Entered movie's webpage will be downloaded as named 'movie_file.html' in the same directory where programs are present.

8. Entred cast's webpage will be downloaded as named 'cast_profile.html' in the same directory where programs are present.
