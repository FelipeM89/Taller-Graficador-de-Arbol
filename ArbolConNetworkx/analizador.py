#!/usr/bin/env python3
import re
import sys
import networkx as nx
import matplotlib.pyplot as plt

def leer_gramatica(ruta):
    reglas = {}
    mapa_tokens = {}
    with open(ruta, "r", encoding="utf-8") as f:
        lineas = [ln.strip() for ln in f if ln.strip() and not ln.strip().startswith("#")]

    i = 0
    if i < len(lineas) and lineas[i].lower().startswith("%tokens"):
        i += 1
        while i < len(lineas) and not lineas[i].lower().startswith("%endtokens"):
            linea = lineas[i]
            nombre, valores = linea.split(":", 1)
            nombre = nombre.strip()
            partes = valores.strip().split()
            lista = []
            for p in partes:
                if len(p) >= 2 and p[0] == "/" and p[-1] == "/":
                    lista.append({"tipo": "regex", "valor": re.compile(p[1:-1])})
                else:
                    lista.append({"tipo": "lit", "valor": p})
            mapa_tokens[nombre] = lista
            i += 1
        if i < len(lineas) and lineas[i].lower().startswith("%endtokens"):
            i += 1
    while i < len(lineas):
        linea = lineas[i]
        izquierda, derecha = linea.split("->", 1)
        no_terminal = izquierda.strip()
        producciones_raw = [p.strip() for p in derecha.split("|")]
        for p in producciones_raw:
            reglas.setdefault(no_terminal, []).append(p.split() if p else [])
        i += 1
    return reglas, mapa_tokens

class AnalizadorLexico:
    def __init__(self, cadena, mapa_tokens, terminales):
        self.cadena = cadena
        self.pos = 0
        self.mapa_tokens = mapa_tokens
        self.terminales = set(terminales)
        if "num" in self.terminales and "num" not in self.mapa_tokens:
            self.mapa_tokens["num"] = [{"tipo": "regex", "valor": re.compile(r"\d+")}]
        if "id" in self.terminales and "id" not in self.mapa_tokens:
            self.mapa_tokens["id"] = [{"tipo": "regex", "valor": re.compile(r"[A-Za-z_][A-Za-z0-9_]*")}]
        for t in list(self.terminales):
            if t not in self.mapa_tokens and len(t) == 1 and not t.isalnum():
                self.mapa_tokens[t] = [{"tipo": "lit", "valor": t}]
    def siguiente_token(self):
        s = self.cadena
        n = len(s)
        while self.pos < n and s[self.pos].isspace():
            self.pos += 1
        if self.pos >= n:
            return None
        mejor = None
        for nombre, reglas in self.mapa_tokens.items():
            if nombre not in self.terminales:
                continue
            for regla in reglas:
                if regla["tipo"] == "regex":
                    mo = regla["valor"].match(s, self.pos)
                    if mo:
                        lex = mo.group(0)
                        if mejor is None or len(lex) > mejor[2]:
                            mejor = (nombre, lex, len(lex))
        for nombre, reglas in self.mapa_tokens.items():
            if nombre not in self.terminales:
                continue
            for regla in reglas:
                if regla["tipo"] == "lit":
                    lit = regla["valor"]
                    if s.startswith(lit, self.pos):
                        if mejor is None or len(lit) > mejor[2]:
                            mejor = (nombre, lit, len(lit))
        if mejor:
            nombre, lex, L = mejor
            self.pos += L
            return {"tipo": nombre, "lexema": lex}
        ch = s[self.pos]
        if ch.isdigit() and "num" in self.terminales:
            m = re.match(r"\d+", s[self.pos:])
            lex = m.group(0)
            self.pos += len(lex)
            return {"tipo": "num", "lexema": lex}
        if (ch.isalpha() or ch == "_") and "id" in self.terminales:
            m = re.match(r"[A-Za-z_][A-Za-z0-9_]*", s[self.pos:])
            lex = m.group(0)
            self.pos += len(lex)
            return {"tipo": "id", "lexema": lex}
        raise ValueError(f"Carácter no reconocido en posición {self.pos}: '{s[self.pos]}'")
    def tokenizar(self):
        lista = []
        while True:
            t = self.siguiente_token()
            if t is None:
                break
            lista.append(t)
        return lista

class NodoAST:
    def __init__(self, etiqueta, hijos=None):
        self.etiqueta = etiqueta
        self.hijos = hijos or []

class AnalizadorSintactico:
    def __init__(self, tokens, gramatica):
        self.tokens = tokens
        self.pos = 0
        self.gramatica = gramatica
        self.tokens_suma, self.tokens_mul, self.tokens_pari, self.tokens_pard = set(), set(), set(), set()
        self.nombres_num, self.nombres_id = set(), set()
        self._detectar_tokens()
    def _detectar_tokens(self):
        no_terminales = set(self.gramatica.keys())
        if "E" in self.gramatica:
            for rhs in self.gramatica["E"]:
                if len(rhs) == 3 and rhs[0] == "E" and rhs[2] == "T":
                    self.tokens_suma.add(rhs[1])
        if "T" in self.gramatica:
            for rhs in self.gramatica["T"]:
                if len(rhs) == 3 and rhs[0] == "T" and rhs[2] == "F":
                    self.tokens_mul.add(rhs[1])
        if "F" in self.gramatica:
            for rhs in self.gramatica["F"]:
                if len(rhs) == 3 and rhs[0] in ("pari", "(") and rhs[2] in ("pard", ")"):
                    if rhs[0] not in no_terminales: self.tokens_pari.add(rhs[0])
                    if rhs[2] not in no_terminales: self.tokens_pard.add(rhs[2])
                for simbolo in rhs:
                    if simbolo == "num": self.nombres_num.add("num")
                    if simbolo == "id": self.nombres_id.add("id")
    def actual(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None
    def consumir(self, esperado):
        tok = self.actual()
        if tok and (esperado is None or tok["tipo"] in esperado):
            self.pos += 1
            return tok
        return None
    def parsear_E(self):
        nodo = self.parsear_T()
        while True:
            tok = self.actual()
            if tok and tok["tipo"] in self.tokens_suma:
                op = tok["lexema"]
                self.consumir({tok["tipo"]})
                derecho = self.parsear_T()
                nodo = NodoAST(op, [nodo, derecho])
            else:
                break
        return nodo
    def parsear_T(self):
        nodo = self.parsear_F()
        while True:
            tok = self.actual()
            if tok and tok["tipo"] in self.tokens_mul:
                op = tok["lexema"]
                self.consumir({tok["tipo"]})
                derecho = self.parsear_F()
                nodo = NodoAST(op, [nodo, derecho])
            else:
                break
        return nodo
    def parsear_F(self):
        tok = self.actual()
        if tok is None:
            raise ValueError("Fin inesperado en F")
        if tok["tipo"] in self.nombres_num or tok["tipo"] == "num":
            self.consumir({tok["tipo"]}); return NodoAST(tok["lexema"])
        if tok["tipo"] in self.nombres_id or tok["tipo"] == "id":
            self.consumir({tok["tipo"]}); return NodoAST(tok["lexema"])
        if tok["tipo"] in self.tokens_pari or tok["tipo"] == "(":
            self.consumir({tok["tipo"]})
            nodo = self.parsear_E()
            nxt = self.actual()
            if nxt and (nxt["tipo"] in self.tokens_pard or nxt["tipo"] == ")"):
                self.consumir({nxt["tipo"]})
                return nodo
            raise ValueError("Falta )")
        raise ValueError(f"Token inesperado en F: {tok}")

def ast_a_grafo(raiz_ast):
    G = nx.DiGraph()
    contador = {"c": 0}
    def agregar_nodo(a):
        contador["c"] += 1
        nid = f"n{contador['c']}"
        G.add_node(nid, etiqueta=str(a.etiqueta))
        for h in a.hijos:
            hid = agregar_nodo(h)
            G.add_edge(nid, hid)
        return nid
    agregar_nodo(raiz_ast)
    return G

def graficar_ast(G, titulo="AST"):
    etiquetas = nx.get_node_attributes(G, "etiqueta")
    try:
        pos = nx.nx_pydot.graphviz_layout(G, prog="dot")
    except Exception:
        pos = nx.spring_layout(G)
    plt.figure(figsize=(10,6))
    nx.draw(G, pos, with_labels=True, labels=etiquetas,
            node_size=2000, node_color="lightblue", font_size=10)
    plt.title(titulo)
    plt.show()

def main():
    if len(sys.argv) < 2:
        print("Uso: python analizador.py gramatica.txt")
        sys.exit(1)
    ruta = sys.argv[1]
    gramatica, mapa_tokens = leer_gramatica(ruta)
    no_terminales = set(gramatica.keys())
    terminales = {simbolo for producciones in gramatica.values() for rhs in producciones for simbolo in rhs if simbolo not in no_terminales}
    cadena = input("Ingrese la cadena a evaluar: ").strip()
    try:
        tokens = AnalizadorLexico(cadena, mapa_tokens, terminales).tokenizar()
        analizador = AnalizadorSintactico(tokens, gramatica)
        ast = analizador.parsear_E()
        if analizador.pos == len(tokens):
            G = ast_a_grafo(ast)
            graficar_ast(G, titulo=f"AST — {cadena}")
        else:
            print("Cadena NO aceptada ❌")
    except Exception as e:
        print("Cadena NO aceptada ❌:", e)

if __name__ == "__main__":
    main()
