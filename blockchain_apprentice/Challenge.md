# Exploring The Ethereum Blockchain

You're an investigator in a string of recent blockchain hacks. One of your current investigations involves an NFT artist who appears to help launder stolen cryptocurrency through suspicious NFT transactions. 

You get your first big big break in the case. You have reason to believe that the NFT artist under investigation owns the wallet address [0xcA5CCFcb44220d850d69F771Ca470701D93CC0D4](https://sepolia.etherscan.io/address/0xcA5CCFcb44220d850d69F771Ca470701D93CC0D4) on the [Sepolia](https://sepolia.etherscan.io/) testnet. 

Take a look at the artist's testnet transactions, and see if the artist has made any mistakes, which may reveal the artist's identity on mainnet.

Once the artist's identity is revealed on mainnet, we can publicly tag the artist's wallet address, freeze their assets, and ensure that no one else falls victim to this artist's deception. We don't want just the owner of the NFT; we want the highest up user we can find!

Objective: Reveal one of the malicious NFT artist's wallet addresses on mainnet. It should be the created of the NFT on the mainnet.

Hint 1: Etherscan is a great way to start exploring transactions on both the Ethereum [mainnet](https://etherscan.io/) as well as [testnets](https://sepolia.etherscan.io/). Read through the source code of contracts, account information, NFT data and such to find the secret.

Hint 2: Data hosted on testnets might not have the same level of sanitization as data hosted on mainnet. What are some things the NFT artist may have forgotten to do prior to transacting on testnet? Read the file information :)
