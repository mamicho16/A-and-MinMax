from pyamaze import maze, agent, COLOR
import time

#Obtener distancia entre dos puntos
def h(c1,c2):
    x1,y1 = c1
    x2,y2 = c2
    return abs(x1-x2) + abs(y1-y2)

def aStar(m, x, y):
    start = (x, y)
    list = [(h(start, m._goal), start)]
    reversePath = {}
    g = {cell: float('inf') for cell in m.grid}
    g[start] = 0
    f = {cell: float('inf') for cell in m.grid}
    f[start] = h(start, m._goal)
    searchPath = [start]

    while list:
        list.sort(key=lambda x: x[0]) #Ordenar lista en funcion del primer elemento de la tupla
        cActual = list.pop(0)[1] #Extraer la posicion del nodo con menor f
        searchPath.append(cActual)

        if cActual == m._goal:
            break

        for d in 'ESNW':
            if m.maze_map[cActual][d]:
                if d == 'E':
                    childCell = (cActual[0], cActual[1] + 1)
                elif d == 'W':
                    childCell = (cActual[0], cActual[1] - 1)
                elif d == 'N':
                    childCell = (cActual[0] - 1, cActual[1])
                elif d == 'S':
                    childCell = (cActual[0] + 1, cActual[1])
                temp_g = g[cActual] + 1
                temp_f = temp_g + h(childCell, m._goal)

                if temp_f < f[childCell]:
                    reversePath[childCell] = cActual
                    g[childCell] = temp_g
                    f[childCell] = temp_f
                    list.append((temp_f, childCell))
                print("Actual: ", cActual, "Vecino: ", childCell, "f_temp: ", temp_f, "f[vecino]: ", f[childCell], "g_temp: ", temp_g, "g[vecino]:", g[childCell])
    opPath = {}
    cell = m._goal
    while cell != start:
        opPath[reversePath[cell]] = cell
        cell = reversePath[cell]
    return searchPath, reversePath, opPath
    
    
tiempo_inicial = time.time()

# Crear un laberinto
m = maze(10,10)
m.CreateMaze(4,9,loopPercent = 60, theme = COLOR.blue)
x=10
y=2
searchPath, reversePath, opPath=aStar(m, x, y)

a=agent(m, x, y, footprints=True, color=COLOR.blue, shape='square')
c=agent(m, x, y, footprints=True,color=COLOR.red, shape='arrow', filled = True)

m.tracePath({a:searchPath})
m.tracePath({c:opPath})
print(m.maze_map)
print(len(searchPath))
print(len(opPath))
tiempo_final = time.time()
tiempo_ejecucion = tiempo_final - tiempo_inicial
print('El tiempo de ejecucion fue:',tiempo_ejecucion) #En segundos
m.run()


