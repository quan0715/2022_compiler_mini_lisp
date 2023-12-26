for i in 1 2 3 4 5 6 7 8
  do
  for j in 1 2
    do
      echo 0$i\_$j.lsp
      python3 main.py < ./data/0$i\_$j\_hidden.lsp
    done
  done