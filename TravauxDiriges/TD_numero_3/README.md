# TD n°3 - parallélisation du Bucket Sort

*Ce TD peut être réalisé au choix, en C++ ou en Python*

Implémenter l'algorithme "bucket sort" tel que décrit sur les deux dernières planches du cours n°3 :

- le process 0 génère un tableau de nombres arbitraires,
- il les dispatch aux autres process,
- tous les process participent au tri en parallèle,
- le tableau trié est rassemblé sur le process 0.

## Temps original

Le temps d'algorithme original: 0.1278 secondes.


## Speed Up

  Nbp           | time   |  Speed up
------------------|---------|-------|
2   | 0.0173| 7.387 |
3   | 0.0116| 11.01 |
4   | 0.0126 | 10.142 |
5   | 0.0105 |  12.171 |

## Commentaires

Pour implémenter la parallélisation au sein du Bucket Sort, il faut penser d'une façon assez peu commune. Chaque processus dans l'environnement parallèle travaille sur un sous-ensemble des données, distribuant les éléments dans des seaux (ou "buckets") locaux. Ensuite, chaque seau est trié indépendamment dans chaque processus. Cette approche tire parti de la puissance de calcul parallèle en réduisant le temps nécessaire pour trier de grandes quantités de données.

L'efficacité de la parallélisation est évidente dans le tableau "Speed Up" ci-dessus, où l'on observe que le temps de traitement diminue significativement à mesure que le nombre de processus (`Nbp`) augmente. Cela démontre l'avantage de diviser la tâche de tri entre plusieurs unités de calcul. Le "Speed Up" est calculé en divisant le temps d'exécution de l'algorithme original par le temps d'exécution parallélisé, montrant combien de fois l'approche parallèle est plus rapide que l'exécution séquentielle.

Il est important de noter que l'efficacité de la parallélisation dépend fortement de la manière dont les données sont distribuées entre les processus et de l'efficacité du tri au sein de chaque seau. Une distribution inégale des données peut entraîner un déséquilibre de charge de travail entre les processus, ce qui peut réduire les bénéfices de la parallélisation. De plus, le choix de l'algorithme de tri utilisé pour trier les éléments au sein de chaque seau peut également avoir un impact significatif sur les performances globales.

En conclusion, la parallélisation du Bucket Sort offre une méthode efficace pour accélérer le traitement de grandes ensembles de données. En tirant parti de la puissance de calcul parallèle, il est possible de réaliser des améliorations significatives du temps d'exécution. Toutefois, pour maximiser les performances, il est crucial de veiller à une distribution équilibrée des données et à une sélection judicieuse de l'algorithme de tri interne.
