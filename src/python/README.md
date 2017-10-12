This is a very basic and maybe not secure way to replace sudolikeaboss for 1Password > 6.8.0

All the hard bits are done by the onepasswordpy library, the source for that is included directly here.  see onepassword/LICENSE.txt for the license.

This replacement for sudolikeaboss talks directly to the 1Password SQLITE datafile.
it only ever does reads from the SQLITE database, and it can run side-by-side with a running unlocked copy of 1Password.

I plan to eventually re-write this in Rust or maybe Go, but I'm still learning those languages, and I wanted a replacement *NOW*. :)

INSTALL:
	python3 setup.py install

SETUP:
	ensure your 1Password sqlite file is in:
	~/Library/Application\ Support/1Password\ 4/Data/
	and named OnePassword.sqlite
	if it isn't you will need to set an env variable SLAB_PATH to point to your 1password sqlite data file.

	This slab needs your 1Password Master Password.
	You can put it in the env SLAB_PASSWORD but that would be stupid.
	the next best thing is to put it in a file
	something like:
	echo "MYMASTERPASSWORD" > ~/.config/.slab_password
	chmod 0400 ~/.config/.slab_password
	if you put it in a different place, then export SLAB_PWPATH to point to it.
	it *MUST* be chmod 0400 or 0600, or this code will hate you, loudly.

	Configure a keybinding to run coprocess and point it at this binary
	something like: /usr/local/bin/slab

