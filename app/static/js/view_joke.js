
var submitJoke = function() {
    var title = $('#titleField')[0].value;
    var content = $('#contentField')[0].value;
    var jokeId = $('#jokeId')[0].value;


    var formdata = {
    	'title': title,
    	'content': content,
        'jokeId': jokeId
    };

    var data = JSON.stringify(formdata);

    var posting = $.post({
        url: "/update_joke",
        data: data,
        success: function(response) {
            console.log("Submitted");
            if (response) {
                if (response.redirect) {
                    window.location.href = response.redirect;
                } else if (response.msg) {
                	console.log("Msg received: " + response.msg)
                } else {
                    console.log("Joke was successfully updated.")
                }
            }
        },
        error: function(data, err) {
            console.log("An error occurred updating this joke.");
        },

        dataType: "json",
        contentType : "application/json;charset=UTF-8",
    });
    console.log("Done");
}
