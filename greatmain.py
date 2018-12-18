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

def delta(X):
    #print(sum([sum(y) for y in Y]), file=sys.stderr)
    if(sum([sum(t) for t in X]) != box_cksm):
        print("Checksum wrong, score will be not used", X,  file=sys.stderr)
        return box_count*100
    Y = distribute(X)
    return np.max(Y[:,0]) - np.min(Y[:,0])
    

def distribute(X):
    """Convert a distribution of boxes to the corresponding weights/volumes """
    #global W
    
    
    Y = np.zeros((truck_count,2))
    #print("Package distributed", sum([len(y) for y in Y]), file=sys.stderr)
    
    Y[:,0] = [sum([W[b,0] for b in t]) for t in X]
    Y[:,1] = [sum([W[b,1] for b in t]) for t in X]
    assert(np.max(Y[:,1]) <= 100)
    return Y
    
def prob_assign(X,Y, free_boxes):
    total = len(free_boxes)
    #print("Boxes unasigned", total, float(total)/box_count, file=sys.stderr)
    #print("Assigned boxes", [len(b) for b in Y], file=sys.stderr)
    
    
    
    #print("Max Boxnumber",np.max([b]), file=sys.stderr)
    assigned_pckgs = [r for t in X for r in t ]
    #print("Assigned",len(assigned_pckgs),"free", total, "Boxcount:", box_count, file=sys.stderr)
    assert(len(free_boxes) + len(assigned_pckgs) == box_count )
    
    #print("Assignment",, file=sys.stderr)
    #Check for double element
    
    assert(len([r for t in X for r in t ]) == len(list(set([r for t in X for r in t ]))))
    
    assert(sum([len(b) for b in X]) == box_count - total)
    assert(np.max(Y[:,1]) <=100)
    for package in range(len(free_boxes)+10):
        
        #print(Y, " total length \n", sum([len(y) for y in Y]), file=sys.stderr)
        
        if len(free_boxes) <= 0:
            #Done
            #print(sum([len(y) for y in Y]), file=sys.stderr)
            assert(len(X)==truck_count and sum([len(b) for b in X]) == box_count)
            return X
            
        #if(len(free_boxes) == np.count_nonzero([not len(y) for y in Y])):
        #    free_trucks = np.nonzero([not len(y) for y in Y])
        #    for i,b in enumerate(free_boxes):
        #        t = free_trucks[i]
        #    return Y
        
        choice = np.random.rand()
        if(choice <= 0.1):
            b = free_boxes.pop(np.random.randint(len(free_boxes)))
            w,v = W[b,:]
            truck_score = np.argsort( (Y[:,0]+w-goal))
            
        elif(choice <=0.2):
            b = free_boxes.pop(np.random.randint(len(free_boxes)))
            w,v = W[b,:]
            truck_score = np.argsort( Y[:,0]+w-goal)
        elif(choice <=0.6 and package >=total/2):
            b = free_boxes.pop(np.argmin([W[x,0] for x in free_boxes]))
            w,v = W[b,:]
            truck_score = np.argsort( Y[:,0]+w-goal)
        
        else:
            b = free_boxes.pop(np.argmax([W[x,0] for x in free_boxes]))
            w,v = W[b,:]
            truck_score = np.argsort( (Y[:,0]+w-goal))
           
        for t in truck_score:
            if(Y[t,1] + v <=100):
                Y[t,0] += w
                Y[t,1] += v
                X[t] = X[t]+[b]
                break
    print("Could not fill all ", file=sys.stderr)
    return None
            
def X_to_Out(X):
    out = [0 for i in range(box_count)]
    for t,y in enumerate(X):
        for b in y:
            out[b]=str(t)
    print(" ".join(out))
    #print("0 0 0 0 0 ...")

def resample(top_5,X,Y):
    """X: 100x2x25
    Y: 25x100x? """
    j=0
    best_samples = [X[A].copy() for A in top_5]
    best_boxes = [Y[:,:,A].copy() for A in top_5]
    for a in top_5:
        
        best_dist = best_samples[int(j/5)]
        for i in range(5):
            #print(" truck load of first trucks" , Y[0,:,a], file=sys.stderr)
            best_trucks  = np.argsort([ abs(Y[t,0,a]-goal) for t in range(truck_count)])            
            
            #A represents X[j] as we use the best models 5 times
            X[j] = [x if i in best_trucks[:50] and np.random.rand() <0.5 else [] for i,x in enumerate(best_dist)]#A) ]
            
            assert(len([r for t in X[j] for r in t ] )== len(list(set([r for t in X[j] for r in t ]))))
            
            j = j+1
            
    for s,x in enumerate(X):
        
        Y[:,:,s] = distribute(x)
            
    return X, Y
            

def find_solution():
    best = None
    print("Goal: ", goal, file=sys.stderr)
    print(min(W[:,0]),max(W[:,0]),min(W[:,1]),max(W[:,1]),file=sys.stderr)
    #First box, with maximum weight 
    B = list(range(box_count))
    Y = np.zeros((truck_count,2,sample_size))
    X = [[[] for i in range(truck_count)] for j in range(sample_size)]
    X_new = [[[] for i in range(truck_count)] for j in range(sample_size)]
    
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
        
        X_new = [[[] for i in range(truck_count)] for j in range(sample_size)]
        for x in X:
            assert(len([r for t in x for r in t ] )== len(list(set([r for t in x for r in t ]))))
        for i,x in enumerate(X):
            assert(len([r for t in x for r in t ] )== len(list(set([r for t in x for r in t ]))))
            B = [b for b in range(box_count) if not b in [b  for t in x for b in t]]
            #print("B,S,Y",len(B), len(Y), len(Y[i]), file=sys.stderr)
            x_next = prob_assign(X[i],Y[:,:,i], B)
            
            assert(len([r for t in  x_next for r in t ]) == len(list(set([r for t in  x_next for r in t ]))))
            if x_next is not None:
                X_new[i] = x_next
        X = X_new[:]
        
        scores = [delta(x) for x in X]
        rank = np.argsort(scores) 
        
        print("Best Score", [scores[r] for r in rank[0:4]], file=sys.stderr)
        if(scores[rank[0]]< top):
            result = X[rank[0]]
            top = scores[rank[0]]
        
        for r in rank[:5]:
            assert(len([r for t in  X[r] for r in t ]) == len(list(set([r for t in  X[r] for r in t ]))))
        X, Y = resample(rank[:5],X,Y)
        for j in range(25):
            assert(len([r for t in X[j] for r in t ] )== len(list(set([r for t in X[j] for r in t ]))))
    X_to_Out(result)

find_solution()


# To debug: print("Debug messages...", file=sys.stderr)

