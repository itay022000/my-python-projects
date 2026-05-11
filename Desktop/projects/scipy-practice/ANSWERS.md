# Practice Questions and Answers

> Generated from `exercises.py` by `generate_answers.py`.
> Run `python generate_answers.py --check` to verify this file is in sync.

## 1. Constants Exercise

### Question 1
**Question:** Convert 12 inches to meters  
**Reference answer:** `12 * const.inch`

---

### Question 2
**Question:** Convert 5 miles to meters  
**Reference answer:** `5 * const.mile`

---

### Question 3
**Question:** Convert 10 feet to meters  
**Reference answer:** `10 * const.foot`

---

### Question 4
**Question:** Convert 3 minutes to seconds  
**Reference answer:** `3 * const.minute`

---

### Question 5
**Question:** Convert 2 hours to seconds  
**Reference answer:** `2 * const.hour`

---

## 2. Optimization Exercise

### Question 1
**Question:** For linear(x) = x - 5, find the root near x0=0  
**Reference answer:** `optimize.root(linear, x0=0.0)`

---

### Question 2
**Question:** For quad(x) = x² - 4x + 3, find the minimum near x0=0  
**Reference answer:** `optimize.minimize(quad, x0=0.0)`

---

### Question 3
**Question:** For h(x) = x² - 9, find the root near x0=3  
**Reference answer:** `optimize.root(h, x0=3.0)`

---

### Question 4
**Question:** For g(x) = x² + 2x + 1, find the minimum near x0=0  
**Reference answer:** `optimize.minimize(g, x0=0.0)`

---

### Question 5
**Question:** For cubic(x) = x³ - 2x - 5, find the root near x0=2  
**Reference answer:** `optimize.root(cubic, x0=2.0)`

---

## 3. Sparse Matrices Exercise

### Question 1
**Question:** Convert dense_matrix to a CSR sparse matrix  
**Reference answer:** `sparse.csr_matrix(dense_matrix)`

---

### Question 2
**Question:** Get the number of non-zero elements in csr_example  
**Reference answer:** `csr_example.nnz`

---

### Question 3
**Question:** Convert csr_example to CSC format  
**Reference answer:** `csr_example.tocsc()`

---

### Question 4
**Question:** Get the shape of csr_example  
**Reference answer:** `csr_example.shape`

---

### Question 5
**Question:** Add sparse.csr_matrix(dense_matrix) and sparse.csr_matrix(dense_matrix2)  
**Reference answer:** `sparse.csr_matrix(dense_matrix) + sparse.csr_matrix(dense_matrix2)`

---

## 4. CSGraph Exercise

### Question 1
**Question:** Find the number of connected components in graph2_sparse  
**Reference answer:** `csgraph.connected_components(graph2_sparse, directed=False, return_labels=False)`

---

### Question 2
**Question:** Check if chain_sparse is connected (has exactly 1 component)  
**Reference answer:** `csgraph.connected_components(chain_sparse, directed=False, return_labels=False) == 1`

---

### Question 3
**Question:** Find the shortest path distance matrix for chain_sparse  
**Reference answer:** `csgraph.shortest_path(chain_sparse, directed=False)`

---

### Question 4
**Question:** Find the shortest path distance matrix for a 3-node fully connected graph (use sparse.csr_matrix(np.array([[0,1,1],[1,0,1],[1,1,0]])))  
**Reference answer:** `csgraph.shortest_path(sparse.csr_matrix(np.array([[0,1,1],[1,0,1],[1,1,0]])), directed=False)`

---

### Question 5
**Question:** Find the shortest path distance matrix for a directed graph (use sparse.csr_matrix(np.array([[0,1,0],[0,0,1],[0,0,0]]))) with directed=True  
**Reference answer:** `csgraph.shortest_path(sparse.csr_matrix(np.array([[0,1,0],[0,0,1],[0,0,0]])), directed=True)`

---

## 5. Spatial Data Exercise

### Question 1
**Question:** Calculate the Euclidean distance between p1 (0, 0) and p2 (5, 12)  
**Reference answer:** `distance.euclidean(p1, p2)`

---

### Question 2
**Question:** Calculate the Manhattan distance between p3 (1, 2) and p4 (4, 6)  
**Reference answer:** `distance.cityblock(p3, p4)`

---

### Question 3
**Question:** Calculate the Chebyshev distance between p5 (2, 3) and p6 (5, 7)  
**Reference answer:** `distance.chebyshev(p5, p6)`

---

### Question 4
**Question:** Calculate pairwise Euclidean distances for points_array [[0, 0], [1, 1], [4, 5]]  
**Reference answer:** `distance.pdist(points_array, metric='euclidean')`

---

### Question 5
**Question:** Calculate the Minkowski distance between p7 (1, 1) and p8 (4, 5) with p=3  
**Reference answer:** `distance.minkowski(p7, p8, p=3)`

---

## 6. Interpolation Exercise

### Question 1
**Question:** Create a linear interpolation function for x_points and y_points  
**Reference answer:** `interpolate.interp1d(x_points, y_points, kind='linear')`

---

### Question 2
**Question:** Create a quadratic interpolation function for x_points2 and y_points2  
**Reference answer:** `interpolate.interp1d(x_points2, y_points2, kind='quadratic')`

---

### Question 3
**Question:** Create a cubic interpolation function for x_points2 and y_points2  
**Reference answer:** `interpolate.interp1d(x_points2, y_points2, kind='cubic')`

---

### Question 4
**Question:** Create a nearest interpolation function for x_points and y_points  
**Reference answer:** `interpolate.interp1d(x_points, y_points, kind='nearest')`

---
