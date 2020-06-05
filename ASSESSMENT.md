# Assessment

## Accomplishments 
My three biggest accomplishments during this project were:
1. Implementing a "friend request" feauture 
2. Implementing multiple graphs (using chart.js)
3. Implementing a structure that keeps track of how the mean changes over time (even if you update grades)

I have listed these feautures from easy to hard. Besides these accomplishments I have added a lot of more tiny feautures that build on the accomplishments above or enhance the user experience in general. 
All the little nuances are found in either/both DESIGN.md or the screencast (which you can find in README.md).

Let me elaborate on what these three feauteres entail. The list is listed from easy to hard.

1. Implementing a "friend request" feauture between parens and students was pretty easy. The hard part was to make one route that handles requests from either parents or students with limited amount of code in one route. This was eventually possible, and now this feauture is fully implemented together with the possibility to delete relations etc. 

2. The first hard part of implementing a graph is choosing an appropriate library that satisfies the following constraints:
- The level of Javascript that is needed to implement the graph needs to be of one of my level. 
- The chosen library should "look" and feel modern.
- The chosen library should be flexible enough to let me make more then one kind of graph. But it definitely needs to include a time-series graph. 
    I first started with D3.js, after which I switched to Google Charts, after which I switched to chart.js with which I stayed.
    Note:
    - It took a very long time to get the timeseries chart running, but I finally managed to do it.
    - It took a long time how I should actually formulate the information that I want to give the graph in way that would make sense.

    Conclusion: I am very happy with my implementation of graphs!

3. Keeping track of how the mean changes sound easier then it is. If you just add grades, then it is very simple: you could either recalculate it from scratch everytime, or just use the old mean (and weights) to calculate the means. Initially I went with the first route, because I did not know any better. When it came to implementing the feauture of updating or deleting a grade, it took a long time to rewrite the old code into something which takes into account the fact that we delete or upgrade grades. I have redesigned my database a lot of times, and ask assistance, but at the end I am very happy with my implementation. I want to stress that this took a lot of time, and is not that self-evident as it may seem at first sight.

## The Big Decisions

### Overall mean of a student
While trying to keep track of the mean of the course, I thought it would be interestinng to see how the student scores on average on every test type (so for instance, maybe the students is better in projects then written tests? Why? etc.).
Also an obvious contender is to keep track of the overall mean of the student. From here I could choose to keep track of it over a period of time, or just remember the last one. Just implemeneting the mean of every course (over time) and of every test type took already so much time away. 
For that reason (a lack of time) I decided to scrap this feauture. 

### Student Absences
At the beginnning of this project I also indicated that I am interested in a system that keeps track of the absences of the student. I dropped this feauture (and also the corresponding class object) purely due to a lack of time. 

### AJAX Live Search
In the beginning I was trying to implement a AJAX Live Search in the signup form for if the user was a student (so he or she could look for school to choose from). Well:
- Problem: To implement AJAX Live search, I would have to attempt something with a pretty steep learning curve. Seeing as my time was limited, I thought it was better to not attempt this at all. Maybe this could have been an option if there was some time left.
- Solution/Decision: We eventually ended up with simply using the `select` tag. Although it as not as elegant of a solution as AJAX Live search, the amount of code and hours needed to implement a list of schools is greatly decreased. The `select` tag also has the feature that if you type in a letter on your keyboard, that it will immediately jump to the options with that letter. This is not immediately apperent for non-experienced end-users, hence AJAX Live Search may have been a better solution. 

After more careful considiration, AJAX Live Search would be overkill in the case of the sign up page, because it is not like there are *that* many schools. But either way, AJAX Live Search could still be a viable alternative for searchtable.js in the future, if the table of users becomes too big. 

### D3.js & Google Charts
As I have eluded to before: 
- The level of Javascript that is needed to implement the graph needs to be of one of my level. 
- The chosen library should "look" and feel modern.
- The chosen library should be flexible enough to let me make more then one kind of graph. But it definitely needs to include a time-series graph. 
I first started with D3.js, after which I switched to Google Charts, after which I switched to chart.js with which I stayed.

The application D3.js was eventually too complicated, but I thought since I had some experience with SVG and TikZ, I should be fine, but this was not the case. Due to lack of time, I tried to use another library: Google Charts.

The syntax used for Google Charts is very simple, but I eventually thought that the Google Charts charts looked outdated. For this reason I searched for another library and eventually found: Chart.js

Chart.js had the best of both worlds: It looked amazing while also having (relatively) simple syntax. I am very happy with my decision to abondon D3.js and Google Charts as fast as I did!

### The mean per course
While trying to add grades to a course (of a student) I noticed that it a long time to reload*. 
This started me thinking about how to optimalize my code. The main question that arose was:
- Should I actually store the mean. 

After careful delibiration with a TA of this course, I concluded that storing the means was to way to go. Reason for this is purely because you want to keep / store the data from when a mean is calculated, which can be easily done with a db.relationship. 
Even though this may be an approach which is not the fastest, it is one that gives me eazy access to all the means/grades without any complex code in the layout files (JinJa).


*Eventually it turned out to be mostly my conncection with my server. 