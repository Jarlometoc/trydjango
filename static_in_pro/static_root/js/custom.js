// Site specific javascript and JQuery

// Test Jquery code to make sure all is in order
$(document).ready( function() {
    $("#about-btn").click( function(event) {
        alert("You clicked the button using Jquery!!!");
    });
});


//refresh to same place on page
//http://www.webdeveloper.com/forum/showthread.php?58146-Keeping-Scrollbar-Position-On-Refresh
function readCookie(name){
    return(document.cookie.match('(^|; )'+name+'=([^;]*)')||0)[2]
}


//for jsmol


