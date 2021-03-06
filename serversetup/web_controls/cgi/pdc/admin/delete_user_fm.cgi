#!/bin/bash
#Delete User
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
#jsharrad@karoshi.org.uk

#
#Website: http://www.karoshi.org.uk

#Detect mobile browser
MOBILE=no
source /opt/karoshi/web_controls/detect_mobile_browser
source /opt/karoshi/web_controls/version

############################
#Language
############################
SHUTDOWN_CODE="${RANDOM:0:3}"

STYLESHEET=defaultstyle.css
TIMEOUT=300
NOTIMEOUT=127.0.0.1
[ -f /opt/karoshi/web_controls/user_prefs/"$REMOTE_USER" ] && source /opt/karoshi/web_controls/user_prefs/"$REMOTE_USER"
export TEXTDOMAIN=karoshi-server

#Check if timout should be disabled
if [[ $(echo "$REMOTE_ADDR" | grep -c "$NOTIMEOUT") = 1 ]]
then
	TIMEOUT=86400
fi
############################
#Show page
############################
echo "Content-type: text/html"
echo ""
echo '
<!DOCTYPE html><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <title>'$"Delete User"'</title><meta http-equiv="REFRESH" content="'"$TIMEOUT"'; URL=/cgi-bin/admin/logout.cgi">
  <link rel="stylesheet" href="/css/'"$STYLESHEET"'?d='"$VERSION"'">
<script src="/all/js/jquery.js"></script>
<script src="/all/js/script.js"></script>
<script src="/all/stuHover.js" type="text/javascript"></script><meta name="viewport" content="width=device-width, initial-scale=1"> <!--480-->'

if [ "$MOBILE" = yes ]
then
echo '<link rel="stylesheet" type="text/css" href="/all/mobile_menu/sdmenu.css">
	<script src="/all/mobile_menu/sdmenu.js">
		/***********************************************
		* Slashdot Menu script- By DimX
		* Submitted to Dynamic Drive DHTML code library: www.dynamicdrive.com
		* Visit Dynamic Drive at www.dynamicdrive.com for full source code
		***********************************************/
	</script>
	<script>
	// <![CDATA[
	var myMenu;
	window.onload = function() {
		myMenu = new SDMenu("my_menu");
		myMenu.init();
	};
	// ]]>
	</script>'
fi

echo '</head>
<body onLoad="start()"><div id="pagecontainer">'
#########################
#Get data input
#########################
DATA=$(cat | tr -cd 'A-Za-z0-9\._:\-')
#########################
#Assign data to variables
#########################
END_POINT=5
function get_data {
COUNTER=2
DATAENTRY=""
while [[ $COUNTER -le $END_POINT ]]
do
	DATAHEADER=$(echo "$DATA" | cut -s -d'_' -f"$COUNTER")
	if [[ "$DATAHEADER" = "$DATANAME" ]]
	then
		let COUNTER="$COUNTER"+1
		DATAENTRY=$(echo "$DATA" | cut -s -d'_' -f"$COUNTER")
		break
	fi
	let COUNTER=$COUNTER+1
done
}

#Assign username
DATANAME=USERNAME
get_data
USERNAME="$DATAENTRY"

#FILE
DATANAME=FILE
get_data
FILE="$DATAENTRY"

#Generate navigation bar
if [ "$MOBILE" = no ]
then
	DIV_ID=actionbox3
	#Generate navigation bar
	/opt/karoshi/web_controls/generate_navbar_admin
else
	DIV_ID=actionbox2
fi

echo '
<form action="/cgi-bin/admin/delete_user.cgi" method="post">
<input name="_FORMCODE_" value="'"$SHUTDOWN_CODE"'" type="hidden">'

[ "$MOBILE" = no ]  && echo '<div id="'"$DIV_ID"'"><div id="titlebox">'

#Show back button for mobiles
if [ "$MOBILE" = yes ]
then
	echo '<div style="float: center" id="my_menu" class="sdmenu">
	<div class="expanded">
	<span>'$"Delete User"'</span>
<a href="/cgi-bin/admin/mobile_menu.cgi">'$"Menu"'</a>
</div></div>
'
else
	echo '<table class="standard" style="text-align: left;" ><tbody>
<tr><td><div class="sectiontitle">'$"Delete User"'</div></td><td><a class="info" target="_blank" href="http://www.linuxschools.com/karoshi/documentation/wiki/index.php?title=Delete_User"><img class="images" alt="" src="/images/help/info.png"><span>'$"Delete users from your system."'</span></a></td></tr></tbody></table><br>'
fi

#Check that this server is not part of a federated setup
if [ -f /opt/karoshi/server_network/servers/"$HOSTNAME"/federated_server ]
then
	echo $"This server is part of a federated system. Users must be deleted on the main federation server." '</div></div></body></html>'
	exit
fi


#Get request data if asked
if [ -z "$FILE" ]
then
	if [ -f /opt/karoshi/user_requests/delete_users/"$FILE" ]
		then
		NEW_USER_DATA=$(sed -n 1,1p /opt/karoshi/user_requests/delete_users/"$FILE")
		FORENAME=$(echo "$NEW_USER_DATA" | cut -d: -f1)
		SURNAME=$(echo "$NEW_USER_DATA" | cut -d: -f2)
		GROUP=$(echo "$NEW_USER_DATA" | cut -d: -f3)
		echo '<input name="_REQUESTFILE_" value="'$FILE'" type="hidden">'
		#Try and get username

		if [[ $(echo "$GROUP" | grep -c ^yr) -gt 0 ]]
		then
			GROUPCHARCOUNT=$(echo "$GROUP" | wc -c)
			let GROUPCHARCOUNT="$GROUPCHARCOUNT"-1
			let GROUPSTARTCHAR="$GROUPCHARCOUNT"-2
			USERNAME=$(echo "${FORENAME:0:1}$SURNAME${GROUP:$GROUPSTARTCHAR:$GROUPCHARCOUNT}" | tr 'A-Z' 'a-z')
		else
			USERNAME=$(echo "${FORENAME:0:1}$SURNAME" | tr 'A-Z' 'a-z')
		fi
	fi
fi

if [ "$MOBILE" = yes ]
then
	echo '<div id="mobileactionbox">'
	echo '<div id="suggestions"></div>
	'$"Username"'<br>
	<input required="required" tabindex= "1" style="width: 160px; height: 30px;" name="_USERNAME_" value="'"$USERNAME"'" size="20" type="text" id="inputString" onkeyup="lookup(this.value);"><br><br>
	'$"Delete Code"' '"$SHUTDOWN_CODE"'<br><br>
	'$"Confirm"'<br>
	<input required="required" tabindex= "2" style="width: 160px; height: 30px;" name="_SHUTDOWNCODE_" maxlength="3" size="3" type="text"><br><br>
	<div id="photobox"><img src="/images/blank_user_image.jpg" width="140" height="180" alt="photo"></div>
	'
else

	echo '
  	<table class="standard" style="text-align: left;" >
		<tbody>
			<tr>
				<td style="width: 180px;">
				'$"Username"'
				</td>
				<td><div id="suggestions"></div><input required="required" tabindex= "1" style="width: 200px;" name="_USERNAME_" value="'"$USERNAME"'" size="20" type="text" id="inputString" onkeyup="lookup(this.value);">
				</td>
				<td>
					<a class="info" target="_blank" href="http://www.linuxschools.com/karoshi/documentation/wiki/index.php?title=Delete_User"><img class="images" alt="" src="/images/help/info.png"><span>'$"Please enter the username that you want to delete. This WILL delete all of the user files and their home folder."'</span></a>
				</td>
			</tr>
			<tr>
				<td>'$"Confirm"'</td>
				<td style="vertical-align: top; text-align: left;"><input style="width: 200px;" required="required" tabindex= "2" name="_SHUTDOWNCODE_" maxlength="3" size="3" type="text"></td>
				<td><a class="info" target="_blank" href="http://www.linuxschools.com/karoshi/documentation/wiki/index.php?title=Delete_User"><img class="images" alt="" src="/images/help/info.png"><span>'$"Type in the number displayed to confirm that you want to delete the user."'</span></a></td>
			</tr>
			<tr>
				<td>'$"Delete Code"'</td>
				<td style="vertical-align: top; text-align: left;"><b>'"$SHUTDOWN_CODE"'</b></td>
			</tr>
		 	<tr>
				<td>'$"Archive home area"'</td>
				<td><input type="checkbox" name="_ARCHIVE_" value="yes"></td>
				<td><a class="info" target="_blank" href="http://www.linuxschools.com/karoshi/documentation/wiki/index.php?title=Delete_User"><img class="images" alt="" src="/images/help/info.png"><span>'$"This will archive the user home area to the archive folder in /home/users."'</span></a></td>
			</tr>
			<tr><td style="vertical-align:top">'$"User Photo"'</td><td><div style="width: 120px;" id="photobox"><img src="/images/blank_user_image.jpg" width="120" height="150" alt="photo"></div></td></tr>
		</tbody>
	</table>'

fi
echo '<br><input value="'$"Submit"'" class="button" type="submit"> <input value="'$"Reset"'" class="button" type="reset"></div>'

[ "$MOBILE" = no ] && echo '</div>'

echo '</form></div></body></html>'
exit

