import csv
import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
from PIL import ImageTk, Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

file = open("C:\\Users\\Hania Kashif\\OneDrive - Habib University\\Semester 2\\DSA\\Project\\MoviesData.csv", "r")
data = list(csv.reader(file, delimiter=","))
file.close()

data = data[1:] #removing the first line
data = [a[:-1] for a in data] #removing the year
graph = {}

def getcostars(g,node): # direct connections of the given actor, adjacency list
    lst = []
    if node:
        for x in g[node]:
            lst.append(x)
    return lst

def addactors(graph,data): #initializing graph and adding actors as nodes
    for movie in data: 
            actors = movie[1].split(',')
            actors = [a.strip() for a in actors]
            for actor in actors: 
                if actor not in graph and actor != "":
                    graph[actor] = []
    return graph

addactors(graph,data)

def convert_to_adj_list(graph,data): # connections adding
    for movie in data:
        moviename = movie[0]
        actors = movie[1].split(',')
        actors = [a.strip() for a in actors] #removing spaces bw name
        for actor in actors:
            if actor != "":
                for actor1 in actors :
                    if actor1 != actor and actor1 != "":
                        tuple1 = (actor1,moviename)
                        tuple2 = (actor,moviename)
                        if tuple1 not in graph[actor]:
                            graph[actor].append(tuple1)
                        if tuple2 not in graph[actor1]:
                            graph[actor1].append(tuple2)
    return graph

convert_to_adj_list(graph,data)

def bfs_shortest_path(graph,source,destination):
    if source == destination:
        return(source)
    visited = []
    path = []
    queue = [(source, path)]
    while queue:
        (actor, path) = queue.pop(0)
        if actor == destination:
            path.append(actor)
            return path
        visited.append(actor)
        for costar, movie in getcostars(graph,actor):
            if costar not in visited:
                queue.append((costar, path + [actor, movie]))  # if no paths exists then this is a void function

def pathtoedges(table): #odd to get movie names 
    edges = []
    if table:
        for movie in range(1,len(table)-1,2):
            edges.append((table[movie-1],table[movie]))
            edges.append((table[movie+1],table[movie]))
    return edges

def pathtonodes(table): #even to get actors
    nodes = []
    if table:
        for actor in range(0,len(table),2):
            nodes.append(table[actor])
    return nodes

canvas = None

def close_window(): # closes code
    root.destroy()

def display_graph():
    global canvas

    output_label.config(text="")
    check = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz '

    Actor1 = node1_entry.get().strip()
    Actor2 = node2_entry.get().strip()

    if len(Actor1)==0:
        output_label.config(text="Please enter a name for Actor 1")
        if canvas:
            canvas.get_tk_widget().grid_forget()
        return
    if len(Actor2)==0:
        output_label.config(text="Please enter a name for Actor 2")
        if canvas:
            canvas.get_tk_widget().grid_forget()
        return

    for a in Actor1: 
        if a not in check:
            output_label.config(text="Please enter a valid name for Actor 1")
            if canvas:
                canvas.get_tk_widget().grid_forget()
            return
    for b in Actor2:
        if b not in check:
            output_label.config(text="Please enter a valid name for Actor 2")
            if canvas:
                canvas.get_tk_widget().grid_forget()
            return

    if Actor1 == Actor2:
        output_label.config(text="They are the same person")
        if canvas:
            canvas.get_tk_widget().grid_forget()
        return

    if Actor1 not in list(graph.keys()):
        output_label.config(text=f"Actor {Actor1} not in data")
        if canvas:
            canvas.get_tk_widget().grid_forget()
        return
    if Actor2 not in list(graph.keys()):
        output_label.config(text=f"Actor {Actor2} not in data")
        if canvas:
            canvas.get_tk_widget().grid_forget()
        return
    
    table = bfs_shortest_path(graph, Actor1, Actor2)
    nodes = pathtonodes(table)
    edges = pathtoedges(table)

    if table == None:
        output_label.config(text=f"No possible path between {Actor1} and {Actor2}")   
        if canvas:
            canvas.get_tk_widget().grid_forget()
        return
    else: 
        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)
    
        fig = plt.figure(figsize=(14, 6))
        pos = nx.spring_layout(G, k=0.5) # arranges the nodes to fit in the fig
        nx.draw_networkx_nodes(G, pos, nodelist=nodes, node_color='#C1C1CD', node_size=500)
        nx.draw_networkx_edges(G, pos, edgelist=edges, width=0.5, alpha=0.5, edge_color='b')
        nx.draw_networkx_labels(G, pos, font_size=10, font_family='serif')

        if canvas:
            canvas.get_tk_widget().grid_forget()
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().grid(row=4, column=1, columnspan=5, padx=5, pady=5)

# create the tkinter window  
root = tk.Tk()
root.title("Star Connections")
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.bind('<Escape>', lambda e: root.quit())

# set the background image
bg_image = tk.PhotoImage(file="background.png")

# Get the size of the window
w, h = root.winfo_screenwidth(), root.winfo_screenheight()

bg_label = tk.Label(root, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
bg_label.image = bg_image

root.geometry("%dx%d+0+0" % (w, h)) # Set the window size to the screen size

# Labels
tk.Label(root, text="Actor 1:").grid(row=1, column=0, padx=0, pady=0)
tk.Label(root, text="Actor 2:").grid(row=2, column=0, padx=0, pady=0)

output_label = tk.Label(root, text="Project: Star Connections")
output_label.grid(row=10, column=0, columnspan=1, padx=5, pady=5)

# Entry Boxes
node1_entry = tk.Entry(root)
node2_entry = tk.Entry(root)
node1_entry.grid(row=1, column=1, padx=5, pady=5)
node2_entry.grid(row=2, column=1, padx=5, pady=5)

# Button
tk.Button(root, text="Find Connection", command=display_graph).grid(row=3, column=1, columnspan=1, padx=5, pady=5)

root.mainloop()
