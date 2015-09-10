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
$(document).ready( function() {
    $('.single-slider').jRange({
        from: 0,
        to: 100,
        step: 1,
        scale: [0,25,50,75,100],
        format: '%s',
        width: 300,
        showLabels: true
    });
});