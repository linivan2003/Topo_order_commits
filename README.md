## Topological Ordered Commits
This is a python script that prints out commits from every single branch in topological order
## Example
In a repository:
```
git log --graph --oneline
```
*   40b13cf (HEAD -> master) Merge branch 'branch-2'
|\
| * c7b574d (branch-2) master c12
| * 190058d master c11
* | 611153b master c3
|/
* b1d3443 master c2
* 6eddf8f m c1
```
topo_order_commits.py will return
```
6eddf8f7c6a3e5993fffe85195dd383a2959be16
b1d3443886413fa19bd79bde0c42f6339c231883
190058d5cd5e378597942ff098c0dae22b0c2ffb
c7b574ddeaa58511be1fb7fe46676262d9e6fe73
611153b63e85ea5c3466bb49081984570a5d1354
40b13cf229e4e51ee5be79a7171a5f72554db296
```

## Usage
topo_order_commits.py must be inside the repository you would like to find information on.
```
Python3 topo_order_commits.py
```


