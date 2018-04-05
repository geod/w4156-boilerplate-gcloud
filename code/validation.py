class Validation:

    def form_input_valid(form):
        uChecker = True
        if form.f_name == "" or form.l_name == "" or form.uni == "" or form.pwd == "":
            uChecker = False
        elif len(form.pwd) < 8 or form.pwd.isupper() or form.pwd.islower() or form.pwd.isdigit():
            uChecker = False
        return uChecker

    # testing
    '''print (form_input_valid("Shelley", "S", "sks2209", "Lunch657"))
    print (form_input_valid("Shelley", "", "sks2209", "Lunch657"))
    print (form_input_valid("Shelley", "S", "sks2209", "lunch657"))'''

# def listing_valid(cafe,date):
