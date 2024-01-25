# ETL Airflow with Docker Compose

This project demonstrates how to set up an ETL (Extract, Transform, Load) pipeline using Airflow and Docker Compose.

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/cindyangelira/airflow-docker.git
    ```

2. Navigate to the project directory:

    ```bash
    cd your-repo
    ```

3. Build and start the Docker containers:

    ```bash
    docker-compose up -d
    ```

4. Access the Airflow web interface:

    Open your web browser and go to `http://localhost:8080`.

## Usage

1. Define your ETL tasks in the `dags` directory.

2. Start the Airflow scheduler:

    ```bash
    docker-compose exec webserver airflow scheduler
    ```

3. Trigger the ETL pipeline:

    ```bash
    docker-compose exec webserver airflow trigger_dag your_dag_id
    ```

4. Monitor the progress and logs in the Airflow web interface.
