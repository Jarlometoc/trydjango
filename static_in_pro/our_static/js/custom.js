// Site specific javascript and JQuery


// Test Jquery code to make sure all is in order
$(document).ready( function() {

    $("#about-btn").click( function(event) {
        alert("You clicked the button using JQuery!");
    });
});


// Test for mainpage
$(document).ready(function(){
    $("p").click(function(){
        $(this).hide();
    });
});


//Jmol slider
