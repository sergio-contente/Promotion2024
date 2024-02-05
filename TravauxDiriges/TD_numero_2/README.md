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

Finalement, on suppose que, en doublant le nombre de donnés, la partie qui sera parallèlisé sera presque 100% et le temps sera le double aussi. Donc, l'accélération maximale avec la même quantité de noeuds sera:

$$S' = 5 + (1-5)0.1\times 2 \\
S' = 4.2
$$

Accélération finale: **4.2**.

## 1.3.1

### Par ligne
  
Temps du calcul de l'ensemble de Mandelbrot sans parallèlisation (1 tâche): 2.46 secondes

- SpeedUp: 1

Temps du calcul de l'ensemble de Mandelbrot avec parallèlisation de 2 tâches : 1.097 secondes

- SpeedUp: 2.24

Temps du calcul de l'ensemble de Mandelbrot avec parallèlisation de 4 tâches: 0.60 secondes

- SpeedUp: 4.1

Temps du calcul de l'ensemble de Mandelbrot avec parallèlisation de 8 tâches: 0.38 secondes

- SpeedUp: 6.47

En utilisant 8 processus différents, on peut obtenir 6.47 d'accélération. On espère que ce nombre augment avec plus processus.

## 1.3.2 

### Maître-Esclave

Temps du calcul de l'ensemble de Mandelbrot avec parallèlisation de 2 tâches : 2.75 secondes

- SpeedUp: 0.89

Temps du calcul de l'ensemble de Mandelbrot avec parallèlisation de 4 tâches: 0.916 secondes

- SpeedUp: 2.68

Temps du calcul de l'ensemble de Mandelbrot avec parallèlisation de 8 tâches: 0.49 secondes

- SpeedUp: 5.02
  
En utilisant 8 processus différents, on peut obtenir 5.02 d'accélération. L'algorithme de maître-esclave est moin efficace que laquel par ligne.

