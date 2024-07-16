
# Sistema Experto de Salud

Este es un sistema experto sencillo para diagnosticar problemas comunes de salud utilizando una interfaz web construida con Flask.

## Estructura del Proyecto

```
proyecto_sistema_experto/
├── app.py
└── templates/
    └── index.html
```

## Requisitos

- Python 3.x
- Flask

## Instalación

1. Clona este repositorio o descarga los archivos.

2. Navega al directorio del proyecto:

    ```sh
    cd proyecto_sistema_experto
    ```

3. Instala Flask si no lo tienes instalado:

    ```sh
    pip install flask
    ```

## Ejecución

1. Ejecuta la aplicación Flask:

    ```sh
    python app.py
    ```

2. Abre un navegador web y ve a `http://127.0.0.1:5000/` para interactuar con el sistema experto.

## Uso

1. Marca los síntomas que tienes de la lista proporcionada.
2. Haz clic en el botón "Diagnosticar".
3. Verás las conclusiones inferidas por el sistema experto basadas en los síntomas seleccionados.

## Código

### app.py

```python
from flask import Flask, request, render_template

app = Flask(__name__)

class SistemaExperto:
    def __init__(self):
        # Base de conocimientos: reglas
        self.reglas = {
            'fiebre': 'tomar_antipiretico',
            'tos': 'tomar_jarabe',
            'dolor_de_cabeza': 'tomar_analgesico',
            'dolor_de_estomago': 'tomar_antiacido',
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
```

### templates/index.html

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Sistema Experto de Salud</title>
</head>
<body>
    <h1>Sistema Experto de Salud</h1>
    <form method="post">
        <label><input type="checkbox" name="sintomas" value="fiebre"> Fiebre</label><br>
        <label><input type="checkbox" name="sintomas" value="tos"> Tos</label><br>
        <label><input type="checkbox" name="sintomas" value="dolor_de_cabeza"> Dolor de cabeza</label><br>
        <label><input type="checkbox" name="sintomas" value="dolor_de_estomago"> Dolor de estómago</label><br>
        <label><input type="checkbox" name="sintomas" value="fatiga"> Fatiga</label><br>
        <button type="submit">Diagnosticar</button>
    </form>
    {% if conclusiones %}
        <h2>Conclusiones</h2>
        <ul>
            {% for hecho, accion in conclusiones %}
                <li>Hecho: {{ hecho }} -> Acción: {{ accion }}</li>
            {% endfor %}
        </ul>
    {% endif %}
</body>
</html>
```


