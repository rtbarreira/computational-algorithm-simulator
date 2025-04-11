(defproject computational-algorithm-simulator "0.1.0-SNAPSHOT"
  :description "Simulador de algoritmos computacionais"
  :license {:name "MIT"}

  :plugins [[lein-project-version "0.1.0"]
            [lein-midje "3.2.2"]
            [lein-cloverage "1.2.4"]
            [lein-vanity "0.2.0"]
            [s3-wagon-private "1.3.5"]
            [lein-ancient "0.7.0"]
            [lein-cljfmt "0.9.2"]
            [lein-nsorg "0.3.0"]
            [changelog-check "0.1.0"]
            [lein-mutate "0.1.0"]]

  :dependencies [[org.clojure/clojure "1.12.0"]
                 [org.clj-commons/pretty "3.3.0"]
                 [funcool/cats "2.4.2"]]

  :test-paths ["test/"])