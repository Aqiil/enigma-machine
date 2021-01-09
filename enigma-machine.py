
import time
import datetime
import sqlite3
from sqlite3 import Error
import os
import random
import re
import collections

class rotor:
    def __init__(self, alphabet, notch, turnover, position, ringSetting):
        """Create new rotor"""
        self._charAlphabet = alphabet #Initialises alphabet as tuple csv
 
        self.alphabet = self.GetAlphabet() #Parses the alphabet as a dictionary so that each character is connected to a position
        self._notch = notch
        self._turnover = turnover
        self._position = int(position) - 1 #Finds the index of the rotor position
        self._ringSetting = int(ringSetting) 
        self.adjustAlphabetByPosition()
 
    def adjustAlphabetByPosition(self):
        """Adjusts alphabet to start on different rotor positions"""
        for i in range(0, self._position): #Rotates rotors until it reaches the input position without stepping or incrementing the position attribute
            self.adjustRotor()
 
    def adjustRotor(self):
        """Rotate the rotor without incrementing it or stepping"""
        #Ensures next positions are within alphabet range
        for k, v in self.alphabet.items():
            self.alphabet[k] = (v - 1)% 26 #Loops the alphabet from Z (26th letter) back to A (1st letter)
 
        #Swaps dictionary format from {‘Key’: value} to {value: ‘Key’} so we can change the characters
        tempAlphabet = {}
        for k, v in self.alphabet.items():
            tempAlphabet[v] = k
        self.alphabet = tempAlphabet
 
        #Changes internal wiring contact to its previous contact
        for k, v in self.alphabet.items():
            charNum = self.ordChar(v)
            prevCharNum = (charNum - 1)% 26
            prevChar = self.chrNum(prevCharNum)
            self.alphabet[k] = prevChar
 
        #Swaps dictionary format from {value: ‘Key’} back to original {‘Key’: value} format
        tempAlphabet = {}
        for k, v in self.alphabet.items():
            tempAlphabet[v] = k
        self.alphabet = tempAlphabet
 
    def changeRingSetting(self):
        """Changes ring setting and creates offset variable"""
        #Input code to accommodate function of Ring setting
 
    def chrNum(self, num):
        """Finds the ASCII code of input index position"""
        char = chr(num + 65) 
        return char 
 
    def cipherFromExternalContact(self, char):
        """Cipher the user input character"""
        self.incrementRotor() #Incements the rotor as the key is 'pressed' on the enigma machine
        char = self.cipherToReflector(char) #Ciphers a character in the forward direction to the reflector
        return char #Returns character
 
    def cipherFromReflector(self, char):
        """Cipher character produced by previous rotor travelling from reflector"""
        inputCharNum = self.GetNumByChar(char) #Finds the index of the value for the input character to find the internal wiring connection
        outputChar = self.chrNum(inputCharNum) #Finds the ASCII code of the index value to find the external rotor connection 
        return outputChar #Returns the external character that the wiring is connected to
 
    def cipherToReflector(self, char):
        """Cipher character produced by previous rotor travelling to reflector"""
        inputCharNum = self.ordChar(char) #Finds the index value of the input ASCII code to find the external rotor connection
        outputChar = self.GetCharByNum(inputCharNum) #Finds the corresponding character of the input to find the internal wiring connection
        return outputChar #Finds the internal wiring contact that the character is connected to
 
    def GetAlphabet(self):
        """Parses alphabet as dictionary"""
        alphabet = list(self._charAlphabet) #Creates a list of the alphabet characters
        numbers = [i for i in range(0,26)] #Creates a list of numbers up to 25
        numberOff = dict( zip(alphabet, numbers)) #Pairs each character with a number in a chronological sequence to number the characters from 0 to 25
 
        return numberOff
 
    def GetCharByNum(self, inputNum):
        """Find the corresponding character of the input number"""
        # ROTOR USE ONLY
        for char, num in self.alphabet.items():
            if num == inputNum: 
                return char
 
    def GetNotch(self):
        """Gets notch position"""
        return self._notch
 
    def GetNotchNum(self):
        """Gets numerical value of notch"""
        num = self.ordChar(self._notch) + 1
        return num
 
    def GetNumByChar(self, inputChar):
        """Finds the corresponding number of the input character"""
        # ROTOR USE ONLY
        for char, num in self.alphabet.items():
            if char == inputChar:
                return num
 
    def GetRingSetting(self):
        """Gets ring setting"""
        return self._ringSetting
 
    def GetRotorPosition(self):
        """Gets position of rotor"""
        position = self._position + 1
        return position
 
    def GetTurnoverNum(self):
        """Get numerical value of turnover character"""
        num = self.ordChar(self._turnover) + 1
        num = num % 26
        return num
 
    def incrementRotor(self):
        """Rotates rotor forward by one position"""
        self._position += 1
        self._position = self._position % 26 
 
        #Ensures next positions are within alphabet range
        for k, v in self.alphabet.items():
            self.alphabet[k] = (v - 1)% 26
 
        #Swaps dictionary format from {‘Key’: value} to {value: ‘Key’} so we can change the characters
        tempAlphabet = {}
        for k, v in self.alphabet.items():
            tempAlphabet[v] = k
        self.alphabet = tempAlphabet
 
        #Changes internal wiring contact to its previous contact
        for k, v in self.alphabet.items():
            charNum = self.ordChar(v)
            prevCharNum = (charNum - 1)% 26
            prevChar = self.chrNum(prevCharNum)
            self.alphabet[k] = prevChar
 
        #Swaps dictionary format from {value: ‘Key’} back to original {‘Key’: value} format
        tempAlphabet = {}
        for k, v in self.alphabet.items():
            tempAlphabet[v] = k
        self.alphabet = tempAlphabet
 
    def ordChar(self, char):
        """Finds the index value of input ASCII code"""
        char = char.upper()
        num = ord(char) - 65
        return num
 
 
class plugboard:
    def __init__(self, connections):
        """Connect plugboard plugs"""
        self._connections = connections.split()
 
    def switchChar(self, char):
        for pair in self._connections:
            for letter in pair:
                if letter == char: #If input matches the letter
                    index = pair.index(letter) #Find the index of the letter
                    index += 1 #Increment it by one
                    sub = pair[(index % len(pair))] #Ensure it is within the index range
                    return sub #Return the substituted character to the user
        else:
            return char #Return character if not in a pair
 
 
class reflector:
    def __init__(self, connections):
        """Set reflector substitution pairs"""
        self._connections = connections.split()
 
    def reflect(self, char):
        for pair in self._connections:
            for letter in pair:
                if letter == char: #If input matches the letter
                    index = pair.index(letter) #Find the index of the letter
                    index += 1#Increment it by one
                    sub = pair[(index % len(pair))] #Ensure it is within the index range
                    return sub #Return the substituted character to the user
 
 
class data:
    def __init__(self):
        """Database creation"""
        self.destination = ''
        self.createFolder() #Create a folder to export databases to
        self.reset() #Create a database connection
 
    def createFolder(self):
        """Create a folder to house the databases"""
        self.destination = self.getPath() #Find the destination to create the folder
        try:
            os.makedirs(self.destination) #Try and make a folder
        except FileExistsError:
            pass #Otherwise continue if an error is encountered because the file exists already
 
    def createTable(self):
        """Create a table within a database"""
        self.c.execute("CREATE TABLE IF NOT EXISTS Enigma(Datum INTEGER PRIMARY KEY, Walzenlage TEXT, Ringstellung TEXT, Steckerverbindungen TEXT, Kenngruppen TEXT)") 
 
    def currentDay(self):
        """Finds the current day"""
        day = datetime.datetime.today().day
        return day
 
    def exportTable(self):
        """Exports the table to the destination folder"""
        try:
            self.createTable() #Create a table
            self.insertData() #Insert the daily settings
            print('Database has been exported to ' + self.destination + '\\'+ self.database + '\n') #Export the table
        except:
            print('Enigma table already exists for this database. Please choose another database.') #Otherwise inform the user that the table exists
            self.reset() #Prompt a new input for the database name
            self.exportTable() #Try and export the new database using recursion
 
    def genCharGroup(self):
        """Creates a character group"""
        alphabet = list('abcdefghijklmnopqrstuvwxyz') #Creates a list of all the alphabet characters
        group = []
        count = 0
        while count != 3: #While the loop total does not equal 3
            i = random.choice(alphabet) #Make a random choice
            alphabet.remove(i) #Remove it from the alphabet
            group.append(i) #And add it to the group array
            count += 1 #Add one to the loop total
        return str(''.join(group)) #Return the string of 3 characters to the user
 
    def genRingSetting(self):
        """Generates a ring setting value"""
        num = random.randrange(0,25) #Generates a random number from 0 to 25
        if num < 10: #If the number is a single digit
            num = str(num) #Turn it into a string
            num = '0' + num #Add a 0 before it
        return str(num) #Return the string of the number to the user in double digit format
 
    def getPath(self):
        """Identifies the path of the application to create the new folder"""
        path = os.path.dirname(os.path.realpath(__file__)) #Finds the path of the application
        path =(os.path.dirname(os.path.realpath(__file__))+ '\\Enigma Settings') #Adds to the directory to create a folder
 
        return path #Returns the folders directory
 
    def insertData(self):
        """Inserts the daily settings into the database"""
        Walzenlage = self.ranRotorOrder() #Obtains a random rotor order
        Ringstellung = self.ranRingSetting() #Obtains s series or random ring settings
        Steckerverbindungen = self.ranPlugboard() #Obtains random plugboard pairs
        Kenngruppen = self.ranCharGroup() #Obtains 4 groups of characters for the Kenngruppen
 
        Datum = 31 #Begins the data entry at day 31
        while Datum != 0: 
            self.c.execute("INSERT INTO Enigma(Datum, Walzenlage, Ringstellung, Steckerverbindungen, Kenngruppen) VALUES (?, ?, ?, ?, ?)",
                           (int(Datum), str(Walzenlage), str(Ringstellung), str(Steckerverbindungen), str(Kenngruppen))) #Inserts the entries generated above into the database
            Walzenlage = self.ranRotorOrder() #Generates new random rotor order
            Ringstellung = self.ranRingSetting() #Generates new random ring settings
            Steckerverbindungen = self.ranPlugboard() #Generates new random plugboard pairs
            Kenngruppen = self.ranCharGroup() #Generates 4 new groups of characters for the Kenngruppen
            Datum -= 1 #Decreases the day by one for the next record entry
 
        self.conn.commit() #Commits all the changes to the database
 
    def ranCharGroup(self):
        """Generates a random string of 4 character group"""
        group = self.genCharGroup() + ' ' + self.genCharGroup() + ' ' + self.genCharGroup() + ' ' + self.genCharGroup()
        return group #Returns a string of 4 character groups
 
    def ranPlugboard(self):
        """Creates random pairs for the plugboard"""
        alphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ') #Creates a list of the alphabet characters
        plugboard = []
 
        while len(alphabet) != 0: #While there are characters remaining in the alphabet
            i = random.choice(alphabet) #Make a random choice
            alphabet.remove(i) #Remove it from the alphabet
            plugboard.append(i) #And add it to the plugboard array
 
        raw_plugboard = ''.join(plugboard) #Join all the characters in the plugboard array into a string
 
        plugboard = [(raw_plugboard[i:i+2]) for i in range(0, len(raw_plugboard), 2)] #Split the array of characters into groups of 2
 
        return ' '.join(plugboard) #Join each of the individual arrays to make a string
 
    def ranRingSetting(self):
        """Creates a random string for the ring setting values"""
        ringSetting = self.genRingSetting() + ' ' + self.genRingSetting() + ' ' + self.genRingSetting()
        return ringSetting #Returns a string of 3 ring setting values
 
    def ranRotorOrder(self):
        """Selects three random rotors for the daily settings"""
        count = 0
        rotors = ['I','II','III','IV','V']
        rotorOrder = []
        while count != 3: #While 3 choices have not been made
            choice = random.choice(rotors) #Make a random choice from the rotors array
            rotorOrder.append(choice) #Add it to the rotorOrder array
            rotors.remove(choice) #And remove it from the rotors array
            count += 1 #Increment the count variable
 
        rotorOrder = ' '.join(rotorOrder) #Join the array to make a string of the 3 rotors
 
        return rotorOrder
 
    def readData(self):
        """Selects the daily settings record for the current day"""
        dayToday = self.currentDay()
 
        loopDbInput = True
 
        while loopDbInput == True: #While there is an error
            try:
                self.c.execute("SELECT * FROM Enigma WHERE Datum = " + str(dayToday)) #Select all the data in the record for the current day
                data = self.c.fetchall() #Store the selected data in this variable
            except:
                print('Error reading database. Please choose another database.') #Inform the user that there is an error connecting to the database 
                self.reset() #Prompt the user to establish a new database connection
            else:
                loopDbInput = False #Otherwise continue with the program
                return data #And return the daily settings 
 
    def reset(self):
        """Creates a new database connection"""
        os.chdir(self.destination) #Changes directory to the 'Enigma Settings' folder
        self.database = str(input('\nEnter the name of the database: ' ) + '.db') #Prompts user to enter database name
        self.conn = sqlite3.connect(self.database) #Established a connection to the database
        self.c = self.conn.cursor() #Creates a cursor to traverse the data set
 
 
class simulation:
    def __init__(self):
        """Run enigma simulation"""
 
    def cipher(self, char):
        position = self._rotorL.chrNum(self._rotorL.GetRotorPosition() - 1), self._rotorM.chrNum(self._rotorM.GetRotorPosition() - 1), self._rotorR.chrNum(self._rotorR.GetRotorPosition() - 1) #Find the current external position of each rotor
 
        if self.visuals == 'Y': #If the user wants to see the encryption process
            print(''.join(position)) #Output the current rotor positions
        char0 = char
        char = self._plugboard.switchChar(char) #Substitute the user input through the plugboard
        char1 = char
        char = self._rotorR.cipherFromExternalContact(char) #Increment the rotor and cipher the plugboard output through the right rotor
        self.singleStep(self._rotorL, self._rotorM, self._rotorR)
        char1 = char
        char = self._rotorM.cipherToReflector(char) #Cipher the output from the right rotor through the middle rotor
        char2 = char
        char = self._rotorL.cipherToReflector(char) #Cipher the output from the middle rotor through the left rotor
        char3 = char
        char = self._UKW.reflect(char) #Reflects the character from the left rotor through the reflector
        char4 = char
        char = self._rotorL.cipherFromReflector(char) #Cipher the output from the reflector through the left rotor
        char5 = char
        char = self._rotorM.cipherFromReflector(char) #Cipher the output from the left rotor through the middle rotor
        char6 = char
        char = self._rotorR.cipherFromReflector(char) #Cipher the output from the middle rotor through the right rotor
        char7 = char
        char = self._plugboard.switchChar(char) #Substitute the output from the right rotor through the reflector
        if self.visuals == 'Y': #If the user wants to see the encryption process
            print(char0,": ",char1, char2, char3, char4, char5, char6,": ",char) #Output the encryption process of the input
            time.sleep(0.1) #Wait 0.1 seconds before continuing to cipher the next character for a gradual effect
 
        self.doubleStep(self._rotorL, self._rotorM, self._rotorR) #Check if a double step will occur on the next key press
        return char #Return the ciphered character
 
    def createCustomWiring(self):
        """Creates custom wiring"""
        loopAlphaInput = True
 
        while loopAlphaInput == True: #While user input is invalid
            try:
                rotorL = str(input('\nEnter left rotor alphabet: ')).upper().strip() #Prompt the user to enter the alphabet for the left rotor
                if not re.match("^[A-Z]+$", rotorL): #Check if the input is within the alphabet 
                    raise ValueError() #Otherwise raise an error
 
                rotorM = str(input('Enter middle rotor alphabet: ')).upper().strip() #Prompt the user to enter the alphabet for the left rotor
                if not re.match("^[A-Z]+$", rotorM): #Check if the input is within the alphabet 
                    raise ValueError() #Otherwise raise an error
 
                rotorR = str(input('Enter right rotor alphabet: ')).upper().strip() #Prompt the user to enter the alphabet for the left rotor
                if not re.match("^[A-Z]+$", rotorR): #Check if the input is within the alphabet 
                    raise ValueError() #Otherwise raise an error
 
            except:
                print("Please limit characters to A - Z\n") #If an error is raised, inform the user that the input is outside the range
 
            else:
                loopAlphaInput = False #Otherwise continue using the program
 
        stepChars = str(input('\nEnter turnover positions: ')).upper().strip() #Prompt the user to enter the 3 turnover characters
        stepL, stepM, stepR = stepChars.split() #Split the user input into 3 seperate variables
        stepL, stepM, stepR = str(stepL), str(stepM), str(stepR) #Ensure the string of each variable is stored
 
        notchPos = input('Enter notch positions: ').upper().strip() #Prompt the user to enter the 3 notch characters
        notchL, notchM, notchR = notchPos.split() #Split the user input into 3 seperate variables
        notchL, notchM, notchR = str(notchL), str(notchM), str(notchR) #Ensure the string of each variable is stored
 
 
        ringSettings = input('\nEnter ring setting positions: ') #Prompt the user to enter the 3 ring setting values
        ringL, ringM, ringR = ringSettings.upper().split() #Split the user input into 3 seperate variables
        ringL, ringM, ringR = int(ringL), int(ringM), int(ringR) #Ensure the integer of each variable is stored
 
        startPos = input('Enter rotor starting positions: ') #Prompt the user to enter the 3 rotor starting positions
        startL, startM, startR = startPos.split() #Split the user input into 3 seperate variables
        startL, startM, startR = int(startL), int(startM), int(startR) #Ensure the integer of each variable is stored
 
 
        plugboardPairs = str(input('\nEnter plugboard pairs: ')).upper().strip() #Prompt the user to enter plugboard pairs
 
        loopReflectorInput = True
 
        while loopReflectorInput == True: #While user input is invalid
            reflectorPairs = str(input('Enter reflector pairs: ')).upper().strip() #Prompt user to enter reflector pairs
            reflectorInput = reflectorPairs.replace(" ", "") #Omit spaces in reflector pairs
 
            if len(reflectorInput) != 26: #Check if all characters in the alphabet have been entered
                print('Please enter all 26 characters from A - Z\n') #Inform user that all characters in the alphabet must be entered
 
            else:
                reflectorFrequencies = collections.Counter(reflectorInput) #Count the frequency of each character 
                reflectorRepeats = {}
                for k, v in reflectorFrequencies.items(): #For every frequency pair
                    if v > 1: #If there is more than one occurrence
                        reflectorRepeats[k] = v #Add it to the reflectorRepeats dictionary
                if len(reflectorRepeats) != 0: #If there are repeats in the reflectorRepeats dictionary
                    print('Each character  may only connect to another character . Try again.\n') #Notify user that there repeats
                    loopReflectorInput = True #Prompt the user to enter the reflector pairs again
                else:
                    loopReflectorInput = False #Otherwise continue with the program
 
        print("\n************     Custom Settings     ************") #Output custom settings
        print("Left Rotor:", rotorL + ", Ring position:", str(ringL) + ", Start position:", str(startL) + ", Notch position:", str(notchL))
        print("Middle Rotor:", rotorM + ", Ring position:", str(ringM) + ", Start position:", str(startM) + ", Notch position:", str(notchM))
        print("Right Rotor:", rotorR + ", Ring position:", str(ringR) + ", Start position:", str(startR) + ", Notch position:", str(notchR))
 
        print("\nPlugboard:", plugboardPairs)
        print("Reflector pairs:", reflectorPairs + '\n')
 
        #FORMAT        rotor('EKMFLGDQVZNTOWYHXUSPAIBRCJ','Y','Q', 1, 1)
        self._rotorL = rotor(rotorL, notchL, stepL, startL, ringL) #Create a rotor object for the left rotor 
        self._rotorM = rotor(rotorM, notchM, stepM, startM, ringM) #Create a rotor object for the middle rotor 
        self._rotorR = rotor(rotorR, notchR, stepR, startR, ringR) #Create a rotor object for the right rotor 
 
        self._UKW = reflector(reflectorPairs) #Create a reflector object using the reflector pairs
 
        self._plugboard = plugboard(plugboardPairs) #Create a plugboard object using the plugboard pairs
 
 
    def displayMenu(self):
        """Outputs main menu"""
        print("**************     MENU     **************")
        print("1. Encrypt/Decrypt using default wiring")
        print("2. Encrypt/Decrypt using custom wiring")
        print("3. Encrypt/Decrypt using imported settings")
        print("4. Generate cipher table")
        print("5. Guidance and operation")
        print("6. Exit application")
        print("Choose an option: ", end = "")
 
    def doubleStep(self, rotorL, rotorM, rotorR):
        """Checks if a double step will occur on the next key press"""
        Mpos = rotorM.GetRotorPosition() #Find the current position of the middle rotor
        Mturn = rotorM.GetTurnoverNum() #Find the turnover position of the middle rotor
 
        if (Mpos == Mturn): #If the rotor is at its turnover position
            if self.visuals == 'Y': #And the user wants to visualise encryption
                print('Double Step') #Notify the user that there is a double step
            rotorM.incrementRotor() #Increment the middle rotor
            rotorL.incrementRotor() #And increment the left rotor
 
    def encryptMessage(self):
        """Encrypts the message and outputs the encrypted ciphertext"""
        loopPrompt = True
 
        while loopPrompt == True: #While user input is invalid
 
            try:
                plaintext = str(input("Enter message to encrypt: ")).upper() #Prompt the user to enter their message
                plaintext = plaintext.replace(" ", "") #Remove spaces from the input message
                if not re.match("^[A-Z]*$", plaintext): #If the input is not within the alphabet
                    raise ValueError() #Raise an error
            except:
                print("Please limit characters to A - Z\n") #And notify the user that the input is outside the range
            else:
                loopPrompt = False #Otherwise continue with the program
 
 
        self.group = int(input('\nEnter the frequency of character grouping: ')) #Prompt user to enter frequency of character grouping
        self.visuals = input('Do you want to visualise encryption (Y/N): ').upper() #Ask if user wants to visualize encryption
 
        plaintext = list(plaintext) #Split the plaintext into an array
 
        ciphertext = ""
 
        for i in plaintext: #For each letter in the plaintext
            char = self.cipher(i) #Cipher the letter
            ciphertext = ciphertext + char #And add it to the ciphertext string
 
        ciphertext = [ciphertext[i:i+int(self.group)] for i in range(0, len(ciphertext), self.group)] #Split the ciphertext into an array according to the user input frequency group
        ciphertext = ' '.join(ciphertext) #Join the array to make a single string
 
        print('\nCiphertext: ', ciphertext, '\n') #Return the split ciphertext to the user
 
    def generateSettings(self):
        """Generates daily settings"""
        database = data() #Create a data object
        database.exportTable() #Export the daily settings
 
    def GetUserSettings(self):
        """Choose settings from regular enigma wiring"""
 
        #                     alphabet, notch, turnover, position, ringSetting
        #                     ABCDEFGHIJKLMNOPQRSTUVWXYZ
        self._rotor1 = rotor('EKMFLGDQVZNTOWYHXUSPAIBRCJ','Y','Q', 1, 1) #Create a default rotor I object
        self._rotor2 = rotor('AJDKSIRUXBLHWTMCQGZNPYFVOE','M','E', 1, 1) #Create a default rotor II object
        self._rotor3 = rotor('BDFHJLCPRTXVZNYEIWGAKMUSQO','D','V', 1, 1) #Create a default rotor III object
        self._rotor4 = rotor('ESOVPZJAYQUIRHXLNFTGKDCMWB','R','J', 1, 1) #Create a default rotor IV object
        self._rotor5 = rotor('VZBRGITYUPSDNHLXAWMJQOFECK','H','Z', 1, 1) #Create a default rotor V object
 
        self._UKWA = reflector('AE BJ CM DZ FL GY HX IV KW NR OQ PU ST') #Create a default A reflector object
        self._UKWB = reflector('AY BR CU DH EQ FS GL IP JX KN MO TZ VW') #Create a default B reflector object
        self._UKWC = reflector('AF BV CP DJ EI GO HY KR LZ MX NW QT SU') #Create a default C reflector object
 
        loopRotors = True
        while loopRotors == True: #While user input is invalid
            rotorL, rotorM, rotorR = input("\nEnter rotor setup: ").upper().split() #Prompt the user to enter the rotor setup
            if rotorL == rotorM or rotorL == rotorR or rotorM == rotorR: #If the user has used the same rotor 
                print('Rotors can not be the same. Try again.') #Inform them that they cannot use the same rotors and prompt again
            else:
                loopRotors = False #Otherwise continue with the program
 
        reflectorType = input("Enter reflector type: ").upper() #Prompt user to enter reflector type
 
        loopPlugboard = True
        while loopPlugboard == True: #While user input is invalid
            plugboardPairs = input('\nEnter plugboard pairs: ').upper().strip() #Prompt user to enter plugboard pairs
            stringPairs = plugboardPairs.replace(" ", "") #Remove any spaces
 
            if len(stringPairs) != 0: #If the user has entered plugboard pairs
                frequencies = collections.Counter(stringPairs) #Count the frequency of each character 
                repeated = {}
                for k, v in frequencies.items(): #For every frequency pair
                    if v > 1: #If there is more than one occurrence
                        repeated[k] = v #Add it to the repeated dictionary
                if len(repeated) != 0: #If there are repeats in the repeated dictionary
                    print('Each character  may only connect to another character. Try again.') #Prompt the user to enter the plugboard pairs again
                    loopPlugboard = True
                else:
                    loopPlugboard = False #Otherwise continue with the program
            else:
                loopPlugboard = False #Continue with the program if there is not input for the plugboard pairs
 
        rotors = {'I':self._rotor1, 'II':self._rotor2, 'III':self._rotor3, 'IV':self._rotor4, 'V':self._rotor5} #Match each rotor type to their rotor object
        reflectors = {'A':self._UKWA, 'B':self._UKWB, 'C':self._UKWC} #Match each reflector type to their reflector object
 
        self._rotorL = rotors.get(rotorL) #Assign the corresponding rotor object to the rotor
        self._rotorM = rotors.get(rotorM)
        self._rotorR = rotors.get(rotorR)
 
        self._UKW = reflectors[reflectorType] #Assign the corresponding reflector object to the reflector
 
        self._plugboard = plugboard(plugboardPairs) #Assign the corresponding plugboard object to the plugboard
 
    def help(self):
        """Displays usage instruction for user"""
        print('\n********** USING DEFAULT WIRING **********')
        print('Enter rotor setup as a sequence of 3 rotors using uppercase or lowercase letter separated by a space between each rotor. Choose from 5 default rotors: I II III IV V.')
        print('Enter reflector type as a single uppercase or lowercase letter. Choose from A B C.')
 
        print('\nEnter plugboard pairs as pairs of uppercase or lowercase letters. Each letter may only be paired with one other letter. All letters do not have to be used.')
        print('Enter message as a string of uppercase or lowercase letters. Spaces in the text will be removed.')
 
        print('\nEnter character grouping as an integer number.')
        print('Enter choice to visualise encryption as a single uppercase or lowercase letter.')
 
 
        print('\n\n********** USING CUSTOM WIRING **********')
        print('Enter rotor alphabet as a string of uppercase or lowercase letters. Each letter may only occur once and every letter must be used.')
 
        print('\nEnter turnover positions as a sequence of 3 uppercase or lowercase letters separated by a space between each letter.')
        print('Enter notch positions as a sequence of 3 uppercase or lowercase letters separated by a space between each letter.')
 
        print('\nEnter ring settings as a sequence of 3 numbers separated by a space between each number')
        print('Enter rotor starting positions as a sequence of 3 numbers separated by a space between each number')
 
        print('\nEnter plugboard pairs as pairs of uppercase or lowercase letters. Each letter may only be paired with one other letter. All letters do not have to be used.')
        print('Enter reflector pairs as pairs of uppercase or lowercase letters. Each letter may only be paired with one other letter. All letters must be used.')
 
        print('\nEnter message as a string of uppercase or lowercase letters. Spaces in the text will be removed.')
 
        print('\nEnter character grouping as an integer number.')
        print('Enter choice to visualise encryption as a single uppercase or lowercase letter.')
 
 
        print('\n\n********** USING IMPORTED SETTINGS **********')
        print('Enter name of database as a single string of characters')
 
        print('\nEnter rotor starting positions as a sequence of 3 numbers separated by a space between each number')
        print('Enter reflector type as a single uppercase or lowercase letter. Choose from A B C.')
 
        print('\nEnter message as a string of uppercase or lowercase letters. Spaces in the text will be removed.')
 
        print('\nEnter character grouping as an integer number.')
        print('Enter choice to visualise encryption as a single uppercase or lowercase letter.')
 
 
        print('\n\n********** GENERATING CIPHER TABLE **********')
        print('Enter name of database as a single string of characters.')
        print("Database will be exported to and saved in 'Enigma Settings' folder")
        time.sleep(2)
        print('\n\nPress enter to return to main menu...')
        input("")
 
    def importSettings(self):
        """Import daily settings from enigma"""
 
        self.ring1, self.ring2, self.ring3, self.ring4, self.ring5 = 0, 0, 0, 0, 0 #Initialise the ring setting values
        self.start1, self.start2, self.start3, self.start4, self.start5 = 1, 2, 3, 4, 5
 
        database = data() #Create a data object
 
        dailySettings = database.readData() #Import the daily settings
        row = dailySettings[0] #Assign the imported data to the row variable
 
        #FORMAT
        #[(1, 'IV V II', '20 09 23', 'TNUVHCQYOMFDRBAIKZGJSXEPLW', 'nft jlx nzj mbu')]
 
        rotors = row[1] #Fetch the data at the first index
        rotorL, rotorM, rotorR = rotors.split() #And split it into 3 seperate rotors
        rotorL, rotorM, rotorR = str(rotorL), str(rotorM), str(rotorR) #Ensure they are string variables
 
        ringSettings = row[2] #Fetch the data at the second index 
        ringL, ringM, ringR = ringSettings.split() #And split it into 3 seperate ring positions
        ringL, ringM, ringR = int(ringL), int(ringM), int(ringR) #Ensure they are integer variables
 
        plugboardPairs = row[3] #Assign the element at the third index to the plugboard pairs
        charGroups = row[4] #Assign the element at the fourth index to the character groups
 
        startL, startM, startR = input('\nEnter rotor starting positions: ').split() #Prompt the user to enter the rotor starting positions
        startL, startM, startR = int(startL), int(startM), int(startR) #Ensure they are integer variables
 
        reflectorType = input("Enter reflector type: ").upper() #Prompt user to enter reflector type
 
        ring = {'I':'ring1', 'II':'ring2', 'III':'ring3', 'IV':'ring4', 'V':'ring5'} #Match rotor types to string of their ring setting variables 
        start = {'I':'start1', 'II':'start2', 'III':'start3', 'IV':'start4', 'V':'start5'} #Match rotor types to string of their start position variables
 
        setLStart = str(start.get(rotorL)) #Get the string of the rotors starting position
        setMStart = str(start.get(rotorM))
        setRStart = str(start.get(rotorR))
 
        vars(self)[setLStart] = startL #Create a dynamic variable using the string of the starting position and set its value as the input value for the left rotor starting position
        vars(self)[setMStart] = startM
        vars(self)[setRStart] = startR
 
        setLRing = str(ring.get(rotorL)) #Get the string of the rotors ring setting 
        setMRing = str(ring.get(rotorM))
        setRRing = str(ring.get(rotorR))
 
        vars(self)[setLRing] = ringL #Create a dynamic variable using the string of the ring setting and set its value as the input value for the left rotor ring setting 
        vars(self)[setMRing] = ringM
        vars(self)[setRRing] = ringR
 
        print("\n************     Imported Settings     ************") #Output the imported settings to the user
        print("Left Rotor:", rotorL + ", Ring position:", str(ringL) + ", Start position:", str(startL))
        print("Middle Rotor:", rotorM + ", Ring position:", str(ringM) + ", Start position:", str(startM))
        print("Right Rotor:", rotorR + ", Ring position:", str(ringR) + ", Start position:", str(startR))
        print("Kenngruppen:", charGroups)
 
        print("Plugboard:", plugboardPairs)
        print("Reflector type:", reflectorType + '\n')
 
        #                     ABCDEFGHIJKLMNOPQRSTUVWXYZ
        self._rotor1 = rotor('EKMFLGDQVZNTOWYHXUSPAIBRCJ','Y','Q', self.start1, self.ring1) #Create a rotor object using the user input for the starting position and ring setting values
        self._rotor2 = rotor('AJDKSIRUXBLHWTMCQGZNPYFVOE','M','E', self.start2, self.ring2)
        self._rotor3 = rotor('BDFHJLCPRTXVZNYEIWGAKMUSQO','D','V', self.start3, self.ring3)
        self._rotor4 = rotor('ESOVPZJAYQUIRHXLNFTGKDCMWB','R','J', self.start4, self.ring4)
        self._rotor5 = rotor('VZBRGITYUPSDNHLXAWMJQOFECK','H','Z', self.start5, self.ring5)
 
        self._UKWA = reflector('AE BJ CM DZ FL GY HX IV KW NR OQ PU ST') #Create the default reflector objects
        self._UKWB = reflector('AY BR CU DH EQ FS GL IP JX KN MO TZ VW')
        self._UKWC = reflector('AF BV CP DJ EI GO HY KR LZ MX NW QT SU')
 
        rotors = {'I':self._rotor1, 'II':self._rotor2, 'III':self._rotor3, 'IV':self._rotor4, 'V':self._rotor5} #Match the rotor types to their objects
        reflectors = {'A':self._UKWA, 'B':self._UKWB, 'C':self._UKWC} #Match the reflector types to their objects
 
        self._rotorL = rotors.get(rotorL) #Assign the corresponding rotor object to the rotor
        self._rotorM = rotors.get(rotorM)
        self._rotorR = rotors.get(rotorR)
 
        self._UKW = reflectors[reflectorType] #Assign the corresponding reflector object to the reflector
 
        self._plugboard = plugboard(plugboardPairs) #Assign the corresponding plugboard object to the plugboard
 
    def Run(self):
        choice = ""
        while choice != "6": #While the user has not exited the application 
            self.displayMenu() #Display the main menu
            choice = input() #Read in user input
            if choice == "1": #If user has chosen the first option
                self.GetUserSettings() #Run GetUserSettings
                self.encryptMessage() #Then run encryptMessage
            elif choice == "2": #If user has chosen the second option
                self.createCustomWiring() #Run createCustomWiring
                self.encryptMessage() #Run encryptMessage
            elif choice == "3": #If user has chosen the third option
                self.importSettings() #Run importSettings
                self.encryptMessage() #Run encryptMessage
            elif choice == "4": #If user has chosen the fourth option
                self.generateSettings() #Run generateSettings
            elif choice == "5": #If user has chosen the fifth option
                self.help() #Run help
            elif choice == "6": #If user has chosen the sixth option
                print('\nThank you for using Enigma machine simulator. Goodbye!') #Output an end message
                time.sleep(4) #Wait 4 seconds before exiting the application
 
    def singleStep(self, rotorL, rotorM, rotorR):
        Rpos = rotorR.GetRotorPosition() #Find the current position of the right rotor
        Rturn = rotorR.GetTurnoverNum() #Find the turnover position of the right rotor
 
        Rturn += 1 #Increment the right rotors turnover position by one
        if Rpos == Rturn: #If the rotors current position is equal to the incremented turnover position of the right rotor
            if self.visuals == 'Y': #And the user has chosen to see the encryption
                print('Single Step') #Notify them that a single step will occur
            rotorM.incrementRotor() #Increment the middle rotor


def Main():
    """Creates the simulation object and runs the simulation"""
    EnigmaSim = simulation() #Creates the simulation object
    EnigmaSim.Run() #Runs the simulation

#If the module is a standalone program, the Main function will be executed
#Otherwise, it can act as a module in another program 
if __name__ == "__main__": 
    Main()
