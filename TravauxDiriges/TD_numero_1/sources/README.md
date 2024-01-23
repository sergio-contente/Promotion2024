
# TD1

`pandoc -s --toc README.md --css=./github-pandoc.css -o README.html`

## lscpu

```
CPU(s):                  16
  On-line CPU(s) list:   0-15
Vendor ID:               AuthenticAMD
  Model name:            AMD Ryzen 7 4800H with Radeon Graphics
    CPU family:          23
    Model:               96
    Thread(s) per core:  2
    Core(s) per socket:  8
    Socket(s):           1
    Stepping:            1
    Frequency boost:     enabled
    CPU max MHz:         2900,0000
    CPU min MHz:         1400,0000
Caches (sum of all):     
  L1d:                   256 KiB (8 instances)
  L1i:                   256 KiB (8 instances)
  L2:                    4 MiB (8 instances)
  L3:                    8 MiB (2 instances)
```

*Des infos utiles s'y trouvent : nb core, taille de cache*

## Produit matrice-matrice

### Permutation des boucles

*Expliquer comment est compilé le code (ligne de make ou de gcc) : on aura besoin de savoir l'optim, les paramètres, etc. Par exemple :*

`make TestProduct.exe && ./TestProduct.exe 1024`

  ordre           | time    | MFlops  | MFlops(n=2048)
------------------|---------|---------|----------------
i,j,k (origine)   | 8.38753 | 7256.033 |
j,i,k             | 8.6158 | 249.249 |
i,k,j             | 30.9459 | 69.3948 |
k,i,j             | 33.5355 | 64.0361 |
j,k,i             | 0.522769 | 4107.9 |
k,j,i             | 0.844189 | 2543.84 |

*Discussion des résultats*

- L'ordre optimal des boucles pour le calcul du produit matrice-matrice, dans ce cas, est j, k, i. Bien que la complexité algorithmique demeure inchangée, cet ordre optimise significativement l'accès à la mémoire. La taille des données d'entrée, qui peut limiter la performance, influe sur la complexité d'accès à la mémoire. Avec l'utilisation de plusieurs cœurs de processeur, la quantité de cache disponible varie, affectant ainsi le temps d'exécution du programme.

- Un aspect crucial de cette optimisation est la manière dont la matrice est stockée en mémoire. Puisque la matrice est stockée colonne par colonne, accéder aux éléments dans l'ordre j, k, i permet un accès séquentiel et contigu en mémoire. Cela signifie que les données sont lues de manière continue, ce qui est nettement plus rapide par rapport à un accès non séquentiel. L'accès continu en mémoire améliore l'utilisation de la ligne de cache, permettant aux données d'être plus proches du processeur et réduisant ainsi la dépendance envers la mémoire RAM, qui est plus lente. Ce rapprochement des données du processeur réduit le temps d'accès et, par conséquent, accélère l'exécution globale du programme.

### OMP sur la meilleure boucle

`make TestProduct.exe && OMP_NUM_THREADS=8 ./TestProduct.exe 1024`

  OMP_NUM         | MFlops  | MFlops(n=2048) | MFlops(n=512)  | MFlops(n=4096)
------------------|---------|----------------|----------------|---------------
1                 |  |
2                 |  |
3                 |  |
4                 |  |
5                 |  |
6                 |  |
7                 |  |
8                 |  |

### Produit par blocs

`make TestProduct.exe && ./TestProduct.exe 1024`

  szBlock         | MFlops  | MFlops(n=2048) | MFlops(n=512)  | MFlops(n=4096)
------------------|---------|----------------|----------------|---------------
origine (=max)    |  |
32                |  |
64                |  |
128               |  |
256               |  |
512               |  |
1024              |  |

### Bloc + OMP

  szBlock      | OMP_NUM | MFlops  | MFlops(n=2048) | MFlops(n=512)  | MFlops(n=4096)|
---------------|---------|---------|-------------------------------------------------|
A.nbCols       |  1      |         |                |                |               |
512            |  8      |         |                |                |               |
---------------|---------|---------|-------------------------------------------------|
Speed-up       |         |         |                |                |               |
---------------|---------|---------|-------------------------------------------------|

### Comparaison with BLAS

# Tips

```
 env 
 OMP_NUM_THREADS=4 ./produitMatriceMatrice.exe
```

```
    for i in $(seq 1 4); do elap=$(OMP_NUM_THREADS=$i ./TestProductOmp.exe|grep "Temps CPU"|cut -d " " -f 7); echo -e "$i\t$elap"; done > timers.out
```
