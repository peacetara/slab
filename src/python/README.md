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
	the next best thing is to put it in a file:
		$ slabpw
	and it will prompt you for the masterpassword and save it to as secure a file as we can make it.
	It's recommended that when you no longer need to use slab, to delete the file:
		$ slabpw delete
	and we will erase the file for you.	
		Eventually slabpw will do something like gpg-agent, and not store in a file.
	Configure a keybinding to run coprocess and point it at this binary
	something like: /usr/local/bin/slab

HOW it works:
	This code opens the SQLite data file, filters out only sudolikeaboss entries, builds a list of titles and asks applescript to show you a list of titles to choose from (applescript never sees or interacts with 1password).  After selecting a list, this code then decrypts the 1 entry and outputs the password.

	This code *could* do nasty things and decrypt every single secret, since it knows your master password, but I promise it doesn't :P  See src/python/slab/main.py for what it actually does.