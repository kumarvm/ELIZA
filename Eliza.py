import json
import random
import re

''' Reads the JSON file into a variable, initialises two empty arrays 
 and returns the variable representing the JSON script and the two empty arrays. '''
def read_file():
    file = open("doctor_script.json")
    data = json.load(file)
    greetings = []
    goodbyes = []
    file.close()

    return data, greetings, goodbyes

''' Prints the welcome message. '''
def print_welcome_message(data, greetings):
    for i in data["greetings"]:
        greetings.append(i)

    print(greetings[random.randint(0, len(greetings) - 1)])

''' Gets the input from the user; ends the program if a quit command is used, otherwise the input_message
 goes through pre substitution, the keywords are then found and stored and get_output() is called. '''
def get_input():
    input_message = input().strip() #Strips any pretailing or trailing spaces

    for j in data["goodbyes"]:
        goodbyes.append(j)

    #Ends the program if quit command is given
    if input_message.lower() in data["quit commands"]:
        print(goodbyes[random.randint(0, len(goodbyes) - 1)])
        quit()
    
    input_message = pre_substitution(input_message)
    keyword, words, sorted_keywords = get_keywords(input_message)
    get_output(keyword, words, input_message, sorted_keywords)

''' Sends the input message through a set of substitution rules 
 that can be found in the JSON script; returns the substituted message. '''
def pre_substitution(input_message):
    for z in data["presub rules"]:
        input_message = re.sub(z, data["presub rules"][z], input_message)

    return input_message

''' Returns an array of words created from the input_message, 
 an array of sorted keywords and the highest priority keyword. '''
def get_keywords(input_message):
    words = input_message.split(" ")
    sorted_keywords = []
    keywords = []
    precedences = []
    
    for x in words:
        for y in data["keywords"]:
            if x in list(y["keyword"]):
                keywords.append(x)
                precedences.append(int(y["precedence"]))
    
    if len(keywords) == 0:
        keyword = ""
    else:
        sorted_precedences = sorted(precedences, reverse=True)
        
        for a in range(len(sorted_precedences)):
            for b in range(len(precedences)):
                if sorted_precedences[a] == precedences[b]:
                    index = b
                    sorted_keywords.append(keywords[index])

        keyword = sorted_keywords[0]

    return keyword, words, sorted_keywords

''' Prints the appropriate output; outputs are based on certain conditions 
 and get_input() is called after the output is printed'''
def get_output(keyword, words, input_message, sorted_keywords):
    if len(keyword) == 0:
        print(data["default"][random.randint(0, len(data["default"]) - 1)]) #If no keywords are found, a default message is printed
        get_input()
    else:
        for a in data["keywords"]:

            if keyword in list(a["keyword"]):

                for b in a["rules"]:
                    match = re.search(str(b["decomposition"]), input_message)

                    if match != None:
                        output = b["reassembly"][random.randint(0, len(b["reassembly"]) - 1)]
                        
                        if output == ":newkey":
                            get_next_keyword(sorted_keywords, keyword, words, input_message) #Finds the next keyword and finds an appropriate output based on that keyword

                        elif re.search("=", output) != None:
                            go_to_equals(keyword, output, words, input_message, sorted_keywords) #Goes to the given keyword and an appropriate output is printed 

                        elif re.search("[0-9]", output) != None: #Requires the program to remember and use the input in its output
                            post_substitution(output, words, keyword)
                            get_input()

                        else:
                            print(output)
                            get_input()

''' Corrects and prints the output by running through a set of substitution rules found in the JSON script '''
def post_substitution(output, words, keyword):
    index_placeholder = output.index("$")
    number = int(output[index_placeholder + 1])
    words_to_sub = []

    for w in range(words.index(keyword) + number, len(words)):
        words_to_sub.append(words[w].lower())
    
    words_checked = [False]*len(words_to_sub)

    for i in range(len(words_to_sub)):
        for rule in data["postsub rules"]:
            if re.search(rule, words_to_sub[i]) != None:

                if words_checked[i] == False:
                    words_to_sub[i] = re.sub(rule, data["postsub rules"][rule], words_to_sub[i])
                    words_checked[i] = True

    string_to_sub = ""
    for word in words_to_sub:
        string_to_sub += word + " "

    string_to_sub = string_to_sub.rstrip()

    output_message = re.sub("\$[0-9]", string_to_sub, output)
    print(output_message)

''' Gets the next keyword in order of descending precedence or priority; if no next keyword is found, then keyword is set to empty and a default message will be printed '''
def get_next_keyword(sorted_keywords, keyword, words, input_message):

    if len(sorted_keywords) > 1:
        old_index = sorted_keywords.index(keyword) + 1
        
        if old_index < len(sorted_keywords):
            keyword = sorted_keywords[old_index]
        else:
            keyword = ""
    else:
        keyword = ""
    
    get_output(keyword, words, input_message, sorted_keywords)

''' Gets the keyword that follows the '=' and get_output() is called after '''
def go_to_equals(keyword, output, words, input_message, sorted_keywords):
    keyword = output[1:]
    get_output(keyword, words, input_message, sorted_keywords)


data, greetings, goodbyes = read_file()
print_welcome_message(data, greetings)
get_input()
