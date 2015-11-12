// Site specific javascript and JQuery


// Test Jquery code to make sure all is in order
$(document).ready( function() {
    $("#about-btn").click( function(event) {
        alert("You clicked the button using Jquery!!!");
    });
});



//async form submission ( lets the user see what they filled in!)
//add: id = "noRefresh" to <form ...
//$(document).ready(function() {
   // $("#H").click(function(event){
       // event.preventDefault();
      //  alert("its working!")

   // });
//});

