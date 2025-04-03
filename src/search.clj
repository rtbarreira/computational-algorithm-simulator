(ns search)

(defn binary-search [coll target]
  (loop [low 0 high (dec (count coll))]
    (if (<= low high)
      (let [mid (quot (+ low high) 2)]
        (cond
          (= (nth coll mid) target) mid
          (< (nth coll mid) target) (recur (inc mid) high)
          :else (recur low (dec mid))))
      -1)))