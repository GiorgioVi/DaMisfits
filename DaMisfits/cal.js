var today = new Date();
var day = today.getDate();
var month = today.getMonth()+1; //January is 0!
var year = today.getFullYear();

var day = new Date(year + "-" + month + "-01").getDay()
day = (day===0) ? 7 : day

//need code to increase n decrease month for calendar changes
