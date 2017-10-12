#!/usr/local/bin/python3
"""sudolikeaboss crappy replacement.
"""
import os
import pprint
import sys
import subprocess
import tempfile


import slab.slablib

SLABSCRIPT="""
    set SlabList to {}
	tell me to Activate

    set Answer to choose from list SlabList with title "sudolikeaboss"


    if Answer is false then
        error number -128 (* user cancelled *)
    else
        set Answer to Answer's item 1 (* extract choice from list *)
    end if

    return Answer
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

def main(args=None):
	"""main code"""
	path=os.getenv("SLAB_PATH","~/Library/Application Support/1Password 4/Data/OnePassword.sqlite")
	path=os.path.expanduser(path)
	#print("opening:{}".format(path))
	k = slab.slablib.SQLKeychain(path)
	password=os.getenv("SLAB_PASSWORD", None)
	if not password:
		password = subprocess.check_output(['/usr/bin/security','find-generic-password','-a','slab','-w'],universal_newlines=True).rstrip()
	if not password:
		pwpath = os.getenv("SLAB_PWPATH","~/.config/.slab_password")
		pwpath = os.path.expanduser(pwpath)
		if os.path.exists(pwpath):
			mode = os.stat(pwpath).st_mode
			assert mode in (33024,33152) ,"SLAB_PWPATH file must be chmod 0400 or 0600"
			password = open(pwpath).read()
			if '\n' in password:
				password = password.rstrip()

	k.unlock(password, filter='sudolikeaboss')
	#pprint.pprint(k.items)
	choices=[]
	if len(k.items) == 1:
		c = k.items[0]['title']
	else:
		for i in k.items:
			choices.append(i['title'])
		#print("choices:%s" % pprint.pformat(choices))
		#c = ''
		# use applescript to get a choice.
		c = choice(choices)
		print(">>",c)

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