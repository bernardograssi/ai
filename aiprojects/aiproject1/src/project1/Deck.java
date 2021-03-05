package project1;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * This class represents the deck of cards used in the game.
 *
 * @author Allen Westgate, Bernardo Santos, and Ryan Farrell
 */
public class Deck {

    private final ArrayList<Card> deck = new ArrayList<>(); // The deck of cards used in the game.

    /**
     * This is the class's constructor.
     *
     * @param suits all the possible suits of the deck (C,D,H,S).
     * @param numbers numbers representing the value of cards (1 to 13).
     */
    public Deck(ArrayList<String> suits, ArrayList<Integer> numbers) {
        
        // Add the cards to the deck.
        for (int i = 0; i < numbers.size(); i++) {
            for (int j = 0; j < suits.size(); j++) {
                Card card = new Card(numbers.get(i), suits.get(j));
                deck.add(card);
            }
        }

        // Shuffle the cards of the deck.
        Collections.shuffle(deck);
    }

    /**
     * This method returns the deck of cards.
     *
     * @return a list containing all the cards of the game.
     */
    public ArrayList<Card> getDeck() {
        return deck;
    }

    /**
     * This method returns a sub deck of the current deck, bounded by a start
     * index and an end index.
     *
     * @param start the index to start the deck sub list (inclusive).
     * @param end the index to end the deck sub list (inclusive).
     * @return the sub list of the deck bounded by the indices.
     */
    public List<Card> getSubDeck(int start, int end) {
        return deck.subList(start, end);
    }

}
