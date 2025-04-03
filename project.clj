(defproject  computational-algorithm-simulator "0.1.0-SNAPSHOT"
  :description "Simulador de algoritmos computacionais"
  :dependencies [[org.clojure/clojure "1.11.1"]
                 [org.clojure/test.check "1.1.1"]]
  :profiles {:dev {:dependencies [[midje "1.10.9"]]}}
  :test-paths ["test"])
