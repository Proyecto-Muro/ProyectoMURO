#ok so this somehow works.

def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(str(i), str(j))
    return(text)


Prob1=r"""Un conjunto de cinco enteros positivos distintos se llama <i>virtual</i> si el máximo común divisor de cualesquiera tres de sus elementos es mayor que $1$, pero el máximo común divisor de cuatro de ellos es igual a $1$. Demostrar que, en cualquier conjunto virtual, el producto de sus elementos tiene al menos $2020$ divisores positivos distintos."""
Prob2=r"""Sea $ABC$ un triángulo con incentro $I$. La recta $BI$ se encuentra con $AC$ en $D$. Sea $P$ un punto en $CI$ tal que $DI=DP$ y $P\ne I$, $E$ el segundo punto de intersección del segmento $BC$ con el circuncírculo de $ABD$ y $Q$ el segundo punto de intersección de la recta $EP$ con el circuncírculo de $AEC$. Demuestra que $\angle PDQ=90^\circ$."""
Prob3=r"""Sea $n\ge 3$ un número entero. Dos jugadores, Ana y Beto, juegan al siguiente juego. Ana etiqueta los vértices de un $n$-ágono regular con los números del $1$ al $n$, en el orden que quiera. Cada vértice debe ser etiquetado con un número diferente. A continuación, colocamos un guajolote en cada uno de los $n$ vértices. 
Estos guajolotes se entrenan para lo siguiente. Si Beto silba, cada guajolote se mueve al vértice adyacente con mayor etiqueta. Si Beto aplaude, cada guajolote se mueve al vértice adyacente con la etiqueta menor. 
Beto gana si, tras un cierto número de silbidos y palmadas, consigue mover todos los guajolotes al mismo vértice. Ana gana si consigue etiquetar los vértices para que Beto no pueda hacerlo. Para cada $n\ge 3$, determina qué jugador tiene una estrategia ganadora."""
Prob4=r"""Sea $n\ge 3$ un número entero. En un juego hay $n$ cajas en un círculo. Al principio, cada caja contiene un objeto que puede ser piedra, papel o tijeras, de forma que no hay dos cajas adyacentes con el mismo objeto, y cada objeto aparece en al menos una caja. 

Al igual que en el juego, piedra gana a tijera, tijera gana a papel y papel gana a piedra. 

El juego consiste en mover objetos de una caja a otra según la siguiente regla: 

<i>Se eligen dos cajas adyacentes y un objeto de cada una de ellas de forma que sean diferentes, y movemos el objeto perdedor a la caja que contiene el objeto ganador. Por ejemplo, si elegimos una piedra de la caja A y unas tijeras de la caja B, movemos las tijeras a la caja A.</i>

Demuestra que, aplicando la regla suficientes veces, es posible mover todos los objetos a la misma caja."""
Prob5=r"""Un conjunto $\{a, b, c, d\}$ de cuatro enteros positivos se llama <i>bueno</i> si hay dos de ellos tales que su producto es múltiplo del mayor común divisor de los dos restantes. Por ejemplo, el conjunto $\{2, 4, 6, 8\}$ es bueno ya que el máximo común divisor de $2$ y $6$ es $2$, y divide $4\times 8=32$.

Encuentra el mayor valor posible de $n$, tal que cualquier conjunto de cuatro elementos con elementos menores o iguales a $n$ sea bueno."""
Prob6=r"""Sea $n\ge 2$ un número entero positivo. Sean $x_1, x_2, \dots, x_n$ números reales no nulos que satisfacen la ecuación
\[\left(x_1+\frac{1}{x_2}\right)\left(x_2+\frac{1}{x_3}\right)\dots\left(x_n+\frac{1}{x_1}\right)=\left(x_1^2+\frac{1}{x_2^2}\right)\left(x_2^2+\frac{1}{x_3^2}\right)\dots\left(x_n^2+\frac{1}{x_1^2}\right). \]
Encuentra todos los valores posibles de $x_1, x_2, \dots, x_n$."""

def htmlproblems(contestname, year, numproblems):
    #define the problems, set as empty if problem does not exist
    Problem=""
    ProblemPosition="1"
    dic = {
        "[Enunciado1]": Prob1,
        "[Enunciado2]": Prob2,
        "[Enunciado3]": Prob3,
        "[Enunciado4]": Prob4,
        "[Enunciado5]": Prob5,
        "[Enunciado6]": Prob6,
        "[Enunciadoproblema]": str(Problem),
        "[concurso]": str(contestname),
        "[año]": str(year),
        "[numproblema]": str(ProblemPosition)
        }
    ProblemsList=[Prob1,Prob2,Prob3,Prob4,Prob5,Prob6]
    #
    #copy file index.txt as a variable
    indexraw=open("yearindex.txt", "r").read()
    #replace variables
    index=replace_all(indexraw, dic)
    #write onto index.html
    with open(str(contestname)+"/"+str(year)+"/"+"index.html", "w") as f:
       f.write(index)
    
    
    for i in range(6):
        #create file pi.html, replace
        problempageraw=open("problempage.txt", "r").read()
        #replace variables
        #define Problem and ProblemPosition in dic
        dic["[Enunciadoproblema]"]=str(ProblemsList[i])
        dic["[numproblema]"]=str(i+1)
        problempage=replace_all(problempageraw, dic)
        with open(str(contestname)+"/"+str(year)+"/"+"p"+str(i+1)+".html", "w") as f:
            f.write(problempage)
        #create file soli.html
        solutionpageraw=open("solutionpage.txt", "r").read()
        solutionpage=replace_all(solutionpageraw, dic)
        with open(str(contestname)+"/"+str(year)+"/"+"sol"+str(i+1)+".html", "w") as g:
            g.write(solutionpage)
        
        
            













