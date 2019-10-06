# Shamelessly copied from https://unix.stackexchange.com/a/223000
read_password() {
  PASS="$(
    # always read from the tty even when redirected:
    exec < /dev/tty || exit # || exit only needed for bash

    # save current tty settings:
    tty_settings=$(stty -g) || exit

    # schedule restore of the settings on exit of that subshell
    # or on receiving SIGINT or SIGTERM:
    trap 'stty "$tty_settings"' EXIT INT TERM

    # disable terminal local echo
    stty -echo || exit

    # prompt on tty
    printf "Password: " > /dev/tty

    # read password as one line, record exit status
    IFS= read -r password; ret=$?

    # display a newline to visually acknowledge the entered password
    echo > /dev/tty

    # return the password for $REPLY
    printf '%s\n' "$password"

    # re-enable terminal local echo
    stty echo || exit

    exit "$ret"
  )"
}

ask_times=3

# To always ensure that we see some terminal output after refreshing the page, we force clear
clear

# Color scripts copied from https://stackoverflow.com/a/58149187
red()     { printf "\e[31m${1}\e[0m"; }
yellow()  { printf "\e[33m${1}\e[0m"; }
green()   { printf "\e[32m${1}\e[0m"; }
cyan()    { printf "\e[36m${1}\e[0m"; }
blue()    { printf "\e[34m${1}\e[0m"; }
magenta() { printf "\e[35m${1}\e[0m"; }

# Generated from http://patorjk.com/software/taag/ with 'Reverse' font
red     "===================================================================================================\n";
red     "=  ====  ======  ============================       ==========  ===================================\n";
yellow  "=  ====  ======  ============================  ====  =========  ===================================\n";
yellow  "=  ====  ======  ============================  ====  =========  =============  ====================\n";
green   "=  ====  ==  ==  =  ==  ==  = ====   ========  ===   ===   ===  ======   ===    ==  ===   ====   ==\n";
green   "=   ==   ======    =======     ==  =  =======      ====     ==    ===     ===  =======  =  ==  =  =\n";
cyan    "==  ==  ===  ==   ====  ==  =  ===    =======  ====  ==  =  ==  =  ==  =  ===  ===  ==  ======  ===\n";
cyan    "==  ==  ===  ==    ===  ==  =  =====  =======  ====  ==  =  ==  =  ==  =  ===  ===  ==  =======  ==\n";
blue    "===    ====  ==  =  ==  ==  =  ==  =  =======  ====  ==  =  ==  =  ==  =  ===  ===  ==  =  ==  =  =\n";
blue    "====  =====  ==  =  ==  ==  =  ===   ========  ====  ===   ===    ====   ====   ==  ===   ====   ==\n";
magenta "===================================================================================================\n";

while [ $ask_times -gt 0 ]
do
  read_password

  # TODO: Figure out better system for shell-based authentication
  if [ "$PASS" = "viking" ]; then
    break
  else
    ask_times=$(( $ask_times - 1 ))
    printf "Incorrect! $(( $ask_times )) times left!\n"
  fi
done

if [ $ask_times -gt 0 ]; then
  printf "Logged in!\n"
  /bin/bash
else
  printf "You have been locked out of the system!"
fi
