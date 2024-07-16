from flask import Flask, request, render_template

app = Flask(__name__)

class SistemaExperto:
    def __init__(self):
        # Base de conocimientos: reglas
        self.reglas = {
            'fiebre': 'tomar_acetaminifen',
            'tos': 'tomar_jarabe',
            'dolor_de_cabeza': 'tomar_analgesico',
            'dolor_de_estomago': 'tomar_Gaviscon',
            'fatiga': 'descansar'
        }

        # Base de conocimientos: hechos iniciales
        self.hechos = {
            'fiebre': False,
            'tos': False,
            'dolor_de_cabeza': False,
            'dolor_de_estomago': False,
            'fatiga': False
        }

    def agregar_hecho(self, hecho, valor):
        self.hechos[hecho] = valor

    def inferir(self):
        conclusiones = []
        hechos_a_procesar = list(self.hechos.items())
        while hechos_a_procesar:
            hecho, valor = hechos_a_procesar.pop(0)
            if valor:
                accion = self.aplicar_regla(hecho)
                if accion:
                    conclusiones.append((hecho, accion))
        return conclusiones

    def aplicar_regla(self, hecho):
        if hecho in self.reglas:
            accion = self.reglas[hecho]
            self.hechos[accion] = True
            return accion
        return None

# Instanciar el sistema experto
sistema_experto = SistemaExperto()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        sintomas = request.form.getlist('sintomas')
        for sintoma in sintomas:
            sistema_experto.agregar_hecho(sintoma, True)
        conclusiones = sistema_experto.inferir()
        return render_template('index.html', conclusiones=conclusiones, sintomas=sintomas)
    return render_template('index.html', conclusiones=[], sintomas=[])

if __name__ == '__main__':
    app.run(debug=True)

    