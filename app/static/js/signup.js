document.addEventListener('DOMContentLoaded', () => {

    // By default, submit button and student options are disabled
    document.querySelector('#submit').disabled = true;

    // Dictionary to keep track of what fields are satisfied
    var status = {"username": false, "password": false, "password_repeat": false, "firstname": false, "lastname": false, "email": false, "school": false, "schoollevel": false, "schoolyear": false};

    // Function that sets status to false and disables button
    function false_status(x){
        status[x] = false;
        document.querySelector('#submit').disabled = true;
    }
    
    // Function that updates status and sets it to true and enables button when necessary
    function true_status(x){
        status[x] = true;

        // Checking if all the fields are properly filled in 
        if (status["username"] == true && status["password"] == true && status["password_repeat"] == true && status["firstname"] == true && status["lastname"] == true && status["email"] == true){
            
            // For students, checking the extra fields
            if(document.querySelector('#student').checked){
                if (status["school"] == true && status["schoollevel"] == true && status["schoolyear"] == true){
                document.querySelector('#submit').disabled = false;
                }
            }

            // For parents there is no extra check
            else{
                document.querySelector('#submit').disabled = false;
            }
            
        }
    }

    document.querySelector('#username').onblur = () => {

         // Initialize new request
         const request = new XMLHttpRequest();
         const username = document.querySelector('#username').value;
         request.open('POST', '/usernamecheck');
    
         // Callback function for when request completes
         request.onload = () => {
            
             // Extract JSON data from request
             const data = JSON.parse(request.responseText);

             // Update the username result div
             if (data.username_success == false) {

                // Warning message
                const contents = data.message;

                // Update input field
                var input_field = document.querySelector('#username');
                input_field.classList.remove("is-valid");
                input_field.classList.add("is-invalid");

                // Show message
                var hidden_element = document.querySelector('#username_message');
                hidden_element.innerHTML = contents;
                hidden_element.classList.remove("valid-feedback");
                hidden_element.classList.add("invalid-feedback");

                // Update status
                false_status("username");
            }    
            else {

               // Update input field
               var input_field = document.querySelector('#username');
               input_field.classList.remove("is-invalid");
               input_field.classList.add("is-valid");

               // Show message
               var hidden_element = document.querySelector('#username_message');
               hidden_element.innerHTML = `Looks good!`;
               hidden_element.classList.remove("invalid-feedback");
               hidden_element.classList.add("valid-feedback");

               // Update status
               true_status("username");
            }
        }

        // Add data to send with request
        const data = new FormData();
        data.append('username', username);

        // Send request
        request.send(data);
        return false;
    };

    document.querySelector('#password').onblur = () => {

        // Initialize new request
        const request = new XMLHttpRequest();
        const password = document.querySelector('#password').value;
        request.open('POST', '/passwordcheck');

        // Callback function for when request completes
        request.onload = () => {

            // Extract JSON data from request
            const data = JSON.parse(request.responseText);

            // Update the password result div
            if (data.password_success == false) {

            // Warning message
            const contents = data.message;

            // Update input field
            var input_field = document.querySelector('#password');
            input_field.classList.remove("is-valid");
            input_field.classList.add("is-invalid");

            // Show message
            var hidden_element = document.querySelector('#password_message');
            hidden_element.innerHTML = contents;
            hidden_element.classList.remove("valid-feedback");
            hidden_element.classList.add("invalid-feedback");

            // Update status
            false_status("password");
        }    
        else {
            // Update input field
            var input_field = document.querySelector('#password');
            input_field.classList.remove("is-invalid");
            input_field.classList.add("is-valid");

            // Show message
            var hidden_element = document.querySelector('#password_message');
            hidden_element.innerHTML = `Looks good!`;
            hidden_element.classList.remove("invalid-feedback");
            hidden_element.classList.add("valid-feedback");

            // Update status
            true_status("password");
        }
    }

       // Add data to send with request
       const data = new FormData();
       data.append('password', password);

       // Send request
       request.send(data);
       return false;
    };

    document.querySelector('#password_repeat').onblur = () => {

        // Initialize new request
        const request = new XMLHttpRequest();
        const password = document.querySelector('#password').value;
        const password_repeat = document.querySelector('#password_repeat').value;
        request.open('POST', '/passwordcrossvalidation');

        // Callback function for when request completes
        request.onload = () => {

            // Extract JSON data from request
            const data = JSON.parse(request.responseText);

            // Update the password result div
            if (data.password_success == false) {

            // Warning message
            const contents = data.message;

            // Update input field
            var input_field = document.querySelector('#password_repeat');
            input_field.classList.remove("is-valid");
            input_field.classList.add("is-invalid");

            // Show message
            var hidden_element = document.querySelector('#password_repeat_message');
            hidden_element.innerHTML = contents;
            hidden_element.classList.remove("valid-feedback");
            hidden_element.classList.add("invalid-feedback");

            // Update status
            false_status("password_repeat");
        }    
        else {
            // Update input field
            var input_field = document.querySelector('#password_repeat');
            input_field.classList.remove("is-invalid");
            input_field.classList.add("is-valid");

            // Show message
            var hidden_element = document.querySelector('#password_repeat_message');
            hidden_element.innerHTML = `Looks good!`;
            hidden_element.classList.remove("invalid-feedback");
            hidden_element.classList.add("valid-feedback");

            // Update status
           true_status("password_repeat");
        }
    }

       // Add data to send with request
       const data = new FormData();
       data.append('password', password);
       data.append('password_repeat', password_repeat);

       // Send request
       request.send(data);
       return false;
    };

    document.querySelector('#first_name').onblur = () => {
        const first_name = document.querySelector('#first_name').value;

        if (first_name.length == 0){

            // Update input field
            var input_field = document.querySelector('#first_name');
            input_field.classList.remove("is-valid");
            input_field.classList.add("is-invalid");

            // Show message
            var hidden_element = document.querySelector('#first_name_message');
            hidden_element.innerHTML = `You must provide a first name.`;
            hidden_element.classList.remove("valid-feedback");
            hidden_element.classList.add("invalid-feedback");

            // Update status
            false_status("firstname");
        }
        else{

            // Update input field
            var input_field = document.querySelector('#first_name');
            input_field.classList.remove("is-invalid");
            input_field.classList.add("is-valid");

            // Show message
            var hidden_element = document.querySelector('#first_name_message');
            hidden_element.innerHTML = `Looks good!`;
            hidden_element.classList.remove("invalid-feedback");
            hidden_element.classList.add("valid-feedback");

            // Update status
            true_status("firstname");
        }
    };

    document.querySelector('#last_name').onblur = () => {
        const first_name = document.querySelector('#last_name').value;

        if (first_name.length == 0){

            // Update input field
            var input_field = document.querySelector('#last_name');
            input_field.classList.remove("is-valid");
            input_field.classList.add("is-invalid");

            // Show message
            var hidden_element = document.querySelector('#last_name_message');
            hidden_element.innerHTML = `You must provide a last name.`;
            hidden_element.classList.remove("valid-feedback");
            hidden_element.classList.add("invalid-feedback");

            // Update status
            false_status("lastname");
        }
        else{

            // Update input field
            var input_field = document.querySelector('#last_name');
            input_field.classList.remove("is-invalid");
            input_field.classList.add("is-valid");

            // Show message
            var hidden_element = document.querySelector('#last_name_message');
            hidden_element.innerHTML = `Looks good!`;
            hidden_element.classList.remove("invalid-feedback");
            hidden_element.classList.add("valid-feedback");

            // Update status
            true_status("lastname");
        }


    };

    document.querySelector('#email').onblur = () => {

        // Initialize new request
        const request = new XMLHttpRequest();
        const email = document.querySelector('#email').value;
        request.open('POST', '/emailcheck');

        // Callback function for when request completes
        request.onload = () => {

            // Extract JSON data from request
            const data = JSON.parse(request.responseText);

            // Update the username result div
            if (data.email_available == false) {

                // Warning message
                const contents = data.message;

                // Update input field
                var input_field = document.querySelector('#email');
                input_field.classList.remove("is-valid");
                input_field.classList.add("is-invalid");

                // Show message
                var hidden_element = document.querySelector('#email_message');
                hidden_element.innerHTML = contents;
                hidden_element.classList.remove("valid-feedback");
                hidden_element.classList.add("invalid-feedback");

                // Update status
                false_status("email");
            } 
            
            // Check if email is properly formatted
            else if (/\S+@\S+\.\S+/.test(email) == false){

                // Update input field
                var input_field = document.querySelector('#email');
                input_field.classList.remove("is-valid");
                input_field.classList.add("is-invalid");

                // Show message
                var hidden_element = document.querySelector('#email_message');
                hidden_element.innerHTML = `Enter a valid email adress.`;
                hidden_element.classList.remove("valid-feedback");
                hidden_element.classList.add("invalid-feedback");

                // Update status
                false_status("email");
            }    
            else {
                // Update input field
                var input_field = document.querySelector('#email');
                input_field.classList.remove("is-invalid");
                input_field.classList.add("is-valid");

                // Show message
                var hidden_element = document.querySelector('#email_message');
                hidden_element.innerHTML = `Looks good!`;
                hidden_element.classList.remove("invalid-feedback");
                hidden_element.classList.add("valid-feedback");

                // Update status
                true_status("email");
            }
        }

        // Add data to send with request
        const data = new FormData();
        data.append('email', email);
        
        // Send request
        request.send(data);
        return false;
    };

    document.querySelector('#student').onchange = () => {
        if (document.querySelector('#student').checked){
            document.querySelector('#studentRole').style.display = "block";
            document.querySelector('#submit').disabled = true;
            true_status("student");
        }
    };

    document.querySelector('#parent').onchange = () => {
        if (document.querySelector('#parent').checked){
            document.querySelector('#studentRole').style.display = "none";
            true_status("parent");
        }
    };

    document.querySelector('#school').onchange = () => {
        if (document.querySelector('#school').value == ''){

            // Update input field
            var input_field = document.querySelector('#school');
            input_field.classList.remove("is-valid");
            input_field.classList.add("is-invalid");

            // Show message
            var hidden_element = document.querySelector('#school_message');
            hidden_element.innerHTML = `You must choose a school.`;
            hidden_element.classList.remove("valid-feedback");
            hidden_element.classList.add("invalid-feedback");

            // Update status
            false_status("school");
        }
        else if (document.querySelector('#school').value == 'other'){

            // Update input field
            var input_field = document.querySelector('#school');
            input_field.classList.remove("is-valid");
            input_field.classList.add("is-invalid");

            // Show message
            var hidden_element = document.querySelector('#school_message');
            hidden_element.innerHTML = `Contact an administrator or tutor to add a new school.`;
            hidden_element.classList.remove("valid-feedback");
            hidden_element.classList.add("invalid-feedback");

            // Update status
            false_status("school");
        }
        else{

            // Update input field
            var input_field = document.querySelector('#school');
            input_field.classList.remove("is-invalid");
            input_field.classList.add("is-valid");

            // Show message
            var hidden_element = document.querySelector('#school_message');
            hidden_element.innerHTML = `Looks good!`;
            hidden_element.classList.remove("invalid-feedback");
            hidden_element.classList.add("valid-feedback");

            // Update status
            true_status("school");
        }
    };
    
    document.querySelector('#schoolLevel').onchange = () => {
        if (document.querySelector('#schoolLevel').value == ''){

            // Update input field
            var input_field = document.querySelector('#schoolLevel');
            input_field.classList.remove("is-valid");
            input_field.classList.add("is-invalid");

            // Show message
            var hidden_element = document.querySelector('#level_message');
            hidden_element.innerHTML = `Choose an education level.`;
            hidden_element.classList.remove("valid-feedback");
            hidden_element.classList.add("invalid-feedback");

            // Update status
            false_status("schoollevel");
        }
        else{

            // Update input field
            var input_field = document.querySelector('#schoolLevel');
            input_field.classList.remove("is-invalid");
            input_field.classList.add("is-valid");

            // Show message
            var hidden_element = document.querySelector('#level_message');
            hidden_element.innerHTML = `Looks good!`;
            hidden_element.classList.remove("invalid-feedback");
            hidden_element.classList.add("valid-feedback");

            // Update status
            true_status("schoollevel");
        }
    };

    document.querySelector('#schoolYear').onchange = () => {
        if (document.querySelector('#schoolYear').value == ''){

            // Update input field
            var input_field = document.querySelector('#schoolYear');
            input_field.classList.remove("is-valid");
            input_field.classList.add("is-invalid");

            // Show message
            var hidden_element = document.querySelector('#year_message');
            hidden_element.innerHTML = `Choose an education year.`;
            hidden_element.classList.remove("valid-feedback");
            hidden_element.classList.add("invalid-feedback");

            // Update status
            false_status("schoolyear");
        }
        else{

            // Update input field
            var input_field = document.querySelector('#schoolYear');
            input_field.classList.remove("is-invalid");
            input_field.classList.add("is-valid");

            // Show message
            var hidden_element = document.querySelector('#year_message');
            hidden_element.innerHTML = `Looks good!`;
            hidden_element.classList.remove("invalid-feedback");
            hidden_element.classList.add("valid-feedback");

            // Update status
            true_status("schoolyear");
        }
    };
 });


 