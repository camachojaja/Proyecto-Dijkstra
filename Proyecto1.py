"""
Proyecto: Algoritmo de Dijkstra
Encuentra la ruta más corta (distancia y secuencia de nodos) entre un
nodo origen y un nodo destino en un grafo ponderado.
"""


class Nodo:
    """Representa un nodo (vértice) del grafo y sus conexiones."""

    def __init__(self, nombre):
        self.nombre = nombre
        # Diccionario de vecinos: {nombre_del_vecino: peso_de_la_arista}
        self.vecinos = {}

    def agregar_vecino(self, vecino, peso):
        """Conecta este nodo con otro nodo mediante una arista con peso."""
        self.vecinos[vecino] = peso

    def __repr__(self):
        return f"Nodo({self.nombre}, vecinos={self.vecinos})"


class Grafo:
    """Grafo ponderado: guarda los nodos y ejecuta Dijkstra."""

    def __init__(self):
        # Diccionario de nodos: {nombre: objeto Nodo}
        self.nodos = {}

    def agregar_nodo(self, nombre):
        """Agrega un nodo al grafo si todavía no existe."""
        if nombre not in self.nodos:
            self.nodos[nombre] = Nodo(nombre)

    def agregar_arista(self, origen, destino, peso, dirigido=False):
        """
        Crea una conexión entre dos nodos con un peso (costo).
        Si dirigido=False, la conexión funciona en ambos sentidos.
        """
        if peso < 0:
            raise ValueError("Dijkstra no admite pesos negativos.")

        # Si los nodos no existen, se crean automáticamente
        self.agregar_nodo(origen)
        self.agregar_nodo(destino)

        self.nodos[origen].agregar_vecino(destino, peso)
        if not dirigido:
            self.nodos[destino].agregar_vecino(origen, peso)

    def dijkstra(self, inicio, destino):
        """
        Calcula la distancia mínima y la ruta completa de inicio a destino.
        Devuelve una tupla: (distancia_total, lista_de_nodos_del_camino)
        """
        # Validar que los nodos existan
        if inicio not in self.nodos or destino not in self.nodos:
            raise ValueError("El nodo de inicio o destino no existe en el grafo.")

        distancias = {}   # Mejor distancia conocida desde 'inicio' a cada nodo
        anteriores = {}   # Nodo previo en el mejor camino (para reconstruir la ruta)
        visitados = set() # Nodos cuya distancia ya es definitiva

        # Inicialización: todos a distancia infinita y sin predecesor
        for nombre in self.nodos:
            distancias[nombre] = float("inf")
            anteriores[nombre] = None

        # La distancia del inicio a sí mismo es 0
        distancias[inicio] = 0

        while len(visitados) < len(self.nodos):
            # Buscar el nodo más cercano (no visitado) con menor distancia
            nodo_actual = None
            menor_distancia = float("inf")

            for nombre in self.nodos:
                if nombre not in visitados:
                    if distancias[nombre] < menor_distancia:
                        menor_distancia = distancias[nombre]
                        nodo_actual = nombre

            # Si no hay más nodos alcanzables, terminamos
            if nodo_actual is None:
                break

            # Si llegamos al destino, terminamos
            if nodo_actual == destino:
                break

            # Marcar el nodo como visitado (su distancia ya es la mínima)
            visitados.add(nodo_actual)

            # Revisar vecinos
            nodo = self.nodos[nodo_actual]

            for vecino, peso in nodo.vecinos.items():
                # Distancia llegando al vecino pasando por nodo_actual
                nueva_distancia = (
                    distancias[nodo_actual] + peso
                )

                # Si es mejor que la conocida, actualizamos (relajación)
                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    anteriores[vecino] = nodo_actual

        # Si el destino nunca fue alcanzado, no existe ruta
        if distancias[destino] == float("inf"):
            return float("inf"), []

        # Construir el camino (de atrás hacia adelante)
        camino = []
        actual = destino

        while actual is not None:
            camino.append(actual)
            actual = anteriores[actual]

        # El camino quedó invertido, lo volteamos
        camino.reverse()
        return distancias[destino], camino


def main():
    """Programa principal: construye un grafo de ejemplo y consulta una ruta."""
    grafo = Grafo()

    # Ejemplo: red de transporte (pesos = minutos de viaje)
    grafo.agregar_arista("A", "B", 4)
    grafo.agregar_arista("A", "C", 2)
    grafo.agregar_arista("B", "C", 1)
    grafo.agregar_arista("B", "D", 5)
    grafo.agregar_arista("C", "D", 8)
    grafo.agregar_arista("C", "E", 10)
    grafo.agregar_arista("D", "E", 2)
    grafo.agregar_arista("D", "F", 6)
    grafo.agregar_arista("E", "F", 3)

    print("Nodos disponibles:", ", ".join(grafo.nodos))

    origen = input("Nodo origen: ").strip().upper()
    destino = input("Nodo destino: ").strip().upper()

    try:
        distancia, camino = grafo.dijkstra(origen, destino)
    except ValueError as error:
        print("Error:", error)
        return

    if not camino:
        print(f"No existe una ruta de {origen} a {destino}.")
    else:
        print("\n--- Resultado ---")
        print("Costo total:", distancia)
        print("Ruta:", " -> ".join(camino))


if __name__ == "__main__":
    main()