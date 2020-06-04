# Review of Code
Reviewer: Simon van Eeden

## Major points of improvement
1. The Javascript code used for the sign up page seems repetitive. Is there a way to shorten it?
    - Answer: Due to the lack of time, I couldn't unfortunately figure out a way to shorten the Javascript code. The problem lies with the fact that I want to check 
    field seperately. I did not know how I could combine all the AJAX requests into one.
2. The routes: `/usernamecheck`, `/passwordcheck`, `/passwordcrossvalidation`, `/emailcheck` could may be combined into one?
    - Answer: In principle, I think this could be done. The problem that I faced is similar to the one I got when I wrote signup.js. When I tried to combine all the routes I got a bunch of errors I could not solve. 
3. The update routes seem like they could be improved. For example the route `/portal/update` contains the code
    ```python

     # Retrieve user information
    userID = request.form.get("userID")
    user = User.query.get(userID)

    # Retrieve new input by admin
    username = request.form.get("username")
    firstName = request.form.get("firstName")
    lastName = request.form.get("lastName")
    schoolID = request.form.get("school")
    levelID = request.form.get("schoolLevel")
    yearID = request.form.get("schoolYear")
    roles = request.form.getlist("role")

    # Check the roles of user
    admin = tutor = parent = student = False 
    if "admin" in roles:
        admin = True
    if "tutor" in roles:
        tutor = True
    if "parent" in roles:
        parent = True
    if "student" in roles:
        student = True

    # Update userinformation
    user.username = username
    user.firstName = firstName
    user.lastName = lastName
    user.schoolID = schoolID
    user.levelID = levelID
    user.yearID = yearID
    user.student = student
    user.parent = parent
    user.tutor = tutor
    user.admin = admin 

    # Commit the changes
    db.session.commit()
    ```
    which seems awfully long, and could may be written more efficiently?
    - Answer: I agree that it looks very long, but I could not find any reasonable way to shorten the code.
4. In the routes `/portal/parent/<int:userID>` and `/portal/student/<int:userID>`, you seem to be trying to combine the classes `Family` and `Users`. Could this not maybe be done using the relationships in models.py? 
    - Answer: Simon rightfully pointed out that this construction could have been more beautifully solved with the use relationships. The problem was that in my `Family` class/table I have two FK (Foreign Keys) that both relate to the `Users` class/table. For this reason I thought I could not use the relationship feauture. But apparently Simon ran into a similar issue, and found a command in which you can tell the relationship command which FK you want to use to create such a relationship. I was not aware of the existence of this code, hence I did not include it. 
5. For your front-end design it is obvious that you used a lot of bootstrap components. Is it not more fun/better to include more of your own twist to the look of the website, for example by using a different font?
    - Answer: I agree that my front-end design of my website is not spectular. Although I added some flair to the website, I agree wholeheartedly that it could have been better. The front-end was at the bottom of my list of priorities, and due to the lack of time, I did not add any fancy feautures to the front-end of the website. I actually liked the font that Bootstrap provides, so that is why I did not include a new font. 

## Minor points of improvement 
Note: Some of these changes have already been made to the code (thanks to Simon).
1. Add docstring comments to all of the functions in the routes.
2. Make use of multiple assignment. 
3. Rather make use of `and` instead of nested if statements.
    - Note: I did not really agree with this. I looked up whether the use of nested if statements vs `and` made any differences in performance, and according to the numerous posts I found on StackExchange, this did not seem to be case. It all came down to a question of readibility. I think the way I wrote my if statements, is the most readable. Adding a bunch of `and`'s to the code, will give a more chaotic feeling while reading in the code (in my opinion). 
4. Add a few extra comments in your Javascript files. 
5. There are two empty lines between the block of imports and the first actual code. Make that one.
    - Note: I was not sure if that is the actual convention. During the Programming 2 course of the Minor Programming at the UvA, the style guide explicitely stated to leave two empty lines. Maybe this is not the case anymore, but just to be sure I left it at two empty lines. 
6. Add two comments in your application.py file.