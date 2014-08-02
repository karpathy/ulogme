// Common utility functions
// TODO: Expand this out, make everything more modular and cleaner

// builds a dictionary of string -> color, in HSL format
function colorHashStrings(arr) {
  var color_hash = {};
  for(var i=0,N=arr.length;i<N;i++) {
    var title = arr[i];
    color_hash[title] = "hsl(" + Math.floor((i+0.5)/N * 360) + ",100%,60%)";
  }
  return color_hash;
}

// utility that looks at the URL of current page and sets QueryString
var QueryString = function () {
  var query_string = {};
  var query = window.location.search.substring(1);
  var vars = query.split("&");
  for (var i=0;i<vars.length;i++) {
    var pair = vars[i].split("=");
      // If first entry with this name
    if (typeof query_string[pair[0]] === "undefined") {
      query_string[pair[0]] = pair[1];
      // If second entry with this name
    } else if (typeof query_string[pair[0]] === "string") {
      var arr = [ query_string[pair[0]], pair[1] ];
      query_string[pair[0]] = arr;
      // If third or later entry with this name
    } else {
      query_string[pair[0]].push(pair[1]);
    }
  } 
    return query_string;
}();

// Javascript promises utilites. I like promises <3
function get(url) {
  return new Promise(function(resolve, reject) {
    var req = new XMLHttpRequest();
    req.open('GET', url);
    req.onload = function() {
      if (req.status == 200) {
        resolve(req.response);
      }
      else {
        reject(Error(req.statusText));
      }
    };
    req.onerror = function() {
      reject(Error("Network Error"));
    };
    req.send();
  });
}

function getJSON(url) {
  // get returns a Promise
  return get(url).then(JSON.parse).catch(function(err) {
    console.log("getJSON failed for", url, err);
    throw err;
  });
}

function getJSON_CACHEHACK(url) {
  // Sometimes caching can refuse to retrieve a JSON object if
  // it has been updated. Appending a random number is a hacky
  // way of preventing this caching and ensures that the newest
  // version is retrieved
  var hackurl = url + '?sigh=' + Math.floor(100000*Math.random());
  return get(hackurl).then(JSON.parse).catch(function(err) {
    console.log("getJSON failed for", url, err);
    throw err;
  });
}

// takes window and key events (ew and ek) and assigns key events
// to windows. Returns the total number of keys pressed
// in every window. Uses a merge-sort-like strategy
function computeKeyStats(ew, ek) {
  var key_stats = {};
  var i = 0;
  var j = 0;
  var ewn = ew.length;
  var ekn = ek.length;
  var cur_window = '';
  
  // merge sort, basically
  while(i<ewn && j<ekn) {
    var popw; // pop window event?
    if(i>=ewn) { popw = false; }
    else if(j>=ekn) { popw = true; }
    else {
      var tw = ew[i].t;
      var tk = ek[j].t;
      popw = tw < tk;
    }
    if(popw) { // process new window event
      cur_window = ew[i].m;
      i++;
    } else { // process key event
      if(cur_window !== '') {
        var fhere = ek[j].s;
        if(key_stats.hasOwnProperty(cur_window)) {
          key_stats[cur_window].f += fhere;
          key_stats[cur_window].n ++;
        } else {
          key_stats[cur_window] = {'f':fhere, 'n':1};
        }
      }
      j++;
    }
  }
  return key_stats;
}

// same idea as computeKeyStats, but outputs "hacking" events, 
// which are contiguous areas of high keystroke activity. That means
// that the person is in hacking mode! :)
function computeHackingStats(ew, ek, hacking_titles) {

  var hacking_stats = {};
  var hacking_events = [];

  var i = 0;
  var j = 0;
  var ewn = ew.length;
  var ekn = ek.length;
  var cur_window = '';
  var hacking_title = false;
  var hacking_counter = 0;
  var hacking_reset_counter = 0;
  var hacking_now = false;
  var hacking_start = -1;
  var hacking_f_accum = 0;

  var total_hacking_time = 0;
  var total_hacking_keys = 0;

  var notHacking = function(t) { // helper function
    hacking_reset_counter++;
    if(hacking_reset_counter > 10) {
      if(hacking_now) {
        // we were hacking and now it ended. record the session
        var h = {};
        h.t0 = hacking_start;
        h.t1 = t;
        h.dt = h.t1 - h.t0; // convenience
        h.ftotal = hacking_f_accum;
        h.intensity = hacking_f_accum / h.dt; // key strokes per second

        total_hacking_time += h.dt;
        total_hacking_keys += h.ftotal;

        hacking_events.push(h);
      }
      hacking_now = false; // and reset tracking vars
      hacking_counter = 0;
      hacking_reset_counter = 0;
      hacking_f_accum = 0;
    }
  }

  // a bit of code duplication here... :( hmmm
  while(i<ewn && j<ekn) {
    var popw;
    if(i>=ewn) { popw = false; }
    else if(j>=ekn) { popw = true; }
    else {
      var tw = ew[i].t;
      var tk = ek[j].t;
      popw = tw < tk;
    }
    if(popw) { // process new window event
      cur_window = ew[i].m;
      hacking_title = hacking_titles.indexOf(cur_window) > -1;
      i++;
    } else {

      // process key event
      if(cur_window !== '') {
        var fhere = ek[j].s;
        if(hacking_title) {
          // current active title is a hacking title. accumulate streak
          // magic numbers alert :)
          if(fhere < 3) { 
            // there are less than 3 keystrokes in last 9 seconds...
            hacking_reset_counter++;
            if(hacking_reset_counter > 10) {
              // way too much time has gone by with no key events. 
              // Person is sleeping. This aint hacking!
              notHacking(tk); 
            }
          } else {
            // there are more than 3 keystrokes in last 9 seconds
            hacking_reset_counter = Math.max(0, hacking_reset_counter - 1);
            hacking_counter += 1;
            if(hacking_counter > 15) {
              // we've built up quite a bit of hacking_counter in this
              // session of relatively more than 3 keystrokes / 9 seconds
              // Lets consider ourselves hacking.
              if(!hacking_now) {
                // we started hacking. record time
                hacking_start = tk;
              }
              hacking_now = true;
            }
            if(hacking_now) {
              hacking_f_accum += fhere;
            }
          }
        } else {
          // current active title is not a hacking title.
          // Person is probably slacking on Facebook or something.
          notHacking(tk);
        }
      }
      j++;
    }
  }

  // store these for convenience
  hacking_stats.total_hacking_keys = total_hacking_keys;
  hacking_stats.total_hacking_time = total_hacking_time;
  hacking_stats.events = hacking_events;
  return hacking_stats;
}