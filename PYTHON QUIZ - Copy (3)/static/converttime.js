var loadtime = localStorage.getItem("time")
console.log(loadtime);

var minutesLabel = document.getElementById("minutes");
var secondsLabel = document.getElementById("seconds");

secondsLabel.innerHTML = pad(loadtime % 60);
minutesLabel.innerHTML = pad(parseInt(loadtime / 60));
//localStorage.setItem("time",0);
function pad(val) {
    var valString = val + "";
    if (valString.length < 2) {
        return "0" + valString;
    } else {
        return valString;
    }
}
