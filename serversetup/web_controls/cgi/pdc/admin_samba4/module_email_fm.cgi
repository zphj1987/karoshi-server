#!/bin/bash
#Copyright (C) 2007  Paul Sharrad

#This file is part of Karoshi Server.
#
#Karoshi Server is free software: you can redistribute it and/or modify
#it under the terms of the GNU Affero General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#Karoshi Server is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU Affero General Public License for more details.
#
#You should have received a copy of the GNU Affero General Public License
#along with Karoshi Server.  If not, see <http://www.gnu.org/licenses/>.

#
#The Karoshi Team can be contacted at: 
#mpsharrad@karoshi.org.uk
#jharris@karoshi.org.uk
#aball@karoshi.org.uk
#
#Website: http://www.karoshi.org.uk
############################
#Language
############################
LANGCHOICE=englishuk
STYLESHEET=defaultstyle.css
TIMEOUT=300
NOTIMEOUT=127.0.0.1
[ -f /opt/karoshi/web_controls/user_prefs/$REMOTE_USER ] && source /opt/karoshi/web_controls/user_prefs/$REMOTE_USER
[ -f /opt/karoshi/web_controls/language/$LANGCHOICE/modules/email/setupemail ] || LANGCHOICE=englishuk
source /opt/karoshi/serversetup/language/$LANGCHOICE/modules/email/setupemail
[ -f /opt/karoshi/web_controls/language/$LANGCHOICE/all ] || LANGCHOICE=englishuk
source /opt/karoshi/web_controls/language/$LANGCHOICE/all

source /opt/karoshi/server_network/domain_information/domain_name

#Check if timout should be disabled
if [ `echo $REMOTE_ADDR | grep -c $NOTIMEOUT` = 1 ]
then
TIMEOUT=86400
fi
############################
#Show page
############################
echo "Content-type: text/html"
echo ""
echo '
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <title>'$TITLE'</title><meta http-equiv="REFRESH" content="'$TIMEOUT'; URL=/cgi-bin/admin/logout.cgi">
<link rel="stylesheet" href="/css/'$STYLESHEET'">
<script src="/all/stuHover.js" type="text/javascript"></script>
</head>
<body onLoad="start()">'

#########################
#Get data input
#########################
TCPIP_ADDR=$REMOTE_ADDR
#DATA=`cat | tr -cd 'A-Za-z0-9\._:\-'`
DATA=`cat | tr -cd 'A-Za-z0-9\._:%\-+'`
#########################
#Assign data to variables
#########################
END_POINT=5
#Assign SERVERNAME

COUNTER=2
while [ $COUNTER -le $END_POINT ]
do
DATAHEADER=`echo $DATA | cut -s -d'_' -f$COUNTER`
if [ `echo $DATAHEADER'check'` = SERVERNAMEcheck ]
then
let COUNTER=$COUNTER+1
SERVERNAME=`echo $DATA | cut -s -d'_' -f$COUNTER`
break
fi
let COUNTER=$COUNTER+1
done

function show_status {
echo '<SCRIPT language="Javascript">'
echo 'alert("'$MESSAGE'")';
echo 'window.location = "/cgi-bin/admin/karoshi_servers_view.cgi"'
echo '</script>'
echo "</body></html>"
exit
}

#Generate navigation bar
/opt/karoshi/web_controls/generate_navbar_admin

#########################
#Check data
#########################
#Check to see that servername is not blank
if [ $SERVERNAME'null' = null ]
then
MESSAGE=$BLANKSERVERMSG
show_status
fi

echo '<form action="/cgi-bin/admin/module_email.cgi" method="post"><div id="actionbox"><b>'$TITLE' - '$SERVERNAME'</b><br><br>
<input name="_SERVERNAME_" value="'$SERVERNAME'" type="hidden">
<input name="_DOMAINPATH_" value="'$REALM'" type="hidden">
<b>'$DESCRIPTIONMSG'</b><br><br>
'$HELPMSG1'<br><br>
<b>'$PARAMETERSMSG'</b><br><br>
  <table class="standard" style="text-align: left;" border="0" cellpadding="2" cellspacing="0">
    <tbody>'

#Check to see if an email server has already been assigned
if [ -f /opt/karoshi/server_network/emailserver ]
then
CURRENTEMAILSERVER=`sed -n 1,1p /opt/karoshi/server_network/emailserver | sed 's/ //g'`
if [ $CURRENTEMAILSERVER != $SERVERNAME ]
then
echo '<tr><td style="width: 180px;">'$CURRRENTMAILSERVERMSG'</td><td>'$CURRENTEMAILSERVER'</td><td><a class="info" href="javascript:void(0)"><img class="images" alt="" src="/images/help/info.png"><span>'$CURRENTSERVERHELP1'</span></a></td></tr>
<tr><td>'$COPYMAILMSG'</td><td><input name="_COPYEMAIL_" value="yes" type="checkbox"></td><td><a class="info" href="javascript:void(0)"><img class="images" alt="" src="/images/help/info.png"><span>'$CURRENTSERVERHELP2'</span></a></td></tr>'
fi
fi

echo '<tr><td style="width: 180px;">
'$DOMAINMSG'</td>
        <td style="vertical-align: top; text-align: right;">mail</td><td>.</td><td>'$REALM'</td><td>
<a class="info" href="javascript:void(0)"><img class="images" alt="" src="/images/help/info.png"><span>'$EMAILDOMAINHELP'</span></a>
      </td></tr>
<tr><td>Web Mail Access</td><td>'


#Check to see if this server has been assigned an alias
if [ -f /opt/karoshi/server_network/aliases/$SERVERNAME ]
then
ALIAS=`sed -n 1,1p /opt/karoshi/server_network/aliases/$SERVERNAME`
echo ''$ALIAS'</td><td>.</td><td>'$REALM'<input type="hidden" name="_ALIAS_" value="'$ALIAS'"></td></tr>'
else
echo '<select name="_ALIAS_"><option></option>'

#Get a set of available aliases to check

#Check www.realm
[ `nslookup www.$REALM 127.0.0.1 | grep -c ^Name:` = 0 ] && echo '<option>www</option>'
COUNTER=1
while [ $COUNTER -le 10 ]
do
[ `nslookup www$COUNTER.$REALM 127.0.0.1 | grep -c ^Name:` = 0 ] && echo '<option>www'$COUNTER'</option>'
let COUNTER=$COUNTER+1
done
echo '</select></td><td>.</td><td>'$REALM'</td><td><a class="info" target="_blank" href="http://www.linuxschools.com/karoshi/documentation/wiki/index.php?title=Moodle_Server"><img class="images" alt="" src="/images/help/info.png"><span>'$ALIASHELP'</span></a></td></tr>'
echo 
fi



echo '</tbody></table><br><br>
</div>
<div id="submitbox">
<input value="'$SUBMITMSG'" class="button" type="submit"> <input value="'$RESETMSG'" class="button" type="reset">
</div>
</form>
</body>
</html>
'
exit
