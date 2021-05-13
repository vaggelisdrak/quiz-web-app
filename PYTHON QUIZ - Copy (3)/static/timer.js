
var minutesLabel = document.getElementById("minutes");
var secondsLabel = document.getElementById("seconds");
console.log(localStorage.getItem("time"));
if(localStorage.getItem("time")==0){
  var totalSeconds = 0;
}
else{
  var totalSeconds = localStorage.getItem("time");
}


setInterval(setTime, 1000);

function setTime() {
  ++totalSeconds;
  secondsLabel.innerHTML = pad(totalSeconds % 60);
  minutesLabel.innerHTML = pad(parseInt(totalSeconds / 60));
}

function pad(val) {
  var valString = val + "";
  if (valString.length < 2) {
    return "0" + valString;
  } else {
    return valString;
  }
}
