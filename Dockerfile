FROM python:3.8

# Agregar el contenido del proyecto al contenedor\ADD . /code

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /code

# Instalar las dependencias listadas en requirements.txt
RUN pip install -r requirements.txt

# Comando para ejecutar la aplicación Flask
CMD python index.py
