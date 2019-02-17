
import utils.constants as constants

def validate(username='', name=''):
	'''
	Returns a dictionary with following structure:
		`is_valid` can be either 0 or 1.
		`message` is a descriptive message for the user.
		When is_valid == 0 (at least one field is invalid):
			- the `message` is rendered on 'signup.html'.
			- the field-name goes in the dict as value for key 'invalid_field'.
		When is_valid == 1 (all fields are valid):
			- no `message` is returned
			- modified fields (if any) are returned with their names as keys.
			- execution continues.
	Example:
	1.
		If username is invalid:
			return {
				'is_valid': 0,
				'message': 'Invalid username. Please choose another.'
			}
	2.
		If name is written as 'roshan Sharma', it's valid, but needs to be
		modified.
			name[0] = name[0].upper()
			return {
				'is_valid': 1,
				'name': name
			}
	'''

	# [username] -:

	# Check for reserved and banned names
	if username.lower() in constants.RESERVED_NAMES:
		return {
			'is_valid': 0,
			'message': 'Username not allowed'
		}

	# [Later] Regex to check for username syntax.

	# [name] -:

	# Convert to title case
	name = name.title()
	return {
		'is_valid': 1,
		'name': name,
		# Other fields can come as needed.
	}
