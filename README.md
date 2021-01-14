## Generating Enjoyable Boggle Boards
### Developed for AM205: Advanced Scientific Computing Final Project, December 2020

We test board generation algorithms for the word search game Boggle, where all players are presented with the same board of letters arranged in a rectangular grid. 
We seek to find the board generation method that makes for the most enjoyable games of Boggle. To find a way to quantify enjoyability, we consider the two extremes 
that limit the enjoyability of a Boggle game. On one end, the game is frustrating if it is too hard to find words and a player sits through a significant portion 
of the game not seeing any new words. On the other end, the game can be boring if it begins to feel like the same words are appearing on every board. We propose 
four board generation algorithms and compare them, ultimately recommending the Seeding algorithm as the one that produces the most enjoyable Boggle boards. To 
efficiently implement a board search and simulate how a person might play a Boggle game, we utilize a prefix tree data structure, which provides efficient lookup 
for variable-length keys.

The demo.ipynb notebook provides examples of how the board algorithms, gameplay modeling, and board search code can be used. 
