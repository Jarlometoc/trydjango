// Site specific javascript and JQuery


// Test Jquery code to make sure all is in order
$(document).ready( function() {
    $("#about-btn").click( function(event) {
        alert("You clicked the button using JQuery!");
    });
});

//async form submission ( lets the user see what they filled in!)
//add: id = "noRefresh" to <form ...
$(document).ready(function() {
    $("#noRefresh").submit(function(event){
        $(this).css("color", "red");
       // event.preventDefault();
    });
});