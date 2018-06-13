function displayCalendar(){
  var dateNow = new Date();
  var month = dateNow.getMonth();
  var day = dateNow.getDate();
  var year = dateNow.getFullYear();
  var yearStrings = ["July 21, 1983 01:15:00"];
  console.log(month);
  //seeing what cycle of school year it is

  //var d = new Date("July 21, 1983 01:15:00");

  if (month > 7){
    var yearStrings = [ "September 1, " + year.toString() + " 01:15:00" , "October 1, " + year.toString() + " 01:15:00" , "November 1, " + year.toString() + " 01:15:00" , "December 1, " + year.toString() + " 01:15:00" , "January 1, " + (year+1).toString() + " 01:15:00" , "February 1, " + (year+1).toString() + " 01:15:00" , "March 1, " + (year+1).toString() + " 01:15:00" , "April 1, " + (year+1).toString() + " 01:15:00" , "May 1, " + (year+1).toString() + " 01:15:00" , "June 1, " + (year+1).toString() + " 01:15:00"];
  }
  else {
    var yearStrings = [ "September 1, " + (year-1).toString() + " 01:15:00" , "October 1, " + (year-1).toString() + " 01:15:00" , "November 1, " + (year-1).toString() + " 01:15:00" , "December 1, " + (year-1).toString() + " 01:15:00" , "January 1, " + year.toString() + " 01:15:00" , "February 1, " + year.toString() + " 01:15:00" , "March 1, " + year.toString() + " 01:15:00" , "April 1, " + year.toString() + " 01:15:00" , "May 1, " + year.toString() + " 01:15:00" , "June 1, " + year.toString() + " 01:15:00" ];
}
  var calendarBody = "";
  var arrayLength = yearStrings.length;
  for (var i = 0; i < arrayLength; i++) {
    calendarBody += displayMonth(yearStrings[i]);
  }
  document.getElementById("calendar").innerHTML=calendarBody;
}

function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function displayMonth(s){


 var htmlContent ="";
 var FebNumberOfDays ="";
 var counter = 1;

 var dateNow = new Date(s);
 //var d = new Date("July 21, 1983 01:15:00");
 var month = dateNow.getMonth();

 var nextMonth = month+1; //+1; //Used to match up the current month with the correct start date.
 var prevMonth = month -1;
 var day = dateNow.getDate();
 var year = dateNow.getFullYear();

 //seeing what cycle of school year it is
 if (month > 7){
   //sept to the
 }

 //Determing if February (28,or 29)
 if (month == 1){
    if ( (year%100!=0) && (year%4==0) || (year%400==0)){
      FebNumberOfDays = 29;
    }else{
      FebNumberOfDays = 28;
    }
 }


 // names of months and week days.
 var monthNames = ["January","February","March","April","May","June","July","August","September","October","November", "December"];
 var dayNames = ["Sunday","Monday","Tuesday","Wednesday","Thrusday","Friday", "Saturday"];
 var dayPerMonth = ["31", ""+FebNumberOfDays+"","31","30","31","30","31","31","30","31","30","31"]


 // days in previous month and next one , and day of week.
 var nextDate = new Date(nextMonth +' 1 ,'+year);
 var weekdays= nextDate.getDay();
 var weekdays2 = weekdays
 var numOfDays = dayPerMonth[month];




 // this leave a white space for days of pervious month.
 while (weekdays>0){
    htmlContent += "<td class='monthPre'></td>";

 // used in next loop.
     weekdays--;
 }

 // loop to build the calander body.
 while (counter <= numOfDays){

     // When to start new line.
    if (weekdays2 > 6){
        weekdays2 = 0;
        htmlContent += "</tr><tr>";
    }



    // if counter is current day.
    // highlight current day using the CSS defined in header.
    if (counter == getRandomInt(1,31)){
      htmlContent +="<td class='absent'  onMouseOver='this.style.background=\"#99ccff\"; this.style.color=\"#FFFFFF\"' "+ "onMouseOut='this.style.background=\"#FF0000\"; this.style.color=\"blue\"'>"+counter+"</td>";
    }else{
        htmlContent +="<td class='monthNow' onMouseOver='this.style.background=\"#99ccff\"'"+
        " onMouseOut='this.style.background=\"#FFFFFF\"'>"+counter+"</td>";

    }


    weekdays2++;
    counter++;
 }



 // building the calendar html body.
 var calendarBody = "<table class='calendar'> <tr class='monthNow'><th colspan='7'>"
 +monthNames[month]+" "+ year +"</th></tr>";
 calendarBody +="<tr class='dayNames'>  <td>Sun</td>  <td>Mon</td> <td>Tues</td>"+
 "<td>Wed</td> <td>Thurs</td> <td>Fri</td> <td>Sat</td> </tr>";
 calendarBody += "<tr>";
 calendarBody += htmlContent;
 calendarBody += "</tr></table>";
 // set the content of div .
 return calendarBody;

}
