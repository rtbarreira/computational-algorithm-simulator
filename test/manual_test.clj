(ns manual-test
  (:require [clojure.test :refer :all]
            [sorting :as sorting]
            [graphs :as graphs]
            [dynamic :as dynamic]
            [search :as search]))

(deftest quicksort-test
  (is (= (sorting/quicksort []) []))
  (is (= (sorting/quicksort [3 3 3 2 2 2]) [2 2 2 3 3 3]))
  (is (= (sorting/quicksort [9 8 7 6 5 4 3 2 1]) [1 2 3 4 5 6 7 8 9]))
  (is (= (sorting/quicksort [8 1 5 9 2 7 3 4])) [1 2 3 4 5 7 8 9]))

(deftest binary-search-test
  (is (= (search/binary-search [1 2 3 4 5 6 7 8 9] 5) 4))
  (is (= (search/binary-search [7 4 3 0 1 8 2] 2) -1)))

(deftest fibonacci-memoized-test
  (let [fib-fn (dynamic/fibonacci-memoized)]
    (is (= (fib-fn 1) 1))
    (is (= (fib-fn 0) 0))
    (is (= (fib-fn 7) 13))))

(deftest bfs-test
  (is (= (graphs/bfs {} :A)
         #{:A}))
  (is (= (graphs/bfs {:A [:B :C], :B [:A :D], :C [:A :E]} :A)
         #{:A :B :C :D :E})))