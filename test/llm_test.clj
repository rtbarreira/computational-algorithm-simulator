(ns llm-test
  (:require [clojure.test :refer :all]
            [sorting :as sorting]
            [graphs :as graphs]
            [dynamic :as dynamic]
            [search :as search]))

(deftest test-quicksort
  (is (= (sorting/quicksort [5 2 9 1 5 6]) [1 2 5 5 6 9])))

(deftest test-bfs
  (is (= (graphs/bfs {:A [:B :C], :B [:A :D], :C [:A :E], :D [:B], :E [:C]} :A)
         #{:A :B :C :D :E})))

(deftest test-fibonacci-memoized
  (let [fib-fn (dynamic/fibonacci-memoized)]
    (is (= (fib-fn 10) 55))))

(deftest test-binary-search
  (is (= (search/binary-search [1 3 5 7 9 11] 7) 3))
  (is (= (search/binary-search [1 3 5 7 9 11] 4) -1)))
