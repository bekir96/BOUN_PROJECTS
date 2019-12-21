### Explanations

- I worked with Yusuf Yüksel and tested with him.

- Yusuf Yüksel's student ID = 2014400051.

- Usage is ./safechat.py



### Important Design Notes

- If you want to send a message to A person, you type a message then in the background, safechat picks two different prime numbers which are g and p.Then with private key it calculates partial key and  sends (g,p,A) which are public keys and partial key to A person.After that A person sends to his partial key to you then both of you calculate key.After that message which you will send is encrypted via full key.A person takes the message and decrypted with	key then reads the message which is in Notification section.

- Each message encrypted with an evolving cypher according to two different random prime numbers.

- Cypher is initially None.

- Init packet sets the cyper None and shares public numbers g and p by generating two different prime numbers.Also, init packet sends to partial key which is calculated via public numbers and private key.

- Cypher evolves based on messages being sent according to random different g and p prime numbers and partial key.

- We create a Diffie-Hellman key exchange class which has some member functions in order to calculate keys , encryption and decryption.



