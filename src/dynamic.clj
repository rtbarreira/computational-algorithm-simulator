(ns dynamic)

(defn fibonacci-memoized []
  (let [cache (atom {0 0, 1 1})]
    (fn [n]
      (if-let [result (@cache n)]
        result
        (let [result (+ ((fibonacci-memoized) (- n 1))
                        ((fibonacci-memoized) (- n 2)))]
          (swap! cache assoc n result)
          result)))))
