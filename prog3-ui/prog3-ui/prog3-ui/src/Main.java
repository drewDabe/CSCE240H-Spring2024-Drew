import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

class Item {
    private String name;
    private String textContent;
    private int wordCount;
    private int lineCount;
    private int charCount;

    public Item(String itemName) {
        this.name = itemName;
        this.textContent = "";
        this.wordCount = 0;
        this.lineCount = 0;
        this.charCount = 0;
    }

    public void updateStatistics(String line) {
        textContent += line + "\n";
        wordCount += line.split("\\s+").length;
        charCount += line.length();
        lineCount++;
    }

    public String getTextContent() {
        return textContent;
    }

    public String getName() {
        return name;
    }

    public int getWordCount() {
        return wordCount;
    }

    public int getLineCount() {
        return lineCount;
    }

    public int getCharCount() {
        return charCount;
    }
}

class Part {
    private String name;
    private List<Item> items;

    public Part(String partName) {
        this.name = partName;
        this.items = new ArrayList<>();
    }

    public void addItem(Item itemName) {
        if (itemName == null) return;
        items.add(itemName);
    }

    public String getName() {
        return name;
    }

    public List<Item> getItems() {
        return items;
    }
}

public class Main {
    
    public static void main(String[] args) {
        boolean running = true;
        Scanner keyboard = new Scanner(System.in);
        ArrayList<Part> GMEparts = countTextStatistics("prog3-ui\\prog3-ui\\txt\\gme.txt");
        ArrayList<Part> TSLAparts = countTextStatistics("prog3-ui\\prog3-ui\\txt\\tsla.txt");
        while (running) {
            System.out.println("What would you like to know? Enter quit or q to exit.");
            String line = keyboard.nextLine();
            if (line.toLowerCase().equals("quit") || line.equals("q")) {
                running = false;
                break;
            }
            String comp = checkForCompany(line);
            if (comp == null) { //If not specified it will default to gamestop
                handleUserInput(line, GMEparts);
            }
            else if (comp.equals("gme")) { // Check to see which company is specified
                handleUserInput(line, GMEparts);
            }
            else if (comp.equals("tsla")) {
                handleUserInput(line, TSLAparts);
            }
        }
        keyboard.close();
    }

    public static ArrayList<Part> countTextStatistics(String filename) {
        try (BufferedReader reader = new BufferedReader(new FileReader(filename))) {

            String line;
            boolean tableContent = false;
            ArrayList<Part> parts = new ArrayList<Part>();
            Part activePart = null;
            Item activeItem = null;

            while ((line = reader.readLine()) != null) {
                if (line.contains("PART I") && !tableContent) {
                    tableContent = true; // Table of contents has started
                    continue;
                }
                if (tableContent) {
                    if (line.equals("PART I")) {
                        break; // Actual content found
                    }
                }
            }
            activePart = new Part("PART I");

            while ((line = reader.readLine()) != null) {
                if (line.contains("PART")) {
                    activePart.addItem(activeItem);
                    parts.add(activePart); // Create a new Part
                    activePart = new Part(line); // Set activePart to the newly created Part
                    continue;
                }
                if (line.contains("ITEM")) {
                    activePart.addItem(activeItem); // Add a new Item to the current Part
                    activeItem = new Item(line); // Set activeItem to the newly created Item
                    activeItem.updateStatistics(line);
                    continue;
                }

                if (activeItem != null) {
                    activeItem.updateStatistics(line); // Update statistics for the active Item
                }
            }
            return parts;
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }
    }

    private static void handleUserInput(String searchOption, ArrayList<Part> parts) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter("output.txt", true))) {
            searchOption = searchOption.toLowerCase();
            searchOption = searchOption.replaceAll("[^a-zA-Z0-9]", " "); // Get rid of special characters.
            boolean printed = false; // Lazy way to see if anything was ever found
            // Output the information
            String company = checkForCompany(searchOption);
            for (Part part : parts) {
                if (checkPartInString(searchOption, part.getName(), parts)) {
                    printed = true;
                    writer.write("Part: " + part.getName() + "\n");
                    System.out.println("Part: " + part.getName());

                    for (Item item : part.getItems()) {
                        writer.write("\tItem: " + item.getName() + "\n");
                        writer.write("\t\tWord Count: " + item.getWordCount() + "\n");
                        writer.write("\t\tLine Count: " + item.getLineCount() + "\n");
                        writer.write("\t\tCharacter Count: " + item.getCharCount() + "\n");
                        writer.write(item.getTextContent());

                        System.out.println("\tItem: " + item.getName());
                        System.out.println("\t\tWord Count: " + item.getWordCount());
                        System.out.println("\t\tLine Count: " + item.getLineCount());
                        System.out.println("\t\tCharacter Count: " + item.getCharCount());
                        System.out.println(item.getTextContent());
                    }
                }
                else {
                    for (Item item : part.getItems()) {
                        String foundtxt = checkItemInString(searchOption, item.getName());
                        if (!foundtxt.equals("NA")) {
                            printed = true;
                            System.out.println(foundtxt);
                            writer.write(foundtxt + "\n");
                            writer.write("\tItem: " + item.getName() + "\n");
                            writer.write("\t\tWord Count: " + item.getWordCount() + "\n");
                            writer.write("\t\tLine Count: " + item.getLineCount() + "\n");
                            writer.write("\t\tCharacter Count: " + item.getCharCount() + "\n");
                            writer.write(item.getTextContent());

                            System.out.println("\tItem: " + item.getName());
                            System.out.println("\t\tWord Count: " + item.getWordCount());
                            System.out.println("\t\tLine Count: " + item.getLineCount());
                            System.out.println("\t\tCharacter Count: " + item.getCharCount());
                            System.out.println(item.getTextContent());
                        }
                    }
                }
            }
            if (!printed && company != null) { // Print the first part if it only has a company name
                Part part = parts.get(0);
                writer.write("Part: " + part.getName() + "\n");
                System.out.println("Part: " + part.getName());

                for (Item item : part.getItems()) {
                    writer.write("\tItem: " + item.getName() + "\n");
                    writer.write("\t\tWord Count: " + item.getWordCount() + "\n");
                    writer.write("\t\tLine Count: " + item.getLineCount() + "\n");
                    writer.write("\t\tCharacter Count: " + item.getCharCount() + "\n");
                    writer.write(item.getTextContent());

                    System.out.println("\tItem: " + item.getName());
                    System.out.println("\t\tWord Count: " + item.getWordCount());
                    System.out.println("\t\tLine Count: " + item.getLineCount());
                    System.out.println("\t\tCharacter Count: " + item.getCharCount());
                    System.out.println(item.getTextContent());
                }
            }
            else if (!printed) { // Nothing was found, nothing was specified/detected
                System.out.println("I do not know this information");
            }
            
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static String checkForCompany(String s) {
        String[] splited = s.split("\\s+");
        if (checkWordInList(splited, "gme") != -1 || checkWordInList(splited, "gamestop") != -1) return "gme";
        if (checkWordInList(splited, "tsla") != -1 || checkWordInList(splited, "tesla") != -1) return "tsla";
        return null;
    }

    public static boolean checkPartInString(String s, String partName, ArrayList<Part> parts) {
        if (s.toLowerCase().equals("tell me everything")) return true; // You can input "tell me everything" and it will print everything
        String[] splited = s.split("\\s+");
        int lookforPart = 0;
        while (lookforPart != -1) {
            lookforPart = checkWordInList(splited, "part");
            if (lookforPart != -1) { // See if the input contains the word "part" at any point
                if (lookforPart < splited.length) {
                    String checkIfNum = splited[lookforPart+1].toLowerCase();
                    if (checkIfNum.equals("1") || checkIfNum.equals("i") || checkIfNum.equals("one")) {
                        if (partName.equals(parts.get(0).getName())) return true;
                        return false;
                    }
                    else if (checkIfNum.equals("2") || checkIfNum.equals("ii") || checkIfNum.equals("two")) {
                        if (partName.equals(parts.get(1).getName())) return true;
                        return false;
                    }
                    else if (checkIfNum.equals("3") || checkIfNum.equals("iii") || checkIfNum.equals("three")) {
                        if (partName.equals(parts.get(2).getName())) return true;
                        return false;
                    }
                    else if (checkIfNum.equals("4") || checkIfNum.equals("iv") || checkIfNum.equals("four")) {
                        if (partName.equals(parts.get(3).getName())) return true;
                        return false;
                    }
                    else {
                        splited[lookforPart] = ""; // Get rid of the word "part" that was found
                    }
                }
            }
        }
        return false;
    }

    public static String checkItemInString(String s, String itemName) {
        s = s.toLowerCase();
        String[] splited = s.split("\\s+");
        int lookforItem = 0;
        while (lookforItem != -1) {
            lookforItem = checkWordInList(splited, "item");
            if (lookforItem != -1) {
                if (lookforItem < splited.length) {
                    if (itemName.toLowerCase().contains(splited[lookforItem] + " " + splited[lookforItem + 1]))
                        return "Responding with " + itemName + " from input value: '" + splited[lookforItem] + " " + splited[lookforItem+1] + "'"; 
                    splited[lookforItem] = "";
                }
                else {
                    splited[lookforItem] = "";
                }
            }
        }
        splited = s.split("\\s+");
        for (int i = 0; i < splited.length; i++) {
            if (itemName.toLowerCase().contains(splited[i]) && (!splited[i].equals("item") && !splited[i].equals("") && splited[i].length() > 5)) return "Responding with " + itemName + " from input value: '" + splited[i] + "'";
        }
        return "NA";
    }

    public static int checkWordInList(String[] sList, String str) {
        str = str.toLowerCase();
        for (int i = 0; i < sList.length; i++) {
            if(sList[i].toLowerCase().contains(str)) return i;
        }
        return -1;
    }
}
