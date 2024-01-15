# Flappy Bird NEAT

## Overview

This project is an implementation of the classic Flappy Bird game using the NEAT (NeuroEvolution of Augmenting Topologies) algorithm. The game features a population of birds that are trained through evolutionary algorithms to navigate through obstacles (pipes) and achieve the highest possible score.

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
python flappy_bird_neat.py
```

This command starts the Flappy Bird game, where a population of birds is trained using the NEAT algorithm to navigate through obstacles.

## Configuration

- **Python version:** 3.12.1

## NEAT Configuration

The NEAT configuration file used for training the birds is located at `config/neat_cfg.txt`. Adjustments to NEAT parameters can be made in this file to experiment with different evolutionary settings.

## Dependencies

- `neat-python==0.92`
- `pygame==2.5.2`

## Acknowledgements

This project is inspired by the Flappy Bird game and the NEAT algorithm. The Flappy Bird assets are utilized for educational purposes and are not owned by the creator of this project.

## License

This project is licensed under the [MIT License](LICENSE). Feel free to use and modify the code for your own projects.