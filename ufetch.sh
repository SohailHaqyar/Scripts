#!/bin/sh
#
# ufetch-popos - tiny system info for pop!_os

## INFO

# user is already defined
host="$(hostname)"
os="$(lsb_release -ds)"
kernel="$(uname -sr)"
uptime="$(uptime -p | sed 's/up //')"
packages="$(dpkg -l | wc -l)"
shell="$(basename "${SHELL}")"

## UI DETECTION

parse_rcs() {
	for f in "${@}"; do
		wm="$(tail -n 1 "${f}" 2> /dev/null | cut -d ' ' -f 2)"
		[ -n "${wm}" ] && echo "${wm}" && return
	done
}

rcwm="$(parse_rcs "${HOME}/.xinitrc" "${HOME}/.xsession")"

ui='unknown'
uitype='UI'
if [ -n "${DE}" ]; then
	ui="${DE}"
	uitype='DE'
elif [ -n "${WM}" ]; then
	ui="${WM}"
	uitype='WM'
elif [ -n "${XDG_CURRENT_DESKTOP}" ]; then
	ui="${XDG_CURRENT_DESKTOP}"
	uitype='DE'
elif [ -n "${DESKTOP_SESSION}" ]; then
	ui="${DESKTOP_SESSION}"
	uitype='DE'
elif [ -n "${rcwm}" ]; then
	ui="${rcwm}"
	uitype='WM'
elif [ -n "${XDG_SESSION_TYPE}" ]; then
	ui="${XDG_SESSION_TYPE}"
fi

ui="$(basename "${ui}")"

## DEFINE COLORS

# probably don't change these
if [ -x "$(command -v tput)" ]; then
	bold="$(tput bold 2> /dev/null)"
	black="$(tput setaf 0 2> /dev/null)"
	red="$(tput setaf 1 2> /dev/null)"
	green="$(tput setaf 2 2> /dev/null)"
	yellow="$(tput setaf 3 2> /dev/null)"
	blue="$(tput setaf 4 2> /dev/null)"
	magenta="$(tput setaf 5 2> /dev/null)"
	cyan="$(tput setaf 6 2> /dev/null)"
	white="$(tput setaf 7 2> /dev/null)"
	reset="$(tput sgr0 2> /dev/null)"
fi

# you can change these
lc="${reset}${bold}${cyan}"         # labels
nc="${reset}${bold}${cyan}"         # user and hostname
ic="${reset}"                       # info
c0="${reset}${cyan}"                # first color

## OUTPUT

cat <<EOF
${c0}  ______
${c0}  \\   _ \\        __  ${nc}${USER}${ic}@${nc}${host}${reset}
${c0}   \\ \\ \\ \\      / /  ${lc}OS:        ${ic}${os}${reset}
${c0}    \\ \\_\\ \\    / /   ${lc}KERNEL:    ${ic}${kernel}${reset}
${c0}     \\  ___\\  /_/    ${lc}UPTIME:    ${ic}${uptime}${reset}
${c0}      \\ \\    _       ${lc}PACKAGES:  ${ic}${packages}${reset}
${c0}     __\\_\\__(_)_     ${lc}SHELL:     ${ic}${shell}${reset}
${c0}    (___________)    ${lc}${uitype}:        ${ic}${ui}${reset}

EOF
