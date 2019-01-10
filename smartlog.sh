#!/bin/bash
##############################################################################
# Smartlog v 1.0
##############################################################################

set -e


LOGDIR=~/.smartlog
SILENT=false
if [ ! -d $LOGDIR ]
then
  mkdir $LOGDIR
fi

OK_SOUND_FILE=$LOGDIR/ok.wav
WARN_SOUND_FILE=$LOGDIR/warn.wav
FAIL_SOUND_FILE=$LOGDIR/fail.wav
PROMPT_SOUND_FILE=$LOGDIR/prompt.wav
INFO_SOUND_FILE=$LOGDIR/info.wav
SEX_SOUND_FILE=$LOGDIR/sex.wav

LOGFILE=$LOGDIR/smartlog
OUTPUTLOG=$LOGDIR/output.log
ERRORLOG=$LOGDIR/error.log

if [ -z $LOG_ALL ]
then
	LOG_ALL=true
fi



##############################################################################
# Color definitions.
##############################################################################
BOLD=`tput bold`
ULINE=`tput smul`
NOLINE=`tput rmul`
RED=`tput setaf 1`
GREEN=`tput setaf 2`
YELLOW=`tput setaf 3`
BLUE=`tput setaf 4`
PURPLE=`tput setaf 5`
NORMAL=`tput sgr0`

##############################################################################
# Depth control
##############################################################################
LOGLEVEL=""

down() {
  export LOGLEVEL="$LOGLEVEL "
}

up () {
  export LOGLEVEL="${LOGLEVEL%?}"
}

##############################################################################
# Type text out
##############################################################################
typeout() {
TEXT="$1"
for (( i=0; i<"${#TEXT}"; i++ )); do
	echo -n "${TEXT:$i:1}"
	sleep .01
done
}
TYPEOUT=false


##############################################################################
# Print abort message and exit.
##############################################################################
timestamp() {
	echo "" >> $LOGFILE
	date    >> $LOGFILE
}
timestamp


##############################################################################
# Print abort message and exit.
##############################################################################
die() {
	if [  "$QUIET" != "true"  ]
	then
		abort "$1"
	fi
	exit 1
}



##############################################################################
# Print alert message, help message and exit.
##############################################################################
error() {
	if [  "$QUIET" != "true"  ]
	then
		alert "$1"
		tip "Check $ERRORLOG for details"
		echo ""
	fi
}



##############################################################################
# Print helpful message.
##############################################################################
optip() {
	tip "You can set it with the $1 option"
}


##############################################################################
# Print helpful message.
##############################################################################
tip() {
	if [  "$QUIET" != "true"  ]
	then
		helper "$1."
		info_ok
	fi
}



##############################################################################
# Print helpful message and exit.
##############################################################################
endtip() {
	if [  "$QUIET" != "true"  ]
	then
		helper "$1."
		echo ""
		exit
	fi
}



##############################################################################
# Print helpful message and exit.
##############################################################################
checklog() {
	if [  "$QUIET" != "true"  ]
	then
		endtip "Check $ERRORLOG for details";
	fi
}



##############################################################################
# Pretty-print a log message.
##############################################################################
typeit() {
	if [ "$TYPEOUT" != "true" ]
	then
		echo -n "$1"
	else
		typeout "$1"
	fi
}

##############################################################################
# Pretty-print a log message.
##############################################################################
logtypeit() {
	if [ "$TYPEOUT" != "true" ]
	then
		echo -n "$1" | tee -a "$LOGFILE"
	else
		typeout "$1"
		echo -n "$1" >> "$LOGFILE"
	fi
}


lecho() {
	if [ "$LOG_ALL" != "true" ]
	then
		typeit "$1"
	else
		logtypeit "$1"
	fi
}


##############################################################################
# Pretty-print a log message.
##############################################################################
log() {
	if [  "$QUIET" != "true"  ]
	then
		MSG="$1"
		LINE="$LOGLEVEL${GREEN}* ${NORMAL}${MSG}...";
		export LOGLINE=$LINE;
		lecho "$LOGLEVEL$LINE"
	fi
}


##############################################################################
# Pretty-print a log message, no ellipsis.
##############################################################################
nlog() {
	if [  "$QUIET" != "true"  ]
	then
		MSG="$1"
		LINE="$LOGLEVEL${GREEN}* ${NORMAL}${MSG}";
		export LOGLINE=$LINE;
		lecho "$LOGLEVEL$LINE"
	fi
}

##############################################################################
# Pretty-print a log message.
##############################################################################
tlog() {
	OLDTYPEOUT=$TYPEOUT
	TYPEOUT=true 
	if [  "$QUIET" != "true"  ]
	then
		MSG="$1"
		LINE="$LOGLEVEL${GREEN}* ${NORMAL}${MSG}...";
		export LOGLINE=$LINE;
		lecho "$LOGLEVEL$LINE"
	fi
	TYPEOUT=$OLDTYPEOUT
}



##############################################################################
# Pretty-print a helper message.
##############################################################################
helper() {
	if [  "$QUIET" != "true"  ]
	then
		MSG="$1"
		LINE="$LOGLEVEL${BLUE}* ${NORMAL}${MSG}";
		export LOGLINE=$LINE;
		lecho "$LOGLEVEL$LINE"
	fi
}



##############################################################################
# Pretty-print a prompt message.
##############################################################################
prompt () {
	if [  "$QUIET" != "true"  ]
	then
		MSG="$1"
		LINE="$LOGLEVEL${PURPLE}*${NORMAL} ${BOLD}${MSG}${NORMAL}: ${NORMAL}";
		export LOGLINE=$LINE;
		if [ "$LOG_ALL" != "true" ]
		then
			echo -n "$LOGLEVEL$LINE"
		else
			echo -n "$LOGLEVEL$LINE"  | tee -a $LOGFILE
			echo "" >> $LOGFILE
		fi
    if [ "$SILENT" == "false" ]
    then
      play -qv .1 $PROMPT_SOUND_FILE
    fi
		read
	fi
}


##############################################################################
# Pretty-print a prompt message; store answer in REPLY; if none, use default.
##############################################################################
prompt_default () {
	MSG="$1"
	LINE="$LOGLEVEL${PURPLE}*${NORMAL} ${BOLD}${MSG}${NORMAL} [$2]: ${NORMAL}";
	export LOGLINE=$LINE;
	if [ "$LOG_ALL" != "true" ]
	then
		echo -n "$LOGLEVEL$LINE"
	else
		echo -n "$LOGLEVEL$LINE"  | tee -a $LOGFILE
		echo "" >> $LOGFILE
	fi
	read REPLY
	if ! check_var "response" $REPLY
	then
		REPLY=$2
		tip "Default set to $REPLY"
	fi
}


##############################################################################
# Pretty-print a prompt message.
##############################################################################
yesno () {
	if [  "$QUIET" != "true"  ]
	then
		MSG="$1"
		LINE="$LOGLEVEL${PURPLE}*${NORMAL} ${BOLD}${MSG}${NORMAL} (y/n): ${NORMAL}";
		export LOGLINE=$LINE;
		if [ "$LOG_ALL" != "true" ]
		then
			echo -n "$LOGLEVEL$LINE"
		else
			echo -n "$LOGLEVEL$LINE"  | tee -a $LOGFILE
			echo "" >> $LOGFILE
		fi
		read 
		case $REPLY in
			[Yy]* ) return 0;;
			[Nn]* ) return 1;;
			* ) tip "Please answer yes or no";;
		esac
		if yesno "$1"
		then
			return 0
		else
			return 1
		fi
	fi
}



##############################################################################
# Pretty-print a warning message.
##############################################################################
warn() {
	if [  "$QUIET" != "true"  ]
	then
		MSG="$1"
		LINE="$LOGLEVEL${YELLOW}*${NORMAL} ${MSG}.";
		export LOGLINE="$LOGLEVEL${YELLOW}*${NORMAL} ${MSG}.";
		lecho "$LOGLEVEL$LINE"
		warn_ok
	fi
}



##############################################################################
# Pretty-print an abort message.
##############################################################################
abort() {
	if [  "$QUIET" != "true"  ]
	then
		MSG="$1"
		LINE="$LOGLEVEL${RED}*${NORMAL} ${MSG}!";
		export LOGLINE="$LOGLEVEL${RED}*${NORMAL} ${MSG}!";
		lecho "$LOGLEVEL$LINE"
		fail
	fi
}



##############################################################################
# Pretty-print an alert message.
##############################################################################
alert() {
	if [  "$QUIET" != "true"  ]
	then
		MSG="$1"
		LINE="$LOGLEVEL${RED}*${NORMAL} ${MSG}!";
		export LOGLINE=$LINE;
		lecho "$LOGLEVEL$LINE"
	#rok
	fi
}




##############################################################################
# Using a LINE, print a status flag of the [  OK  ] variety.
##############################################################################
flag() {
	if [  "$QUIET" != "true"  ]
	then
		LINE=$1
		#let COLS=$(tput cols)-${#LOGLINE}+${#LINE}
		let COLS=$(tput cols)-${#LOGLINE}+${#LINE}-${#LOGLEVEL}
		if [ "$LOG_ALL" != "true" ]
		then
			printf "%${COLS}s\n" "$LINE"
		else
			printf "%${COLS}s\n" "$LINE" | tee -a $LOGFILE
		fi
	fi
}


##############################################################################
# Print [  OK  ] message.
##############################################################################
ok() {
	flag "[${GREEN}  OK  ${NORMAL}]"
  if [ "$SILENT" == "false" ]
  then
    play -qv .1 $OK_SOUND_FILE
  fi
}



##############################################################################
# Print [ FAIL ] message.
##############################################################################
fail() {
	flag "[${RED} FAIL ${NORMAL}]"
  if [ "$SILENT" == "false" ]
  then
    play -qv .1 $FAIL_SOUND_FILE
  fi
	success=0;
}


##############################################################################
# Print [  OK  ] message, in yellow.
##############################################################################
yok() {
	flag "[${YELLOW}  OK  ${NORMAL}]"
}


##############################################################################
# Print [  OK  ] message, in red.
##############################################################################
rok() {
	flag "[${RED}  OK  ${NORMAL}]"
}


##############################################################################
# Print [ WARN ] message, in yellow.
##############################################################################
warn_ok () {
	flag "[${YELLOW} WARN ${NORMAL}]"
  if [ "$SILENT" == "false" ]
  then
    play -qv .1 $WARN_SOUND_FILE
  fi
}


##############################################################################
# Print [ WARN ] message, in yellow.
##############################################################################
info_ok () {
	flag "[${BLUE} INFO ${NORMAL}]"
  if [ "$SILENT" == "false" ]
  then
    play -qv .1 $INFO_SOUND_FILE
  fi
}


##############################################################################
# Print [ WARN ] message, in yellow.
##############################################################################
ask_ok () {
	flag "[${PURPLE} ASK  ${NORMAL}]"
}




check_cmd () {
	log "Checking if $1 command exists"
	if command -v $2 2> /dev/null > /dev/null
	then
		ok;  return 0;
	else
		fail; return 1;
	fi
}


check_dir () {
	log "Checking if $1 directory exists";
	if [ -d "$2" ]
	then
		ok;   return 0;
	else
		yok;  return 1;
	fi
}


require_dir () {
	if ! check_dir "$1" "$2"
	then
		die "The $1 directory was not found"
	fi
}


check_file () {
	log "Checking if $1 file exists";
	if [ -f "$2" ]
	then
		ok;     return 0;
	else
		yok;   return 1;
	fi
}


require_file () {
	if ! check_file "$1" "$2"
	then
		die "The $1 directory was not found"
	fi
}


check_var () {
	log "Checking if $1 variable is set";
	if [ -z "$2" ]
	then
		yok;     return 1;
	else
		ok;       return 0;
	fi
}


require_var () {
	if ! check_var "$1" "$2"
	then
		die "The $1 variable was not set"
	fi
}


require_var_file () {
	if ! check_var "$1" "$2"
	then
		die "File variable $1 not set"
	fi
	if ! check_file "$1" "$2"
	then
		die "File $1 does not exist"
	fi
}


require_var_dir () {
	if ! check_var "$1" "$2"
	then
		die "The $1 directory variable was not set"
	fi
	if ! check_dir "$1" "$2"
	then
		die "The $1 directory does not exist"
	fi
}


##############################################################################
# Requires that a directory, pointed to by a variable, exist; if not it
# uses a default option.  Die upon failure.  Note: the second argument must 
# be passed in single quotes.
##############################################################################
require_var_dir_default () {
	var=\$$2
	val=`eval echo $var`
	if ! check_var "$1 directory" "$val"
	then
		tip "Setting default to $3"
		eval $2=$3
	fi
	if ! check_dir "$1" "$3"
	then
		die "The $1 dir does not exist"
	fi
}


##############################################################################
# Same as above, for file.
##############################################################################
require_var_file_default () {
	var=\$$2
	val=`eval echo $var`
	if ! check_var "$1 file" "$val"
	then
		tip "Setting default to $3"
		eval $2=$3
	fi
	if ! check_file "$1" "$3"
	then
		die "The $1 file does not exist"
	fi
}



s_if() {
	log "$1";
	if $2
	then
		ok;   return 0;
	else
		fail; return 1;
	fi
}


spinner() {
    local pid=$1
    local delay=0.10
    local spinstr='|/-\'
    while [ "$(ps a | awk '{print $1}' | grep $pid)" ]; do
        local temp=${spinstr#?}
        printf " [%c]  " "$spinstr"
        local spinstr=$temp${spinstr%"$temp"}
        sleep $delay
        printf "\b\b\b\b\b\b"
    done
    printf "    \b\b\b\b"
}


s_exn () {
	log "$1";
	if $2 2>> $ERRORLOG 1>> $OUTPUTLOG
	then
		ok;   return 0;
	else
		fail; return 1;
	fi
}


s_ex () {
	log "$1";
	$2 2>> $ERRORLOG 1>> $OUTPUTLOG &
  play -qv .1 $SEX_SOUND_FILE
	spinner $!
	#wait $!
	if [ $? == "0" ]
	then
		ok;   return 0;
	else
		fail; return 1;
	fi
}


offer_to_create() {
	if ! check_dir "$1" "$2"
	then
		if yesno "Directory does not exist. Create it?"
		then
			s_ex "Making directory" \
                             "mkdir $2"
		else
			die "Could not create directory"
		fi
	fi
}


reset_logs() {
	QUIET=true
	export OUTPUTLOG="$1.out"
	if check_file "$1.out" "$1.out"
	then
		rm "$1.out"
	fi
	export ERRORLOG="$1.err"
	if check_file "$1.err" "$1.err"
	then
		rm "$1.err"
	fi
	QUIET=false
}


cleanup_empty() {
	for file in `ls`
	do
		if [[ ! -s $file ]]
		then
			rm $file 1> /dev/null 2> /dev/null
		fi
	done
}
