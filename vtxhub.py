from requests import *
import json,random,time,re,sys

abc = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
acc = []
def vtxhub(mail,password):
	fname = mail.split("@")[0][:6] #"".join([random.choice(abc) for _ in range(10)])
	lname = mail.split("@")[0][6:] #"".join([random.choice(abc) for _ in range(10)])
	data = {
	    "fname":fname,
	    "lname":lname,
	    "email": mail,
	    "captcha": "03AGdBq26Bt2Zk-wE93Qt6fGnpAKzrUthsVG_FoQ1h9RUceL8j4RUXY8sjRiYTDbL_8xUlw9FvgTBuDA0VtXUMqH6dGx9z50jQZ2w-nk4ilF_xPWShslt1g07YDvmXo9p_hfVRA1uM1pNDPxENJ0MkM_zzcxbAKcAYqt39bUhScD35I_P33ZE76uYtcK56xu7wGrG0k2RMYRC4pv9siwFaVxxLcmV34Eg9FYjO3bhdOo8ELfvjwPV82gfj0ANzyFRsPPKwdbbh1oiaBTbS4YbBGDJETk9lFpDqyeRLNraErurPAi9sBx9EsEjNU6xZmgmvoZhikfzaiLssMCiktxvZUyZCLSFOElXKBr-yM_VWNJhOAk7Iucdrno3iw65QptF54k2OQWSzORwTvfzEz4Jtu4pmdd03HxRI0_cTrcqxtUp-vdzHx3NKH65j-UAs2scaep0W71Si5pKkWERz1tUWUAO0MuCUlwud8rELdwpbuW0ASSs9fbJnMRI"
	}
	print(f"""Create new account with random credentials
First Name   : {fname}
Last Name    : {lname}
Email        : {mail}
Passsword    : {password}""")
	x = post("https://api.vtxhub.com/v1/user",data=data).json()
	if not x["error"]:
		#print(f"Success send email verification to {mail}")
		res = {"success":True,"error":False,"data":x}
		code = x["data"]["user"]["code"]
		handle = x["data"]["user"]["handle"]
		time.sleep(5)
		success = setpass(code,handle,password)
		if success:
			acc.append({"email":mail,"password":password})
	else:
		res = {"success":False,"error":True,"data":x}
		print("Status       : Failed")
	return res
def setpass(code,handle,password):
	data = {
	"password": password,
	"handle": handle,
	"code": code
	}
	resp = post("https://api.vtxhub.com/v1/oauth/grant/basic",data=data)
	try:
		resp = resp.json()
		print("Status       : Success")
		print("*"*40)
		print()
		success = True
	except:
		resp = resp.text
		print("Status       : Failed")
		print(f"Response    : {resp}")
		print("*"*40)
		print()
		success = False
	return success
def getemail():
	print("Get new email..")
	r = get("https://tempail.com/")
	mail = re.search(r"data\-clipboard\-text\=\"(.*?)\"",r.text).group(1)
	return mail

if __name__ == '__main__':
	print("====== \033[96mvtxhub.com\033[0m Auto Create Account ======\n")
	if len(sys.argv) > 1:
		#print(sys.argv)
		if len(sys.argv) == 3:
			for _ in range(int(sys.argv[2])):
				vtxhub(getemail(),sys.argv[1])
		elif len(sys.argv) == 2:
			vtxhub(getemail(),sys.argv[1])
		else:
			print("Use: python vtxhub.py <set passwd> <amount>")
		if acc:
			import json
			json.dump({"result":acc},open("results.json","w"),indent=2)
			print("Results saved to 'results.json'")
	else:
		print("Use: python vtxhub.py <set passwd> <amount>")
