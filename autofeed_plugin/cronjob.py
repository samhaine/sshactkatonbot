from datetime import date, timedelta
import requests
import sqlite3

conn = sqlite3.connect('autofeed.sqlite')
cur = conn.cursor()

def get_todays_posts():
	date_dict = {'today': date.today(), 'approved': False}
	cur.execute('select * from autofeed_plugin_approver join autofeed_plugin_linkpost where autofeed_plugin_linkpost.date=:today and autofeed_plugin_approver.approved=:approved', date_dict)
	return cur.fetchall()

if __name__ == "__main__":
	posts = get_todays_posts()
	approvers = {}
	for row in posts:
		user = row['name']
		if approvers[user]:
			approvers[user].append((row['link'], row['autofeed_plugin_linkpost.id']))
		else:
			approvers[user] = [(row['link'], row['autofeed_plugin_linkpost.id'])]

	for approver, links in approvers.itemize():
		msg = compose_msg(links)
		request.post('localhost/sendMessage', {'users': [approver], 'msg': msg})

def compose_msg(links):
	msg = "Do you approve the following links?<br>"
	for link, link_id in links:
		msg += str(link_id) + " " + link + "<br>"

	return msg