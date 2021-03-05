package project1;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Stack;
import java.util.TreeMap;

/**
 * This class represents a state of the game.
 *
 * @author Allen Westgate, Bernardo Santos, and Ryan Farrell
 */
public class GameState {

    private Map<String, Stack<Card>> foundation = new TreeMap<>(); // Foundation spots, mapped by suits, so: {"C": Stack<Card>, "D": Stack<Card> ... }
    private ArrayList<Card> freecells = new ArrayList<>(); // Free cells where cards can be put without worrying about suit or value.
    private ArrayList<ArrayList<Card>> piles = new ArrayList<>(); // All the piles as a list of lists. The first pile is the first item of the list and so on.
    private int heuristic; // The heuristic value of the state.
    private ArrayList<Action> path = new ArrayList<>(); // The path to get to the state.

    /**
     * This is the constructor method responsible for generating the initial
     * state, where no parameters are needed. Subject to change!
     */
    public GameState() {

    }

    /**
     * This is the constructor method responsible for generating a state that is
     * not the initial one.
     *
     * @param foundation the foundation spots of the state.
     * @param freecells the free cells of the state.
     * @param piles the piles of the state.
     */
    public GameState(Map<String, Stack<Card>> foundation, ArrayList<Card> freecells, ArrayList<ArrayList<Card>> piles, ArrayList<Action> actions) {

        // Build the foundations according to the values passed through parameters.
        foundation.entrySet().forEach(entry -> {
            String key = entry.getKey();
            Stack<Card> stackOfCards = new Stack<>();
            this.foundation.put(key, stackOfCards);
            for (Card card : entry.getValue()) {
                this.foundation.get(key).add(card);
            }

        });

        // Build the freecells.
        freecells.forEach(card -> {
            this.freecells.add(card);
        });

        // Build the piles.
        for (int i = 0; i < piles.size(); i++) {
            ArrayList<Card> cardArray = new ArrayList<>();
            this.piles.add(cardArray);
            for (int j = 0; j < piles.get(i).size(); j++) {
                Card card = piles.get(i).get(j);
                this.piles.get(i).add(card);
            }
        }

        // Build the path.
        for (int j = 0; j < actions.size(); j++) {
            this.path.add(actions.get(j));
        }
    }

    /**
     * This method generates the deck of cards for the game and shuffles it.
     *
     * @return a Deck of cards, randomly shuffled.
     */
    public Deck generateDeck() {
        ArrayList<String> suits = new ArrayList<>() {
            {
                add("S");
                add("C");
                add("D");
                add("H");
            }
        };

        ArrayList<Integer> numbers = new ArrayList<>();
        for (int i = 1; i <= 13; i++) {
            numbers.add(i);
        }

        return new Deck(suits, numbers);
    }

    /**
     * This method generates the initial state of the game by initializing the
     * free cells, the piles and the foundations.
     */
    public void generateInitialState(int numFreecells) {
        // Initialize the free cells.
        freecells = new ArrayList<>() {
            {
                for (int i = 0; i < numFreecells; i++) {
                    add(null);
                }
            }
        };

        // Initialize the piles.
        piles = new ArrayList<>();

        // Initialize the foundation spots.
        foundation = new TreeMap<>() {
            {
                put("C", new Stack());
                put("D", new Stack());
                put("H", new Stack());
                put("S", new Stack());
            }
        };

        // Generate the deck of cards.
        Deck deck = generateDeck();

        // Limiters of indices used to populate the piles correctly.
        ArrayList<Integer> limiters = new ArrayList<>() {
            {
                add(-1);
                add(6);
                add(13);
                add(20);
                add(27);
                add(33);
                add(39);
                add(45);
                add(51);
            }
        };

        // Populate piles by adding a card to each spot.
        for (int i = 0; i < 8; i++) {
            ArrayList<Card> stackPile = new ArrayList<>();
            List<Card> cards = deck.getSubDeck(limiters.get(i) + 1, limiters.get(i + 1) + 1);

            for (int j = 0; j < cards.size(); j++) {
                stackPile.add(cards.get(j));
            }

            piles.add(stackPile);
        }

    }

    /**
     * This method prints the state of the game.
     */
    public void printState() {
        System.out.println("FreeCell Solitaire");
        System.out.print("Free Cells: ");
        for (int f = 0; f < freecells.size(); f++) {
            if (freecells.get(f) != null) {
                System.out.print(" [" + freecells.get(f) + "]");
            } else {
                System.out.print(" [ ] ");
            }
        }

        System.out.print("\nFoundations: ");
        foundation.entrySet().forEach(entry -> {
            if (entry.getValue().isEmpty()) {
                System.out.print(entry.getKey() + ":[ ] ");
            } else {
                System.out.print(entry.getKey() + ":[");
                entry.getValue().forEach(card -> {
                    if (!card.equals(entry.getValue().peek())) {
                        System.out.print(card + ",");
                    } else {
                        System.out.print(card);
                    }
                });

                System.out.print("]");
            }
        });

        System.out.print("\n");
        for (int k = 0; k < 65; k++) {
            System.out.print("-");
        }

        System.out.print("\n|");
        for (int i = 1; i < 9; i++) {
            System.out.printf("%4s%4s", Integer.toString(i), "|");
        }

        System.out.println("");
        for (int k = 0; k < 65; k++) {
            System.out.print("-");
        }

        System.out.print("\n");
        for (int c = 0; c < piles.stream().mapToInt(List::size).max().getAsInt(); c++) {
            System.out.print("|");
            String line = "";
            for (ArrayList<Card> cards : piles) {
                if (c < cards.size()) {
                    if (cards.get(c) == (null)) {
                        System.out.printf("%4s%4s", " ", "|");
                    } else {
                        System.out.printf("%4s%4s", cards.get(c), "|");
                        line += cards.get(c);
                    }
                } else {
                    System.out.printf("%4s%4s", " ", "|");
                }
            }

            System.out.println("");
            for (int k = 0; k < 65; k++) {
                System.out.print("-");
            }
            System.out.println("");

        }

    }

    /**
     * This method checks whether or not the game is finished.
     *
     * @return true if game is finished, false otherwise.
     */
    public boolean isGameFinished() {
        // If there is any card still in the free cells.
        if (!freecells.stream().noneMatch(card -> (card != null))) {
            return false;
        }

        // If there is any card in the piles.
        for (int i = 0; i < piles.size(); i++) {
            for (int j = 0; j < piles.get(i).size(); j++) {
                if (piles.get(i).get(j) != null) {
                    return false;
                }
            }
        }

        // If the size of each stack in the foundations is 13.
        return foundation.values().stream().noneMatch(stack -> (stack.size() != 13));
    }

    /**
     * This method returns whether or not a certain pile is empty.
     *
     * @param pile the pile to be checked.
     * @return true if pile is empty, false otherwise.
     */
    public boolean isPileEmpty(ArrayList<Card> pile) {
        return pile.stream().noneMatch(card -> (card != null));
    }

    /**
     * This method returns a list of possible actions given the current state of
     * the game.
     *
     * @return List of Action objects; if none, then null.
     */
    public ArrayList<Action> getPossibleActions() {
        ArrayList<Action> actions = new ArrayList<>();

        // Get all the possible actions from all the piles.
        this.piles.forEach(pile -> {
            if (!isPileEmpty(pile)) {
                ArrayList<Action> newActions = getPileActions(this.piles.indexOf(pile));
                if (newActions != null) {
                    newActions.forEach(action -> {
                        actions.add(action);
                    });
                }
            }
        });

        // Get all the possible actions from all the freecells.
        this.freecells.forEach(cell -> {
            if (cell != null) {
                ArrayList<Action> freeCellActions = getActions(cell);
                if (freeCellActions != null) {
                    freeCellActions.forEach(action -> {
                        actions.add(action);
                    });
                }
            }
        });

        return actions;
    }

    /**
     * This method returns a list of actions that the last card of a given pile
     * (mapped by the index) can perform.
     *
     * @param index the index of the pile.
     * @return List of Action objects; if none, then null.
     */
    public ArrayList<Action> getPileActions(int index) {
        ArrayList<Action> actions = new ArrayList<>();
        Card aCard = getPileLastCard(index);
        if (aCard != null) {
            ArrayList<Action> newActions = getActions(aCard);
            if (newActions != null) {
                newActions.forEach(action -> {
                    actions.add(action);
                });
            }
        }

        return actions;
    }

    /**
     * This method returns a list of possible actions of a given card.
     *
     * @param aCard the card to be used to check possible actions.
     * @return the List of Action objects; if none, then null.
     */
    private ArrayList<Action> getActions(Card aCard) {
        ArrayList<Action> possibleActions = new ArrayList<>();
        Card lastCard = null;

        // Check if card can go to foundation.
        String suit = aCard.getSuit();
        this.foundation.entrySet().forEach(entry -> {
            if (entry.getKey().equals(suit)) {
                Card tmpCard = null;
                if (!entry.getValue().empty()) {
                    tmpCard = entry.getValue().peek();
                }

                // If card can go to foundation, then create the action and add
                // it to the possible actions list.
                if (aCard.canBePutOnTopOfFoundation(tmpCard)) {
                    String originType_3 = (this.freecells.contains(aCard) ? "freecell" : "pile");
                    if (originType_3.equals("pile")) {
                        possibleActions.add(new Action(originType_3, "foundation", this.getPileIndexFromCard(aCard), aCard.getSuit(), aCard, this));
                    } else {
                        possibleActions.add(new Action(originType_3, "foundation", this.freecells.indexOf(aCard), aCard.getSuit(), aCard, this));
                    }
                }
            }
        });

        // If a card can be moved to foundation, return the list of possible
        // actions just with it, as it is always the most rational move.
        if (possibleActions.size() > 0) {
            return possibleActions;
        }

        // Check if card can be moved to another pile.
        for (int i = 0; i < this.piles.size(); i++) {
            lastCard = this.getPileLastCard(i);

            // If card can be moved to pile, then create the action and add it 
            // to the possible actions list.
            if (aCard.canBePutOnTopOfPile(lastCard)) {
                String originType = (this.freecells.contains(aCard) ? "freecell" : "pile");
                if (originType.equals("pile")) {
                    possibleActions.add(new Action(originType, "pile", this.getPileIndexFromCard(aCard), i, aCard, this));
                } else {
                    possibleActions.add(new Action(originType, "pile", this.freecells.indexOf(aCard), i, aCard, this));
                }
            }
        }

        // Check if card can go to a freecell.
        for (int j = 0; j < this.freecells.size(); j++) {
            // If card can be moved to free cell, then create the action and add it 
            // to the possible actions list.
            if (this.freecells.get(j) == null) {
                String originType_2 = (this.freecells.contains(aCard) ? "freecell" : "pile");
                if (originType_2.equals("pile")) {
                    possibleActions.add(new Action(originType_2, "freecell", this.getPileIndexFromCard(aCard), j, aCard, this));
                } else {
                    possibleActions.add(new Action(originType_2, "freecell", this.freecells.indexOf(aCard), j, aCard, this));
                }
            }
        }

        // Return the possible actions from a card in a given state.
        return possibleActions;
    }

    /**
     * This method returns the index of the pile where the card is located.
     * Example: 4S is the last card of the first pile, then 0 will be returned
     * (representing the index of the first pile).
     *
     * @param aCard the card used to have its index retrieved.
     * @return -1 if card not found, an integer index otherwise.
     */
    public int getPileIndexFromCard(Card aCard) {
        for (int i = 0; i < this.piles.size(); i++) {
            for (int j = 0; j < this.piles.get(i).size(); j++) {
                if (this.piles.get(i).get(j).equals(aCard)) {
                    return i;
                }
            }
        }
        return -1;
    }

    /**
     * This method returns the index of the card in the pile where it is
     * located. Example: 4S is the last card of the first pile, then 7 will be
     * returned (representing the index of the last card of the first pile).
     *
     * @param the card used to have its index retrieved.
     * @return -1 if card not found, an integer index otherwise.
     */
    public int getCardIndex(Card aCard) {
        for (int i = 0; i < this.piles.size(); i++) {
            for (int j = 0; j < this.piles.get(i).size(); j++) {
                if (this.piles.get(i).get(j).equals(aCard)) {
                    return j;
                }
            }
        }
        return -1;
    }

    /**
     * This method returns a Card representing the last Card object found in the
     * given pile (mapped by index).
     *
     * @param indexOfPile index of the pile.
     * @return a Card object if there is any, otherwise null.
     */
    public Card getPileLastCard(int indexOfPile) {
        Card lastCard = null;
        for (int i = 0; i < this.piles.get(indexOfPile).size(); i++) {
            if (this.piles.get(indexOfPile).get(i) != null) {
                lastCard = this.piles.get(indexOfPile).get(i);
            }
        }
        return lastCard;
    }

    /**
     * This method returns the foundation spots.
     *
     * @return the foundation spots.
     */
    public Map<String, Stack<Card>> getFoundation() {
        return foundation;
    }

    /**
     * This method returns the free cells spots.
     *
     * @return the free cell spots.
     */
    public ArrayList<Card> getFreecells() {
        return freecells;
    }

    /**
     * This method returns the list of piles.
     *
     * @return the list of piles.
     */
    public ArrayList<ArrayList<Card>> getPiles() {
        return piles;
    }

    /**
     * This method returns the path taken from the initial state to the current
     * state.
     *
     * @return a list of actions from the initial state to the current one.
     */
    public ArrayList<Action> getPath() {
        return this.path;
    }

    /**
     * This method returns the path of the state as a string.
     *
     * @return a string representing the path from the initial state to the
     * current one.
     */
    public ArrayList<String> getPathAsString() {
        ArrayList<String> p = new ArrayList<>();
        this.path.forEach(a -> {
            p.add(a.toString());
        });

        return p;
    }

    /**
     * This method returns the heuristics of the current state.
     *
     * @return the heuristic value of the current state.
     */
    public int getHeuristics() {
        return this.heuristic;
    }

    /**
     * This method performs the action passed by parameter. It moves a card from
     * an origin to a destination, adds it to the path, clears all the null
     * values, and calculates the heuristic of the given state.
     *
     * @param action the Action to be performed.
     */
    public void performAction(Action action) {
        // Replace card's origin for a null value.
        if (action.getOrigin().equals("pile")) {
            try {
                this.piles.get(action.getOriginIndex())
                        .set(getCardIndex(action.getCard()), null);
            } catch (java.lang.IndexOutOfBoundsException n) {

            }

        } else {
            this.freecells.set(action.getOriginIndex(), null);
        }

        // Put card in the destination.
        switch (action.getDestination()) {
            case "pile" -> {
                if (isPileEmpty(this.piles.get(action.getDestinationIndex()))) {
                    this.piles.get(action.getDestinationIndex()).add(0, action.getCard());
                } else {
                    this.piles.get(action.getDestinationIndex()).add(action.getCard());
                }
            }
            case "freecell" -> {
                this.freecells.set(action.getDestinationIndex(), action.getCard());
            }
            case "foundation" -> {
                Stack<Card> stack = this.foundation.get(action.getCard().getSuit());
                if (!stack.isEmpty()) {
                    if (!stack.peek().equals(action.getCard())) {
                        this.foundation.get(action.getCard().getSuit()).add(action.getCard());
                    }
                } else {
                    this.foundation.get(action.getCard().getSuit()).add(action.getCard());
                }

            }

        }

        this.path.add(action); // Add Action to path.
        clearNullValues(); // Clear null values in the piles.
        this.heuristic = this.calculateHeuristics(); // Calculates the heuristic of the state after the action was performed.
    }

    /**
     * This method clears the null values from the piles.
     */
    public void clearNullValues() {
        // Remove null values from piles.
        for (int i = 0; i < this.piles.size(); i++) {
            for (int j = 0; j < this.piles.get(i).size(); j++) {
                if (this.piles.get(i).get(j) == null) {
                    this.piles.get(i).remove(j);
                }
            }
        }

    }

    /**
     * This method returns the number of cards left on a given pile.
     *
     * @param cards the list of cards to be used.
     * @return an integer representing the number of cards left on the pile.
     */
    public int getNumberOfCardsLeftOnPile(ArrayList<Card> cards) {
        int count = 0;
        for (Card card : cards) {
            if (card != null) {
                count += 1;
            }
        }
        return count;
    }

    /**
     * This method checks whether or not the given card passed by parameter is
     * ready to move to a pile or free cell.
     *
     * @param aCard card to be moved.
     * @return true if card can be moved somewhere, false otherwise.
     */
    public boolean isCardReadyToMoveOnTopOf(Card aCard) {
        // Look in the free cells.
        for (int i = 0; i < freecells.size(); i++) {
            Card tmpCard = freecells.get(i);
            if (tmpCard != null) {
                if (tmpCard.canBePutOnTopOfPile(aCard)) {
                    return true;
                }
            }
        }

        // Look in the piles.
        for (int j = 0; j < piles.size(); j++) {
            Card lastCard = getPileLastCard(j);
            if (lastCard != null) {
                if (lastCard.canBePutOnTopOfPile(aCard)) {
                    return true;
                }
            }
        }
        return false;
    }

    /**
     * This method checks whether or not a given action will expose a card that
     * can be moved to a foundation.
     *
     * @param action the action to be performed.
     * @return true if action is exposing card to a foundation, false otherwise.
     */
    public boolean isActionExposingCardToFoundation(Action action) {
        if (getCardIndex(action.getCard()) == 0 || action.getOrigin().equals("freecell")) {
            return false;
        }

        int primaryIndex = getPileIndexFromCard(action.getCard());
        int secondaryIndex = getCardIndex(action.getCard()) - 1;
        Card successor = piles.get(primaryIndex).get(secondaryIndex);
        if (foundation.get(successor.getSuit()).empty() && successor.getValue() == 1) {
            return true;
        } else if (foundation.get(successor.getSuit()).empty() && successor.getValue() != 1) {
            return false;
        }

        return successor.canBePutOnTopOfFoundation(foundation.get(successor.getSuit()).peek());

    }

    /**
     * This method calculates the number of cards on top of another card in a
     * pile.
     *
     * @param index_1 the pile index of the card.
     * @param index_2 the index of the pile inside the piles (the index in the
     * column).
     * @return the number of cards on top of another.
     */
    public int calculateCardsOnTopOf(int index_1, int index_2) {
        ArrayList<Card> pile = new ArrayList<>();

        // Populate new list with the same cards of the pile.
        try {
            this.piles.get(index_1).forEach(card -> {
                pile.add(card);
            });
        } catch (IndexOutOfBoundsException n) {

        }

        // Calculate cards on top of the given card.
        int count = 0;
        for (int i = index_2 + 1; i < pile.size(); i++) {
            if (pile.get(i) != null) {
                count += 1;
            }
        }

        // If no card has been found on top of it, return -1 (to decrease the 
        // value of the heuristics, meaning that the action is good).
        if (count == 0) {
            return -1;
        }

        // Return the number of cards on top of it.
        return count;
    }

    /**
     * This method returns the number of empty piles in the game.
     *
     * @return the number of empty piles in the game.
     */
    public int numberOfEmptyPiles() {
        int count = 0;
        for (ArrayList<Card> pile : this.piles) {
            if (isPileEmpty(pile)) {
                count += 1;
            }
        }

        return count;
    }

    /**
     * This method calculates the heuristic value of the current state.
     *
     * @return the integer value representing the heuristic of the current
     * state.
     */
    public int calculateHeuristics() {
        int h = 0;
        
        // For each foundation pile, locate the next card to be placed, and 
        // count the number of cards on top of it.
        for (Map.Entry<String, Stack<Card>> entry : this.foundation.entrySet()) {
            // If stack is empty.
            if (entry.getValue().empty()) {
                // Look for Ace.
                String cardSuit = entry.getKey();
                int cardValue = 1;
                Card searchCard = new Card(cardValue, cardSuit);
                // Check if it is in a freecell
                boolean inFreecell = false;
                for (Card card : this.freecells) {
                    if (card != null) {
                        if (card.equals(searchCard)) {
                            inFreecell = true;
                        }
                    }
                }
                
                // If not in free cell, calculate number of cards on top of it.
                if (!inFreecell) {
                    h += calculateCardsOnTopOf(getPileIndexFromCard(searchCard), getCardIndex(searchCard));
                } 
                // If in a free cell, then add 0 to the heuristic value.
                else {
                    h += 0;
                }
            } 
            // If the last card in the foundation spot is a king, then add 0 to
            // the heuristic, as no other card will be placed on top of it.
            else if (entry.getValue().peek().getValue() == 13) {
                h += 0;
            } 
            // Else, calculate the number of cards on top of the next one to be
            // placed on top of the current last card in foundation.
            else {
                String cardSuit = entry.getKey();
                int cardValue = entry.getValue().peek().getValue() + 1;
                Card searchCard = new Card(cardValue, cardSuit);
                boolean inFreecell = false;
                for (Card card : this.freecells) {
                    if (card != null) {
                        if (card.equals(searchCard)) {
                            inFreecell = true;
                        }
                    }
                }
                if (!inFreecell) {
                    h += calculateCardsOnTopOf(getPileIndexFromCard(searchCard), getCardIndex(searchCard));
                } else {
                    h += 0;
                }
            }

        }

        // Multiply heuristics by 2 if no free cells available or no empty 
        // columns.
        if ((this.freecells.stream().noneMatch(card -> (card != null))) && (this.numberOfEmptyPiles() > 0)) {
            h *= 2;
        }

        // Return the heuristic value.
        return h;
    }

    /**
     * This method checks whether or not our search has reached a dead end.
     * @return true if dead end has been reached, false otherwise.
     */
    public boolean isDeadEnd() {
        return this.getPossibleActions().size() < 1;
    }

    /**
     * This method checks if a state is equal to the current one.
     * @param state the state to be compared.
     * @return true if they are the same, false otherwise.
     */
    public boolean equals(GameState state) {
        return this.id().equals(state.id());
    }

    /**
     * This method returns the unique id of the current state.
     * @return a string id of the current state.
     */
    public String id() {
        String id = "";
        for (int k = 0; k < this.getPiles().size(); k++) {
            for (int t = 0; t < this.getPiles().get(k).size(); t++) {
                id += Integer.toString(this.getPiles().get(k).get(t).getValue()) + this.getPiles().get(k).get(t).getSuit();
            }
            id += ";";
        }

        for (Map.Entry<String, Stack<Card>> f : this.foundation.entrySet()) {
            for (Card card : f.getValue()) {
                id += Integer.toString(card.getValue()) + card.getSuit();
            }
            id += ";";
        }

        return id;
    }

    /**
     * This method prints the path from the initial state to the goal state.
     * @param initialState the initial state of the game.
     */
    public void PrintPathToSolution(GameState initialState) {
        System.out.println("Initial State: ");
        initialState.printState();
        System.out.println("Number of actions taken: " + this.path.size());
        System.out.println("Actions taken: ");

        for (int i = 0; i < this.getPath().size(); i++) {
            initialState.performAction(this.getPath().get(i));
            System.out.println((i + 1) + ". " + this.getPath().get(i).toString());
            if ((i % 10 == 0 && i != 0) || (i == this.getPath().size() - 1)) {
                initialState.printState();
            } 

        }
    }
}
