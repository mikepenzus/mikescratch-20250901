``` mermaid
classDiagram
class API {
    Deck[] getDecks(username)
    Card[] getCards(username, deckId)
    Card addCard(username, deckId, front, back)
    deleteCard(username, deckId, cardId)
    storeTest(username, deckId, cardId, response)
    Card getNextCard(username, deckId)
}

class Deck {
    id
    name
    noTrialsPerDay
    owner
}

class Card {
    id
    front
    back
    deckId
    lastReviewDate
    lastReviewNoTrials
    nextDate
}

Deck *--> Card

```

### Response
* FAIL
* HARD
* EASY

