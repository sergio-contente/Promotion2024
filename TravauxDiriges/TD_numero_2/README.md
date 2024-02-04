# TD2

## 1.1.1
Un scénario sans interblocage serait un scénario dans lequel les processus ou les threads n'auraient pas à attendre indéfiniment les ressources détenues par d'autres processus. Par exemple: l'algorithme du banquier.
## 1.1.2
C'est l'inverse, quand un processus attend à finalisation de l'autre à cause d'utiliser les ressources partagés entre les deux. Un example classique est le dîner des philosophes. En programmation parallèle, on peut imaginer un scénario où un processus attend le donnés qui vient d'un autre qui attend pour lequel du premier aussi.
## 1.1.3
Au sein de la programmation parallèle, on peut suposer qu'il soit un scénario trés commun, puisque souvent les ressources sont le même pour les differents processus. En géneral, dans des environnements hautement compétitifs comportant de nombreux processus et des ressources limitées, la probabilité de blocages peut être importante.

## 1.2.a
En utilisant la Loi d'Amdhal pour le cas d'Alice et en tennant compte infinis processeurs:
$$
p = 0.9
\quad
n \gg 1
\\
S_{\infin} = \frac{1}{1-p} = \frac{1}{0.1} = 10
$$
Donc, l'acceélération théorique maximale d'Alice sera 10.
## 1.2.b
En utilisant l'équation de la loi d'Amdhal, à mon avis il faut utiliser les nombre de noeud que rendent l'acceleration atteindre de 50% jusqu'à 75% de son maximal théorique puisque après le nombre optimal de noeuds est celui pour lequel l'augmentation incrémentielle de l'accélération commence à diminuer de manière significative en raison de facteurs tels que la surcharge de communication et de synchronisation entre les noeuds.

Du coup, en prennant 60% du maximal:
$$
 6 = \frac{1}{1-0.9 + \frac{0.9}{n}} \\
 n = 13.5
$$
Donc, il faut utiliser **14** noeuds.
## 1.2.c
Voici la Lois de Gustafson:
$$
S = n + (1 - n)f \quad f = 1 - p
$$

L'énoncé du problème nous dit que Alice a obtenu una accélération maximale de 4. Alors, on peut calculer le nombre de noeuds qu'elle prend:

$$4 = n + (1-n)0.1 \\
n = 4.33 \approx 5$$

Finalement, on suppose que, en doublant le nombre de donnés, la partie qui sera parallèlisé sera presque 100%. Donc, l'accélération maximale avec la même quantité de noeuds sera:

$$S' = 4 + (1-4)*0.01 \\
S' = 4.96 \approx 5
$$

Accélération finale: **5**.

## 1.3.1

Temps du calcul de l'ensemble de Mandelbrot sans parallèlisation : 2.46 secondes

Temps du calcul de l'ensemble de Mandelbrot avec parallèlisation : 0.65 secondes

Speedup:
$$
S = \frac{ts}{tp} = \frac{2.46}{0.65} = 3.78
$$

En utilisant 4 processus différents, on peut obtenir 3.78 d'accélération. Les deux nombres sont proches, c'est-à-dire que la parallèlisation a été efficient et san surcharge de communication entre taches.

## 1.3.2

## 1.4.1

Temps pour calculer le produit (sans parallèlisation): 4.5 e-05 secondes

Temps pour calculer le produit avec la parallèlisation par colonnes : 
2.8 e-05 secondes

Speedup:
$$
S = \frac{ts}{tp} = \frac{4.5}{2.8} = 1.6
$$

C'est-à-dire que l'on a obtenu una optimisation sublineaire et on peut supposer que cela soit à cause de que la charge de travail n'est pas parfaitement équilibrée entre les tâches.

## 1.4.2

Temps pour calculer le produit (sans parallèlisation): 4.5 e-05 secondes

Temps pour calculer le produit (lignes): 3.17e-05 secondes

Speedup:
$$
S = \frac{ts}{tp} = \frac{4.5}{3.17} = 1.2
$$

C'est-à-dire que l'on a obtenu una optimisation sublineaire et on peut supposer que cela soit à cause de que la charge de travail n'est pas parfaitement équilibrée entre les tâches.

**Du coup, l'optimisation par colonnes est meilleure que laquelle par lignes.**
