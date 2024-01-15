# Flappy Bird NEAT

## Overview

Flappy Bird NEAT is a Python implementation of the popular Flappy Bird game, enhanced with the NEAT (NeuroEvolution of Augmenting Topologies) algorithm. This project showcases the application of evolutionary algorithms in training a population of virtual birds to navigate through challenging obstacles, demonstrating the power of machine learning in achieving intelligent and adaptive behavior.

### Key Features

- **NEAT Algorithm Integration:** Utilizes the NEAT algorithm to evolve neural networks that control the behavior of virtual birds, allowing them to autonomously learn and adapt their strategies over successive generations.

- **Dynamic Obstacle Navigation:** Birds are tasked with navigating through dynamically generated obstacles (pipes) by flapping their wings. The NEAT-trained neural networks determine the birds' actions, showcasing the emergence of intelligent decision-making.

- **Scoring System:** Tracks the performance of each bird in terms of the distance traveled and awards fitness scores accordingly. The goal is to achieve the highest possible score by efficiently maneuvering through obstacles.

## Installation

1. **Clone the repository:**
   
   ```bash
   git clone https://github.com/ssspetrovic/flappy-bird-ga.git
   ```

2. **Navigate to the project directory:**
   
   ```bash
   cd flappy-bird-neat
   ```

3. **Create a virtual environment (optional but recommended):**
   
   ```bash
   python3.12 -m venv venv
   ```

4. **Activate the virtual environment:**
   
   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On Unix or MacOS:

     ```bash
     source venv/bin/activate
     ```

5. **Install the required packages:**
   
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the NEAT algorithm with the provided configuration file:

```bash
python main.py
```

This command initiates the Flappy Bird game, where a population of birds undergoes training via the NEAT algorithm, showcasing the evolution of intelligent behaviors.

## Configuration

- **Python version:** 3.12.1

## NEAT Configuration

The NEAT configuration file used for training the birds is located at `config/neat_cfg.txt`. Experiment with this file to fine-tune NEAT parameters and observe the impact on the learning process.

## Dependencies

- `neat-python==0.92`
- `pygame==2.5.2`

## Acknowledgements

This project draws inspiration from the classic Flappy Bird game and highlights the potential of the NEAT algorithm in creating adaptive and intelligent agents. The Flappy Bird assets are employed for educational purposes and are not owned by the creator of this project.

## License

This project is licensed under the [MIT License](LICENSE). Feel free to use and modify the code for your own projects.
