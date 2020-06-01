# Design of the Student Tracker application

To understand to context in which this document was written, we first the reader to README.md.

In this document we elucidate on which features of this application are going to be implemented to make it a minimum viable product and we will also expand on the user interface sketches as given in the document README.md. Also, the preliminary database design is going to be treated after which we conclude with a list of (external) data sources / APIs that we might want to include in this application. 

## Main Features 
The first main feature of this application is that students can add / delete / update grades. These grades will be summarized with the help of graphs (per course). 
The second feature of this application is that the tutors can keep track of the student absences.

The properties of the grades will be discussed in the database design.

### Extra Features
If time permits, we may want to add 
- Blog Posts such that tutors and administrators can leave messages on the application for the students / parents (e.g. vacation days etc.).
- Implementation of more grading systems.
- Implementation of the difference between a regular test and school / central exam test.
- Implementation of a multi-language website (English and Dutch).
- Implementation of a calendar system, to see which students correspond with which times.

These (extra) features were already listed in the README.md document. We have not included these features in the preliminary database design. 

## User Interface

When a user first visits the web application, the user will be met with a home page. Depending on who is logged in, the home page may have different URL's in the navigation bar as seen by the sketches down below:

![Sketch of Homepage](doc/img/sketch-home-page-1.png)
![Sketch of Homepage](doc/img/sketch-home-page-2.png)

If time permits, we may add a contact page with a contact form and an embedded google map as you can see down below:
![Sketch of Contact](doc/img/sketch-home-page-3.png)

If you are logged in (or have just signed up), you have access to a portal. The administrators and tutors can see the list of students, while a student can view only their own page. Parents can also see a list of students, but that list is limited to their own children.

![Sketch of Portal](doc/img/sketch-portal-1.png)
![Sketch of Portal](doc/img/sketch-portal-2.png)

All the other features are self-evident from the above sketches (like adding grades via modals etc.). 

## Database Design 
The preliminary design (UML diagram) of the database can be found below. In this diagram FK is shorthand for "Foreign Key" and PK is shorthand for "Primary Key".
![UML-Diagram database design](doc/img/uml-diagram-1.png)

## List of APIs
For the minimum viable product, in principle, there is no need to use any external data sources or APIs. However, there exists a Magister API that may be compatible in such a way that all grades could be automatically entered (provided that the student has authenticated the transmission between Magister and this application). 
The problem is that the Magister API documentation does not provide sufficient information regarding the implementation with Python as it seems to lean more to an implementation with PHP, which we will not use in this application. 

For the demonstration of this product, it may be handy to compose a file that automatically imports dummy students / parents and grades / absences into our database. 

Lastly, as we have said before, if time would permit it, we would like to also embed a google map in the contact page. For this, the Google Maps API would be needed. 


## Updated database design 
The updated design (UML diagram) of the database can be found below. In this diagram FK is shorthand for "Foreign Key" and PK is shorthand for "Primary Key".
![UML-Diagram database design](doc/img/uml-diagram-2.png)





