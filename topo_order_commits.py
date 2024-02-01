import os
import sys
import zlib
#strace -f -e trace=execve python your_script.py, i checked the execve, and it only called python, it did not call anything from git it means that there is no calls to git.
class	CommitNode:
    def	 	__init__ 	(self,	commit_hash):   
        self.commit_hash    = commit_hash  
        self.parents	= set()
        self.children	= set()
        
    def add_parent(self, parent_commit):
        self.parents.add(parent_commit)

    def add_child(self, child_commit):
        self.children.add(child_commit)
        
    def show_info(self):
        print("Parents:", self.parents)
        print("Children:", self.children)

    def show_children(self):
        return self.children

    def has_no_parents(self):
        if not self.parents:
            return 1
        return 0
    def remove_parents(self):
        self.parents = set()
    
def get_git_directory():
    cwd = os.getcwd()
    
    while cwd != '/':
        pwd = os.path.dirname(cwd)
        git_path = os.path.join(cwd,".git")
        if os.path.exists(git_path):
            return cwd
        else:
            cwd = pwd
    print ("Not inside a Git repository",file=sys.stderr)
    sys.exit(1)

def local_branch_names(directory):
    contents = os.listdir(directory)
    branches = {}
    for x in contents:          #go through each content of .git/refs/heads
        path = os.path.join(directory,x)           
        if os.path.isfile(path): #if file read it and save in dictionary
            file = open(path, 'r')
            commit_hash = file.readline().strip()
            file.close
            branches[x] = commit_hash
        elif os.path.isdir(path): #recursively find local branches in directories
            sub_branches = local_branch_names(path)
            branches.update({sub_branch: commit_hash for sub_branch, commit_hash in sub_branches.items()})
    return branches
def get_parent_hashes(working_directory,commit_hash):
    first_two = commit_hash[:2]  
    last_38 = commit_hash[2:]
    filename = os.path.join(working_directory,".git","objects",first_two,last_38) #open directory to commit
    compressed_contents = open(filename, 'rb').read()     #decompress to read contents of commit
    decompressed_contents = zlib.decompress(compressed_contents)
    final_contents = decompressed_contents.decode('utf-8').split('\n') # split into new lines
    parent_hashes = set()
    for line in final_contents: #go through each line and if it starts with parent add to the parent_hashes set
        if line.startswith('parent'):
            _, parent_hash = line.split(' ')
            parent_hashes.add(parent_hash)  # Store parent hashes in the set
    return((parent_hashes))

def build_commit_graph(working_directory,branches):
    graph = {} #stores CommitNodes key:hash value:CommitNode
    hashes_processed = set() #branch heads processed
    hashes_to_process = list(branches.values())
    while len(hashes_to_process) != 0:
        current_commit = hashes_to_process.pop(0)
        #print("processing " + current_commit)
        if current_commit in hashes_processed:
            continue
        if current_commit not in graph:
            node = CommitNode(current_commit)
            graph[current_commit] = node
        current_node = graph[current_commit]
        parent_commits = get_parent_hashes(working_directory,current_commit)
        for parent_commit in parent_commits:
            if parent_commit not in hashes_processed:
                hashes_to_process.append(parent_commit)
            if parent_commit not in graph:
                node = CommitNode(parent_commit)
                graph[parent_commit] = node
            parent_node = graph[parent_commit]
            parent_node.add_child(current_commit)
            current_node.add_parent(parent_commit)
            hashes_processed.add(current_commit)
    return graph

def topo_sort(graph):
    for key,value in graph.items():
        if value.has_no_parents() ==  1:
            start_commit = key
    sorted_list = []  # empty list that contains sorted elements (L)
    start = set() # starting set (S)
    start.add(start_commit)
    while len(start) != 0:
        commit = start.pop()
        node = graph[commit]
        sorted_list.append(commit)
        children = node.show_children()
        for child_commit in sorted(children):
            graph[child_commit].remove_parents()
            if graph[child_commit].has_no_parents() == 1:
                start.add(child_commit)
    if len(sorted_list) != len(graph):
                          print("error")
                          return;
    else:
                          return (sorted_list)

def print_sorted_order(graph,sorted_list):
    for commit in sorted_list:
        print(commit)
        
    
def topo_order_commits():
    working_directory = get_git_directory()    #get git directory
    directory = os.path.join(working_directory,".git","refs","heads")
    branches = local_branch_names(directory)   #find branch names, store in dictionary called branches
    graph = build_commit_graph(working_directory,branches)
    #for key, value in graph.items():
     # print(f"CommitNode: {key}")
      #print(value)
      #value.show_info()
      #print()
    sorted_list = topo_sort(graph)
    #print(sorted_list)
    print_sorted_order(graph,sorted_list)
    #Print the sorted order (can be helper function)


topo_order_commits()
