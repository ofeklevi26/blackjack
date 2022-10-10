#importing for shuffle method
import random
import time
suits = ('♠', '♥', '♦', '♣')
ranks = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace')
values = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, 
            '9':9, '10':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

#creating class for cards 
class Card:
	def __init__(self,suit,rank):
		self.suit=suit
		self.rank=rank
		self.value=values[rank]

	def __str__(self):
		return f'{self.rank}{self.suit}'

#creating class for deck 
class Deck:
	def __init__(self):
		self.all_cards=[]
		for suit in suits:
			for rank in ranks:
				self.all_cards.append(Card(suit,rank))

	def shuffle(self): #shuffling the cards in a deck
		random.shuffle(self.all_cards)

	def deal_one(self): #dealing out of the deck one card
		return self.all_cards.pop()

#creating a class for a bank of a player
class Bank:
	def __init__(self,name,amount):
		self.name=name
		self.amount=amount

	def deposit(self,depositing=0):
		self.amount+=depositing

	def draw(self,drawing=0):
		if drawing>self.amount:                                 #check case when drawing more that you have
			print(f'you dont have enough money, you have bet all you got left: {self.amount} dollars')
			tempi=self.amount
			self.amount=0
			return tempi
		else:
			self.amount-=drawing
			return drawing

#creating a class for a player's hand, can store cards, count value
class Hand:
	def __init__(self,name):
		self.cards=[]
		self.name=name

	def value(self):
		totalval=0
		for i in range(0,len(self.cards)):
			totalval+=self.cards[i].value
		return totalval

	def hit(self,card):
		self.cards.append(card)
		for i in range(0,len(self.cards)):
			if self.value()>21 and self.cards[i].rank=='Ace':
				self.cards[i].value=1

	def __str__(self):
		allcardsinhand=str(self.cards[0])
		for i in range(1,len(self.cards)):
			allcardsinhand=allcardsinhand+' and '+str(self.cards[i])
		return allcardsinhand

#creating a bet for a player, can be zero in each new round
class Bet:
	def __init__(self,name):
		self.name=name
		self.amount=0

	def add_bet(self,how_much):
		self.amount+=how_much
		
	def new_round(self):
		self.amount=0

def check_blackjack(ranHand=Hand('example')):
	black=0
	jack=0
	for i in range(0,len(ranHand.cards)):
		for kind in ['Jack', 'Queen', 'King']:
			if kind==ranHand.cards[i].rank:
				black+=1
		if ranHand.cards[i].rank=='Ace':
			jack+=1
	return black==1 and jack==1

#Main body
gameon=input('Wanna play BlackJack? Y/N\n').upper()
if gameon=='Y':                          #the game starts
	player_name=input('enter your name\n')
	dealer_bank=Bank('Dealer',10000000000000000000000000000000000000000000)
	player_how_much_money=int(input('how much money you have? (dollars)\n'))
	player_bank=Bank(player_name,int(player_how_much_money))
print('\n'*5) #for spacing
while gameon=='Y' and player_bank.amount>0:   #when player wants to play and he has money
	print(f'you have got {player_bank.amount} dollars in the bank\n')
	deck=Deck() #creating deck
	deck.shuffle() #shuffeling the deck
	player_bet=Bet(player_name)
	moneyround=int(input('place your bet for the round (dollars) \n'))
	player_bet.add_bet(player_bank.draw(moneyround))
	player_hand=Hand(player_name)
	dealer_hand=Hand('Dealer')
	player_hand.hit(deck.deal_one()) #giving first card to player
	dealer_hand.hit(deck.deal_one()) #giving first card to dealer
	player_hand.hit(deck.deal_one()) #giving second card to player
	dealer_hand.hit(deck.deal_one()) #giving second card to dealer
	print(f"Player's hand is {player_hand} and it equals {player_hand.value()}")
	print(f"Dealer's first card is {dealer_hand.cards[0]} and it equals {dealer_hand.cards[0].value}")

	if check_blackjack(player_hand): #if player got blackjack he wins double the money he bet on
		print(f'BlackJack! you have earned twice your bet of:{player_bet.amount} dollars')
		player_bank.deposit(player_bet.amount*3) 
		player_bet.new_round() #reseting the bet amount
		gameon=input('wanna start another round? Y/N\n').upper()
		if gameon=='Y':
			print("\n"*5)
			continue
			
		else:
			break


	player_choice=input('hit or stay?\n')
	while player_choice!='hit' and player_choice!='stay':
		player_choice=input('error pick again: hit or stay\n')
	while player_choice=='hit':
		player_hand.hit(deck.deal_one())
		print(f"Player's hand is {player_hand} and it equals {player_hand.value()}\n")
		if player_hand.value()>21:
			print(f'BUST! you have lost your bet: {player_bet.amount}')
			player_bet.new_round()
			print('\n'*5)
			gameon=input('wanna start another round? Y/N\n').upper()
			break
		player_choice=input('hit or stay?\n')
		while player_choice!='hit' and player_choice!='stay':
			player_choice=input('error pick again: hit or stay\n')
	#if it breaks out the while loop, the player lost his bet or he picked "stay"

	if player_choice=='stay':
		print('Dealer will now show his whole hand\n')
		time.sleep(2)
		print(f"Dealer's hand is {dealer_hand} and it equals {dealer_hand.value()}\n")
		time.sleep(3)
		while dealer_hand.value()<=player_hand.value():
			print('Dealer will now draw a card\n')
			dealer_hand.hit(deck.deal_one())
			time.sleep(3)
			print(f"Dealer's hand is {dealer_hand} and it equals {dealer_hand.value()}\n")
			time.sleep(3)
			if dealer_hand.value()>21:
				print(f'dealer BUSTED, player won the bet and earned {player_bet.amount}\n')
				player_bank.deposit(player_bet.amount*2)
				player_bet.new_round()
				print('\n'*5)
				gameon=input('wanna start another round? Y/N\n').upper()
				break
		if player_bet.amount==0: #player bet zero when round ends therefore if code continue to run means the dealer won
			continue
		elif dealer_hand.value()>player_hand.value():
			print(f"Dealer's hand worth {dealer_hand.value()} and {player_name}'s hand worth {player_hand.value()}")
			print(f"Dealer wins, you have lost your bet of {player_bet.amount} dollars")
			player_bet.new_round()
			print('\n'*5)
		gameon=input('wanna start another round? Y/N\n').upper()
	if player_bank.amount==0:
		print(f'out of money, {player_name} you broke')
		deposit_more=input(f'{player_name} do you wanna deposit more money into your bank? Y/N\n').upper()
		if deposit_more=='Y':
			new_deposit=int(input('how much dollars to deposit?'))
			player_bank.deposit(new_deposit)
			player_how_much_money+=new_deposit
		else:
			break
totalgain=abs(player_how_much_money-player_bank.amount)
if player_how_much_money>player_bank.amount:
	print(f'{player_name} you have total losses of {totalgain} dollars')
elif player_how_much_money<player_bank.amount:
	print(f'{player_name} you have total earnings of {totalgain} dollars')
else:
	print(f"{player_name} you didn't earn or lost money, your bank is untouched")

