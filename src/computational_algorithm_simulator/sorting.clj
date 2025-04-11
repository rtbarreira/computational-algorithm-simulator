(ns computational_algorithm_simulator.sorting)

(defn quicksort [coll]
      (if (empty? coll)
        []
        (let [pivot (first coll)
              smaller (filter #(<= % pivot) (rest coll))
              larger (filter #(> % pivot) (rest coll))]
             (concat (quicksort smaller) [pivot] (quicksort larger)))))
