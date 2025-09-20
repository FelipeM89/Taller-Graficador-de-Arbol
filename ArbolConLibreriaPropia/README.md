#  Analizador Sintáctico con Árbol AST en Consola

Este proyecto implementa un **analizador sintáctico** en Python que recibe:  

1. Un archivo de gramática (`gramatica.txt`).  
2. Una cadena de entrada a evaluar.  

El programa valida si la cadena pertenece a la gramática y, si es aceptada, **muestra el Árbol de Sintaxis Abstracta (AST)** de forma visual en consola usando una **librería propia de graficación**.

---

##  Requisitos

- **Python 3.7+**
- Sistema operativo Linux, macOS o Windows.  

---

##  Ejecución

1. Clona o descarga este repositorio.  
2. Guarda tu gramática en un archivo llamado `gramatica.txt` (ejemplo incluido en el repositorio).  
3. Ejecuta el programa desde la terminal:  

```bash
python analizador.py gramatica.txt

```

## ¿Cómo funciona? (Explicación profunda)

El sistema sigue el modelo clásico de un **mini compilador**, dividido en fases:

### 1. Lectura de la gramática
- Se carga desde `gramatica.txt`.  
- Contiene **tokens** (símbolos terminales) y **producciones** de la gramática libre de contexto (GLC).  

Ejemplo:

E -> E opsuma T | T
T -> T opmul F | F
F -> pari E pard | num | id


---

### 2.  Análisis léxico (Autómata finito)
- Convierte la cadena en una lista de **tokens** usando expresiones regulares.  
- Ejemplo: `2+3*2` → `[num(2), opsuma(+), num(3), opmul(*), num(2)]`.  
- **Herramienta computacional:** *Autómata finito*.  
  - Se encuentra en la clase `AnalizadorLexico`.  
  - Funciona porque clasifica secuencias de caracteres en categorías (tokens) o las rechaza.

---

### 3.  Análisis sintáctico (Gramática libre de contexto)
- Valida que la secuencia de tokens cumple la gramática.  
- Se implementa con **descenso recursivo**: cada no terminal (`E`, `T`, `F`) tiene su propia función.  
- **Herramienta computacional:** *Gramática libre de contexto (GLC)*.  
  - Se encuentra en la clase `AnalizadorSintactico`.  
  - Garantiza que la cadena se analiza según la jerarquía de reglas.

---

### 4.  Construcción del AST
- Una vez validada la cadena, se construye un **Árbol de Sintaxis Abstracta (AST)**.  
- Cada nodo representa un operador o un valor, omitiendo detalles de la gramática.  
- **Herramienta computacional:** *Árbol de sintaxis abstracta*.  
  - Implementado en la clase `NodoAST`.  
  - Permite representar la estructura jerárquica de la expresión.

---

### 5.  Graficación del AST en consola
- Se usa una **librería propia (`graficador.py`)** para mostrar el AST.  
- Funciona de forma recursiva, dibujando ramas con caracteres (`└──`, `├──`, `│`) y niveles con sangrías.  
- Ejemplo visual:  
---
<img width="202" height="100" alt="image" src="https://github.com/user-attachments/assets/478a7b46-9a75-4c6a-b8cf-de0c5ededd37" />

---

- **Herramienta computacional:** *Teoría de grafos* simplificada.  
  - Se encuentra en la clase `Graficador`.  
  - Cada nodo del AST se imprime con sus hijos, formando un árbol jerárquico sin necesidad de librerías externas.

---

## Flujo completo de ejecución

1. Leer gramática (`gramatica.txt`).  
2. Tokenizar cadena con un autómata finito (`AnalizadorLexico`).  
3. Analizar sintácticamente con GLC (`AnalizadorSintactico`).  
4. Construir AST (`NodoAST`).  
5. Mostrar AST en consola (`Graficador.imprimir_arbol`).  

## Pruebas
---
<img width="522" height="214" alt="image" src="https://github.com/user-attachments/assets/22ae09ff-5a6c-4dd7-a2fa-8d8b91b6a70d" />

---
<img width="522" height="214" alt="image" src="https://github.com/user-attachments/assets/b67d9182-d996-4f5f-b307-54541068a180" />

---
<img width="547" height="96" alt="image" src="https://github.com/user-attachments/assets/91388daf-f22a-4d6a-942a-4510e0a5c184" />

---
<img width="608" height="153" alt="image" src="https://github.com/user-attachments/assets/46365c06-2e08-4b2a-afcf-13b38961831e" />
