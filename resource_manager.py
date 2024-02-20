
class process:
    def __init__(self):
        self.state = 1
        self.parent = -1
        self.children = []
        self.resources = []
        self.priority = -1

class resource:
    def __init__(self):
        self.state = 0
        self.waitlist = []
        self.inventory = -1

def create(p):
    global pcb
    global rl
    for i in range(0, 16):
        if pcb[i] == -1:
            newone = process()
            newone.state = 1
            newone.priority = p
            pcb[i] = newone
            pcb[current_process()].children.append(i)
            newone.parent = current_process()
            rl[p].append(i)
            print("process " + str(i) + " created")
            scheduler()
            break
        elif i == len(pcb) - 1:
            print("too many processes")

def destroy(j):
    global pcb
    global rl

    #only can delete current or child process
    if j == current_process() or j in pcb[current_process()].children:
        #remove j from parents list of children
        theparent = pcb[j].parent
        if theparent != -1:
            #print("child being removed " + str(pcb[theparent].children) + "current" + str(j))
            #print("child being removed " + str(theparent))
            
            pcb[theparent].children.remove(j)
            #print("again" + str(pcb[theparent].children))
        
        #release resources
        theresources = pcb[j].resources
        for r, k in theresources:
            releasefordes(r, k)
        #j and decendesnt are removed
        remove(j)

        #removing j from rl

        for thelist in rl:
            if j in thelist:
                thelist.remove(j)

        print(str(total) + " process/es destroyed")
        scheduler()
    else:
        print("process not in child")
        file1.write("-1 ")



def remove(j):

    
  
    global pcb
    global total

    if len(pcb[j].children) == 0:
   

        #print("removing process" + str(j))
        pcb[j] = -1
        total +=1
    else:
        for child in pcb[j].children:
            #print("in process " + str(j) + "child " + str(child))
            if child in rl[pcb[child].priority]:
                rl[pcb[child].priority].remove(child)
            remove(child)
        #print("need to backtrack" + str(j) + "j delete here")
        pcb[j] = -1
        total +=1
        


def request(r, k):
    global rcb
    global rl

    if len(pcb[current_process()].resources) == 0:
        
        if rcb[r].state >= k:
               
                rcb[r].state -= k
                pcb[current_process()].resources.append((r, k))
                print("resource " + str(r) + " allocated " + str(k) + " units")
                scheduler()
                return
        else:
         
            pcb[current_process()].state = 0
            prior = pcb[current_process()].priority
            
            rl[prior].remove(current_process())
       
            rcb[r].waitlist.append((current_process(), k))
            print("process " + str(current_process()) + " blocked")
            
            scheduler()
    #print("made it 3 " + str (len(pcb[current_process()].resources))) 

    for x in range(0, len(pcb[current_process()].resources)):
     
        if pcb[current_process()].resources[x][0] == r:
            #RETEST WITH THIS
            if k <= rcb[r].state:
            
                
                old = pcb[current_process()].resources[x][1]
                pcb[current_process()].resources.append((x, old + k))
                pcb[current_process()].resources.pop(x)
                #print(str(pcb[current_process()].resources[x][1]))
            else:
                print("resource exists for process")
            break
        elif x == len(pcb[current_process()].resources) -1:
         
            if rcb[r].state >= k:
                rcb[r].state -= k
                pcb[current_process()].resources.append((r, k))
                print("resource " + str(r) + " allocated " + str(k) + " units")
            
            else:
                pcb[current_process()].state = 0
                prior = pcb[current_process()].priority
                rl[prior].remove(current_process())
                rcb[r].waitlist.append((current_process(), k))
                print("process " + str(current_process()) + " blocked")
            
                scheduler()

    
            
def releasefordes(r, k):
    for thing in pcb[current_process()].resources:
        if thing[0] == r and k <= thing[1]:
            if k == thing[1]:
                pcb[current_process()].resources.remove((r, k))
            else:
                difference = thing[1] - k
                thing[1] = difference


            rcb[r].state += k
            while (len(rcb[r].waitlist) != 0 and rcb[r].state>0):
                thenext = rcb[r].waitlist[0]
                if rcb[r].state >= k:
                    rcb[r].state -= k
                    pcb[thenext[0]].resources.append((r, k))
                    pcb[thenext[0]].state = 1
                    rcb[r].waitlist.pop(0)
                    prior = pcb[thenext[0]].priority
                    rl[prior].append(thenext[0])
                else:
                    break

            scheduler()
            break
        else:
            pass

        

        print("resource " + str(r) + " released")
    else:
        pass      


def scheduler():
    global isinit
    global init_counter
    print("process " + str(current_process()) + " running")
    s = str(current_process())
    if isinit == True and init_counter == 1:
        file1.write(s + " ")
        isinit = False
    elif isinit == True:
        file1.write("\n" + s + " ")
        isinit = False
    else:
        file1.write(s + " ")


def release(r, k):
    if r <= 3:

        for thing in pcb[current_process()].resources:
            if thing[0] == r and k <= thing[1]:
                if k == thing[1]:
                    pcb[current_process()].resources.remove((r, k))
                else:
                    difference = thing[1] - k
                    thing[1] = difference


                rcb[r].state += k
                while (len(rcb[r].waitlist) != 0 and rcb[r].state>0):
                    thenext = rcb[r].waitlist[0]
                    if rcb[r].state >= k:
                        rcb[r].state -= k
                        pcb[thenext[0]].resources.append((r, k))
                        pcb[thenext[0]].state = 1
                        rcb[r].waitlist.pop(0)
                        prior = pcb[thenext[0]].priority
                        rl[prior].append(thenext[0])
                    else:
                        break

                scheduler()
               
                break
            else:
                file1.write("-1 ")
                

            print("resource " + str(r) + " released")
    else:
        file1.write(str(-1) + " ")
        print("error")



def timeout():
    global rl
    current = current_process()
    if current != 0:
        prior = pcb[current].priority
        rl[prior].pop(0)
        rl[prior].append(current)
        scheduler()
    else:
        scheduler()


def init():
    global pcb
    global rcb
    global rl
    global isinit
    global init_counter
    init_counter += 1

    pcb = [-1] * 16
    r0 = resource()
    r0.state = 1
    r0.inventory = 1

    r1 = resource()
    r1.state = 1
    r1.inventory = 1

    r2 = resource()
    r2.state = 2
    r2.inventory = 2

    r3 = resource()
    r3.state = 3
    r3.inventory = 3

    rcb = [r0, r1, r2, r3]

    process0 = process()
    process0.parent = 0
    pcb[0] = process0
    rl = [[0], [], []]
    isinit = True
    scheduler()

def current_process():
    for i in range(2, -1, -1):
        if len(rl[i]) == 0:
            pass
        else:
            return rl[i][0]

if __name__ == '__main__':

    pcb = []
    rcb = []
    rl = []
    total = -1
    isinit = False
    init_counter = 0

    pcb = [-1] * 16
    r0 = resource()
    r0.state = 1
    r0.inventory = 1

    r1 = resource()
    r1.state = 1
    r1.inventory = 1

    r2 = resource()
    r2.state = 2
    r2.inventory = 2

    r3 = resource()
    r3.state = 3
    r3.inventory = 3

    rcb = [r0, r1, r2, r3]

    process0 = process()
    process0.parent = 0
    pcb[0] = process0
    rl = [[0], [], []]
    

    file1 = open('output.txt', 'w')
    
    with open("input.txt") as file:
        for item in file:

            action = item.split()
            #print(action)

            if action == []:
                pass
            
            elif action[0] == 'cr':
                if int(action[1]) < 1 or int(action[1]) > 2:
                    print("errorr")
                    
                else:
                    create(int(action[1]))
            elif action[0] == 'de':
                total = 0
                destroy(int(action[1]))
                    #print(pcb[0].children)
            elif action[0] == 'rq':
                if current_process() == 0:
                    print("can't request on process 0")
                elif int(action[1]) in [0, 1, 2, 3]:
                    request(int(action[1]), int(action[2]))
                else:
                    print("resource dne")
                    file1.write("-1 ")
            elif action[0] == 'rl':
                release(int(action[1]), int(action[2]))
            elif action[0] == "to":
                timeout()
            elif action[0] == "in":
                init()
    
            else:
                break

    file1.close()
            
                

