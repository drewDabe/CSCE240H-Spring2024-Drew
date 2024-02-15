import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

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
    public static List<Part> parts;
    public static void main(String[] args) {
        if (args.length != 2 || !args[0].equals("-t")) {
            System.err.println("Usage: java Main -t <search_option>");
            return;
        }

        String searchOption = args[1];
        countTextStatistics("prog2processor\\prog2processor\\txt\\gme.txt", searchOption);
    }

    public static void countTextStatistics(String filename, String searchOption) {
        try (BufferedReader reader = new BufferedReader(new FileReader(filename));
             BufferedWriter writer = new BufferedWriter(new FileWriter("output.txt", true))) {

            String line;
            boolean tableContent = false;
            parts = new ArrayList<>();
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
            searchOption = searchOption.toLowerCase();
            // Output the information
            for (Part part : parts) {
                if (checkPartInString(searchOption, part.getName())) {
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
                            System.out.println(foundtxt);
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
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static boolean checkPartInString(String s, String partName) {
        if (s.toLowerCase().equals("all information")) return true; // You can input "all information" and it will print everything
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
            if (itemName.toLowerCase().contains(splited[i]) && (!splited[i].equals("item") && !splited[i].equals("") && splited[i].length() > 3)) return "Responding with " + itemName + " from input value: '" + splited[i] + "'";
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
