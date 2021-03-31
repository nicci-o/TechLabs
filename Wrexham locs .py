#!/usr/bin/env python
# coding: utf-8

# In[1]:


#######################################################################################
# LIBRARIES
#######################################################################################

import pandas as pd # Pandas library
import numpy as np # Numpy library
import tkinter as tk # tk Interface library used for pop up boxes
import sys # Used for the command sys.exit() to break the program at that point
from tkinter import *
from PIL import ImageTk, Image

#######################################################################################
# FUNCTIONS
#######################################################################################

def dijkstra(graph,start,goal):
    '''
Find the shortest distance between two points from a graph variable.
The graph must be in the form of a dictionary in a dictionary for this function to run
correctly.
    '''
    shortest_distance={}  #will be constantly updated as code goes along, key (e.g. node) and value (e.g. shortest distance) can be inserted: {a:6}
    predecessor={} #used to find shortest path, include where path came from (shortest way from a to c has predecessor b to a)
    unseenNodes = graph 
    infinity = 999999
    path = []
    #all final distances need to be set to infinity except for start: needs to be set to 0
    for node in unseenNodes:
        shortest_distance[node]=infinity 
    shortest_distance[start]=0
    
    while unseenNodes:
        minNode=None
        for node in unseenNodes:
            if minNode is None:
                minNode = node
            elif shortest_distance[node] < shortest_distance[minNode]:
                minNode=node
                
        for childNode, weight in graph[minNode].items():
            if weight + shortest_distance[minNode]< shortest_distance[childNode]:
                shortest_distance[childNode]=weight + shortest_distance[minNode]
                predecessor[childNode]= minNode
        unseenNodes.pop(minNode)    
    # print(shortest_distance) /can be changed to print(predecessors)
    
    currentNode = goal
    while currentNode !=start:
        try:
            path.insert(0,currentNode)
            currentNode = predecessor[currentNode]
        except KeyError:
            print('Path not reachable')
            break
    path.insert(0,start)
    if shortest_distance[goal]!=infinity:
        return [shortest_distance[goal], path]

def make_the_points(table):
    '''
You upload a table and it will tell you if your table is compatable, i.e. it looks like a
square, symetric matrix with no values along the leading diagonal. If it is, then it will
generate a list of points for you. If not, the program will be terminated and an error
showing what went wrong will apear too.
    '''
    if table.shape[0] != table.shape[1]: # Making sure you have a square matrix
      print('Error in .xlsx file: number of columns != number of rows\nTerminating program')
      return None

    for i in range(table.shape[0]): # Checking your column and row headers are formatted correctly
        if (table.index[i] != table.columns[i]) or (table.index[i][0] == ' '): # if (column and row don't equal) or (there is a space at the start of them)
            print('Your columns/rows are not formatted correctly')
            return None
        
    count = 0
    for row in table.index:
        count += pd.notnull(table[row][row]) # Checking the leading diagonal has no values entered
      
        for column in table.index: # All of this is checking to see if you have a symetric matrix
            if (pd.notnull(table[row][column] or pd.notnull(table[column][row]))):
                if table[row][column] != table[column][row]:
                    print("A to B should be the same as B to A!")
                    print(f"The DataFrame has different values for ('{row}' to '{column}') and ('{column}' to '{row}')")
                    print("Go back and check the .xlsx file is correctly filled out\nTerminating program")
                    return None
                
    if count != 0: # if it doesn't equal 0 then it has at least one value along the leading diagonal
        print("Vertex to itself should not have a value assigned to it!")
        print("Go back and check the .xlsx file is correctly filled out\nTerminating program")
        return None
  
    return table.index

def create_graph(table, points):
    '''
Function that creates the graph out of a compatable (square matrix) DataFrame which can
be used by the dijkstras(graph, start, goal) function.
    '''
    Lists = [{} for i in range(table.shape[0])] # Creating a list of dictionaries
    graph = {}
    
    #for i in table.loc[points[0]][table.loc[points[0]].notnull()].index: print(table.at[points[0],i])
    
    #count2 = 0
    count1 = 0
    for point in points:
      for L in table.loc[point][table.loc[point].notnull()].index:
          if L != point: Lists[count1][L] = table.at[point, L] # Filling in the dictionaries
      graph[point] = Lists[count1]
      count1 += 1
    return graph



def route2(s):
    route = []
    for count in range(len(s)-1):
        checker = 0
        for point1 in s[count].split(','):
            for point2 in s[count + 1].split(','):
                if point1 == point2:
                    route.append(point1)
                    checker += 1
        if checker == 0:
            print('ERROR WITH HOW ROAD NAME WAS ENTERED')
            print(s)
            return None

    to_remove = []
    for i in range(len(route)-1):
        if route[i] == route[i+1]: to_remove.append(route[i])
    for i in to_remove: route.remove(i)
    return ' to '.join(route)



#######################################################################################
# REST OF PROGRAM
#######################################################################################

table = pd.read_excel('UPDATED_LOCATIONS.xlsx', index_col=0) # Importing the file with our data on it and making it into a DataFrame.

points = make_the_points(table) # If .xlsx file is formatted correctly, this will return table.index, else it will return None

if points is None: sys.exit() # If something is wrong with the way your .xlsx file is formatted, program will terminate at this point.

graph = create_graph(table, points) # Creates a graph compatible with the dijkstras function.

#**************************************************************************************************************


#######################################################################################
# Making the pop-up window
#######################################################################################


root=Tk()
root.title('Choose your path to happiness')
root.geometry('800x1000')
root.configure(background='#04B45F')
root.iconbitmap('smiley.ico')


def increase_label_font():
    fontsize = fontStyle['size']
    labelExample['text'] = fontsize+4
    fontStyle.configure(size=fontsize+4)


#upload images 

PointB_img = ImageTk.PhotoImage(Image.open('B5099 Alexandra Road.png'))
my_photolabelB = Label(image=PointB_img)

PointD_img = ImageTk.PhotoImage(Image.open('Empress Road Alexandra Road.png'))
my_photolabelD = Label(image=PointD_img)

PointC_img = ImageTk.PhotoImage(Image.open('B5099 Empress Road.png'))
my_photolabelC = Label(image=PointC_img)

PointE_img = ImageTk.PhotoImage(Image.open('B5099 Princess Street.png'))
my_photolabelE = Label(image=PointE_img)

PointF_img = ImageTk.PhotoImage(Image.open('Princess street Alexandra Road.png'))
my_photolabelF = Label(image=PointF_img)

PointG_img = ImageTk.PhotoImage(Image.open('B5099 A5152 Hampden Road.png'))
my_photolabelG = Label(image=PointG_img)

PointH_img = ImageTk.PhotoImage(Image.open('Alexandra Road A5152 Poyser Street.png'))
my_photolabelH = Label(image=PointH_img)

PointI_img = ImageTk.PhotoImage(Image.open('Edward Street A5152.png'))
my_photolabelI = Label(image=PointI_img)

PointJ_img = ImageTk.PhotoImage(Image.open('Hampden Road Poyser Street.png'))
my_photolabelJ = Label(image=PointJ_img)

PointK_img = ImageTk.PhotoImage(Image.open('Edward Street Poyser street.png'))
my_photolabelK = Label(image=PointK_img)

PointL_img = ImageTk.PhotoImage(Image.open('Fairy Road Court Road.png'))
my_photolabelL = Label(image=PointL_img)

PointM_img = ImageTk.PhotoImage(Image.open('Fairy Road Erddig Road Trevor Street.png'))
my_photolabelM = Label(image=PointM_img)

PointN_img = ImageTk.PhotoImage(Image.open('Sontley Road Erddig Road Trevor Street.png'))
my_photolabelN = Label(image=PointN_img)

PointO_img = ImageTk.PhotoImage(Image.open('Erdigg Road Bath Road.png'))
my_photolabelO = Label(image=PointO_img)

PointP_img = ImageTk.PhotoImage(Image.open('Erddig Road Fairfield Street Wellington Road.png'))
my_photolabelP = Label(image=PointP_img)

PointQ_img = ImageTk.PhotoImage(Image.open('Wellington Road A5152.png'))
my_photolabelQ = Label(image=PointQ_img)

PointR_img = ImageTk.PhotoImage(Image.open('A5152 Bath Road.png'))
my_photolabelR = Label(image=PointR_img)

PointS_img = ImageTk.PhotoImage(Image.open('A5152 Belmont Road.png'))
my_photolabelS = Label(image=PointS_img)

PointT_img = ImageTk.PhotoImage(Image.open('Empress Road A5152 Meredith Street.png'))
my_photolabelT = Label(image=PointT_img)

PointU_img = ImageTk.PhotoImage(Image.open('Fairy Road Belmont Road.png'))
my_photolabelU = Label(image=PointU_img)

PointV_img = ImageTk.PhotoImage(Image.open('Meredith Street Court Road.png'))
my_photolabelV = Label(image=PointV_img)

#create label
Label (root, text='Where would you like to start?', bg='#04B45F',fg='white',font='none 12 bold').grid(row=1, column=0,sticky=W, pady=5)

# Drop Down Box Start
    

def selected(event):
    
    
    myLabel = Label(root, text='Your starting point is:',bg='#04B45F',fg='white',font='none 12 bold').grid(row=4, column=0,sticky=W, pady=5)
    myLabel2 = Label(root, text=clicked.get(),bg='#04B45F',fg='white',font='none 12 bold').grid(row=4, column=2,sticky=W,pady=5)
    if clicked.get()==points[0]: 
         my_photolabelB.grid(row=4, column=8,sticky=W, padx=10)
    elif clicked.get()==points[1]:
         my_photolabelC.grid(row=4, column=8,sticky=W, padx=10)
    elif clicked.get()==points[2]:
         my_photolabelD.grid(row=4, column=8,sticky=W, padx=10)
    elif clicked.get()==points[3]:
         my_photolabelE.grid(row=4, column=8,sticky=W, padx=10)
    elif clicked.get()==points[4]:
         my_photolabelF.grid(row=4, column=8,sticky=W, padx=10)
    elif clicked.get()==points[5]:
         my_photolabelG.grid(row=4, column=8,sticky=W, padx=10)
    elif clicked.get()==points[6]:
         my_photolabelH.grid(row=4, column=8,sticky=W, padx=10)
    elif clicked.get()==points[7]:
         my_photolabelI.grid(row=4, column=8,sticky=W, padx=10)
    elif clicked.get()==points[8]:
         my_photolabelJ.grid(row=4, column=8,sticky=W, padx=10)
    elif clicked.get()==points[9]:
         my_photolabelK.grid(row=4, column=8,sticky=W, padx=10)
    elif clicked.get()==points[10]:
         my_photolabelL.grid(row=4, column=8,sticky=W, padx=10)
    elif clicked.get()==points[11]:
         my_photolabelM.grid(row=4, column=8,sticky=W, padx=10)
    elif clicked.get()==points[12]:
         my_photolabelN.grid(row=4, column=8,sticky=W, padx=10)
    elif clicked.get()==points[13]:
         my_photolabelO.grid(row=4, column=8,sticky=W, padx=10)
    elif clicked.get()==points[14]:
         my_photolabelP.grid(row=4, column=8,sticky=W, padx=10)
    elif clicked.get()==points[15]:
         my_photolabelQ.grid(row=4, column=8,sticky=W, padx=10)
    elif clicked.get()==points[16]:
         my_photolabelR.grid(row=4, column=8,sticky=W, padx=10)
    elif clicked.get()==points[17]:
         my_photolabelS.grid(row=4, column=8,sticky=W, padx=10)
    elif clicked.get()==points[18]:
         my_photolabelT.grid(row=4, column=8,sticky=W, padx=10)
    elif clicked.get()==points[19]:
         my_photolabelU.grid(row=4, column=8,sticky=W, padx=10)
    elif clicked.get()==points[20]:
         my_photolabelV.grid(row=4, column=8,sticky=W, padx=10)
            
options = points
    
clicked=StringVar()
clicked.set(options[0])

drop = OptionMenu(root, clicked, *options, command=selected)
drop.grid(row=3, column=0,sticky=W, pady=5)

# Drop Down Box Finish

#create label
Label (root, text='Where would you like to finish?', bg='#04B45F',fg='white',font='none 12 bold').grid(row=5, column=0, sticky=W, pady=5)


def selected(event):
    myLabel3 = Label(root, text='Your finishing point is:',bg='#04B45F',fg='white',font='none 12 bold').grid(row=7, column=0, sticky=W, pady=5)
    myLabel4 = Label(root, text=clicked2.get(),bg='#04B45F',fg='white',font='none 12 bold').grid(row=7, column=2, sticky=W, pady=5)
    if clicked2.get()==points[0]:
         Label.grid_forget and my_photolabelB.grid(row=7, column=8,sticky=W, padx=20)
    elif clicked2.get()==points[1]:
         my_photolabelC.grid(row=7, column=8,sticky=W, padx=20)
    elif clicked2.get()==points[2]:
         my_photolabelD.grid(row=7, column=8,sticky=W, padx=20)
    elif clicked2.get()==points[3]:
         my_photolabelE.grid(row=7, column=8,sticky=W, padx=20)
    elif clicked2.get()==points[4]:
         my_photolabelF.grid(row=7, column=8,sticky=W, padx=20)
    elif clicked2.get()==points[5]:
         my_photolabelG.grid(row=7, column=8,sticky=W, padx=20)
    elif clicked2.get()==points[6]:
         my_photolabelH.grid(row=7, column=8,sticky=W, padx=20)
    elif clicked2.get()==points[7]:
         my_photolabelI.grid(row=7, column=8,sticky=W, padx=20)
    elif clicked2.get()==points[8]:
         my_photolabelJ.grid(row=7, column=8,sticky=W, padx=20)
    elif clicked2.get()==points[9]:
         my_photolabelK.grid(row=7, column=8,sticky=W, padx=20)
    elif clicked2.get()==points[10]:
         my_photolabelL.grid(row=7, column=8,sticky=W, padx=20)
    elif clicked2.get()==points[11]:
         my_photolabelM.grid(row=7, column=8,sticky=W, padx=20)
    elif clicked2.get()==points[12]:
         my_photolabelN.grid(row=7, column=8,sticky=W, padx=20)
    elif clicked2.get()==points[13]:
         my_photolabelO.grid(row=7, column=8,sticky=W, padx=20)
    elif clicked2.get()==points[14]:
         my_photolabelP.grid(row=7, column=8,sticky=W, padx=20)
    elif clicked2.get()==points[15]:
         my_photolabelQ.grid(row=7, column=8,sticky=W, padx=20)
    elif clicked2.get()==points[16]:
         my_photolabelR.grid(row=7, column=8,sticky=W, padx=20)
    elif clicked2.get()==points[17]:
         my_photolabelS.grid(row=7, column=8,sticky=W, padx=20)
    elif clicked2.get()==points[18]:
         my_photolabelT.grid(row=7, column=8,sticky=W, padx=20)
    elif clicked2.get()==points[19]:
         my_photolabelU.grid(row=7, column=8,sticky=W, padx=20)
    elif clicked2.get()==points[20]:
         my_photolabelV.grid(row=7, column=8,sticky=W, padx=20)
        
options2 = points

clicked2=StringVar()
clicked2.set(options2[0])

drop2 = OptionMenu(root, clicked2, *options, command=selected)
drop2.grid(row=6, column=0, sticky=W, pady=5)


#Submit Button

def submit_entries():
    counter = 0
    if clicked.get() == clicked2.get(): # Checking they have chosen unique start and goal point
        Label (root, text ='Please choose a different end point to your starting point',bg='#04B45F',fg='white',font='none 20 bold').grid(row=20,column=0,sticky=W, pady=5)
        counter += 1

    if counter == 0: # Checking the route given back is correct. If it isn't then the names in the .xlsx file are quite possibly incorrect.
        start = clicked.get(); goal = clicked2.get()
        solution = dijkstra(graph, start, goal) #solution[0] is the shortest path, route2(solution[1]) is the route taken
        route = route2(solution[1])
    if route == None: Label (root, text ='ERROR FINDING ROUTE',bg='#04B45F',fg='white',font='none 20 bold').grid(row=20,column=0,sticky=W, pady=5)

    if counter == 0:
        print(solution)
        print(route)
        Label (root, text ='The route you should take to avoid interaction:',bg='#04B45F',fg='white',font='none 12 bold').grid(row=22,column=0,sticky=W, pady=5)
        Label (root, text =route ,bg='#04B45F',fg='white',font='none 12 bold').grid(row=22,column=2,sticky=W, pady=5)
        Label (root, text =f'Your route is estimated to have {int(solution[0])} people on it',bg='#04B45F',fg='white',font='none 12 bold').grid(row=42,column=0,sticky=W)
    
    
    
##add submit button
Button(root,text='Submit',width=14, command=submit_entries).grid(row=8,column=0,sticky=W)


#Quote Label

Label (root, text ='Happiness is a direction, not a place.',bg='#04B45F',fg='white',font='none 12 bold').grid(row=50,column=0, sticky=W,pady=5)
Label (root, text ='— Sydney J. Harris',bg='#04B45F',fg='white',font='none 12 bold').grid(row=51,column=0,sticky=W)

#exit label
Label (root,text='Click to exit:',bg='#04B45F',fg='white', font='none 12 bold').grid(row=65, column=0, sticky=W, pady=5)

#exit function
def close_window():
       root.destroy()
       exit()
       
##add exit button
Button(root,text='Exit',width=14, command=close_window).grid(row=70,column=0,sticky=W)


root.mainloop()


# In[ ]:



    
    

