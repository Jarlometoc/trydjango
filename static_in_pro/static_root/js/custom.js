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

var jmolApplet;
jmol_isReady = function(applet) {
	document.title = ("JSmol is ready")
	Jmol._getElement(applet, "appletdiv").style.border="1px solid blue"
}               
var Info = {
	width: 300,
	height: 300,
	debug: false,
	color: "black",
	use: "HTML5",
	j2sPath: "j2s",
	readyFunction: jmol_isReady,
	script: "set antialiasDisplay;"
}
