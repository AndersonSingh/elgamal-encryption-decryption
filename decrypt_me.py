# import modules needed.
import elgamal_module as elgamal
from Crypto.Cipher import DES

# main function of script to decrypt message.
if __name__ == '__main__':

	# shared secret key for DES encryption.
	secret_key = raw_input('Enter the shared secret key.\n')
	secret_key = secret_key.strip()

	if len(secret_key) != 8:
		print 'Incorrect secret key length.'
		exit()

	# open file with private key and read the encrypted private key. 
	private_key_file = open('privatekey.dat', 'r')
	encrypted_private_key = private_key_file.read()

	# get the iv from the user.
	random_iv = raw_input('Enter the random IV for decryption.\n')
	random_iv = str(random_iv)

	# decrypt the private key.
	private_key = DES.new(secret_key, DES.MODE_CBC, random_iv).decrypt(encrypted_private_key)
	private_key = int(private_key)

	# open the public key to get the large prime number.
	public_key_file = open('publickey.dat', 'r')
	
	public_key = public_key_file.read()
	public_key = public_key.split(',')

	# needed for decryption.
	large_prime = public_key[0]


	# get the ciphertext from the file.
	ciphertext_file = open('letter.txt', 'r')
	ciphertext = ciphertext_file.read()

	# convert ciphertext to proper format.
	d = []
	for item in ciphertext.split(','):
		item = item.split(':')
		d.append((int(item[0]), int(item[1])))


	# decrypt the message using elgamal.
	decrypted_message = elgamal.decrypt(d, int(private_key),int(large_prime))

	# print the decrypted message to the screen.
	print 'The decrypted message is: {}'.format(decrypted_message)