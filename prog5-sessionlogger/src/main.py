from collections import defaultdict
from Levenshtein import distance as levenshtein_distance
import time
import csv
import statistics
import sys

class Item:
    def __init__(self, item_name):
        self.name = item_name
        self.text_content = ""
        self.word_count = 0
        self.line_count = 0
        self.char_count = 0

    def update_statistics(self, line):
        self.text_content += line + "\n"
        self.word_count += len(line.split())
        self.char_count += len(line)
        self.line_count += 1

    def __str__(self):
        return f"\tItem: {self.name}\n\t\tWord Count: {self.word_count}\n\t\tLine Count: {self.line_count}\n\t\tCharacter Count: {self.char_count}\n{self.text_content}"
    
    def __eq__(self, itemName):
        if itemName == None:
            return False
        return itemName.lower() in self.name.lower()


class Part:
    def __init__(self, part_name):
        self.name = part_name
        self.items = []

    def add_item(self, item_name):
        if item_name is not None:
            self.items.append(item_name)

    def get_items(self):
        return self.items

    def __str__(self):
        s = f"Part: {self.name}\n"
        for item in self.items:
            s += str(item) + "\n"
        return s
    
    def __eq__(self, partName):
        if partName == None:
            return False 
        if partName == True:
            return True
        return self.name.lower() == partName.lower()
    

class Query:
    def __init__(self, user_phrases, parts=None, items=None, sample_out=None, part_list=None):
        self.phrases = user_phrases
        self.parts_in_query = parts
        self.items_in_query = items
        self.sys_output = sample_out
        self.part_list = part_list
        self.query_value = 9223372036854775807

    def calculate_value(self, s):
        self.query_value = 9223372036854775807
        for phrase in self.phrases:
            match_value = self.calculate_match_value(phrase.lower(), s.lower())
            if match_value < self.query_value:
                self.query_value = match_value

    def get_query_value(self):
        return self.query_value

    def get_part(self):
        if self.part_list != None:
            return True
        return self.parts_in_query
    
    def get_item(self):
        return self.items_in_query

    def match_part(self, parts):
        return self.parts_in_query in parts

    @staticmethod
    def calculate_match_value(s1, s2):
        max_len = max(len(s1), len(s2))
        if max_len == 0:
            return 9223372036854775807
        dist = levenshtein_distance(s1, s2, weights=(2,4,5)) #Change weighting to get the balance you want
        #print(max_len)
        #print(float(dist))
        return dist

def count_text_statistics(filename):
    parts = []
    active_part = None
    active_item = None
    table_content = False
    over = True

    with open(filename, 'r', encoding='utf-8') as file:  # Specify the encoding as 'utf-8'
        for line in file:
            line = line.strip() # Remove leading/trailing whitespace and newline characters
            if "PART I" in line and not table_content and over: # Maybe could be optimized I just copied everything over
                table_content = True
                continue
            if table_content and over:
                if line == "PART I": 
                    over = False
                    table_content = False
                    active_part = Part("PART I")
                continue

            if "PART" in line:
                parts.append(active_part)
                active_part = Part(line)
                continue
            if "ITEM" in line:
                active_part.add_item(active_item)
                active_item = Item(line)
                active_item.update_statistics(line)
                continue

            if active_item is not None:
                active_item.update_statistics(line)
        active_part.add_item(active_item)
        parts.append(active_part)

    return parts


def check_for_gamestop(s):
    s_list = s.split()
    return any(word.lower() in s_list for word in ["gme", "gamestop", "gstop", "gmstp", "gmestop", "gamestop's", "gme's", "gamestops", "gmes"])

def check_for_tesla(s):
    s_list = s.split()
    return any(word.lower() in s_list for word in ["tsla", "tesla", "tsl", "tesl", "tesla's", "teslas", "tslas", "tsla's"])

def main():
    if len(sys.argv) < 2:
        running = True
        GME_parts = count_text_statistics("..\\data\\gme.txt") # change paths as needed
        TSLA_parts = count_text_statistics("..\\data\\tsla.txt")
        
        system_response = [
            Query(["hey", "hi", "hello", "sup", "howdy"], sample_out="Hello"), #Handle Greeting
            Query(["thanks", "thank you", "thx"], sample_out="No problem. Let me know if you need anything else"), # You can really add anything you want here, but
            Query(["part i", "part 1", "first part"], "Part I"), # It may skew some of the math I do to calculate distance if you add a million 3 letter words
            Query(["part ii", "part 2", "second part"], "Part II"), # Just keep that in mind, you might need to change weight for added letters or # of standard deviations 
            Query(["part iii", "part 3", "third part"], "Part III"),
            Query(["part iv", "part 4", "fourth part"], "Part IV"),
            Query(["item 1", "item i", "business"], None, "Item 1.",),
            Query(["item 1a", "risks", "risk factors"], None, "Item 1A"),
            Query(["item 1b", "staff comments", "unresolved comments"], None, "Item 1B"),
            Query(["item 2", "item ii", "properties"], None, "Item 2"),
            Query(["item 3", "legal proceedings", "law"], None, "Item 3"),
            Query(["item 4", "mine safety", "safety disclosures"], None, "Item 4"),
            Query(["item 5", "equity securities", "market for registrant", "Registrant's Common Equity", "stockholder matters"], None, "Item 5"),
            Query(["item 6", "reserved", "information reserved"], None, "Item 6"),
            Query(["item 7", "Financial Condition", "Results of Operations", "Management's Discussion"], None, "Item 7."),
            Query(["item 7a", "quantitative disclosures", "qualitative disclosures", "market risk"], None, "Item 7A"),
            Query(["item 8", "financial statements", "supplementary data"], None, "Item 8"),
            Query(["item 9", "Accountants on Accounting", "Financial Disclosure", "Changes in Accountants", "Disagreements with Accountants"], None, "Item 9."),
            Query(["item 9a", "Controls", "Proceedures"], None, "Item 9A"),
            Query(["item 9b", "other information", "miscellaneous info"], None, "Item 9B"),
            Query(["Item 9c", "Foreign disclosures", "Regarding Foreign Jurisdictions", "Prevent Inspections"], None, "Item 9C"),
            Query(["item 10", "Directors", "Executive Officers", "corporate governance"], None, "Item 10"),
            Query(["item 11", "Executive compensation"], None, "Item 11"),
            Query(["item 12", "Security ownership", "Stockholder Matters", "Beneficial Owners"], None, "Item 12"),
            Query(["item 13", "Director Independence", "Relationships", "Related Transactions"], None, "Item 13"),
            Query(["item 14", "Principal accountant", "fees and services"], None, "Item 14"),
            Query(["item 15", "Exhibits", "Financial Statement Schedule"], None, "Item 15"),
            Query(["item 16", "Summary", "Form 10-K Summary"], None, "Item 16"),
            Query(["tell me everything"], part_list=["Part I", "Part II", "Part III", "Part IV"])
        ]
        user_queries = 0
        system_responses = 0

        prog_output_ver = "4-4VerFinal_dabe"
        current_time = time.strftime("%Y%m%d_%H%M%S")
        global filename # This is good programming practices I think
        filename = f"..\\data\\chat_sessions\\{prog_output_ver}_{current_time}.txt"
        now = time.time()
        while running:
            user_input = input("What would you like to know? Enter 'quit' or 'q' to exit.\n")
            if user_input.lower() in ["quit", "q"]:
                with open('..\\data\\chat_statistics.csv', 'a', newline='') as csvfile:
                    fieldnames = ['chat_file', 'user_utterance', 'system_utterance', 'time']
                    # Can just go by num, no need to add its own id. According to docs: Regardless of how the fieldnames are determined, the dictionary preserves their original ordering.
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writerow({'chat_file': filename, 'user_utterance': user_queries, 'system_utterance': system_responses, 'time': format(time.time() - now, ".2f")})
                running = False
                break
            user_queries += 1 # Should only be called when the user puts in something that isn't q or quit
            if check_for_gamestop(user_input):
                if handle_user_input(user_input, GME_parts, system_response):
                    system_responses += 1
            elif check_for_tesla(user_input):
                if handle_user_input(user_input, TSLA_parts, system_response):
                    system_responses += 1
            else: #By default assume asking about GME
                if handle_user_input(user_input, GME_parts, system_response):
                    system_responses += 1
    else:
        option = sys.argv[1]
        if option == "-summary":
            total_chats = 0
            user_queries = 0
            system_responses = 0
            total_duration = 0
            with open('..\\data\\chat_statistics.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    total_chats += 1
                    user_queries += int(row['user_utterance'])
                    system_responses += int(row['system_utterance'])
                    total_duration += float(row['time']) # Stored with 2 decimals but will round to .9999 if not careful
            print(f'There are {total_chats} chats to date with user asking {user_queries} times and system respond {system_responses} times. Total duration is {format(total_duration, ".2f")} seconds')
        elif option == "-showchat":
            if len(sys.argv) < 3:
                print("Usage: python main.py -showchat <chat_id>")
                return
            chat_id = int(sys.argv[2]) # Will call an error if not a number but i want that so
            i = 1 # Header row means need to start 1 to get expected number
            with open('..\\data\\chat_statistics.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if i == chat_id:
                        f = open(row['chat_file'], 'r')
                        print(f"Chat {chat_id} chat is: \n\n")
                        print(f.read()) # Should print everything regardless of format, so the txt files can be however they want
                        return
                    i += 1
                print(f"ERROR: there are only {i-1} chat sessions. Please choose a valid number")
        elif option == "-showchat-summary": # Basically same as above
            if len(sys.argv) < 3:
                print("Usage: python main.py -showchat-summary <chat_id>")
                return
            chat_id = int(sys.argv[2])
            i = 1
            with open('..\\data\\chat_statistics.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if i == chat_id:
                        print(f'Chat {chat_id} has user asking {row["user_utterance"]} times and system respond {row["system_utterance"]} times. Total duration is {row["time"]} seconds')
                        return
                    i += 1
            print(f"ERROR: there are only {i-1} chat sessions. Please choose a valid number")
        else:
            print("Invalid option")

def handle_user_input(line, parts, responses):
    min = 9223372036854775807
    score_list = []
    for q in responses:
        q.calculate_value(line)
        score_list.append(q.get_query_value())
        if q.get_query_value() < min:
            min = q.get_query_value()
    f = open(filename, "a", encoding='utf-8') # At this point we know the user input is valid or at least didn't cause an error, we can write it
    f.write(f"\nUser: {line}\n") # Probably best to open and close the file everytime because I know python can cause some exestential horrors if you improperly access files
    passing_score = statistics.mean(score_list) - (statistics.stdev(score_list)*1.8) # This is the threshold for something to print, change as wanted. Probably calculate the 2 to be closer or further
    s_list = line.split()
    if (any(word.lower() in s_list for word in ["item", "part"])): #cheaters way, i'll come back to it
        passing_score = min
    if passing_score < min:
        print(line)
        print("I do not know this information")
        f.close()
        return False
    response_to_print = []
    for q in responses: # Check for other outputs while shortening the amount that needs to be gone in for loop to less, could be further refined
        if (q.get_query_value() <= passing_score):
            if (q.sys_output != None): 
                print(q.sys_output)
                f.write(f'System: {q.sys_output}')
                f.close()
                return True
            response_to_print.append(q)
    for p in parts:
        printed = False
        for q in response_to_print:
            if p == q.get_part():
                print(p)
                printed = True
                f.write(f'System: Printed information about... {p.name}\n')
                break
        if printed: # Continue actually means skip. It's kinda confusing. pass means continue
            continue
        for i in p.get_items():
            for q in response_to_print:
                if i == q.get_item():
                    print(i)
                    f.write(f'System: Printed information about... {i.name}\n')
                    break
    f.close()
    return True

if __name__ == "__main__":
    main()