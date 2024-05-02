import random
import simpy
import flet as ft

global prob_retrabajo

def main(page: ft.Page):
    
    page.scroll="always"
    t = ft.Text()
    t.value=""

    def obtener_datos(e):
        global prob_retrabajo
        tiempo_compra= (int(tb1.value))
        intervalo=(int(tb2.value))
        tiempo_simulacion=(float(tb3.value))
        cola=(float(tb4.value))
        num_clientes=(int(tb5.value))
        prob_retrabajo=(float(tb4.value))
        iniciar(tiempo_compra, intervalo, cola, num_clientes,tiempo_simulacion)
  
   
    tb1 = ft.TextField(label="Tiempo Promedio de compra (minutos)")
    tb2 = ft.TextField(label="intervalo promedio de llegada de clientes (en minutos)")
    tb3 = ft.TextField(label="tiempo total de simulación")
    tb4 = ft.TextField(label="Ingrese la probabilidad de retrabajo (entre 0 y 1)")
    tb5 = ft.TextField(label="número de clientes")
   
    b = ft.ElevatedButton(text="Iniciar", on_click=obtener_datos)
    page.add(tb1, tb2, tb3, tb4, tb5, b, t)

    def cliente(env, nombre, supermercado, cola):
        t.value += (f'{nombre} llega al supermercado en el minuto {env.now:.2f}. \n')
        t.update()

        with supermercado.request() as solicitud:
            yield solicitud
            while True:
                t.value += (f'{nombre} entra al supermercado en el minuto {env.now:.2f}.\n')
                t.update()

                tiempo_compra = random.randint(5, 15)
                yield env.timeout(tiempo_compra)
                if random.random() > prob_retrabajo:
                    break
                t.value += (f'{nombre} necesita retrabajo y vuelve a la cola en el minuto {env.now:.2f}. \n')
                t.update()

            cola[0] -= 1
            t.value += (f'{nombre} sale del supermercado en el minuto {env.now:.2f}. Hay {cola[0]} clientes en la cola. \n')
            t.update()
        page.update()

    def setup(env, tiempo_compra, intervalo, cola, num_clientes):
          supermercado = simpy.Resource(env, capacity=1)
          for i in range(num_clientes):
              yield env.timeout(random.randint(intervalo - 2, intervalo + 2))
              cola[0] += 1
              env.process(cliente(env, f'Cliente {i+1}', supermercado, cola))

    def iniciar(tiempo_compra, intervalo, cola, num_clientes,tiempo_simulacion):
          env = simpy.Environment()
          cola = [0]  
          env.process(setup(env, tiempo_compra, intervalo, cola, num_clientes))
          env.run(until=tiempo_simulacion)

ft.app(target=main)

