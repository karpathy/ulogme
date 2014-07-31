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
  // get returns a Promise
  var hackurl = url + '?sigh=' + Math.floor(100000*Math.random());
  return get(hackurl).then(JSON.parse).catch(function(err) {
    console.log("getJSON failed for", url, err);
    throw err;
  });
}
