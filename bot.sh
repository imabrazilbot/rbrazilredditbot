#!/bin/bash

### BEGIN INIT INFO
# Provides:          folha-reddit-bot
# Required-Start:
# Required-Stop:
# Should-Stop:
# X-Start-Before:
# Default-Start:     S
# Default-Stop:      0 1 6
# Short-Description: Run bot
# Description:
### END INIT INFO

set -e

# Include core init functions if needed
. /lib/lsb/init-functions

PARAM=/etc/default/bot
if [ -f $PARAM ]; then
    . "$PARAM"
fi

stop() {
    # only bot running as py 3.5 atm
    pgrep python3.5 | xargs kill
}

run() {
    source /home/pi/folha-reddit/.env && \
                nohup /home/pi/.venvs/folha/bin/python3.5 /home/pi/folha-reddit/main.py &
}

case "${1:-}" in
    stop)
        echo "I don't use this, I never stop"
        echo "Ok, I actually do stop"
        stop
        ;;
    restart|reload|force-reload)
        stop
        run
        ;;
    start)
        echo "Starting bot"
        ;;

    *)
        echo "Usage: ${0:-} {start|stop|status|restart|reload|force-reload}" >&2
        exit 1
        ;;
esac
