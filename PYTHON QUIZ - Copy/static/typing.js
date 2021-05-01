var i = 0;
var txt = 'Fill in the form';
var speed = 120;

function typeWriter() {
if (i < txt.length) {
    document.getElementById("demo").innerHTML += txt.charAt(i);
    i++;
    setTimeout(typeWriter, speed);
}
}
setTimeout(window.onload = typeWriter, 1000);