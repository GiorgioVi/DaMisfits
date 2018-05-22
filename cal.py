#!/usr/bin/python
print "Content-Type: text/html\n"
print ''

# CGI FORM RESULTS
import cgi
formresults = cgi.FieldStorage()

import datetime
import calendar

now = datetime.datetime.now()
year = now.year
month = now.month

# what weekday the first day of month is
WDFOM = datetime.date(year, month, 1).weekday()

# how many days in the month before
bmonth = month - 1  # Calculating the previous month
byear = year
if bmonth < 1:  # Accounting for the wrapping around
    byear -= 1
    bmonth += 12
amonth = month + 1  # Calculating the next month
ayear = year
if amonth > 12:  # Accounting for the wrapping around
    ayear += 1
    amonth -= 12
WDFLM = calendar.monthrange(byear, (bmonth))[1]

# how many days in current month
numinmonth = calendar.monthrange(year, (month))[1]


L = []
pre = (WDFOM + 1) % 7  # Number of days of the previous month
while pre > 0:
    L.append(WDFLM - pre)  # Add those days in
    pre -= 1
cur = 1
while cur <= numinmonth:  # Adding in the days in the current month
    L.append(cur)
    cur += 1
nex = 1
while len(L) % 7 > 0:  # Adding in days until the calendar ends on Saturday
    L.append(nex)
    nex += 1


def maketable(test):  # Makes the table
    final = "<table border='1'>\n"
    final += "<tr> <th> Sunday </th> \
<th> Monday </th> <th> Tuesday </th> <th> Wednesday </th> \
<th> Thursday </th> <th> Friday </th> <th> Saturday </th> </tr>\n"
    for x in range(len(test)):
        if x % 7 == 0:
            final += '<tr>'
        final += '<td>' + str(test[x]) + '</td>'
        if x % 7 == 6:
            final += '</tr>\n'
    final += '</table>'
    return final

# Printing everything out
print "<h1>" + calendar.month_name[month] + ", " + str(year) + "<h1>"
print maketable(L)
# Link for previous month using the previously calculated month and year
blink = ' <button type="button"> <a href="cal.py?year=' + str(byear)
blink += '&month=' + str(bmonth) + '"> Previous </a></button>'
print blink
# Link for next month using the previously calculated month and year
alink = '<button type="button"> <a href="cal.py?year=' + str(ayear)
alink += '&month=' + str(amonth) + '"> Next </a></button>'
print alink
