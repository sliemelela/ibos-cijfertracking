# Process Book
In this file we will describe our most important findings and challenges during the project. 
Generally we will try to adhere to the following structure:
- We have made choice X.
- We expect Y to happen because of X at this moment in time.
- The reason why we think Y will happen.

## Week 1

### Monday, May 18th 2020
- Creating Heroku Postgresql Database
- Setting up the flask app

### Tuesday, May 19th 2020
- Implemented log in page
- Implemented signup page

#### Problem 
During the process of developing a signup page, I wanted to include an option for a (future) student to select a school by searching for the school. 
This could have been achieved in multiple ways. 
1. Using the HTML5 `datalist` tag.
2. Implementing AJAX Live Search.

Both methods posed some problems. 
1. Unfortunately, the `datalist` tag is not supported in Bootstrap 4. From the numerous of posts that highlight this problem since the implementations of Bootstrap since 2017, we can not assume this will be a solution that will prove to be good when developing a front-end based on Bootstrap.
2. To implement AJAX Live search, I would have to attempt something with a pretty steep learning curve. Seeing as my time was limited, I thought it was better to not attempt this at all. Maybe this could be an option when there is some time left.

#### Solution
We eventually ended up with simply using the `select` tag. Although it as not as elegant of a solution as AJAX Live search, the amount of code and hours needed to implement a list of schools is greatly decreased. The `select` tag also has the feature that if you type in a letter on your keyboard, that it will immediately jump to the options with that letter. This is not immediately apperent for non-experienced end-users, hence AJAX Live Search may have been a better solution. 

This was the first real compromise of this project.

### Wednesday, May 20th 2020
- Finished models.py for the priliminary database design as found in DESIGN.md
- Added a logout

### Thursday, May 21th 2020
- Added a tutor portal.
- Added a way to add grades and courses per user. 
- Added a user interface to add courses and also grades.

### Friday, May 22th 2020
- Did research on what is the best way to add a graph to the website.
- Cleaned up some of the code. 

#### Problem 
I have tried implementing a d3.js graph, but this was a hard task at hand for two reasons:
1. The library d3.js is not user-friendly at all. I have noticed that I do not have sufficient time or experience to try to implement a d3.js graph. I thought I could handle it, since I had some experience with SVG, but this did not seem to pan out. 
2. I have trouble storing the mean of a user of a course. Should I make an extra table or extra columns to existing tables that keep track of the mean per day? Per half day? At what interval should I update it. 


#### Solution
1. I have tried searching for alternatives to d3.js. An alternative that I think will be easiest to implement will be Google Charts. 
2. I think it will be easiest to calculate the mean of a course everytime a new course is added. Everytime the mean is calculated, I also need to keep track of when that happened for when I will be implementing a graph. How to exactly keep track of the data, I am not exactly sure yet. I am contemplating between adding columns to the `courses` table, or maybe making a new table all together. 

### Satuday, May 23th 2020
Note: Nothing of value was done today. 
Plan for Sunday:
- Implementing a graph.
- Implementing a user interface for all other MVP feautures, except for the absences. I will leave that for monday. Alpha version ETA excluding absences is monday, with absences probably tuesday. 
- PS. Oops, I see have forgotton to commit my changes the last couple of days. My bad!

### Sunday, May 24th 2020
- Made a new Mean class that keeps track of the evolution of the mean. A possible improvement: I calculate the mean by retrieving all the grades everytime.
- I determined that Google Charts is not the right fit after all. I have done a little bit more research, and I think I will resort to using chart.js
    - Creating a time series chart with Chart.js is harder than I anticipated. I am stil determined to do it with chart.js though. 
    - Successfully added a chart after a ton of hours. It turns out that one of the errors I was stuck on for a couple of hours was simply that I loaded the chart.js library in the wrong order.

Plan for tomorrow: Add all other feautures, and finish alpha version.

## Week 2

### Monday, May 25th 2020
- Added overview of all users in admin portal.
    - Still to be implemented:
        1. Changing roles of users
        2. Signup page for tutors/admins
        3. Sorting and searching through tables
- Added the possibility for parents to add children and children to add parents. Parents are then able to check out the pages of their children. Every request must be accepted.
- Added two charts (bar chart and radar chart) to the student page.
    - At the moment of writing this, there seems to be a bug with the radar chart.
- Improved the chart in the course page.

#### Problem
I lost a lot of time today due to the Heroku database maintanance. I have to compensate for this tommorrow. 
I think I want to skip the absences feauture for now, but rather focus on some extra feautures when it comes to the existing system. Deleting grades, updating grades.

#### Solution
The priority of working tomorrow will be:
1. Fix the little bugs and clean the code I have now (and also test a lot).
2. Add change role functionality to admins.
3. Signup page for tutors/admins.
4. Add functionality to add grades and delete grades (also putting the grades in a table).
5. Adding the power for the admin to delete accounts.
6. Fix up the code again.

From tomorrow I will reassess the project progression, and look whether I should add more feautures (like the absences).

### Tuesday, May 26th 2020
- Fixed little bugs and cleaned up the python code.

#### Problem
I ran into a major issue when I tried to add the feauture to update the grades. The problem lies in how I calculate the means and how I keep track of them.
The code is riddled with tiny mistakes that I did not notice, so it is no up to me to fix all these issues before going on.

### Wednesday, May 27th 2020
- Solved the problem of May 26th (see below)
- Added the functionality to delete grades
- Added the functionality to update grades
- Added the functionality for admins to change roles of users and also change other user information (username, email etc.)
- Added the functionality on the admin page to sort tables by clicking on the header (plugin).
- Added the functionality on the admin page to search through all the users (tutorial/codepen).

I am planning to do the following tomorrow:
- Add functionality to delete parents / children. 
- Add functionality to add students to groups on the admin page.
- Polish the front end.
- Polish the code.
- Make a screencast.

I have determined I do not have sufficient time to implement a calendar system per student for the absences, so this is something I will leave behind (for now).
Also, I have also forsaken to make a special signup page for the admins/tutors. Changing roles will have to make due for now. 

#### Solution (to 2020-05-27 problem)
I have combed through most mistakes, but I must say it took way longer than I ever expected. I redesigned my database design several times, and eventually I gave up on keeping track of the overall mean of a student. In the future this can be easily implemented, but together with the fact that I did not know what the convention was of calculating the overall mean:
- Should I take the mean over all courses?
- Should I take the mean over all test types?
- Should I take a weighted mean over all courses, where the weight per course is arbitrarily assigned?
- Should I take the weighted mean over all grades?
    - If I would implement this, I would assume that the weights that every teacher assigns per course, would be equal, but this would be naive.

Due to the numerous of possibilies and the lack of convention, I have determined that the overall mean is not an insightful metric to include. This saves me time, the database space and also saves the web-app a little bit of time calculating stuff.

### Thursday, May 28th 2020
- Polished the front end.
- Added some animations (some of which I may remove).
- Fixed some bugs along the way.

Still to do:
- Functionality to delete parents/children.
- Functionality to add students to groups from tutor page.
- Fill in dummy text in contact, testimonials (or remove those pages).
- Polish code.
- Make screencast.

Note to self: Could have definitely worked harder today, but I was a little bit tired from last week, hence the decrease in performance today. Tomorrow is the final day I can do.

### Friday, May 29th 2020
- Added the delete parents/children functionality.
- Added the functionality for the tutor to add new students to groups and reassign them as well.
- Gave the tutor page a face lift.
- Gave the parent page a face lift.
- Fixed some bugs along the way. 
- Made screencast:
    - I am not that happy with my screencast. I could be better, if it is permitted, I will refilm it on a later date (tomorrow for instance).

Plans for weekend:
- Polish code.
- Maybe give the site a better front end design.
- Maybe redo the screencast. 
