
# ulogme


> ### How productive were you today? How much code have you written? Where did your time go?

Keep track of your productivity throughout the day: visualize your active window titles and the number of keystrokes in beautiful daily HTML timelines. Current features:

- Records your active window title throughout the day
- Records the frequency of key presses throughout the day
- Everything runs completely locally: none of your data is uploaded anywhere
- All generate reports are just HTML and JSON files, ready to be archived for your future viewing pleasure or analysis.

## Demo

See a [live demo here.](http://cs.stanford.edu/people/karpathy/ulogme)

## Getting Started

Project is still in early stages and currently only works on Ubuntu. The workflow right now is as follows:

- Clone the repository: `git clone https://github.com/karpathy/ulogme.git`
- `cd` inside and run `sudo ./ulogme.sh` (note: sudo is required for `showkey` command). This will launch two scripts for listening to your keyboard activity and active window and log the activity into log files in the `keyfreq` and `activewin` folders.  The log files simply contain the unix time stamp and associated data. Leave this recording for a while, then
- Run `python export_events.py`, which will write JSON files into `render/` directory. The `index.html` file will read these and create your visualizations
- Go to `render/render_settings.js` and modify the title mappings according to your own preferences. As an example, one rule specifies that if a window title contains "Google Chrome", it should simply all be grouped into category called "Google Chrome". Follow the provided example.
- Start a webserver inside `render/`, for example using `python -m SimpleHTTPServer` and open a window at the root, probably `http://localhost:8000/`. Enjoy the visualization!

## TODO
- **MAC OSX support**. Requires port of functionality in `logactivewin.sh` and `keyfreq.sh` to MAC OSX.
- Possibly incorporate support for lowres screen snapshots. These can already be logged with `./logdesktop.sh` but are not yet displayed
- Much more visualizations and analysis!

## License
BSD 2 clause license
