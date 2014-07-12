
# I can't for the life of me figure out how to catch a keyboard interrupt
# in the PyObjCTools framework. As a workaround, when the Python event
# sniffer starts it writes a file called .python_pid with the pid of the
# current process. Instead of invoking the Python event sniffer directly,
# we launch it in the background here and loop infinitely. The shell script
# catches keyboard interrupts and kills the correct Python process.

mkdir -p logs

DEV=true

PID_FILE="$(pwd)/.python_pid"
ACTIVE_WINDOW_FILE="$(pwd)/logs/activewin.txt"
KEYSTROKE_FILE="$(pwd)/logs/keyfreq.txt"

control_c() {
  cat .python_pid | xargs kill
  rm -f $PID_FILE
  exit
}

trap control_c SIGINT

if [ "$DEV" = true ]; then
  # Directly invoke the python script
  python osx/ulogme_osx.py \
    --pid_file=$PID_FILE \
    --active_window_file=$ACTIVE_WINDOW_FILE \
    --keystroke_file=$KEYSTROKE_FILE \
    &
else
  # Run the app version
  ./osx/dist/ulogme_osx.app/Contents/MacOS/ulogme_osx \
    --pid_file=$PID_FILE \
    --active_window_file=$ACTIVE_WINDOW_FILE \
    --keystroke_file=$KEYSTROKE_FILE \
    &
fi


while true; do
  sleep 10
done
