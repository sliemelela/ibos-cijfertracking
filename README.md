# Student Tracker

A lot of tutor companies (including the one I am working in) want to keep track of the results of their students. 
This application provides a way for students / parents and the tutors to see what those results are. 
The two main features of this application are:
- Adding / Changing / Deleting student grades and analyzing these grades with relevant graphs.
- Keeping track of the student absences.


## Problem statement

In the tutor company IBOS, the results/grades of the students are tracked in the old fashioned way: with paper. Because of this, it is generally hard to see whether there is any signigicant change in the actual performance of the student. Also, with paper comes the problems of physical storage which we immediately omit by implementing this system.
Also, the company never had a coherent way to keep track of the student absences.

Since there is a common held belief that students that always arrive on time (and are thus considered organized and responsible), have better grades, we also wish to investigate the correlation of student absences with their performance. 

## Solution description

In this application, there are four kind of accounts: student, tutor, parents and administrators. Students can give permission for other parent accounts to view their results and the corresponding analysis (graphs). Students can not view other student their results and parents can only view results they are being permitted to see. Tutors can access all grades/absences etc., but can not (for example) view the flask-admin page. Administrators can access every route, can change roles of already existing accounts and are the only ones who can make tutor accounts.

The first main feauture of this application is a way to add the grades / delete grades / change grades, after which we want to be able to analyze that they have gotten from their school. 
Such a "grade" has context surrounding it, such as:
- The weight of the grade;
- The corresponding class of the grade;
- The type of test it was (project, written test, essay, presentation etc.);
- When the grade was first inserted;
- When the grade was updated;
- When the test was of that corresponding grade.

In the IBOS, students fill in their own grades to make it more practical. However, we do not want students to fill in fake grades. 
So the grades can only be filled in by students when supervised (when given the OK so to speak) by a tutor or administrator account. 
That permission will also be revoked when the tutor/administrator sees fit.

Since some schools use unorthodox grading systems like the MLA (Montessori Lyceum), we want to also give the students and tutors the possibility to add and analyse those grades. 
This application will be tailored towards the Dutch school system. 

The second main feature is in contrast very simple (namely keeping track of the student absences), but we expand on this by relating this back to the performance/grades.


### Extra Features
If time permits, the following feautures will be implemented: 
- Blog Posts such that tutors and administrators can leave messages on the application for the students / parents (e.g. vacation days etc.).
- Implementation of more grading systems
- Implementation of the difference between a regular test and school / central exam test.
- Implementation of a multi-language website (English and Dutch)
- Implementation of a calendar system, to see which students correspond with which times

### Solutions by existing apps

- Microsoft Excel: An argument could be made to keep track of the results using Microsoft Excel, but that entails a non-user friendly environment for both studunts/parents and new tutors that are not familiar with Microsoft Excel. 
- Magister: At virtually any school in The Netherlands, the application "Magister" is used to keep track of the performance of the students. The problem with Magister is that you can not properly see that changes in performance of the students, because the only thing that "Magister" keeps track of are the actual grades. There are no relevant summaries included that may guide or help the tutors or teachers. Magister is good for storing grades, but not handy for any meaningful analysis. Besides this, it would not be practical (or even ethical) to ask for all the login information of all the students such that the tutors can view  


## Languages and utilities
This application is going to be run on a flask server. For this reason, we use:
- Python 3.x
- Flask 
    - flask-login
    - flask-admin

For storing data we use a POSTGRESQL Database hosted by Heroku, which we manage via migrations in a python file. 
We will also use Javascript to handle requests that can be solved on the client-side and also for the implementation of AJAX. 

## Details and sketches

When a user first visits the web application, the user will be met with a home page. Depending on who is logged in, the home page may have different URL's in the navigation bar as seen by the sketches down below:

![Sketch of Homepage](doc/img/sketch-home-page-1.png)
![Sketch of Homepage](doc/img/sketch-home-page-2.png)

If you are logged in (or have just signed up), you have access to a portal. The administrators and tutors can see the list of students, while a student can only their own page. Parents can also see a list of students, but that list is limited to their own children.

![Sketch of Portal](doc/img/sketch-portal-1.png)
![Sketch of Portal](doc/img/sketch-portal-2.png)

TODO: Describe different ways that your application will be used, with all relevant screens sketched out


