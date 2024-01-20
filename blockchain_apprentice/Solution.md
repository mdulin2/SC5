1. On Sepolia testnet, look up the provided wallet address
2. Notice the NFT safeMint transaction
3. Go to the NFT contract that minted the NFT
   * https://sepolia.etherscan.io/address/0x90611952040b06f11ddcd61b26274f404ccd89e2#readContract
4. Get the NFT IPFS address from the NFT contract
   * It's hardcoded in safeMint
   * Alternatively, we can use the tokenURI function
5. Go to the IPFS and download the NFT
6. Get the EXIF data from the NFT and notice that there is an address under Owner
7. Look up the address on mainnet 
   * Important-- Notice that this is the Owner of the NFT, not the creator (this is not the solution)
9. In mainnet, notice that this address also owns an NFT on mainnet
10. Go to the NFT transaction on mainnet and grab the creator address
    * https://etherscan.io/nft/0x1f5767efbd7dbeebef3471018c7a1f69d46c5392/0
    * 0x36d312a77F2Db341b6fD76Eb3D0f1cfbC4215930
11. The creator address is the solution to this challenge