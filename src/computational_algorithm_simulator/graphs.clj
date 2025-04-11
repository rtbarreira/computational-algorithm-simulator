(ns computational_algorithm_simulator.graphs)

(defn bfs [graph start]
  (loop [queue [start] visited #{}]
    (if (empty? queue)
      visited
      (let [node (first queue)
            neighbors (remove visited (get graph node []))]
        (recur (concat (rest queue) neighbors) (conj visited node))))))

