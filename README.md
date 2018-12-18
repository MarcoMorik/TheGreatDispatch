From 
# https://www.codingame.com



Genetic Algorithm to optimize this binpacking challenge. 

# TheGreatDispatch
Distribute the given boxes into a hundred trucks so that the lightest and heaviest have the smallest possible weight difference.

 (x) Rules

You are a great tycoon who needs to move materials, equipment and gold from Chicago to New York to build your next sky scraper. You have a convoy of 100 trucks and a variable amount of boxes to move. Unfortunately there are unscrupulous villains who would like to steal the gold from one of your shipments. They work at the highway weigh station and plan to pillage a truck that holds gold. They think the trucks with gold will be much heavier than the trucks without.

Your mission is to sneak the gold passed by distributing the boxes across the trucks in a way that the lightest truck and the heaviest truck weigh almost the same amount.

The villains have a sophisticated contraption that will tell them the largest weight difference of a convoy, the higher the difference, the more likely the heaviest trucks contain gold. In order to minimize the chances of an attack on one of your trucks, can you outsmart them with a strong algorithm to allocate the boxes?

You are given a list of boxes, each with a weight and a volume. Your code must output for each box, in the same order as they were given, in which of the 100 trucks labelled 0 to 99 you decide to place that box.

Each truck can carry a maximum volume of boxes of 100. You should assume the box volumes simply add together on a given truck. There is no limit on the weight of the boxes.

If you successfully place each box in the trucks, you will be awarded a delta score corresponding to the weight difference of your heaviest and lightest trucks. You will be ranked according to the sum of this value for every validation test case, the lower the better.

