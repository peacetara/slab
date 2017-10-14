#!/usr/local/bin/python3
"""sudolikeaboss crappy replacement.
"""
import getpass
import getopt
import os
import pprint
import sys
import subprocess
import tempfile
import slab.slablib

SLABSCRIPT="""
	tell app "System Events"
		Activate

		set SlabList to {}
		set Answer to (choose from list SlabList with title "sudolikeaboss")

		if Answer is false then
			error number -128 (* user cancelled *)
		else
			set Answer to Answer's item 1 (* extract choice from list *)
		end if
	end tell
	tell app "iTerm2"
		Activate
		return Answer
	end tell
"""

def choice(choices):
	"""give user a choice of items. return selected item"""
	fd = tempfile.NamedTemporaryFile(delete=False)
	#choices = ['a','b','c']
	s = '{ "' + '","'.join(choices) + '" }'
	fd.write(SLABSCRIPT.format(s).encode('utf-8'))
	name = fd.name
	#print("fname:%s" % name)
	fd.close()

	try:
		out = subprocess.check_output(['/usr/bin/osascript',name],universal_newlines=True)
		#str(out).strip().replace('\n','')
		out = out.rstrip()
		#print("out:%s" % out)
	except:
		sys.exit()

	os.unlink(name)
	return out

def getPWPath():
	"""get PW path"""
	path = os.getenv("SLAB_PWPATH","~/.config/.slab_password")
	path=os.path.expanduser(path)
	return path

def pwentry():
	"""create a secure file for the master password keys.
	TODO: update this to work with keychain.
	"""
	pwpath = getPWPath()
	try:
		opts, args = getopt.getopt(sys.argv[1:], "h:v", ["help", "delete"])
	except getopt.GetoptError as err:
		print(err)
		sys.exit(2)
	if 'delete' in args:
		os.unlink(pwpath)
		sys.exit(0)
	if os.path.exists(pwpath):
		os.unlink(pwpath)
	fd = open(pwpath, mode='w')
	os.chmod(pwpath, 33024)
	print("This will save your MasterPassword in as secure a file as we can make.")
	pwd = getpass.getpass()
	fd.write(pwd)

def main(args=None):
	"""main code"""
	path=os.getenv("SLAB_PATH","~/Library/Application Support/1Password 4/Data/OnePassword.sqlite")
	path=os.path.expanduser(path)

	#print("opening:{}".format(path))
	k = slab.slablib.SQLKeychain(path)

	password=os.getenv("SLAB_PASSWORD", None)
	if password:
		print("You used the SLAB_PASSWORD environment variable... Please consider alternatives!")

	if not password:
		password = subprocess.check_output(['/usr/bin/security','find-generic-password','-a','slab','-w'],universal_newlines=True).rstrip()

	if not password:
		pwpath = getPWPath()
		if os.path.exists(pwpath):
			mode = os.stat(pwpath).st_mode

			assert mode in (33024,33152) ,"SLAB_PWPATH file must be chmod 0400 or 0600"

			password = open(pwpath).read()
			if '\n' in password:
				password = password.rstrip()
	try:
		k.unlock(password, filter='sudolikeaboss')
		del password
	except:
		print("The password supplied does not unlock 1Password. Aborting.")
		sys.exit(3)

	#pprint.pprint(k.items)
	choices=[]
	if len(k.items) == 1:
		c = k.items[0]['title']
	else:
		for i in k.items:
			choices.append(i['title'])

		# use applescript to get a choice.
		c = choice(choices)

	# go through all the sudolikeaboss items and print the password when match found.
	for i in k.items:
		if i['title'] == c:
			#pprint.pprint(k.item(i['id']))
			for f in k.item(i['id'])['details']['fields']:
				if f['designation'] == 'password':
					print(f['value'])
					sys.stdout.flush()

	#pprint.pprint(k.item(1421))
	return 0

if __name__ == '__main__':
	sys.exit(main(sys.argv))