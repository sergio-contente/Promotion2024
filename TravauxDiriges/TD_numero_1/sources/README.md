
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
i,j,k (origine)   | 8.38753 | 7256.033 | 284.706
j,i,k             | 8.6158 | 249.249 | 288.213
i,k,j             | 30.9459 | 69.3948 | 106.394
k,i,j             | 33.5355 | 64.0361 | 97.3361
j,k,i             | 0.522769 | 4107.9 | 4066.91
k,j,i             | 0.844189 | 2543.84 | 2449.21

*Discussion des résultats*

- L'ordre optimal des boucles pour le calcul du produit matrice-matrice, dans ce cas, est j, k, i (avec 1024 MFlops). Bien que la complexité algorithmique demeure inchangée, cet ordre optimise significativement l'accès à la mémoire. La taille des données d'entrée, qui peut limiter la performance, influe sur la complexité d'accès à la mémoire. Avec l'utilisation de plusieurs cœurs de processeur, la quantité de cache disponible varie, affectant ainsi le temps d'exécution du programme.

- Un aspect crucial de cette optimisation est la manière dont la matrice est stockée en mémoire. Puisque la matrice est stockée colonne par colonne, accéder aux éléments dans l'ordre j, k, i permet un accès séquentiel et contigu en mémoire. Cela signifie que les données sont lues de manière continue, ce qui est nettement plus rapide par rapport à un accès non séquentiel. L'accès continu en mémoire améliore l'utilisation de la ligne de cache, permettant aux données d'être plus proches du processeur et réduisant ainsi la dépendance envers la mémoire RAM, qui est plus lente. Ce rapprochement des données du processeur réduit le temps d'accès et, par conséquent, accélère l'exécution globale du programme.

### OMP sur la meilleure boucle

`make TestProduct.exe && OMP_NUM_THREADS=8 ./TestProduct.exe 1024`

  OMP_NUM         | MFlops  | MFlops(n=2048) | MFlops(n=512)  | MFlops(n=4096)
------------------|---------|----------------|----------------|---------------
1                 | 3527.48 | 3511.72 | 3620.33 | 3542.87
2                 | 6422.96 | 6931.43 | 4760.09 | 6925.14
3                 | 9177.06 | 10377.4 | 5728.34 | 10307.9
4                 | 11882.8 | 13091.4 | 6115.88 | 13739.9
5                 | 13665.8 | 16391.0 | 7098.22 | 15926.4
6                 | 15748.3 | 18085.6 | 10091.0 | 17073.1
7                 | 18219.7 | 20177.7 | 6090.04 | 19385.8
8                 | 15664.5 | 16224.9 | 9646.20 | 15925.7

__OBSERVATION__
- Chaque fois que j'ai essayé d'utiliser la directive "#pragma omp parallel for collapse (3)", j'ai reçu l'erreur: 
   - Erreur numérique : valeur attendue pour *MATRIX* -> *VALEUR ESPÉRÉE*  mais valeur trouvée : *VALEUR TROUVÉE*
 - Pour cette raison, j'ai utilisé la directive: "#pragma omp parallel for collapse (2)" qui parallelise seulement le 2 boucles plus intérieures.

### Produit par blocs

`make TestProduct.exe && ./TestProduct.exe 1024`

  szBlock         | MFlops  | MFlops(n=2048) | MFlops(n=512)  | MFlops(n=4096)
------------------|---------|----------------|----------------|---------------
origine (=max)    | 20496.80 | 15346.30 | 10249.5 | 10750.30
32                | 5337.27 | 5807.84 | 4027.19 | 6035.72
64                | 8923.07 | 14189.60 | 5848.28 | 14224.80
128               | 15290.90 | 11878.70 | 4894.64 | 12780.50
256               | 16136.20 | 20702.60 | 8027.80 | 17770.40
512               | 19300.80 | 20114.40 | 10181.40 | 20754.80
1024              | 20254.70 | 17763.00 | 10521.80 | 17385.60

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
