# ELIZA
Python implementation of Joseph Weizenbaum's chatbot ELIZA from 1966.

## Motivation
This project was created as it caught my attention as a challenge and it seemed like a interesting project. It was also created to showcase Python skills.

## How to use the code to run ELIZA
In a powershell terminal, write python Eliza.py to start the chatbot. An initial message will then appear on the terminal. Write your response in the terminal and hit enter. Eliza should respond as programmed. To stop the chatbot, simply enter a quit command (such as quit). Other quit commands can be found in the doctor_script.json file.

## How ELIZA works
The input message is first cleaned of punctuation and extra spaces that are before and after the input message. If the input message is a quit command (see doctor_script.json for these commands), the chatbot sends a final message and ends. 
Otherwise, the input message goes through a set of pre-substitution rules (can be found in doctor_script.json), the keywords of the input message are found and ordered in order of descending precedence (the keywords and precedence depend on the script). The program then goes to the matching decomposition rule that is associated with the most precedent keyword, randomly chooses a reassembly rule and based on the reassembly rule, outputs a certain message to the terminal. The program then prompts the user for another input.

If the reassembly rule is ':newkey', then the program goes to the next keyword in the order of precedence and does all of the above.
If the reassembly rule contains '=' followed by a word, then the program goes to that word's entry in the script and chooses a reassembly rule that associated with that word.
If the reassembly rule contains '$' followed by a number, then the program will use a part of the input message in the output message (acts as a memory function). The appropriate part of the input message is substituted into the output message and then the new output message goes through a set of post-substitution rules (can be found in doctor_script.json). The message is then sent to the terminal.
If the reassembly rule doesn't match any of the above conditions, then the reassembly rule is printed as the output message as normal.

## Screenshots


## IDE and Libraries used
Visual Studio Code, json, re, random
