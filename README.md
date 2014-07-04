
# ulogme


> ### How productive were you today? How much code have you written? Where did your time go?

Keep track of your productivity throughout the day: visualize your active window titles and the number of keystrokes in beautiful daily HTML timelines. Current features:

- Records your active window title throughout the day
- Records the frequency of key presses throughout the day
- Everything runs completely locally: none of your data is uploaded anywhere
- All generate reports are just static HTML and JSON files, ready to be archived for your future viewing pleasure or analysis.

The project currently **only works on Ubuntu**.

## Demo

See a [live demo here.](http://cs.stanford.edu/people/karpathy/ulogme)

## Getting Started

To start recording:

1. Clone the repository: `git clone https://github.com/karpathy/ulogme.git`
2. `cd` inside and run `./ulogme.sh` (note: this will ask you for sudo authentication which is required for `showkey` command). This will launch two scripts for listening to your keyboard activity and active window and log the activity into log files in the `keyfreq` and `activewin` folders.  The log files simply contain the unix time stamp and associated data.

Note, you may need to get some packages on Ubuntu (such as `xdotool` and `wmctrl`). You can simply `sudo apt-get install` both of them. To view the results, proceed as follows:

1. Run `python export_events.py`. This will write JSON files into `render/` directory. The `index.html` file will later read these to show the visualization
2. Go to `render/render_settings.js` and modify the title mappings according to your own preferences (the input to the `mapwin` function is raw window title. The output should be your desired window categories). As an example, one rule specifies that if a window title contains "Google Chrome", it should simply all be grouped into category called "Google Chrome". Follow the provided example.
3. Start a webserver inside `render/`, for example using `python -m SimpleHTTPServer` and open a window at the root, probably `http://localhost:8000/`. Enjoy the visualization!

### Note taking

You can record notes! For example if I'm about to head out to a meeting, I run `./note.sh`. The script asks me to input a note and then simply saves it in `logs/notes.txt` with current timestamp. You can also add notes retrospectively: In the visualization inteface, click any past event of interest and ulogme will give you the timestamp at that time, which you can use as first argument to `./note.sh` to specify a note for that time.

## TODO
- **MAC OSX support**. Requires port of functionality in `logactivewin.sh` and `keyfreq.sh` to MAC OSX.
- Possibly incorporate support for lowres screen snapshots. These can already be logged with `./logdesktop.sh` but are not yet displayed
- Much more visualizations and analysis!

## License
BSD 2 clause license
