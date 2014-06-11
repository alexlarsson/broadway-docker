export LANG="en_US.UTF-8"
export LC_MEASUREMENT="en_US.utf8"
export LC_MONETARY="en_US.utf8"
export LC_NUMERIC="en_US.utf8"
export LC_PAPER="en_US.utf8"
export LC_TIME="en_US.utf8"
export DBUS_SESSION_BUS_ADDRESS=`dbus-daemon --session --print-address --fork`
export XDG_CURRENT_DESKTOP=GNOME
export XDG_MENU_PREFIX="gnome-"
broadwayd&
exec /panel.js
