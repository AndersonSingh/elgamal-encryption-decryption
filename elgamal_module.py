import random
import math

# this function is for fast modulo expontentiation.     
def modulo(factor,power,modulus):
    
    result = 1
    
    while power > 0:
        
        if power % 2 == 1: 
            result = (result * factor) % modulus
            power = power - 1 
        
        power = power / 2
        factor = (factor * factor) % modulus
        
    return result


# miller rabin prime test. 
def is_prime_miller_rabin(p):

	if p < 2:
		return False

	if p == 2:
		return True

	if p % 2 == 0:
		return False

	if p == 3: 
		return True

	s = p - 1
	r = 0
	iterations = 20

	while s % 2 == 0:
		r = r + 1
		s = s // 2

	for i in range(0, iterations):

		# select a random a value. 
		a = random.randrange(2, p - 1)

		x = modulo(a, s, p)

		if x == 1 or x == p - 1:
			continue

		for i in range(0, r - 1):
			
			x = modulo(x, 2, p)

			if x == p - 1: 
				break;
		else:
			return False

	return True


def generate_large_prime(keysize):

	while True:
		number = random.randrange(2**(keysize-1), 2**(keysize))

		if is_prime_miller_rabin(number):
			return number

# function for question 2 part 1.
def trial_division_method(p):

	factors = []

	num_sqrt = int(math.ceil(math.sqrt(p)))

	for a in range(2, num_sqrt + 1):

		while p % a == 0:
			factors.append(a)
			p = p / a


	if p > 1:
		p = int(p)
		factors.append(p)

	return factors

# -1 ouput means no primitive roots.
def smallest_primitive_root(p):

	temp = p - 1

	factors = list(set(trial_division_method(temp)))

	for g in range(2, p):

		flag = 0

		for q in factors: 
			result = pow(g, (p - 1) // q, p)
			if result == 1: 
				flag = 1
				break;

		if flag == 0:
			return g

	return -1

def inverse_of_a(a, p):

	result = modulo(a, p - 2, p)
	return result


# this function will generate, a public key and private key pair. 
def generate_key_pair():

	#adjust this later.
	keysize = 16

	flag = 0

	# it is possible for no primitive root to exist,
	while flag == 0:
		q = generate_large_prime(keysize)
		g = smallest_primitive_root(q)

		if g != -1:
			flag = 1

	x_a = random.randint(2, q - 2)
	y_a = modulo(g, x_a, q)


	return { 'private_key' : (x_a), 'public_key' : (q, g, y_a) }



def encrypt(plaintext, public_key):

	plaintext = str(plaintext)

	q = public_key[0]
	g = public_key[1]
	y_a = public_key[2]

	ciphertext = []

	for ch in plaintext:

		small_k = random.randint(1, q - 1)
		big_K = modulo(y_a, small_k, q)

		M = ord(ch)

		C1 = modulo(g, small_k, q)
		C2 = (big_K * M) % q
	
		ciphertext.append((C1, C2))

	return ciphertext


def decrypt(ciphertext, private_key, large_prime):

	plaintext = '';

	q = large_prime
	x_a = private_key

	for C in ciphertext:

		C1 = C[0]
		C2 = C[1]

		big_K = modulo(C1, x_a, q)

		big_K_inverse = inverse_of_a(big_K, q)

		M = (C2 * big_K_inverse) % q

		plaintext += str(unichr(M))

	return plaintext

# if __name__ == '__main__':

# 	keys = generate_key_pair()
# 	d = encrypt('hello world', keys['public_key'])
# 	print(decrypt(d, keys['private_key']))