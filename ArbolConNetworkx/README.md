
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
