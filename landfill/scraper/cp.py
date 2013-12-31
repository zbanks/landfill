from cpbot import CPBot
import time

def get_torrent(cesspool,url):
	cp=CPBot(cesspool)
	uid=cp.assert_success(cp.doCommand({"cmd":"add","args":{"type":"torrent","args":{"url":url}}}))['uid']

	def remove():
		print {"cmd":"rm","args":{"uid":uid}}
		cp.assert_success(cp.doCommand({"cmd":"rm","args":{"uid":uid}}))

	while True:
		d=dict([(dl['uid'],dl) for dl in cp.assert_success(cp.doCommand({"cmd":"pool"}))])
		if uid not in d:
			raise Exception('Download was removed.')
		dl=d[uid]
		if dl['status']=='error':
			remove()
			raise Exception('Encountered an error while downloading: {0}'.format(dl['error']))
		if dl['status']=='complete':
			break
		time.sleep(3)

	return uid

if __name__=='__main__':
	get_torrent('http://localhost:9500/cmd','magnet:?xt=urn:btih:0d067e6a15a75fa1d562a78c3409d20907488fcb&dn=Die+Hard+%5B1988%5D+DvdRip+%5BEng%5D+-+Thizz&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Ftracker.publicbt.com%3A80&tr=udp%3A%2F%2Ftracker.istole.it%3A6969&tr=udp%3A%2F%2Ftracker.ccc.de%3A80&tr=udp%3A%2F%2Fopen.demonii.com%3A1337')
