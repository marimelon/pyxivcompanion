# pyxivcompanion
This is a library for accessing the API used by FFXIV Companion App from Python.

It is written based on [xivapi/companion-php](https://github.com/xivapi/companion-php)


## Example
```python

from pyxivcompanion.account import Account
from pyxivcompanion.token import Token

from pyxivcompanion.address_book import AddressBook

async def Example():
    # Get a list of characters
    login: LoginObj = await Account.login('SQEX_ID', 'SQEX_PASSWORD')
    characters = await login.get_characters()
    for character in characters.accounts[0].characters:
        print(f'{character.cid}, {character.name}, {character.world}')
        
    # Login a character
    token = await Token.create_new_token('cid', 'SQEX_ID', 'SQEX_PASSWORD')
    # or
    # token = await Token.create_new_token_from_loginobj('cid', login)
    
    # Get the AddressBook.
    result,response = await AddressBook.get_addressbook(token=token)
    # Friend List
    print('Friend List')
    for friend in result.addressBook.fr.characters:
        print(f' {friend.name}, {friend.world}')
    # Linkshell
    for linkshell in result.addressBook.ls:
        print(linkshell.name)
        for character in linkshell.characters:
            print(f' {character.name}, {character.world}')
```
