## Project 2
Student Name: Taotao Pan
Student ID: 45004821
Student Email: taotao.pan@uqconnect.edu.au

This report consists of two parts, in the first part, several neighbourhood based similarity algorithms are presented along with the theory, formula and some details. In the second part, network embedding algorithm called deepwalk is demonstrated as well.

### Neighbourhood based
There are a family of methods belong to neighbourhood based algorithm, the fundamental principle behind neighbourhood based methods is to find the common neighbours between two vertexes, and according different implementation, normalization may be added or penalty term may be added. In this project, three subsets of neighbourhood based methods are implemented. They are
- jaccard similarity
- Adamic/Adar
- preferential attachment

#### Jaccard similarity
jaccard similarity is essentially using set operation to measure the what the percentage of the common neighbour nodes shares the total neighbours. The formula for jaccard similarity is [1](#Reference)
$$
score(u,v) = \frac{|\Gamma(u)\cap \Gamma(v)|}{|\Gamma(u)\cup \Gamma(v)|}
$$
here, $u$ and $v$ represent two vertexes in a graph. The numerator of this formula means the common neighbours and the denominator means the total neighbours, to make it more concrete, there is a image about set operation.

![Screen Shot 2020-06-03 at 10.01.23 AM](https://i.imgur.com/XQ2IkrD.png)

#### Adamic/Adar
Adamic/Adar method uses similar concept as jaccard similarity. However, it adds a penalty term to reduce the influence of big figure inside a graph. For example, celebrities or super stars may followed by many people, but among these followers, many of them may not know each other. Therefore, if we just add this directly to the calculation as jaccard similarity, the calculation has significant bias. The way we do is adding penalty. The formula for adamic/adar is [2](#Reference)
$$
\sum_{w\in \Gamma(u)\cap \Gamma(v)}\frac{1}{log|\Gamma(w)|}
$$
the subscript of the summation notation is essentially doing a set intersection operation. However, there is a caveat when using this method. Since as you can see from this formula, we have a division in this formula. Therefore, we have to avoid $log(1) = 0$, in other words, self-loop vertex is prohibited.

#### Preferential attachment
Preferential attachment is a simple method. Its simplicity is based on empirical research [3](#Reference)
> on the basis of empirical evidence, that the probability of co-authorship of x and y is
correlated with the product of the number of collaborators of x and y.

The formula for preferential attachment is
$$
|\Gamma(u)||\Gamma(v)|
$$
However, due to the nature of its over simplicity. It is often not compete with the other two methods.

#### Result
By running the given data set. We have got the following result
| methods  | accuracy |
|---|---|
| Jaccard similarity  |  0.7 |
| Adamic/Adar  |  0.73 |
| Preferential attachment  |  0.2 |

the evaluation method is based on `Accuracy` of `confusion matrix` or in other words the corrected prediction divide by total.
Next second a more sophisticated method family called network embedding is presented.

### Network embedding
Network embedding refers to the approach of learning latent low-dimensional representations for the connections in a network [4](#Reference). In other words, it maps the high-dimensional data to a low-dimensional to easy study. Many machine learning algorithms require the input data is a real vector. However, in some cases, tabular data is not always easy to get. For example, graph based structure, it is possible to generate a adjacency matrix for a graph, but often the generated matrix was too sparse, which causes a lot of waste on memory.

The way that network embedding does is using the feature vectors that generated from random walk to build a neural network. Then mapping the high-dimensional data to lower-dimension. The lower-dimension data is essentially the hidden layer

This project uses `word2vec` to implement the network embedding algorithm. First of all, we use random walk to capture the structure of the graph. Based on different strateies, the generated feature vectors may different. In this project, we use three strategies, they are
- BFS search
- DFS search
- BFS_DFS search

BFS search is able to capture the local structure of a graph. Which losses the global structure, following is a sample snippets for BFS search to implement random walk
```python
def __bfs_search(self, node: str) -> List[str]:
    return [choice([node] + self.neighbours[node])
            for _ in range(self.walk_length)]
```

next is DFS search, it walk as far as it can. Therefore, the global structure is easier to be captured by this type of random walk
```python
def __dfs_search(self, node: str) -> List[str]:
    res: List[str] = [node]
    for _ in range(self.walk_length-1):
        node = choice(self.neighbours[node])
        res.append(node)
    return res
```

Last one is the combination of BFS search and DFS search, based on certain probability (using BFS or DFS), the random walk chooses where to go, following is the sample snippets
```python
def __bfs_dfs_search(self, node: str) -> List[str]:
    res: List[str] = [node]

    for _ in range(self.walk_length-1):
        if random() > self.probability:
            n = choice(self.neighbours[node])
            res.append(n)
        else:
            res.append(choice([node] + self.neighbours[node]))
    return res
```

#### Result
Based on different hyper parameters the we have list several results here

```python
random_walk_params = {
    'walk_length': 5,
    'iteration': 100,
    'strategy': Walk.BFS
}
hyper_params = {
    'min_count': 1,
    'workers': multiprocessing.cpu_count(),
    'iter': 10,
    'seed': 10,
    'sg': 1,
    'window': 4,
    'size': 100,
    'compute_loss': True,
    'callbacks': [callback(valid_set)]
}
```

Here is the loss and accuracy

|iteration| loss |  accuracy    |
|--|------|------------------------|
|0| 1943373.75  |  0.59 |
|1| 185376.0  |  0.61|
|2| 191433.5  |  0.61 |
|3| 195640.0  |  0.61 |
|4| 171899.75  |  0.61 |
|5| 210418.75  |  0.61 |
|6| 209109.75  |  0.61 |
|7| 177862.25  |  0.6 |
|8| 174686.25  |  0.62 |
|9| 178442.75  |  0.61 |

After change walk strategy from BFS to DFS
|iteration| loss |  accuracy    |
|--|------|---------------------|
|0 | 1870610.0 | 0.6 |
|1 | 324327.75 | 0.61 |
|2 | 301049.5 | 0.59 |
|3 | 295237.0 | 0.58 |
|4 | 301935.0 | 0.59 |
|5 | 289403.25 | 0.6 |
|6 | 293565.5 | 0.59 |
|7 | 333270.25 | 0.6 |
|8 | 291376.25 | 0.59 |
|9 | 295144.5 | 0.59 |

After changing `walk_length` to 20, and window size to 10
|iteration| loss |  accuracy    |
|--|------|---------------------|
|0 | 8594959.0 | 0.6 |
|1 | 6794286.0 | 0.59 |
|2 | 5991741.0 | 0.62 |
|3 | 5907518.0 | 0.61 |
|4 | 5906334.0 | 0.59 |
|5 | 4512994.0 | 0.6 |
|6 | 4457916.0 | 0.6 |
|7 | 4500480.0 | 0.61 |
|8 | 4483288.0 | 0.61 |
|9 | 4466108.0 | 0.61 |

## Summary
Overall, in this project. There are two main stream of algrithms are presented. One is memory based method like neighbourhood methods, another is based on machine learning. By this particular dataset, neighbourhood based method outperforms than machine learning based method like deep walk. However, this evidence is not necessarily say that neighbourhood based methods are always better than machine learning based method, because machine learning based methods have good performance on large volumn of dataset.


## Reference
[1] [Jacaard coefficient](https://networkx.github.io/documentation/stable/reference/algorithms/generated/networkx.algorithms.link_prediction.jaccard_coefficient.html#networkx.algorithms.link_prediction.jaccard_coefficient)
[2] [adamic adar index](https://networkx.github.io/documentation/stable/reference/algorithms/generated/networkx.algorithms.link_prediction.adamic_adar_index.html#networkx.algorithms.link_prediction.adamic_adar_index)
[3] [The link prediction problem for social networks](http://www.cs.cornell.edu/home/kleinber/link-pred.pdf)
[4] [Network embedding](https://arxiv.org/pdf/1911.11726.pdf)