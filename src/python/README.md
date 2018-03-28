This is a very basic and maybe not secure way to replace sudolikeaboss for 1Password > 6.8.0

All the hard bits are done by the `onepasswordpy` library, the source for that is included directly here. Please see `onepassword/LICENSE.txt` for the license.

This replacement for `sudolikeaboss` talks directly to the 1Password SQLITE data file.
It only ever reads from the SQLITE database, and it can run side-by-side with a running unlocked copy of 1Password.


### INSTALL

```
  $ sudo python3 setup.py install
```

if you are using OpsnSSL on a newer macOS system where it has been deperecated in favor of the built-in SSL libraries; you can use the following invocation after a `brew install openssl` (assuming you have not installed Homebrew's OpenSSL already):

```
  $ sudo -s  
  # LDFLAGS=-L/usr/local/opt/openssl/lib CPPFLAGS=-I/usr/local/opt/openssl/include python3 setup.py install
```

### SETUP

  1. Firstly, ensure your 1Password sqlite file is in:

     ```
     ~/Library/Application\ Support/1Password\ 4/Data/
     ```

     and is named `OnePassword.sqlite`
  
     If it isn't you will need to set an environment variable `SLAB_PATH` to point to your 1Password `sqlite` data file.

  2. This version of `slab` needs your 1Password Master Password.
  
     You can make it available in any of the following ways:
  
     1. Use MacOS's Keychain Access App:
  
        * Creating the SLAB Entry in the MacOS Keychain:

           ```
           $ security add-generic-password -a slab -s slab-password -j "1P SLAB Access" -T /usr/bin/security -w
           ```

           If you don't mind your password showing up in your shell `history` you could add it after the `-w` parameter; else the program will prompt you for it.

        * Update the password in the Keychain App:

           ```
           $ security add-generic-password -a slab -s slab-password -U -w
           ```

     2. you could put it in a file:

        ```
        $ echo "MYMASTERPASSWORD" > ~/.config/.slab_password
        $ chmod 0400 ~/.config/.slab_password
        ```

     It ***must*** be `chmod` either 0400 (owner read *only*) or 0600 (owner read/write *only*), or this code will complain bitterly.

  3. Configure a keybinding to run coprocess and point it at this binary; something like binding `⌘\` to `/usr/local/bin/slab`.

### HOW it works

  This code opens the SQLite data file, filters out only `sudolikeaboss` entries, builds a list of titles and then asks a chooser to show you a list of titles to choose from.
  
  The Chooser never sees your passwords, or interacts, directly with 1Password.

  If you have choose installed (https://github.com/sdegutis/choose) @ /usr/local/bin it will use that instead of Applescript.
  
  After selecting an item from the list, this code then decrypts the entry and outputs the password.

  This code *could* do (very) nasty things and decrypt every single secret, since it knows your master password. I promise it doesn't, but it ***could***. See `src/python/slab/main.py` for what it actually does.
