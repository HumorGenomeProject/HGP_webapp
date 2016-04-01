

/* Script for signing into web app using an email and password */
/* @author Osama Sakhi */

/* Used to allow enter button to submit form when inside the form */
$(function() {
    $('#loginForm').each(function() {
        $(this).find('input').keypress(function(e) {
            // Enter pressed?
            if(e.which == 10 || e.which == 13) {
                loginSubmit();
            }
        });
    });
});


var loginSubmit = function() {
    var email = $('#emailField')[0].value;
    var password = $('#passwordField')[0].value;

    // TODO: Must hash password before sending over

    var formData = {
        email: email,
        password: password
    };
    var data = JSON.stringify(formData);

    /* Make AJAX HTTP Post Reuqest */
    /*
     * If successful, redirect user
     * If unsuccessful, show message on the page form
     */
    var posting = $.post({
        url: "/signin",
        data: data,
        success: function(response) {
            console.log("POSTed");
            if (response) {
                if (response.redirect) {
                    // Login success
                    window.location.href = response.redirect;
                } else {
                    // Login failed
                    console.log("Incorrect username or password");
                    alert("Incorrect username or password");
                    updateform();
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
