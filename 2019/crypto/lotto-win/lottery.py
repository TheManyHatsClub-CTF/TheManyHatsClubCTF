#!/usr/local/bin/python
import random, time

# Function to generate a winner number with the seed's value
def next(seed):
	# Max winner number
	MAX = 2000000000
	# Min winner number
	MIN = 1

	# Change of the seed
	seed = seed * seed + seed

	# Truncation of the seed
	if (seed > 0xFFFFFFFF):
		seed = int(hex(seed)[-8:], 16)

	# Return of [new seed, new winner number]
	return [seed, seed % (MAX - MIN) + MIN]

# Initialization of a random seed, which value can be between 0x1337 and 0xFFFFFFFF
seed = random.randint(0x1337, 0xFFFFFFFF)


# Source code is shown
print("""Trust in Lotto-Win. Trust in open source:
def next(seed):
	# Max winner number
	MAX = 2000000000
	# Min winner number
	MIN = 1

	# Change of the seed
	seed = seed * seed + seed

	# Truncation of the seed
	if (seed > 0xFFFFFFFF):
		seed = int(hex(seed)[-8:], 16)

	# Return of [new seed, new winner number]
	return [seed, seed % (MAX - MIN) + MIN]

# Initialization of random seed
seed = random.randint(0x1337, 0xFFFFFFFF)""")


# Some numbers are generated so the user has a hint for the attack
lotto = []
for i in range(5):
	seed, num = next(seed)
	lotto.append(str(num))

while True:
	# Last lottery numbers are shown
	print("\n\n\nLast Lottery numbers:\n" + '\n'.join(lotto))
	
	# Users will have to wait 5 minutes in order to enter a lottery number, so bruteforce is mitigated
	print("Wait 5 minutes to play the next round of lottery...")
	time.sleep(300)

	# User enters its lottery number
	user_num = input("Enter your lottery number: ")

	# A winner number is generated and the seed changes
	seed, num = next(seed)

	# Num gets converted to string
	num = str(num)

	# Winner number is compared to the users number
	if user_num == num:
		print("WOW! YOU WON THE LOTTERY!! GET YOUR REWARD WITH THE CODE 'TMHC{Lucki3r_th4n_Pelayo}'!!!1!11!")
		exit()
	else:
		print("Keep trying ;)")
	lotto.append(num)
