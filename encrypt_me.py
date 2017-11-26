# import modules needed.
import elgamal_module as elgamal

from Crypto.Cipher import DES
from Crypto import Random

from random import choice
from string import ascii_uppercase


# main function of script to encrypt message. 
if __name__ == '__main__':

	# shared secret key for DES encryption.
	secret_key = '-8B key-'

	# generate a random string of length 8 to use as the IV. 
	random_iv = ''.join(choice(ascii_uppercase) for i in range(8))

	print 'INFO: The decryption script will need the IV: {}'.format(random_iv)

	# keys contains the private and public key. 
	keys = elgamal.generate_key_pair()

	private_key = keys['private_key']
	public_key = keys['public_key']

	# apply padding to the private key.
	padding_amt = 8 - (len(str(private_key)) % 8)
	padding = ''

	for i in range(0, padding_amt):
		padding += ' '

	formatted_private_key = str(private_key) + padding
	formatted_public_key = str(public_key[0]) + ',' + str(public_key[1]) + ',' + str(public_key[2])

	print 'Step 1 - The private key: {}'.format(private_key)
	print 'Step 2 - The pubic key: {}'.format(public_key)

	print 'Step 3 - Encrypting the private key (DES) with password: {}'.format(secret_key)
	encrypted_private_key = DES.new(secret_key, DES.MODE_CBC, random_iv).encrypt(formatted_private_key)


	print 'Step 4 - Saving the encrypted private key to file privatekey.dat'	
	private_key_file = open('privatekey.dat', 'w')
	private_key_file.write(encrypted_private_key)
	private_key_file.close()

	print 'Step 5 - Saving public key to file publickey.dat'
	public_key_file = open('publickey.dat', 'w')
	public_key_file.write(str(formatted_public_key))
	public_key_file.close()

	print 'Step 6 - Encrypt the message.'
	message = raw_input('Enter a message to encrypt.\n')
	message_encrypted = elgamal.encrypt(message, keys['public_key'])

	# write the encrpyted message to file. 
	message_file = open('letter.txt', 'w')
	
	data = ''
	for item in message_encrypted:
		data += str(item[0]) + ':' + str(item[1]) + ','
	data = data[:-1]

	message_file.write(data)
	message_file.close()

	print 'Steps 7, 8, 9 - Send emails with the encrypted message and necessary decryption information to your classmate.'

