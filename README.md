# WarGod

WarGod is a "river of news"-style RSS aggregator that generate static html
pages. It is intended to be executed periodically by crontab.

# Usage

Create the file <code>~/.config/wargod/rss</code> and put one RSS url by line
in it. Every line with a <code>#</code> as first character will be ignored then
just simply run the command "wargod", this will create a file name
"output.html" in your home directory.

# Inspiration/credit

WarGod can be describe as minimalist version of
[rawdog](http://offog.org/code/rawdog.html). In fact, for the moment the only
improvement in comparison to rawdog is that WarGod, when it discovered a new
RSS, will only add the newest items of it instead of all of it. The other
improvement for me is that it's less than 100 lines of code (where rawdog is
around 1500 lines of code). I intent to make it way more easy to have severals
output files with WarGod than it is the case with rawdog (it's the reason of
this project in fact, I want to do this in another way than you do this with
rawdog right now).
