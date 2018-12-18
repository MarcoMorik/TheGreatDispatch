import sys
import math
import numpy as np

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
truck_count = 100
truck_cap = 100
box_count = int(input())
W = np.zeros((box_count,2))
box_cksm = np.sum(range(box_count))
sample_size=25

for i in range(box_count):
    weight, volume = [float(j) for j in input().split()]
    W[i,:] = [weight, volume]
    
goal= np.sum(W[:,0]) / 100.

def delta(Y):
    #print(sum([sum(y) for y in Y]), file=sys.stderr)
    if(sum([sum(y) for y in Y]) != box_cksm):
        return box_count*100
    X = distribute(Y)
    return np.max(X[:,0]) - np.min(X[:,0])
    

def distribute(Y):
    """Convert a distribution of boxes to the corresponding weights/volumes """
    global W
    
    
    X = np.zeros((truck_count,2))
    #print("Package distributed", sum([len(y) for y in Y]), file=sys.stderr)
    
    X[:,0] = [sum([W[b,0] for b in t]) for t in Y]
    X[:,1] = [sum([W[b,1] for b in t]) for t in Y]
    assert(np.max(X[:,1]) <= 100)
    return X
    
def prob_assign(X,Y, free_boxes):
    total = len(free_boxes)
    #print("Boxes unasigned", total, float(total)/box_count, file=sys.stderr)
    #print("Assigned boxes", [len(b) for b in Y], file=sys.stderr)
    
    
    print(sum([len(b) for b in Y]), total, file=sys.stderr)
    #print("Max Boxnumber",np.max([b]), file=sys.stderr)
    #Check for double element
    assert(len([r for t in Y for r in t ]) == len(list(set([r for t in Y for r in t ]))))
    
    assert(sum([len(b) for b in Y]) == box_count - total)
    assert(np.max(X[:,1]) <=100)
    for package in range(len(free_boxes)+10):
        
        #print(Y, " total length \n", sum([len(y) for y in Y]), file=sys.stderr)
        
        if len(free_boxes) <= 0:
            #Done
            #print(sum([len(y) for y in Y]), file=sys.stderr)
            assert(len(Y)==truck_count and sum([len(b) for b in Y]) == box_count)
            return Y
            
        #if(len(free_boxes) == np.count_nonzero([not len(y) for y in Y])):
        #    free_trucks = np.nonzero([not len(y) for y in Y])
        #    for i,b in enumerate(free_boxes):
        #        t = free_trucks[i]
        #    return Y
        
        choice = np.random.rand()
        if(choice <= 0.1):
            b = free_boxes.pop(np.random.randint(len(free_boxes)))
            w,v = W[b,:]
            truck_score = np.argsort( (X[:,0]+w-goal))
            
        elif(choice <=0.2):
            b = free_boxes.pop(np.random.randint(len(free_boxes)))
            w,v = W[b,:]
            truck_score = np.argsort( abs((X[:,0]+w-goal)))
        elif(choice <=0.6 and package >=total/2):
            b = free_boxes.pop(np.argmin([W[x,0] for x in free_boxes]))
            w,v = W[b,:]
            truck_score = np.argsort( abs((X[:,0]+w-goal)))
        
        else:
            b = free_boxes.pop(np.argmax([W[x,0] for x in free_boxes]))
            w,v = W[b,:]
            truck_score = np.argsort( (X[:,0]+w-goal))
           
        for t in truck_score:
            if(X[t,1] + v <=100 and b not in [b  for t in Y for b in t]):
                X[t,0] += w
                X[t,1] += v
                Y[t].append(b)
                
                break
    print("Could not fill all ", file=sys.stderr)
    return None
            
def Y_to_Out(Y):
    out = [0 for i in range(box_count)]
    for t,y in enumerate(Y):
        for b in y:
            out[b]=str(t)
    print(" ".join(out))
    #print("0 0 0 0 0 ...")

def resample(top_5,X,Y):
    """X: 100x2x25
    Y: 25x100x? """
    j=0
    for A in top_5:
        for i in range(5):
            best_trucks  = np.argsort([ abs(X[t,0,A]-goal) for t in range(truck_count)])
            
            
            #A represents Y[j] as we use the best models 5 times
            Y[j] = [y if i in best_trucks[:50] and np.random.rand() <0.5 else [] for i,y in enumerate(Y[A])]#A) ]
            
            assert(len([r for t in Y[j] for r in t ] )== len(list(set([r for t in Y[j] for r in t ]))))
            X[:,:,j] = distribute(Y[j])
           
            j = j+1
            
            
    return X, Y
            

def find_solution():
    best = None
    print("Goal: ", goal, file=sys.stderr)
    print(min(W[:,0]),max(W[:,0]),min(W[:,1]),max(W[:,1]),file=sys.stderr)
    #First box, with maximum weight 
    B = list(range(box_count))
    X = np.zeros((truck_count,2,sample_size))
    Y = [[[] for i in range(truck_count)] for j in range(sample_size)]
    
    """
    sorted_box = np.argsort(W[:,0])
    print(sorted_box[-100:],file=sys.stderr)
    for i,b in enumerate(sorted_box[-100:]):
        if(W[b,0]<0.52*goal):
            break
        free_boxes.remove(b)
        X[i,:]=W[b,:]
        Y[i].append(b)
        print("There was a huge weight, could be used. Yeah ;) ", file=sys.stderr)
    """ 
    top=1000000
    for epoch in range(5):
        for i in range(sample_size):
            #B = [b for b in range(box_count) if not b in [b  for t in Y[i] for b in t]]
            B = [b for b in range(box_count)]
            for t in Y[i]:
                for b in t:
                    if(b in B):
                        B.remove(b)
                    else:
                        print("could not find box", b, file=sys.stderr)
            #print("B,S,Y",len(B), len(Y), len(Y[i]), file=sys.stderr)
            y_next = prob_assign(X[:,:,i],Y[i], B)
            assert(len([r for t in  y_next for r in t ]) == len(list(set([r for t in  y_next for r in t ]))))
            if y_next is not None:
                Y[i] = y_next
            
        scores = [delta(y) for y in Y]
        rank = np.argsort(scores) 
        
        print("Best Score", [scores[r] for r in rank[0:4]], file=sys.stderr)
        if(scores[rank[0]]< top):
            result = Y[rank[0]]
            top = scores[rank[0]]
        
        for r in rank[:5]:
            
            assert(len([r for t in  Y[r] for r in t ]) == len(list(set([r for t in  Y[r] for r in t ]))))
        X, Y = resample(rank[:5],X,Y)
        
    Y_to_Out(result)

find_solution()


# To debug: print("Debug messages...", file=sys.stderr)

