

/* Script for signing up as a user */
/* @author Osama Sakhi */

/* Used to allow enter button to submit form when inside the form */
$(function() {
    $('#signupForm').each(function() {
        $(this).find('input').keypress(function(e) {
            // Enter pressed?
            if(e.which == 10 || e.which == 13) {
                signupSubmit();
            }
        });
    });
});


var signupSubmit = function() {

    var email = $('#emailField')[0].value;
    var password1 = $('#passwordField1')[0].value;
    var password2 = $('#passwordField2')[0].value;
    var fname = $('#fnameField')[0].value;
    var lname = $('#lnameField')[0].value;
    var isPrivileged = $('#privilegedType')[0].checked;


    // If passwords do not match, alert user, stop form submission
    if (password1 != password2) {
        alert("Passwords mismatch");
        return;
    }

    console.log("Passwords match. Hashing password now");
    // Hash passwords here, just to protect possibility of users' true passwords getting out to a hacker.
    // TODO: Must hash password before sending over
    var password = password1;

    var userType = null;
    // TODO: Most likely need another check somehow. Will figure it out later
    if (isPrivileged) {
        console.log("Registering user is privileged");
        userType = 'privileged';
    } else {
        userType = 'regular';
    }

    var formData = {
        email: email,
        password: password,
        fname: fname,
        lname: lname,
        userType: userType
    };
    var data = JSON.stringify(formData);

    /* Make AJAX HTTP Post Reuqest */
    /*
    * If successful, redirect user
    * If unsuccessful, show message on the page form
    */
    var posting = $.post({
        url: "/register",
        data: data,
        success: function(response) {
            console.log("POSTed");
            if (response) {
                if (response.redirect) {
                    // Login success
                    window.location.href = response.redirect;
                } else if (response['email_unavailable']) {
                    // TODO: Make user enter alternate email, alert them somehow
                    console.log("Email unavailable");
                    alert("Email unavailable");
                } else {
                    console.log("Unable to register user")
                }
            }
        },
        error: function(data, err) {
            console.log("POST error");
        },

        dataType: "json",
        contentType : "application/json;charset=UTF-8",
    });
}

var updateform = function() {
    // Do something
    console.log("Updating form.")
}
