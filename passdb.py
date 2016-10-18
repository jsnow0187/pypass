from getpass import getpass
import os
from Crypto.Cipher import AES
import base64 
##Adds username and password to a list
##that is entered into a dictionary and written to file
def addDb(service, uname, pw):
	##encrypts the information entered from user
	salt, cipher = crypt(pw)
	
	##encodes the encrypted information to be written to file
	salt=str(base64.b64encode(salt))
	cipher=str(base64.b64encode(cipher))
	
	#adds user information to a list
	newCred = [uname, cipher, salt]
	
	#adds list to a dict
	passdb[service]=newCred
	
	#write data to file
	f=open('passdb.txt', 'a')
	f.write(service+','+uname+','+cipher+','+salt+'\n')
	f.close()
	
	return(passdb)
	
	
##encrypt function
def crypt(pw):
	#prompts user for the master key used to decrypt
	master = getpass('Enter your master key: ')
	##check if the master is 16bytes 
	if len(master) != 16:
		##either pads the key to 16,32 bytes depending on the size
		if len(master) < 16:
			master = master.zfill(16)
		elif len(master) > 16:
			master = master.zfill(32)
	##check if password is 16bytes
	if len(pw) != 16:
		##pads password to 16 or 32 bytes
		if len(pw) < 16:
			pw = pw.zfill(16)
		elif len(pw) > 16:
			if  len(pw) < 32:
				pw = pw.zfill(32)
			elif len(pw) > 32:
				pw = pw.zfill(64)
	##create the salt
	salt = os.urandom(16)
	
	#create the cipher
	cipher = AES.new(master, AES.MODE_CBC, salt).encrypt(pw)
	#cipher = encryption_packet.encrypt(pw)
	
	return(salt, cipher)
	
	
	
##decrypt function	
def decrypt(salt, cipher):
	##prompt user for the master key
	master = getpass('What is the master key: ')
	
	##pad master to a multiple of 16
	if len(master) != 16:
		if len(master) < 16:
			master = master.zfill(16)
		elif len(master) > 16:
			master = master.zfill(32)
			
			
	#print('salt is %s ' %salt)
	#print('cipher is %s ' %cipher)
	
	#Decrypt 
	plain = str(AES.new(master, AES.MODE_CBC, salt).decrypt(cipher)).strip('\'b0')
	#plain = decrypt_pack.decrypt(cipher)
	#plain = str(plain)
	#plain = plain.strip('\'b0')
	return(plain)
	
	
	
##Searches the dict for service and returns the username and password	
def loadpass(service):
	
	##pulls the list containing login info from the password dict
	a = passdb[service]
	
	##decodes the cipher and salt grabbed from dict
	cipher = base64.b64decode(a[1].strip('b\''))
	salt = base64.b64decode(a[2].strip('b\''))
	
	##grabs the username from dict
	username = a[0]
	
	##runs the salt and cipher through decrypt function
	password = decrypt(salt=salt, cipher=cipher)
	
	#returns username and password to main program
	return(username,password)
	
	
	
	
##loads the DB file into a dict
def loadDb():
	try:
		db = open('passdb.txt','r')
	except:
		db = open('passdb.txt', 'w')
	dbDict={}
	dbList=[]
	try:
		for line in db:
			a,b,c,d=line.strip('\n').split(',')
			dbList=[b,c,d]
			dbDict[a]=dbList
	except:
		pass
	db.close()
	return(dbDict)



passdb = loadDb()
print(passdb)
while True:
	print('1: Get Pass')
	print('2: Add New')
	print('0: Quit')
	while True:
		try:
			select = int(input('What is your selection?: '))
			break
		except:
			print('Invalid Selection')
	if select == 0:
		break
	elif select == 1:
		trylimit=0
		while True:
			serv = input('What is the service: ')
			if serv in passdb:
				uname, pw = loadpass(serv)
				print('The password and username name for %s:\nUser: %s  Password: %s' %(serv, uname, pw))
				break
			else:
				print('Invalid input, try again')
				trylimit+=1
				if trylimit==3:
					print('Too Many failed attempts, Goodbye!')
					exit()
	elif select == 2:
		serv = input('What service: ')
		uname = input('What is the user name: ')
		pw = getpass('What is the pw: ')
		passdb=addDb(serv,uname,pw)
		
