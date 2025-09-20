
#  Analizador Sintáctico y Generador de Árbol de Sintaxis Abstracta (AST)

Este proyecto implementa un **analizador léxico y sintáctico** en Python que, a partir de una **gramática definida en un archivo de texto**, permite:

1. **Leer y tokenizar** una expresión de entrada.
2. **Verificar** si la expresión es válida según la gramática.
3. **Construir** el Árbol de Sintaxis Abstracta (AST).
4. **Graficar** el AST utilizando `matplotlib` y `networkx`.

---

##  Herramientas utilizadas

- **Python 3**  → lenguaje de programación principal.
- **Expresiones Regulares (`re`)** → para la definición de tokens.
- **NetworkX** → para representar el árbol como un grafo.
- **Matplotlib** → para graficar el AST.
- **Graphviz (opcional)** → si está instalado, mejora la disposición del árbol.

---

## Archivos principales

- `analizador.py` → código del analizador léxico, sintáctico y graficador del AST.
- `gramatica.txt` → archivo de texto donde se define la gramática (tokens y reglas de producción).

Ejemplo de `gramatica.txt`:

```txt
%tokens
opsuma: +
opmul: *
pari: (
pard: )
%endtokens

E -> E opsuma T | T
T -> T opmul F | F
F -> pari E pard | num | id
```
## Cómo ejecutar el proyecto
1. Instalar dependencias
Asegúrate de tener Python 3 instalado. Luego instala las librerías necesarias:
```bash
 pip install matplotlib networkx
```
2. Ejecutar el analizador
```bash
python3 analizador.py gramatica.txt
```
El programa pedirá ingresar una expresión, por ejemplo:
```bash
Ingrese la cadena a evaluar: 2+3*2
```

## ¿Cómo funciona?

El sistema implementa un **mini compilador** en Python dividido en tres fases principales:  

---

### 1. Lectura de la gramática

- El programa comienza leyendo un archivo de texto (`gramatica.txt`) donde está definida la **gramática libre de contexto (GLC)**.  
- La gramática se divide en dos partes:
  - **Tokens** (`%tokens … %endtokens`): indican los símbolos terminales como `+`, `*`, `(`, `)`, `num`, `id`.  
  - **Producciones**: describen cómo se pueden construir expresiones a partir de los símbolos no terminales (`E`, `T`, `F`).  

Ejemplo:

E -> E opsuma T | T
T -> T opmul F | F
F -> pari E pard | num | id



Esto define que:
- Una **expresión (E)** puede ser otra expresión sumada a un término, o solo un término.  
- Un **término (T)** puede ser otro término multiplicado por un factor, o solo un factor.  
- Un **factor (F)** puede ser un número, un identificador o una subexpresión entre paréntesis.  

---

### 2.  Análisis léxico (Tokenización)

El **analizador léxico** convierte la cadena ingresada por el usuario (ejemplo: `2+3*2`) en una secuencia de **tokens**:  

[num(2), opsuma(+), num(3), opmul(*), num(2)]


- Esto se logra con **expresiones regulares (`re` en Python)** que identifican números, identificadores y símbolos.  
- Si aparece un carácter no reconocido por la gramática, el analizador léxico genera un error.  

**Herramienta computacional**:  
- **Autómata finito** → se encuentra en la clase `AnalizadorLexico`.  
  - El método `siguiente_token()` recorre la cadena carácter por carácter, **cambiando de estado implícitamente según los patrones regulares**.  
  - Por ejemplo, al leer un número, el autómata avanza hasta que encuentra un carácter no numérico.  
  - Es un autómata porque clasifica secuencias de caracteres en categorías válidas (tokens) o las rechaza.  

---

### 3.  Análisis sintáctico (Parsing)

El **analizador sintáctico** toma los tokens y trata de encajarlos en las reglas de la gramática:  

- Usa un método de **descenso recursivo**, es decir, funciones que se llaman entre sí para procesar la expresión según las producciones de la gramática.  
- Si la cadena cumple con todas las reglas, se acepta.  
- Si en algún punto no coincide con la gramática, se lanza un error de sintaxis.  

Ejemplo válido: `2+3*2`  
Ejemplo inválido: `2-2` (porque `-` no está definido en la gramática).

  **Herramienta computacional**:  
- **Gramática libre de contexto (GLC)** → implementada en la clase `AnalizadorSintactico`.  
  - El método `parsear_E()` implementa la regla `E -> E opsuma T | T`.  
  - El método `parsear_T()` implementa `T -> T opmul F | F`.  
  - El método `parsear_F()` implementa `F -> (E) | num | id`.  
  - Es una GLC porque la validez de una cadena depende de su estructura jerárquica, no de un contexto externo.  

---

### 4.  Construcción del Árbol de Sintaxis Abstracta (AST)

- Una vez validada la cadena, el sistema construye el **Árbol de Sintaxis Abstracta (AST)**.  
- El AST es una representación jerárquica donde cada nodo representa un operador o un operando.  
- A diferencia del árbol de derivación, el AST **omite detalles innecesarios** de la gramática (como paréntesis o reglas intermedias).  

Ejemplo para `2+3*2`:
<img width="1008" height="603" alt="image" src="https://github.com/user-attachments/assets/ea49343f-dab9-41e2-8aad-f965f40f7281" />


 **Herramienta computacional**:  
- **Árbol de sintaxis abstracta (AST)** → implementado en la clase `NodoAST`.  
  - Cada nodo (`NodoAST`) almacena un operador o un valor numérico/identificador.  
  - Sus hijos representan los operandos.  
  - Se construye en el analizador sintáctico al ir combinando subexpresiones válidas.  

---

### 5.  Graficación del AST

- El AST se convierte en un **grafo dirigido** utilizando la librería **NetworkX**.  
- Cada nodo del AST se representa como un vértice en el grafo y las relaciones padre-hijo como aristas.  
- Con **Matplotlib**, se renderiza el grafo en pantalla para mostrar el árbol visualmente.  
- Si está instalado **Graphviz**, se utiliza para generar una distribución más ordenada de los nodos.  

 **Herramientas computacionales**:
- **Teoría de grafos** → se encuentra en la función `ast_a_grafo()`.  
  - El AST se traduce a un grafo en `networkx`, donde cada nodo tiene una etiqueta y se conecta con sus hijos.  
- **Visualización científica** → en la función `graficar_ast()`.  
  - Se usa `matplotlib` para dibujar el grafo en pantalla.  
  - Si `graphviz` está disponible, mejora la disposición jerárquica con `graphviz_layout`.  

---

### 6.  Flujo completo de ejecución

1. Cargar gramática desde `gramatica.txt`.  
2. Tokenizar la cadena ingresada (autómata finito en `AnalizadorLexico`).  
3. Analizar sintácticamente los tokens (GLC en `AnalizadorSintactico`).  
4. Construir el AST (`NodoAST`).  
5. Convertirlo en grafo (`ast_a_grafo`).  
6. Mostrar el AST graficado (`graficar_ast`).  

Si en cualquier paso ocurre un error (token no reconocido, error sintáctico, etc.), se informa al usuario y no se genera el AST.  

---




