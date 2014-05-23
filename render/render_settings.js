// various settings for the rendering, to be set by user

/*
This function takes a raw window title w as string
and outputs a more compact code, to be treated as a single
unit during rendering. Every single possibility output from
this function will have its own row and its own analysis,
so it is recommended that only few possible outputs exist,
and use of MISC category as shown in example is encouraged.
*/
function mapwin(w) {
  wbefore = w;
  if(w.indexOf("Gmail")>-1) w = "Gmail";
  if(w.indexOf("Inotebook")>-1) w = "INotebook";
  if(w.indexOf("Google Chrome")>-1) w = "Google Chrome";
  if(w.indexOf("karpathy@")>-1) w = "Terminal";
  if(w.indexOf("MATLAB")>-1) w = "Matlab";
  if(w.indexOf("Figure")>-1) w = "Matlab";
  if(w.indexOf("Sublime Text")>-1) w = "Sublime Text 2";
  if(w.indexOf("TeXworks")>-1) w = "Latex";
  if(w === '__LOCKEDSCREEN') w = "Locked Screen";
  // none of the rules matched? fold into MISC
  if(w === wbefore) {
    console.log('folding into MISC: ' + w);
    w = 'MISC'; // none of the rules applied
  }
  return w;
}

// list of titles that classify as "hacking", or being productive in general
// the main goal of the day is to get a lot of focused sessions of hacking
// done throughout the day. Windows that arent in this list do not
// classify as hacking, and they break "streaks" (events of focused hacking)
// the implementation is currently quite hacky, experimental and contains 
// many magic numbers.
var hacking_titles = ["Inotebook", "Terminal", "Matlab", "Sublime Text 2", "Latex"];
var draw_hacking = false; // by default turning this off

// draw notes row?
var draw_notes = true;

// experimental coffee levels indicator :)
// looks for notes that mention coffee and shows 
// levels of coffee in body over time
var draw_coffee = false;
