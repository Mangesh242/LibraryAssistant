import speech_recognition as sr 

def record():
	r = sr.Recognizer()
	with sr.Microphone() as source:
		print("Say Something...")
		audio = r.listen(source)
	print("Time over, thanks")
	try:
		text = r.recognize_google(audio)
		print(text)
		return text
	except:
		pass
	return " didnt get text"
if __name__ == '__main__':
    record()
