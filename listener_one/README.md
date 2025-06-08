# Listener One Service

This service is a key component of the [FoundIT-Computer-Vision-Powered-Lost-and-Found-Mobile-Application](https://github.com/AchrefHemissi/FoundIT-Computer-Vision-Powered-Lost-and-Found-Mobile-Application)'s messaging infrastructure, specifically designed to process messages related to item similarity searches. It acts as a bridge between the RabbitMQ message broker and the `similarity_search_service`.

## Overview

The `listener_one` service is responsible for consuming messages from the `task_queue_similarity` within RabbitMQ. These messages typically contain data or requests that require a similarity search to be performed. Upon receiving a message, `listener_one` processes it and then interacts with the `similarity_search_service` (located in the `lostfound-smart_matching-and-fraud_detection-microservices` repository) to execute the actual similarity matching logic. After the `similarity_search_service` completes its task, `listener_one` is responsible for publishing the results back to RabbitMQ, specifically to the `result_similarity_queue`.

## Key Responsibilities

*   **Message Consumption**: Continuously listens for and retrieves messages from the `task_queue_similarity` in RabbitMQ.
*   **Orchestration with Similarity Search Service**: Triggers and coordinates the execution of similarity search operations by communicating with the dedicated `similarity_search_service`.
*   **Result Publishing**: Sends the results obtained from the `similarity_search_service` back to the `result_similarity_queue` in RabbitMQ, making them available for other services (like the `gateway`) to consume.
*   **Asynchronous Processing**: Enables the system to handle similarity search requests asynchronously, improving overall system responsiveness and scalability.

## Technologies Used

*   **Python**: The primary programming language for the service logic.
*   **RabbitMQ Client Libraries**: For seamless interaction with the RabbitMQ message broker.
*   **Docker**: For containerization, ensuring consistent and isolated deployment.
*   **Docker Compose**: For defining and running the service and its dependencies in a multi-container environment, simplifying setup and management.

## Setup and Installation

To get the `listener_one` service up and running locally, follow these steps:

1.  **Clone the main repository**:

    ```bash
    git clone https://github.com/AchrefHemissi/lostfound-messaging-infrastructure.git
    cd lostfound-messaging-infrastructure/listener_one
    ```

2.  **Environment Configuration**: Ensure you have a `.env` file or equivalent environment variables configured for necessary settings, particularly the RabbitMQ connection details. This is essential for the listener to connect to the message broker and its queues.

3.  **Build and Run with Docker Compose**:

    Navigate to the `listener_one` directory and execute the following command:

    ```bash
    docker-compose up --build
    ```

    This command will:
    *   Build the Docker image for the `listener_one` service.
    *   Start the service container along with its dependencies, which typically includes a RabbitMQ instance.

## Usage

Once the `listener_one` service is running, it will automatically start consuming messages from the `task_queue_similarity`. It will then process these messages by interacting with the `similarity_search_service` and publish the results back to the `result_similarity_queue`. This service operates continuously in the background, ensuring that similarity search requests are handled efficiently as they arrive in the message queue.



