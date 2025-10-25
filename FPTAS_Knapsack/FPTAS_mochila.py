import math
import json

'''
supposing taht the data is given at the format of [[peso,valor],...,[peso,valor]]
'''

# 269 879 100000 2_10000_1000_1 3_10000_1000_1

ruta = r"C:\Users\usuario_local\Downloads\269.json"

epsilon = 0.6

data = [[1, 2], [10, 10]]
data1 = [[1, 2], [2, 3], [3, 4], [4, 5]]

def encontrar_w(data):
    '''
    funcion auxiliar para calcular W
    Args:
          data(list): lista de [[peso,valor],...,[peso,valor]]
    Returns:
          maxi(float/int): valor maximo, cual es W
    '''
    maxi = 0
    for line in data:
        if maxi < line[1]:
            maxi = line[1]
    return maxi

def pd_main_capacidad(data, capacidad, epsilon, debug = False):
    '''
    la programcion dinamica principal segun la capacidad de la mochila
    Args: 
          data(list): lista de [[peso,valor],...,[peso,valor]]
          capacidad(float/int): capacidad de la mochila
          epsilon(float): el parametro epsilon
    Returns:
          dp(list): la lista de dp
    '''
    w = encontrar_w(data) #el valor maximo
    n = len(data)
    k = epsilon * w / n
    dp = [[0 for _ in range(capacidad+1)] for _ in range(n+1)]
    for i in range(1, n+1, 1):
        if (debug): print("into a new circle with i = " + str(i))
        for j in range(1, capacidad+1, 1):
            if data[i-1][0] > j:
                dp[i][j] = dp[i-1][j]
            else:
                dp[i][j] = max(dp[i-1][j], data[i-1][1]//k+dp[i-1][j-data[i-1][0]])
        if (debug): print("v es " + str(data[i-1][1]) + " y v' es " + str(data[i-1][1]//k))
    if (debug): print("out of loop of main PD")
    return dp

def pd_locate(dp, data, capacidad, debug = False):
    '''
    la funcion para localizar los elementos a coger
    Args:
          dp(list): la lista de dp
          data(list): lista de [[peso,valor],...,[peso,valor]]
          capacidad(float/int): capacidad de la mochila
    Returns:
          locations(list): lista que indica cuales son los cogidos
    '''
    locations = []
    w = capacidad
    for i in range(len(data), 0, -1):
        if dp[i][w] == dp[i-1][w]:
            if (debug): print(str(i) + "-esimo elemento no ha sido cogido")
            pass
        else: #dp[i][w] == dp[i-1][w - data[i-1][0]] + data[i-1][1]:
            if (debug): print(str(i) + "-th element has been taken with a value of " + str(data[i-1][0]))
            locations.append(i)
            w -= data[i-1][0]
        if w == 0:
            if (debug): print("all check out of loop")
            break
        if (debug): print("has ran a circle")
    return locations

def suma_data(data, k = 1):
    '''
    encontrar la suma V_sum
    Args:
          data(list): lista de [[peso,valor],...,[peso,valor]]
          k(float): la modificardor K
    Returns:
          v_sum(int/float): la suma total
    '''
    v_sum = 0
    for elem in range(len(data)):
        v_sum += int(data[elem][1]/k)
    return v_sum

def pd_main_peso(data, capacidad, epsilon, debug = False):
    '''
    la programcion dinamica principal peso minimo necesario para alcanzar un cierto valor
    Args: 
          data(list): lista de [[peso,valor],...,[peso,valor]]
          capacidad(float/int): capacidad de la mochila
          epsilon(float): el parametro epsilon
    Returns:
          dp(list): la lista de dp
    '''
    w = encontrar_w(data) #el valor maximo
    n = len(data)
    k = epsilon * w / n
    v_sum = suma_data(data, k)
    dp = [[[w * w * n * n, ""] for _ in range(v_sum + 1)] for _ in range(n + 1)]
    dp[0][0][0] = 0
    for i in range(1, n+1):
        if (debug): print("into a new circle with i = " + str(i))
        for j in range(v_sum+1):
            if j >= data[i-1][1]//k:
                if(debug): print("v = " + str(j) + " is larger or equal than v_i = " + str(data[i-1][1]//k))
                if(debug): print("dp[i-1][v] = " + str(dp[i-1][j][0]) + " and dp[i-1][v-vi]+wi = "+ str(dp[i-1][j - int(data[i-1][1]//k)][0] + data[i-1][0]))
                if dp[i-1][j][0] < dp[i-1][j - int(data[i-1][1]//k)][0] + data[i-1][0]:
                    dp[i][j][0] = dp[i-1][j][0]
                    dp[i][j][1] = dp[i-1][j][1]
                    if (debug): print("Not taking " + str(i) + "-th element" + "with current set = ("+ str(dp[i][j][0]) +", " + dp[i][j][1] + ")")
                else:
                    dp[i][j][0] = dp[i-1][j - int(data[i-1][1]//k)][0] + data[i-1][0]
                    #dp[i][j][1] = dp[i-1][j][1] + str(i) + " "
                    dp[i][j][1] = dp[i-1][j - int(data[i-1][1]//k)][1] + str(i-1) + " "
                    if (debug): print("Taken " + str(i-1) + "-th element" + "with current set = (" + str(dp[i][j][0]) +", " + dp[i][j][1] + ")")
            else:
                    dp[i][j][0] = dp[i-1][j][0]
                    dp[i][j][1] = dp[i-1][j][1]
    if (debug): print("out of loop of main PD")

    dp_opt = ""
    v_max = 0
    for v in range(v_sum + 1):
        if dp[n][v][0] <= capacidad:
            v_max = v
    dp_opt = dp[n][v_max][1]

    v_max = 0
    for i in [int(j) for j in dp_opt.split()]:
        v_max += data[i][1]
    return dp_opt, v_max

def segun_capacidad(data, capacidad, epsilon):
    pd = pd_main_capacidad(data, capacidad, epsilon)
    location = pd_locate(pd, data, capacidad)
    result = 0
    for i in location:
        result += data[i-1][1]
    return result

'''
if __name__ == "__main__":
    capacidad_test = 10
    epsilon_test = 0.5
    result = segun_capacidad(data, capacidad_test, epsilon_test)
    print(result)
'''

def read_file(path, debug = False):
    with open(path, "r") as fil:
        fi = json.load(fil)
        capacidad = fi["capacity"]
        data = []
        peso = fi["item_weights"]
        valor = fi["item_values"]
        for i in range(int(fi["item_count"])):
            data.append([peso[i], valor[i]])
    if (debug): print("reading done succesfully")
    return data, capacidad

if __name__ == "__main__":
    data, capacidad = read_file(ruta)
    #result = FPTAS_mochila.segun_capacidad(data, capacidad, epsilon)
    result = pd_main_peso(data, capacidad, epsilon)
    print(result)
