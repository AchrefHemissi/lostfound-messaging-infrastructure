# Gateway Service

This service acts as the central entry point and API Gateway for the [FoundIT-Computer-Vision-Powered-Lost-and-Found-Mobile-Application](https://github.com/AchrefHemissi/FoundIT-Computer-Vision-Powered-Lost-and-Found-Mobile-Application). It is a crucial component of the messaging infrastructure, responsible for handling incoming requests from the frontend, routing them to the appropriate backend microservices, and managing asynchronous communication via RabbitMQ.

## Overview

The `gateway` service serves as the primary interface between the main backend system(firebase) and the various backend microservices. Its main function is to receive requests, direct them to the correct service for processing, and then relay the responses back to the firebase. It plays a vital role in orchestrating the flow of information within the system, ensuring that messages are efficiently and reliably delivered.

## Key Responsibilities

*   **Request Routing**: Directs incoming requests from the firebase to the relevant microservices (e.g., Similarity Search Service, Suspicious User Detection Service, Unstructured Data Storage Service).
*   **RabbitMQ Integration**: Communicates with RabbitMQ to send messages to task queues (`task_queue_similarity`, `task_queue_suspicious`) and consume results from response queues (`result_similarity_queue`, `result_suspicious_queue`). This enables asynchronous processing and decouples services.
*   **API Management**: Acts as an API Gateway, potentially handling concerns like authentication, rate limiting, and load balancing before forwarding requests.
*   **Orchestration**: Coordinates the flow of data and messages between different parts of the LostFound system.

## Technologies Used

*   **Python**: The primary programming language for the service logic.
*   **RabbitMQ Client Libraries**: For interacting with the RabbitMQ message broker.
*   **Docker**: For containerization, ensuring consistent deployment.
*   **Docker Compose**: For defining and running the service and its dependencies in a multi-container environment.

## Setup and Installation

To get the `gateway` service up and running locally, follow these steps:

1.  **Clone the main repository**:

    ```bash
    git clone https://github.com/AchrefHemissi/lostfound-messaging-infrastructure.git
    cd lostfound-messaging-infrastructure/gateway
    ```

2.  **Environment Configuration**: Ensure you have a `.env` file or equivalent environment variables configured for necessary settings, particularly the RabbitMQ connection details. This is crucial for the gateway to connect to the message broker.

3.  **Build and Run with Docker Compose**:

    Navigate to the `gateway` directory and execute the following command:

    ```bash
    docker-compose up --build
    ```

    This command will:
    *   Build the Docker image for the gateway service.
    *   Start the gateway container along with its dependencies, which typically includes a RabbitMQ instance.

## Usage

Once the `gateway` service is running, it will begin listening for incoming requests from the frontend. It will then publish messages to RabbitMQ exchanges, which will be routed to the appropriate listener services (`listener_one` and `listener_two`). After the listener services process the messages, they will send results back to RabbitMQ queues, which the gateway will consume to provide responses back to the frontend.



