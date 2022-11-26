entero a = 10;
entero b = 20;
booleano c = verdadero;
caracter d = 'a';
entero i = 0;

funcion vacio imprimir_n (entero n, cadena s) {
    mientras (i < n) {
        imprimir (s);
        i = i + 1;
    };
};

funcion vacio principal () {
    leer a;
    imprimir_n (a, "¡Hola, Mundo!");
    si (a < b) {
        imprimir ("a es menor que b");
    } sino {
        imprimir ("a es menor o igual que b");
    };
    retornar ((40 + a) - b) * 2;
};