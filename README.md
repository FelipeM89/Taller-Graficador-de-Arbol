# Taller-Graficador-de-Arbol

Este repositorio contiene dos implementaciones diferentes de un **analizador sintáctico** que construye y grafica el **Árbol de Sintaxis Abstracta (AST)** a partir de una gramática definida en un archivo de texto.

---

##  Estructura del repositorio

- **`ArbolConLibreriaPropia/`**  
  Implementación del analizador que utiliza una **librería propia (`graficador.py`)** para mostrar el AST directamente en consola.  
  - El árbol se imprime con líneas (`└──`, `├──`, `│`) y sangrías.  
  - No depende de librerías externas para graficar.  

- **`ArbolConNetworkx/`**  
  Implementación del analizador que usa las librerías **NetworkX** y **Matplotlib** para graficar el AST como un **grafo visual**.  
  - Cada nodo se representa como un vértice y las relaciones padre-hijo como aristas.  
  - Opción de integrar `graphviz` para una disposición más ordenada.  


---

## Ejecución

Cada carpeta contiene su propio `README.md` con instrucciones detalladas de instalación y uso.  
