from requests import Session
from threading import Thread as td
import vtxhub
import time,re

_inbox = []
def timer(tread):
	for i in range(10000):
		if tread.is_alive():
			print(f"\rWaiting.. ({i+1}s)",end="",flush=True)
			time.sleep(1)
		else:
			break
def update(ses,control_data):
	while True:
		x = ses.post("https://tempail.com/en/api/kontrol/",data=control_data)
		code = x.status_code
		if code == 200:
			_inbox.append(re.search(r"a\ href\=\"(.*?)\"",x.text).group(1))
			subject = re.findall(r"div.*?baslik\"\>(.*?)\<",x.text)[-1]
			print(f"\nNew Inbox: {subject}")
			break
		time.sleep(10)
def tempmail():
	ses = Session()
	ses.headers = {"user-agent":"Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Mobile Safari/537.36"}
	print("Get new email..")
	r = ses.get("https://tempail.com/")
	mail = re.search(r"data\-clipboard\-text\=\"(.*?)\"",r.text).group(1)

	# data
	tarih = re.search(r"tarih\=\"(\d+)\"",r.text).group(1)
	oturum = r.cookies.get("oturum")

	control_data = {
		"geri_don":"https://tempail.com/en/",
		"tarih":tarih,
		"oturum":oturum
		}
	print(f"New mail: {mail}")
	print("Registering new account for Vortex with new email..")
	verification_has_sent = vtxhub.vtxhub(mail)
	if verification_has_sent["success"]:
		inbox = []
		t = td(target=update,args=(ses,control_data))
		t.start()
		while t.is_alive():
			timer(t)
		print("Get message..")
		#msg_no = inbox[0].split("_")[-1].replace("/","")
		#msg_url = "https://tempail.com/en/api/icerik/?oturum={oturum}&mail_no={msg_no}"
		msg = ses.get(_inbox[0])
		msg_url = re.search(r"iframe\ src\=\"(.*?\/en/api.*?)\"",msg.text).group(1)
		print("Reading message & get set password URL..")
		msg = ses.get(msg_url)
		print(msg.text)
		pass_url = [x for x in re.findall(r"href\=\"(.*?)\"",msg.text) if "bitvisory" in x and x.endswith("/")]
		print(pass_url)
		#msg_content = re.search(r"dir\=\"auto\"\>(.*?)\<",msg.text).group(1)
		#print("Message: ",msg_content)
	else:
		print("Failed creating new Vortex account.")
		print(verification_has_sent["error"])

tempmail()
