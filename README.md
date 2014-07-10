
# ulogme


> ### How productive were you today? How much code have you written? Where did your time go?

Keep track of your productivity throughout the day: visualize your active window titles and the number of keystrokes in beautiful, daily HTML timelines. Current features:

- Records your active window title throughout the day
- Records the frequency of key presses throughout the day
- Everything runs completely locally: none of your data is uploaded anywhere

The project currently **only works on Ubuntu**.

## Demo

See a [live demo here.](http://cs.stanford.edu/people/karpathy/ulogme)

(this is now a little bit of an old demo, but still gets the main idea across)

## Getting Started

**To start recording:**

1. Clone the repository: `git clone https://github.com/karpathy/ulogme.git`
2. `cd` inside and run `./ulogme.sh` (note: this will ask you for sudo authentication which is required for `showkey` command). This will launch two scripts for listening to your keyboard activity and active window and log the activity into log files in the `logs` folder. Only the frequency of keystrokes is recorded. Every log file is very simply just the unix time stamp followed by data, one per line.

**Note**, you may need to get some packages on Ubuntu (such as `xdotool` and `wmctrl`). You can simply `sudo apt-get install` both of them. To view the results, proceed as follows:

**To view results:**

1. Run `python export_events.py`. This will write JSON files into `render/` directory. The `index.html` file inside will later read these to show the visualization
2. Copy `render/render_settings_example.js` to `render/render_settings.js` and modify the title mappings according to your own preferences (the input to the `mapwin` function is raw window title. The output should be your desired window categories). As an example, one rule specifies that if a window title contains "Google Chrome", it should simply all be grouped into category called "Google Chrome". Follow the provided example. The `display_groups` variable dictates which mapped titles will appear together in every row in the visualization.
3. Start the web server viewer: `python ulogme_serve.py`, and go to to the provided address )for example `http://localhost:8123`).

### User Interface

The user interface can switch between a single day view and an overview view. The interface also has a refresh button on top right which recomputes and refreshes only the current view.

To recompute all days, go to the Overview page and hit refresh there.

### Note taking

You can record notes by clicking any event in the timeline. 

This can be useful as a diary, but also if you'd like to later correlate notes with your productivity or other things later. For example, I tinkered around with recording whenever I get coffee and then correlating my productivity with the my caffeine levels. Or the impact that meetings and other interruptions have on my productivity. Or the amount of sleep I get that day, etc.

## License
MIT
