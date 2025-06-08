# Listener Two Service

This service is a crucial component of the [FoundIT-Computer-Vision-Powered-Lost-and-Found-Mobile-Application](https://github.com/AchrefHemissi/FoundIT-Computer-Vision-Powered-Lost-and-Found-Mobile-Application)'s messaging infrastructure, specifically designed to process messages related to suspicious user detection. It acts as a bridge between the RabbitMQ message broker and the `suspicious_user_detection_service`.

## Overview

The `listener_two` service is responsible for consuming messages from the `task_queue_suspicious` within RabbitMQ. These messages typically contain data or requests that require analysis for suspicious activities. Upon receiving a message, `listener_two` processes it and then interacts with the `suspicious_user_detection_service` (located in the `lostfound-smart_matching-and-fraud_detection-microservices` repository) to execute the actual fraud detection logic. After the `suspicious_user_detection_service` completes its task, `listener_two` is responsible for publishing the results back to RabbitMQ, specifically to the `result_suspicious_queue`.

## Key Responsibilities

*   **Message Consumption**: Continuously listens for and retrieves messages from the `task_queue_suspicious` in RabbitMQ.
*   **Orchestration with Suspicious User Detection Service**: Triggers and coordinates the execution of suspicious user detection operations by communicating with the dedicated `suspicious_user_detection_service`.
*   **Result Publishing**: Sends the results obtained from the `suspicious_user_detection_service` back to the `result_suspicious_queue` in RabbitMQ, making them available for other services (like the `gateway`) to consume.
*   **Asynchronous Processing**: Enables the system to handle suspicious user detection requests asynchronously, improving overall system responsiveness and scalability.

## Technologies Used

*   **Python**: The primary programming language for the service logic.
*   **RabbitMQ Client Libraries**: For seamless interaction with the RabbitMQ message broker.
*   **Docker**: For containerization, ensuring consistent and isolated deployment.
*   **Docker Compose**: For defining and running the service and its dependencies in a multi-container environment, simplifying setup and management.

## Setup and Installation

To get the `listener_two` service up and running locally, follow these steps:

1.  **Clone the main repository**:

    ```bash
    git clone https://github.com/AchrefHemissi/lostfound-messaging-infrastructure.git
    cd lostfound-messaging-infrastructure/listener_two
    ```

2.  **Environment Configuration**: Ensure you have a `.env` file or equivalent environment variables configured for necessary settings, particularly the RabbitMQ connection details. This is essential for the listener to connect to the message broker and its queues.

3.  **Build and Run with Docker Compose**:

    Navigate to the `listener_two` directory and execute the following command:

    ```bash
    docker-compose up --build
    ```

    This command will:
    *   Build the Docker image for the `listener_two` service.
    *   Start the service container along with its dependencies, which typically includes a RabbitMQ instance.

## Usage

Once the `listener_two` service is running, it will automatically start consuming messages from the `task_queue_suspicious`. It will then process these messages by interacting with the `suspicious_user_detection_service` and publish the results back to the `result_suspicious_queue`. This service operates continuously in the background, ensuring that suspicious user detection requests are handled efficiently as they arrive in the message queue.



