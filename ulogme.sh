#!/bin/bash

if [ "$(uname)" == "Darwin" ]; then
  # This is a Mac
  ./osx/run_ulogme_osx.sh
else
  # Assume Linux
  sudo echo -n ""
  sudo ./keyfreq.sh &
  ./logactivewin.sh
fi
