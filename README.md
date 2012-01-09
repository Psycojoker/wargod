# WarGod

WarGod is a "river of news"-style RSS aggregator that generate static html
pages. It is intended to be executed periodically by crontab.

# Usage

All your urls are to be put in the file<code>~/.config/wargod/rss</code>. The syntaxe is very simple:

* one rss per line
* every line that have <code>#</code> as first non-blank character is ignored
* new to each RSS you can put an infinite quantity of file name, those will be the output files for this RSS
* if no file name is specified then "output.html" will be used
* if you add the keyword "extend" next to a feed (with the filename(s)) the readability algorithms will be used on the link of each items of this feed to get the content of the item instead of using what is in the <description> tag. This is usefull for RSS that only provide a part of the article.

Once this is done, run the command "wargod" (you can see the options with
--help), this will create output html files for your RSS.

I recommend you to put this command in your crontab.

# Inspiration/credit

WarGod can be describe as minimalist version of
[rawdog](http://offog.org/code/rawdog.html). I've started this project because
the way to output RSS in different files is unfunny in rawdog and that it's
code isn't structured at all in a way that would allow this easily.

The differences with rawdog are:

* way younger project with a lot less features
* in consequence a way smaller code base (around 100 lines vs around 1500 lines)
* when you add a new RSS, only the newest item is added to the output so you don't overflow it each time you add a new RSS
* very easy way to output a RSS in several files
