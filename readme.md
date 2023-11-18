Here is how you can run the tic tac toe game with local blockchain

1. Install fe lang and Foundry. Make sure that the "fe_mac" (or fe) command and the "anvil" command works well locally. 
Install python 3.10+

2. Compile the smart contract tictactoe.fe
./fe_mac build tictactoe.fe   --overwrite 
or (./fe build tictactoe.fe   --overwrite ) for non-mac user

3. launch "anvil" command to launch the blockchain locally. Write down the private key

4. deploy the smart contract with

cast send --rpc-url localhost:8545 --private-key {{private_key}} --create $(cat output/TicTacToe/TicTacToe.bin)

5. get the private key from the "anvil" command terminal and modify the file "config.ini" according the contract address and the private key. Save the file "config.ini"

6. Launch the game with

python tictactoe.py