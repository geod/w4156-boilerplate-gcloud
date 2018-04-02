class Validation:

	def user_valid(f_name, l_name, uni, pwd):
		uChecker = True
		if(f_name == "" or l_name == "" or uni == "" or pwd == ""):
			uChecker = False
		elif (len(pwd)<8 or pwd.isupper() or pwd.islower() or pwd.isdigit()):
			uChecker = False
		return uChecker

	#testing
	print (user_valid("Shelley", "S", "sks2209", "Lunch657"))
	print (user_valid("Shelley", "", "sks2209", "Lunch657"))
	print (user_valid("Shelley", "S", "sks2209", "lunch657"))

	# def listing_valid(cafe,date):
		




