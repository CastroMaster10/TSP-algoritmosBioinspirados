*Problema de TSP

option optcr=0.0001

set
i/0*39/;
*como el i y el j son lo mismo, declaramos un alias
Alias
(i,j);

table c(i,j)
$onDelim
$include matrizDistancias/40 nodos/matrizDistancia0.csv
$offDelim
;



variable
z;

positive Variable
u(i);

binary variable
x(i,j);

Equations
obj
r1
r2
r3;

obj.. z=E=sum((i,j),x(i,j) * c(i,j));
r1(i).. sum(j,x(i,j)) =E= 1;
r2(j).. sum(i,x(i,j)) =E= 1;
r3(i,j) $(ord(i) > 1 and ord(j)> 1 and ord(i) <> ord(j)).. u(i) - u(j) + card(i) * x(i,j) =L= card(i) - 1;

model transporte /all/;
solve transporte using MIP min z;

*Te funciona para problemas enteros 