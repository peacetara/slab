`slab` is a [sudolikeaboss](https://github.com/ravenac95/sudolikeaboss) replacement; and sudolikeaboss is a 1Password utility to interact with iTerm2 and type in your (speacially defined) Login passwords in your Terminal session for you.

This code talks directly to your 1Password local vault (SQLite data file) and works with 1Password > 6.8.0. It has been tested up to version 6.8.4 so far, but it should be pretty stable to new versions. Please do file an "Issue" if you run into any problems.

Currently only the python version works, [see the README](https://github.com/peacetara/slab/blob/master/src/python/README.md) for more.

I plan to eventually re-write this in Rust, or maybe Go, but I'm still learning those languages, and I needed a replacement *NOW*. Re-writes accepted as pull-requests! :)
