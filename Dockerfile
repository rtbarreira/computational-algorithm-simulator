FROM clojure:lein-2.10.0

WORKDIR /app
COPY . /app

# Instalar dependências do projeto
RUN lein deps

# Instalar Python, venv e unzip
RUN apt-get update && apt-get install -y python3-pip python3-venv unzip

# Criar e ativar ambiente virtual para o Flask
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Atualizar pip e instalar Flask no venv
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copiar api.py
COPY api.py /app/api.py

EXPOSE 5000
CMD ["python", "api.py"]
