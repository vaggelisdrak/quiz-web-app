var i = 0;
var txt = "Choose the quiz's level of difficulty :";
var speed = 120;

function typeWriter() {
if (i < txt.length) {
    document.getElementById("demo").innerHTML += txt.charAt(i);
    i++;
    setTimeout(typeWriter, speed);
}
}
setTimeout(window.onload = typeWriter, 1000);