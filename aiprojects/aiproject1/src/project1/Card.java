package project1;

/**
 * Class that represents a card of the deck.
 *
 * @author Allen Westgate, Bernardo Santos, and Ryan Farrell
 */
public class Card {

    private final int value; // The value of the card, i.e.: A = 1, 2 = 2, J = 11...
    private final String suit; // The suits of the cards, i.e.: C = Clubs, D = Diamonds, H = Hearts, S = Spades.

    /**
     * This is the class's constructor.
     *
     * @param value the value of the card.
     * @param suit the suit of the card.
     */
    public Card(int value, String suit) {
        this.value = value;
        this.suit = suit;
    }

    /**
     * This method returns the value of the card.
     *
     * @return the value of the card as an integer.
     */
    public int getValue() {
        return value;
    }

    /**
     * This method returns the suit of the card.
     *
     * @return the suit of the card as a String.
     */
    public String getSuit() {
        return suit;
    }

    /**
     * This method checks if the current card object (this.) can be put on top
     * of the card passed as a parameter.
     *
     * @param aCard the card used to check if the current card can be put on top
     * of it.
     * @return true if card can be put on top, false otherwise.
     */
    public boolean canBePutOnTopOfPile(Card aCard) {
        if (aCard == null) {
            return true;
        }
        if (aCard.getValue() != this.getValue() + 1) {
            return false;
        }

        return compatibleSuitsOnPile(aCard);
    }

    /**
     * This method checks if the current card(this.) can be put on top of
     * foundation.
     *
     * @param aCard last card on the foundation stack, or null if there is none.
     * @return true if card can be put on stack, false otherwise.
     */
    public boolean canBePutOnTopOfFoundation(Card aCard) {

        if (aCard == null && this.getValue() == 1) {
            return true;
        } else if (aCard == null && this.getValue() != 1) {
            return false;
        } else {
            return this.getSuit().equals(aCard.getSuit())
                    && (this.getValue() == aCard.getValue() + 1);
        }
    }

    /**
     * This method checks if the current card (this.) has a compatible suit to
     * be put on top of the card passed as a parameter; i.e.: if the current
     * card has Clubs suit, then it can only be moved to a pile where the last
     * card has either Diamonds or Hearts as its suit.
     *
     * @param aCard the last card of the pile where the current card is checking
     * if it can be moved there.
     * @return true if the card be moved to the pile, false otherwise.
     */
    public boolean compatibleSuitsOnPile(Card aCard) {
        String suits = aCard.getSuit() + this.getSuit();
        return suits.equals("CD")
                || suits.equals("DC")
                || suits.equals("CH")
                || suits.equals("HC")
                || suits.equals("SD")
                || suits.equals("DS")
                || suits.equals("SH")
                || suits.equals("HS");
    }

    /**
     *
     * @param aCard
     * @return
     */
    @Override
    public boolean equals(Object aCard) {
        if (aCard == this) {
            return true;
        }

        if (!(aCard instanceof Card)) {
            return false;
        }

        Card card = (Card) aCard;

        return this.getSuit().equals(card.getSuit())
                && this.getValue() == card.getValue();
    }

    /**
     * This method converts the object to a String.
     *
     * @return the String representation of the object.
     */
    @Override
    public String toString() {
        String valueString = Integer.toString(value);
        switch (value) {
            case 1 ->
                valueString = "A";
            case 11 ->
                valueString = "J";
            case 12 ->
                valueString = "Q";
            case 13 ->
                valueString = "K";
            default -> {
            }
        }

        return valueString + suit;
    }

}
