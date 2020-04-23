## Project 1
Student Name: Taotao Pan
Student ID: 45004821
Student Email: taotao.pan@uqconnect.edu.au

This report consists of two parts, in the first part, a betweeness centrality algorithm called brandes betweenness centrality will be presented along with the theory, formula and some details. In the second part, another classic centrality algorithm called pagerank will be demonstrated as well.

### Brandes algorithm
Betweenness centrality analysis has many real world applications, areas are covered like analyzing real time traffic congestion to reduce the pressure of centain hotspot routes. Another application is network traffic analysis. For example, to mitigate the cost of critical routes failure, network designer may have to add redundant routes to reduce the risk. Betweenness centrality measures the number of times the shortest path passes between different nodes [1](#Reference). In order to find the shortest path between all pair of nodes, there are generally $\mathcal{O}(n^3)$ times and $\mathcal{O}(n^2)$ spaces [2](#Reference). However, brandes algorithm only requires $\mathcal{O}(n+m)$ space and $\mathcal{O}(nm)$ time complexity in unweighted graph. Following describes how brandes algorithm works.

Brandes algorithm traverses through the whole graph twice. In the forward traveral, by utilizing BFS search, it records the number of ways that from one node to another node in shortest path. In the backward traversal, each nodes get its centrality measure by sharing the centrality from its children based on number of shortest paths passed from it.

##### Formula
a simpler version of betweenness centrality measure is
$$
C_B(v)=\sum_{s,t\in v}\frac{\sigma(s,t|v)}{\sigma(s,t)}
$$
where $v$ represents a set of nodes, $s,t$ stands for source and target respectivly, in plain English, the formula above means the centrality for any node in a network is the number of shortest path from $s$ to $t$ in which pass through this node divide by the total number of shortest paths. Based on this formula, brandes algorithm introduces an extra term called one-side dependencies
$$
\delta(s|v) = \sum_{s\in v}\delta(s,t|v)
$$
The full brandes algorithm is following
$$
\delta(s|v) = \sum_{\substack{(v,w)\in E \\ w:d(s,w)=d(s,v)+1}}\frac{\sigma(s,v)}{\sigma (s,w)}(1+\delta(s|w))
$$

The first part $\frac{\sigma (s,v)}{\sigma (s,w)}$ is essentially the proportion of the shortest paths each preceding nodes share. For example, if two nodes point to one node, each of these two nodes contribute 2 and 4 shortest paths to the next node. In backward flow, each gets $\frac{2}{6}=\frac{1}{3}$ and $\frac{4}{6}=\frac{2}{3}$ respectively.

The next part of brandes algorithm is $1+\delta(s|w)$. Which is essentially the dependencies get from previous node in a backward flow. The dependency for the first node is 0.

##### Implementation details
In the forward flow, a BFS search is implemented, the most important one is backward flow. Here is the snippets for backward flow.

![Screen Shot 2020-04-23 at 1.30.19 PM](https://i.imgur.com/MRhqXnC.png)

##### Result
The top 10 nodes are

> 107, 1684, 3437, 1912, 1085, 0, 698, 567, 58, 428

The table following is the top 10 nodes with weight
|node | weight  |
|-------------|-------------|
|107   | 7837158.288881488 |
|1684  | 5510611.373816563 |
|3437  | 3853050.303142949 |
|1912  | 3741874.424513491 |
|1085  | 2433193.516720963 |
|0     | 2389030.2261587656 |
|698   | 1884086.4929644049 |
|567   | 1574031.8111882368 |
|58    | 1379227.9667493433 |
|428   | 1052366.1355515202 |


### Pagerank
Pagerank is a very famous centrality measure algorithm, it was developed by google's two creators. The general idea behind pagerank is like reference of paper. If one paper is cited by many other papers we consider this paper as an important paper. Which means its centrality is larger, when this paper refers another paper which not cited by many papers, even that paper is not cited by many other papers, it still get certain amount of score from that important paper.
##### Formula
$$
C_p = \alpha A^TD^{-1}C_p + \beta1
$$
where $A$ here is the adjacency matrix of the whole network, in an unweighted network, this value can be ignored, because all weights are just 1. $D^{-1}$ is the reciprocal of the diagonal matrix. Which essentially the reciprocal of the number of out-degree. $\alpha$ is controlling term, it is useful when we know the context of the network and $\beta$ is the bias term, it generally calculated as $1-\alpha$. Although above calculation can be done in a matrix format, in a large network, to create a adjacency matrix is generally not considered as efficient. Therefore, a power iteration version of pagerank is used to implement pagerank, next section gives the pseudocode.

##### Power iteration pseudocode
$$
\text{Set }c^0 \leftarrow 1, k \leftarrow 1 \\
1: c^k \leftarrow \alpha A^Tc^{k-1} + \beta1 \\
2: \text{if} ||c^k - c^{k-1}|| > \epsilon \\
3: k \leftarrow k + 1, \text{goto 1}
$$

##### Implementation detail
the whole algorithm is not complex. However, since we do not use matrix multiplication, there is a caustion in updating weights. When updating weights inside loop, lastest weights need to refer old weights, if we do not have a copy of old weights, the updated weights generate error. Following code is the kernal of this algorithm
![Screen Shot 2020-04-22 at 10.25.16 PM](https://i.imgur.com/TPpe7QR.png)

##### Result
The top 10 central nodes in given dataset is

> 107, 3437, 0, 1684, 1912, 348, 414, 3980, 686, 698

Here is the node rank with weights

| node |           weight       |
|------|------------------------|
|107   | 1.416440134230379e+175 |
|3437  | 5.886373407453194e+174 |
|0     | 1.313773439780986e+171 |
|1684  | 9.52634329068737e+166 |
|1912  | 5.055498693610239e+148 |
|348   | 1.1822452830083829e+125 |
|414   | 1.3512442578476555e+121 |
|3980  | 2.788244572013808e+120 |
|686   | 2.1766146771985174e+118 |
|698   | 3.7020934420872314e+98 |

## Summary
Brandes algorithm uses a smart way to the reduce brute force way to calculate the total number of shortest path between two different nodes. The difficult part of this algorithm is to understand the pair denpendency concept. For pagerank, the implementation in networkx is another version that different from our course. However, the general idea is same. The implementation in networkx adds some extra term, like dangling term [3](#Reference). What's more, when determine stopping the iteration, networkx uses the threshold to multiply the total number of nodes，hence when there are a lot nodes in a graph, the convergence time can be reduced.


## Reference
[1] [social network analysis](https://cambridge-intelligence.com/keylines-faqs-social-network-analysis/)
[2] [a fast algorithm for betweenness centrality](https://d1b10bmlvqabco.cloudfront.net/attach/k6oypy582xc46g/k6pzzh0uq171kp/k8vic6pjvyh6/A_faster_algorithm_for_betweenness_centrality.pdf)
[3] [pagerank](http://ilpubs.stanford.edu:8090/422/1/1999-66.pdf)