#!/usr/bin/env python3

import os
import pprint
import json
import sys
import sqlite3

from onepassword import crypt_util
from onepassword.keychain import _AbstractKeychain

class SQLKeychain(_AbstractKeychain):
	def _open(self, path=None):
		"""connect to DB"""
		if not path:
			path = ':memory:'
		conn = sqlite3.connect(path)
		conn.row_factory = sqlite3.Row
		self.conn = conn
	def item(self, itemID):
		"""return item info by ID."""
		item = {}
		for i in self.items:
			if i['id'] == itemID:
				item = i
				break
		with self.conn:
			q = "select i.key_data, d.data from item_details d, items i where i.id = d.item_id and i.id=?;"
			r = self.conn.execute(q, (itemID,))
			r = r.fetchone()
			r = json.loads(self.decrypt_data(r['key_data'], r['data']))
			item['details'] = r
		return item
	def _profile(self, profileName='default'):
		"""return master salt"""
		with self.conn:
			r = self.conn.execute("select id,salt,iterations,master_key_data,overview_key_data from profiles where profile_name=?", (profileName,))
			r = r.fetchone()
			self.profile = r
	def _categories(self):
		"""return a list of every category"""
		with self.conn:
			q = "select id, singular_name from categories where profile_id=?"
			r = self.conn.execute(q, (self.profile['id'],))
			self.categories = []
			for c in r:
				self.categories.append((c['id'], c['singular_name']))
	def _loadKeys(self, password):
		super_master_key, super_hmac_key = crypt_util.opdata1_derive_keys(
			password,
			self.profile['salt'],
			self.profile['iterations']
		)
		#clean up the master password since we no longer need it.
		del password
		self.master_key, self.master_hmac = crypt_util.opdata1_decrypt_master_key(
			self.profile['master_key_data'],
			super_master_key,
			super_hmac_key
			)
		self.overview_key, self.overview_hmac = crypt_util.opdata1_decrypt_master_key(
			self.profile['overview_key_data'],
			super_master_key,
			super_hmac_key
		)
	def _loadItems(self, filter=None):
		"""load item overview data
		we can apply a 'filter', so far we only support 'sudolikeaboss'
		which will only load overview items that are sudolikeaboss items.
		"""
		q = """select distinct i.id, c.singular_name as category, i.overview_data from items i, categories c where c.id = i.category_id and not i.trashed order by i.id;"""
		self.items = []
		with self.conn:
			r = self.conn.execute(q)
			for i in r:
				o = self.decrypt_overview(i['overview_data'])
				#u = self.decrypt_overview(i['url_data'])
				o = json.loads(o)
				#u = json.loads(u)
				item = {
					'id': i['id'],
					#'urls': u,
				}
				for k,v in o.items():
					item[k] = v
				if filter == 'sudolikeaboss':
					if 'url' in item:
						if item['url'] == 'sudolikeaboss://local':
							self.items.append(item)
				else:
					self.items.append(item)
		#print(len(self.items))
	def unlock(self, password, filter=None, profileName='default'):
		"""unlock the master keychain"""
		self._profile(profileName)
		self._loadKeys(password)
		#delete password since we no longer need it.
		del password
		self._categories()
		self._loadItems(filter)
		return True
	def decrypt_overview(self, blob):
		return crypt_util.opdata1_decrypt_item(
			blob,
			self.overview_key,
			self.overview_hmac
		)

	def decrypt_data(self, key_blob, data_blob):
		key, hmac = crypt_util.opdata1_decrypt_key( key_blob, self.master_key, self.master_hmac)
		return crypt_util.opdata1_decrypt_item(data_blob, key, hmac)

def main(args):
	"""main code"""
	path=os.path.expanduser(u'~/src/1p/OnePassword.sqlite')
	print("opening:{}".format(path))
	k = SQLKeychain(path)
	k.unlock('test', filter='sudolikeaboss')
	pprint.pprint(k.items)
	pprint.pprint(k.item(1))
	return 0

if __name__ == '__main__':
	sys.exit(main(sys.argv))