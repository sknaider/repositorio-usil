#include <iostream>
#include <vector>
#include <string>
#include <cstdlib>
#include <ctime>

using namespace std;

class Card {
public:
    int value;
    string suit;
    string rank;

    Card(int v, string s, string r) : value(v), suit(s), rank(r) {}
};

class Deck {
public:
    vector<Card> cards;

    Deck() {
        string suits[] = { "Corazones", "Diamantes", "Treboles", "Picas" };
        string ranks[] = { "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jota", "Reina", "Rey", "As" };

        for (string suit : suits) {
            for (int i = 0; i < 13; i++) {
                Card card(i + 2, suit, ranks[i]);
                cards.push_back(card);
            }
        }
    }

    void shuffle() {
        srand(time(0));
        random_shuffle(cards.begin(), cards.end());
    }

    Card drawCard() {
        Card card = cards.back();
        cards.pop_back();
        return card;
    }
};

class Player {
public:
    vector<Card> hand;
    int score;

    Player() : score(0) {}

    void addCard(Card card) {
        hand.push_back(card);
        score += card.value;
    }

    void reset() {
        hand.clear();
        score = 0;
    }
};

void showHand(const Player& player, const string& playerType) {
    cout << playerType << " mano:";
    for (const Card& card : player.hand) {
        cout << " " << card.rank << " de " << card.suit;
    }
    cout << " (Puntuación: " << player.score << ")" << endl;
}

void playTurn(Player& player, Deck& deck, const string& playerType) {
    char choice;
    while (true) {
        showHand(player, playerType);
        cout << "¿Quieres pedir carta? (s/n): ";
        cin >> choice;

        if (choice == 's') {
            Card card = deck.drawCard();
            player.addCard(card);
            if (player.score > 21) {
                showHand(player, playerType);
                cout << playerType << " ha perdido." << endl;
                break;
            }
        } else {
            break;
        }
    }
}

string determineWinner(const Player& player, const Player& dealer) {
    if (player.score > 21) {
        return "Dealer";
    } else if (dealer.score > 21 || player.score > dealer.score) {
        return "Jugador";
    } else if (dealer.score > player.score) {
        return "Dealer";
    } else {
        return "Empate";
    }
}

int main() {
    Deck deck;
    deck.shuffle();

    Player player;
    Player dealer;

    player.addCard(deck.drawCard());
    dealer.addCard(deck.drawCard());
    player.addCard(deck.drawCard());
    dealer.addCard(deck.drawCard());

    if (player.score > 21) {
        showHand(player, "Tu");
        cout << "¡Tu mano inicial supera 21! Has perdido." << endl;
        return 0;
    }

    playTurn(player, deck, "Tu");
    if (player.score <= 21) {
        while (dealer.score < 17) {
            Card card = deck.drawCard();
            dealer.addCard(card);
        }

        showHand(dealer, "Dealer");
        string winner = determineWinner(player, dealer);
        cout << "El ganador es: " << winner << endl;
    }

    return 0;
}
