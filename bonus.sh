for i in 1 2 3 4
  do
  for j in 1 2
    do
      echo b$i\_$j.lsp
      python3 main.py < ./data/b$i\_$j\_hidden.lsp
    done
  done