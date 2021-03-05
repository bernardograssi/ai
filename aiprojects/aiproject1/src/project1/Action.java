package project1;

/**
 * This class represents an action to be made in the game, where a card ought to
 * be moved from a given location (such as "pile" or "freecell") to another one
 * (such as "pile", "freecell", or "foundation"). It also contains an origin
 * index variable, representing the index of the pile or free cell where it is
 * coming from. It also contains a destination index, representing either the
 * foundation (in case of the String variable), a free cell or a pile (in case
 * of the integer variable).
 *
 * @author Allen Westgate, Bernardo Santos, and Ryan Farrell
 */
public class Action {

    private String origin; // The origin of the Action ("freecell" or "pile").
    private String destination; // The destination of the Action ("freecell", "pile", or "foundation").
    private int originIndex; // The index of origin of the Action, representing the pile it is located or the free cell.
    private int destinationIndex; // The index of destination of the Action if it is being moved to a free cell or to a pile.
    private String destinationKey; // The index (or key) of destination of the Action if it is being moved to the foundation spot of its suit.
    private Card card; // The card associated with the action.
    private GameState state; // The state that the action creates.

    /**
     * Constructor method used when moving to free cell or pile.
     *
     * @param origin origin of the Action.
     * @param destination destination of the Action.
     * @param originIndex index of origin of the Action.
     * @param destinationIndex index of destination of the Action.
     * @param card the card associated with the action.
     * @param state the state that the action creates.
     */
    public Action(String origin, String destination, int originIndex, int destinationIndex, Card card, GameState state) {
        this.origin = origin;
        this.destination = destination;
        this.originIndex = originIndex;
        this.destinationIndex = destinationIndex;
        this.destinationKey = "";
        this.card = card;
        this.state = state;
    }

    /**
     * Constructor method used when moving to foundation.
     *
     * @param origin origin of the Action.
     * @param destination destination of the Action.
     * @param originIndex index of origin of the Action.
     * @param destinationKey key of destination of the Action.
     * @param card the card associated with the action.
     * @param state the state that the action creates.
     */
    public Action(String origin, String destination, int originIndex, String destinationKey, Card card, GameState state) {
        this.origin = origin;
        this.destination = destination;
        this.originIndex = originIndex;
        this.destinationIndex = -1;
        this.destinationKey = destinationKey;
        this.card = card;
        this.state = state;
    }

    /**
     * This method returns the state associated with the action.
     * @return 
     */
    public GameState getState() {
        return state;
    }

    /**
     * This method returns the origin of the Action.
     *
     * @return the origin of the Action.
     */
    public String getOrigin() {
        return origin;
    }

    /**
     * This method returns the destination of the Action.
     *
     * @return the destination of the Action.
     */
    public String getDestination() {
        return destination;
    }

    /**
     * This method returns the index of origin of the Action.
     *
     * @return the index of origin of the Action.
     */
    public int getOriginIndex() {
        return originIndex;
    }

    /**
     * This method returns the index of destination if Action represents moving
     * a card to a free cell or pile.
     *
     * @return
     */
    public int getDestinationIndex() {
        return destinationIndex;
    }

    /**
     * This method returns the key of the destination if Action represents
     * moving a card to a foundation spot.
     *
     * @return the key of the destination.
     */
    public String getDestinationKey() {
        return destinationKey;
    }

    /**
     * This method returns the card associated with the action.
     *
     * @return the card associated with the action.
     */
    public Card getCard() {
        return card;
    }

    /**
     * This method converts an action object to a string.
     * @return the string form of the action.
     */
    @Override
    public String toString() {
        String dest = "";
        if (destinationIndex == -1) {
            dest = destinationKey;
        } else {
            dest = Integer.toString(destinationIndex + 1);
        }
        return card.toString() + " from " + origin + " #" + (originIndex + 1) + " to " + (destination) + " #" + (dest);
    }

}
