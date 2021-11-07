#Imports kivy stuff
from kivy.app import App 
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty

#Imports tkinter stuff (used for the pop-up file selection window and default error windows)
import tkinter as tk
from tkinter import filedialog

#Other imports
import string
import collections
import enchant
from regex import findall



#Configuration of the window
Config.set("graphics", "resizable", False) 
Config.set("graphics", "width", "1024")
Config.set("graphics", "height", "768")

root = tk.Tk()
root.withdraw()
root.iconbitmap("Images/Caesar_icon.ico")




#The class of the Main menu (middle)
class MainMenu(Screen):
    pass




#The class of the Decrypt menu (left)
class DecryptMenu(Screen):
    #Connects Kivy widgets with the Python code
    in_words = ObjectProperty(None)
    out_words = ObjectProperty(None)
    in_shift = ObjectProperty(None)



    #Activates the proccess of encoding
    def decode_btn(self):
        #If the shift is given
        if self.in_shift.text != '':

            if self.in_shift.text.isnumeric():
                decoded = ''
    
                for letter in range(len(self.in_words.text)):
                    decoded += shift_letter(self.in_words.text[letter], 26 - int(self.in_shift.text))

                self.out_words.text = decoded

            else: 
                tk.messagebox.showerror(title="Not a number", message="Shift is not a numeric value")

        #If the shift is not given
        else:
            if self.in_words.text != "":
                #If the text is only one word
                if len(self.in_words.text.split()) == 1:
                    test_results = word_test(self.in_words.text)
                    self.out_words.text = test_results[0]
                    self.in_shift.text = str(26 - test_results[1])


                #If the text is more than one word
                elif len(self.in_words.text.split()) > 1:
                    test_results = sentence_test(self.in_words.text)
                    self.out_words.text = test_results[0]
                    self.in_shift.text = str(26 - test_results[1])




    #Decodes from the txt file
    def decode_txt_btn(self):
        if self.in_shift.text.isnumeric() or self.in_shift.text == "":
            #Loads the file
            file_path = filedialog.askopenfilename()
            decoded_file_path = file_path[:-4] + "_decoded.txt"
        
            #If the file has .txt extension
            if file_path[-4:] == ".txt":
                with open(file_path, "r") as file: 
                    lines = file.read().splitlines()

                
                #If shift is unknown
                if self.in_shift.text == "":
                    longest = max(findall(r"[A-Za-z]+|\S"," ".join(lines)), key=len)
                    shift = word_test(longest)[1]

                    self.in_shift.text = str(26 - shift)
            
                    for current_line in lines:
                        decoded_line = ""
                
                        for letter in range(len(current_line)):
                            decoded_line += shift_letter(current_line[letter], shift)

                        with open(decoded_file_path, "a") as decoded_file:
                            decoded_file.write(decoded_line + "\n")

                    tk.messagebox.showinfo(title="Saved", message="Saved into " + decoded_file_path.split("/")[-1])

                else:
                    for current_line in lines:
                        decoded_line = [shift_letter(current_line[letter], 26 - int(self.in_shift.text)) for letter in range(len(current_line))]
                        with open(decoded_file_path, "a") as decoded_file: 
                            decoded_file.write("".join(decoded_line) + "\n")

                    tk.messagebox.showinfo(title="Saved", message="Saved into " + decoded_file_path.split("/")[-1])
                
            else: 
                tk.messagebox.showerror(title="Filetype error", message="Not a txt document")

        else: 
            tk.messagebox.showerror(title="Not a number", message="Shift is not a numeric value")
            
            

    #Increases the shift by one and decodes
    def options_right_btn(self):
        if self.in_shift.text.isnumeric():
            if int(self.in_shift.text) + 1 == 27: 
                self.in_shift.text = "1"

            else: 
                self.in_shift.text = str(int(self.in_shift.text) + 1)

            self.decode_btn()

        else: 
            tk.messagebox.showerror(title="Not a number", message="Shift is not a numeric value")



    #Decreses the shift by one and decodes
    def options_left_btn(self):
        if self.in_shift.text.isnumeric():
            if int(self.in_shift.text) - 1 == 0: 
                self.in_shift.text = "26"

            else:
                self.in_shift.text = str(int(self.in_shift.text) - 1)

            self.decode_btn()

        else: 
            tk.messagebox.showerror(title="Not a number", message="Shift is not a numeric value")





#The class of the Encrypt menu (right)
class EncryptMenu(Screen):
    #Connects Kivy widgets with the Python code
    in_words = ObjectProperty(None)
    out_words = ObjectProperty(None)
    in_shift = ObjectProperty(None)



    #Activates the proccess of encoding
    def encode_btn(self):
        if self.in_shift.text.isnumeric():
            encoded = ''
    
            for letter in range(len(self.in_words.text)):
                encoded += shift_letter(self.in_words.text[letter], int(self.in_shift.text))

            self.out_words.text = encoded

        else:
            tk.messagebox.showerror(title="Not a number", message="Shift is not a numeric value")



    #Encodes from the txt file
    def encode_txt_btn(self):
        if self.in_shift.text.isnumeric():

            file_path = filedialog.askopenfilename()
            encoded_file_path = file_path[:-4] + "_encoded.txt"
        
            #If the file has .txt extension
            if file_path[-4:] == ".txt":
                with open(file_path, "r") as file:
                    lines = file.read().splitlines()
 

                for current_line in lines:
                        encoded_line = ""
                
                        for letter in range(len(current_line)):
                            encoded_line += shift_letter(current_line[letter], int(self.in_shift.text))

                        with open(encoded_file_path, "a") as encoded_file:
                            encoded_file.write(encoded_line + "\n")

                tk.messagebox.showinfo(title="Saved", message="Saved into " + encoded_file_path.split("/")[-1])

        else:
            tk.messagebox.showerror(title="Not a number", message="Shift is not a numeric value")




#The necessary class to control the windows
class WindowManager(ScreenManager):
    pass





#The main class that loads Caesar_interface.kv file that should be in the same directory
class CaesarApp(App):
    def build(self):
        self.icon= 'Images/Caesar_icon.ico'
        kivy_interface = Builder.load_file('Caesar_interface.kv')
        return kivy_interface



#Takes the letter and the shift and returns the new letter according to the shift
def shift_letter(letter, shift):

    #If the letter is lowercase
    if letter.islower():
        deciphered_index = string.ascii_lowercase.index(letter) + shift
        deciphered_index = deciphered_index - (deciphered_index // 26) * 26
        return string.ascii_lowercase[deciphered_index]

    #If the letter is uppercase
    elif letter.isupper():
        deciphered_index = string.ascii_uppercase.index(letter) + shift
        deciphered_index = deciphered_index - (deciphered_index // 26) * 26
        return string.ascii_uppercase[deciphered_index]

    #If not a letter
    else:
        return letter



#Takes the word and returns the deciphered word and the shift 
def word_test(text): 
    most_frequent_letter = collections.Counter(text.lower()).most_common(1)[0][0]

    #Goes over the letter frequency list to brute-force the shift
    for alph_counter in alph_frequency:
        guess = ''
        shift = get_diff(most_frequent_letter, alph_counter)

        #Goes over each letter and shifts them
        for i in range(len(text)):
            if text[i].isalpha():
                guess += shift_letter(text[i], shift)

            else:
                guess += text[i]
            
        #Checks if the word exists
        if dictionary.check(guess):
            return guess, shift

    tk.messagebox.showerror(title="Decryption failed", message="Sorry, automatic decryption failed, please use \"Other options\"")
    return guess, shift



#Takes the text(more than one word is expected) and returns the deciphered text and the shift
def sentence_test(text):
    result = ""

    #Finds the longest word and decodes it
    longest = max(findall(r"[A-Za-z]+|\S",text), key=len)
    shift = word_test(longest)[1]

    #Replaces every letter in the text with the shifted letter
    for letter in text:
        if letter.isalpha():
            result += shift_letter(letter, shift)

        else:
            result += letter

    return result, shift



#Takes two letters and returns the distance between the first letter and the second letter as integer
def get_diff(first_letter, second_letter):
    diff = ord(first_letter) - ord(second_letter)

    if diff > 0:
        return(26 - diff)
    
    else:
        return (abs(diff))



#English dictionary and list of letters by the usage frequency
dictionary = enchant.Dict("en_US")
alph_frequency = ['e', 't', 'a', 'o', 'i', 'n', 's', 'r', 'h', 'd', 'l', 'u', 'c', 'm', 'f', 'y', 'w', 'g', 'p', 'b', 'v', 'k', 'x', 'q', 'j', 'z']



CaesarApp().run()