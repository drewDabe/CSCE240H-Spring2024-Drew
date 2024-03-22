from collections import defaultdict
from Levenshtein import distance as levenshtein_distance

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
        for phrase in self.phrases:
            match_value = self.calculate_match_value(phrase, s)
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
        dist = levenshtein_distance(s1, s2, weights=(2,4,5))
        #print(max_len)
        #print(float(dist))
        return dist

    #def __str__(self, parts):
    #    s = ""
    #    for part in self.parts_in_query:
    #        s += str(parts[part]) + "\n"
    #    for item in self.items_in_query:
    #        s += str(item) + "\n"
    #    return s

def count_text_statistics(filename):
    parts = []
    active_part = None
    active_item = None
    table_content = False
    over = True

    with open(filename, 'r', encoding='utf-8') as file:  # Specify the encoding as 'utf-8'
        for line in file:
            line = line.strip() # Remove leading/trailing whitespace and newline characters
            if "PART I" in line and not table_content and over:
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
        parts.append(active_part)

    return parts


def check_for_gamestop(s):
    s_list = s.split()
    return any(word.lower() in s_list for word in ["gme", "gamestop", "gstop", "gmstp", "gmestop", "gamestop's", "gme's", "gamestops", "gmes"])

def check_for_tesla(s):
    s_list = s.split()
    return any(word.lower() in s_list for word in ["tsla", "tesla", "tsl", "tesl", "tesla's", "teslas", "tslas", "tsla's"])

def main():
    running = True
    GME_parts = count_text_statistics("txt\gme.txt") # change paths as needed
    TSLA_parts = count_text_statistics("txt\tsla.txt")
    
    system_response = [
        Query(["hey", "hi", "hello", "sup", "howdy"], sample_out="Hello"), #Handle Greeting
        Query(["part I", "part 1", "first part"], "Part I"),
        Query(["part II", "part 2", "second part"], "Part II"),
        Query(["part iii", "part 3", "third part"], "Part III"),
        Query(["part iv", "part 4", "fourth part"], "Part IV"),
        Query(["item 1", "item i", "business"], None, "Item 1",),
        Query(["item 1a", "risks", "risk factors"], None, "Item 1A"),
        Query(["item 1b", "staff comments", "unresolved comments"], None, "Item 1B"),
        Query(["item 2", "item ii", "properties"], None, "Item 2"),
        Query(["item 3", "legal proceedings", "law"], None, "Item 3"),
        Query(["item 4", "mine safety", "safety disclosures"], None, "Item 4"),
        Query(["item 5", "equity securities", "market for registrant", "Registrant's Common Equity", "stockholder matters"], None, "Item 5"),
        Query(["item 6", "reserved", "information reserved"], None, "Item 6"),
        Query(["item 7", "Financial Condition", "Results of Operations", "Management's Discussion"], None, "Item 7"),
        Query(["item 7a", "quantitative disclosures", "qualitative disclosures", "market risk"], None, "Item 7A"),
        Query(["item 8", "financial statements", "supplementary data"], None, "Item 8"),
        Query(["item 9", "Accountants on Accounting", "Financial Disclosure", "Changes in Accountants", "Disagreements with Accountants"], None, "Item 9"),
        Query(["item 9a", "Controls", "Proceedures"], None, "Item 9A"),
        Query(["item 9b", "other information", "miscellaneous info"], None, "Item 9B"),
        Query(["Item 9c", "Foreign disclosures", "Regarding Foreign Jurisdictions", "Prevent Inspections"], None, "Item 9C"),
        Query(["item 10", "Directors", "Executive Officers", "corporate governance"], None, "Item 10"),
        Query(["item 11", "Executive compensation"], None, "Item 11"),
        Query(["item 12", "Security ownership", "Stockholder Matters", "Beneficial Owners"], None, "Item 12"),
        Query(["item 13", "Director Independence", "Relationships", "Related Transactions"], None, "Item 13"),
        Query(["item 14", "Principal accountant", "fees and services"], None, "Item 14"),
        Query(["item 15", "Exhibits", "Financial Statement Schedule"], None, "Item 15"),
        Query(["item 16", "Summary", "Form 10-K Summary"], "Item 16"),
        Query(["tell me everything"], part_list=["Part I", "Part II", "Part III", "Part IV"])
    ]

    while running:
        user_input = input("What would you like to know? Enter 'quit' or 'q' to exit.\n")
        if user_input.lower() in ["quit", "q"]:
            running = False
            break
        if check_for_gamestop(user_input):
            handle_user_input(user_input, GME_parts, system_response)
        elif check_for_tesla(user_input):
            handle_user_input(user_input, TSLA_parts, system_response)
        else:
            handle_user_input(user_input, GME_parts, system_response)


def handle_user_input(line, parts, responses):
    min = 9223372036854775807
    average_score = 0.0
    for q in responses:
        q.calculate_value(line)
        average_score += q.get_query_value()
        if q.get_query_value() < min:
            min = q.get_query_value()
    average_score = average_score / len(responses)
    #print(average_score)
    if average_score - min < 10:
        print(line)
        print("I do not know this information")
        return
    f = open("output.txt", "w", encoding='utf-8')
    #print(min)
    for p in parts:
        printed = False
        for q in responses:
            if q.get_query_value() <= min:
                if p == q.get_part():
                    print(p)
                    printed = True
                    f.write(str(p))
                    break
        if printed:
            continue
        for i in p.get_items():
            for q in responses:
                if q.get_query_value() <= min:
                    if i == q.get_item():
                        print(i)
                        f.write(str(i))
                        break

if __name__ == "__main__":
    main()
