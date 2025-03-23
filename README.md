# Metro Route Optimization Project

This project is part of the **Global AI Hub Akbank Python ile Yapay Zekaya Giriş Bootcamp**. It simulates a metro network and provides two main functionalities:
1. Finding the route with the least number of transfers between two stations.
2. Finding the fastest route between two stations, considering transfer times.

## Technologies and Libraries Used
- **Python**: The project is implemented in Python.
- **Collections Module**: Used for creating queues with `deque`.
- **Heapq Module**: Used for implementing priority queues in the A* algorithm.

## Algorithms Used

### Breadth-First Search (BFS)
- **Purpose**: Finds the route with the least number of transfers between two stations.
- **How it works**: 
  - Starts from the initial station and explores all neighboring stations level by level.
  - Keeps track of visited stations to avoid loops.
  - Stops when the target station is found, ensuring the path has the minimum number of transfers.

### A* Algorithm
- **Purpose**: Finds the fastest route between two stations, considering travel and transfer times.
- **How it works**:
  - Uses a heuristic to estimate the cost to reach the target station.
  - Prioritizes paths with lower total travel time.
  - Considers transfer penalties when switching metro lines.

## Example Usage and Test Results

### Scenario 1: From AŞTİ to OSB
- **Route with least transfers**: AŞTİ -> Kızılay -> Ulus -> Demetevler -> OSB
- **Fastest route (24 minutes)**: AŞTİ -> Kızılay -> Ulus -> Demetevler -> OSB

### Scenario 2: From Batıkent to Keçiören
- **Route with least transfers**: Batıkent -> Demetevler -> Gar -> Keçiören
- **Fastest route (21 minutes)**: Batıkent -> Demetevler -> Gar -> Keçiören

### Scenario 3: From Keçiören to AŞTİ
- **Route with least transfers**: Keçiören -> Gar -> Sıhhiye -> Kızılay -> AŞTİ
- **Fastest route (14 minutes)**: Keçiören -> Gar -> Sıhhiye -> Kızılay -> AŞTİ

## Ideas for Further Development
- **Visualization**: Add a graphical representation of the metro network and routes.
- **Real-time Data**: Integrate real-time metro schedules and delays.
- **User Interface**: Develop a user-friendly interface for easier interaction.

## How to Run the Project
1. Clone the repository.
2. Ensure Python is installed on your system.
3. Run the `metro_simulation.py` script.
4. Follow the prompts to test different scenarios.

## Contact
For any questions or further information, please contact the project maintainer.
