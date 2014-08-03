
# ulogme


> ### How productive were you today? How much code have you written? Where did your time go?

Keep track of your computer activity throughout the day: visualize your active window titles and the number of keystrokes in beautiful HTML timelines. Current features:

- Records your active window title throughout the day
- Records the frequency of key presses throughout the day
- Record custom note annotations for particular times of day, or for day in general
- Everything runs completely locally: none of your data is uploaded anywhere
- Beautiful, customizable interface in full HTML/CSS/JS powered by d3js

The project currently **only works on Ubuntu and OSX**.

## Demo

See a blog post (along with multiple screenshots) describing the project [here.](http://karpathy.github.io/2014/08/03/quantifying-productivity/)

## Getting Started

**To start recording (Ubuntu instructions)**

1. Clone the repository to some folder: `$ git clone https://github.com/karpathy/ulogme.git`
2. If you're on Ubuntu, make sure you have the dependencies: `$ sudo apt-get install xdotool wmctrl`
3. `cd` inside and run `$ ./ulogme.sh` (note: this will ask you for sudo authentication which is required for `showkey` command). This will launch two scripts. One records the frequency of keystrokes and the other records active window titles. Both write their logs into log files in the `logs/` directory. Every log file is very simply just the unix time stamp followed by data, one per line.

**To start recording (OSX instructions)**

TODO. But on OSX, just run `./ulogme.sh` should be fine.

**The user interface**

1. As a one-time setup, copy over the example settings file to your own copy: `$ cp render/render_settings_example.js render/render_settings.js` to create your own `render_settings.js` settings file. In this file modify everything to your own preferences. Follow the provided example to specify title mappings: A raw window title comes in, and we match it against regular expressions to determine what type of activity it is. For example, the code would convert "Google Chrome - some cool website" into just "Google Chrome". Follow the provided example and read the comments for all settings in the file.
2. Once that's set up, start the web server viewer: `$ python ulogme_serve.py`, and go to to the provided address) for example `http://localhost:8123`) in your browser. Hit the refresh button on top right every time you'd like to refresh the results based on most recetnly recorded activity

## User Interface

The user interface can switch between a single day view and an overview view by link on top. You have to hit the refresh button every time you'd like to pull in new data.

#### Single day page

- You can enter a reminder "blog" on top if you'd like to summarize the day for yourself or enter other memos.
- Click on any bar in the *barcode view* to enter a custom (short) note snippet for the time when the selected activity began. I use this to mark meetings, track my coffee/food intake, sleep time, or my total time spent running/swimming/gym or to leave notes for certain patterns of activity, etc. These could all later be correlated with various measures of productivity, in future.

#### Overview page

- You can click the window titles to toggle them on and off from the visualization 
- Clicking on the vertical bars takes you to the full statistics for that day.

## Known issues
- One Ubuntu user reported broken view with no data. On further inspection we found that the logs were corrupt. One of the lines in a file in `/logs` was, instead of looking as `{timestamp} {data}`  looked as `@@@@@@@{timestamp} {data}`, in other words an odd character was appended to the timestamp somehow. We manually erased these characters from the log file to fix the issue.
- Legacy code note: if you used ulogme from before 28 July, you will have to run `$ python legacy_split_events.py` to convert your events files, once.

## Contributing

The Ubuntu and OSX code base are a little separate on the data collection side. However, they each just record very simple log files in `/logs`. Once the log files are written, `export_events.py` takes the log files, does some simple processing and writes the results into `.json` files in `/render`. The Javascript/HTML/CSS UI codebase is all common and all lives in `/render`.

### Ubuntu
ulogme has three main parts: 

1. Recording scripts `keyfreq.sh` and `logactivewin.sh`. You probably won't touch these.
2. Webserver: `ulogme_serve.py` which wraps Python's `SimpleHTTPServer` and does some basic communication with the UI. For example, the UI can ask the server to write a note to a log file, or for a refresh.
3. The UI. Majority of the codebase is here, reading the `.json` files in `/render` and creating the visualizations. There are several common `.js` files, and crucially the `index.html` and `overview.html` files. I expect that most people might be able to contribute here to add features / cleanup / bugfix.

### OSX code
Things get a little ugly in OSX if you want to change anything with recording the log files because you have to recompile these portions any time you make any changes. It's ugly and it had to be done. However, if you're only interested in hacking with the UI, just change Javascript in `render` and no recompile is necessary, naturally.

## License
MIT
