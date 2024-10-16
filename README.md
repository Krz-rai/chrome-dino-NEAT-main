# NEAT-based Chrome Dinosaur Game

This Python project is based on the Chrome Dinosaur game, where a dinosaur must avoid obstacles like cacti and birds. The dinosaur's behavior is controlled by a neural network that evolves using the NEAT (NeuroEvolution of Augmenting Topologies) algorithm. The AI learns to jump, run, and duck to avoid obstacles, improving over multiple generations.

## Features
- **Obstacle Avoidance**: The dinosaur learns to avoid cacti (small and large) and birds that appear on the screen.
- **AI Evolution**: The NEAT algorithm is used to evolve the neural network controlling the dinosaur's movements.
- **Real-Time Visualization**: Watch the dinosaur evolve and improve as it learns to survive longer in the game.

## Prerequisites

To run this project, you'll need the following dependencies:

- **Python 3.x**
- **Pygame**: For game visualization and rendering.
- **NEAT-Python**: For implementing the neuroevolution.

You can install the dependencies using the following command:

```bash
pip install pygame neat-python
```

## How It Works

1. **Neural Network Inputs**: The neural network controlling the dinosaur receives the following inputs:
   - Dinosaur's Y-position and bottom position.
   - Distance between the dinosaur and the nearest obstacle.
   - The type, height, and width of the nearest obstacle (Small Cactus, Large Cactus, Bird, Bird2, Bird3).
   - Vertical distance between the dinosaur and a bird.
   - Game speed.
   - Whether the dinosaur is jumping or ducking.

2. **Movement Decision**: Based on these inputs, the neural network outputs two values:
   - Whether the dinosaur should jump or duck.
   - Whether the dinosaur should keep running.

3. **Rewards and Penalties**:
   - The dinosaur is rewarded for avoiding obstacles and surviving longer.
   - The dinosaur is penalized for colliding with obstacles.
   
4. **Fitness Evaluation**: Each dinosaur's fitness score is determined by how far it survives without hitting obstacles. The best-performing dinosaurs are kept for the next generation.

## Code Breakdown

### 1. **`Dinosaur` Class**
Defines the dinosaur's behavior, including its ability to jump, run, and duck. The dinosaur's movement is controlled by the neural network outputs.

### 2. **`Obstacle` and Derived Classes**
Defines the obstacles (cacti and birds) that the dinosaur must avoid. There are several variations of cacti and birds, each with different characteristics.

### 3. **`Cloud` Class**
Represents clouds moving in the background to create a dynamic environment.

### 4. **`main(genomes, config)` Function**
This is the core loop where the NEAT algorithm runs. Each dinosaur is controlled by a neural network, and the game simulates their behavior. Dinosaurs receive rewards or penalties based on their performance.

### 5. **`run(config_path)` Function**
Initializes the NEAT algorithm, sets up the game environment, and runs the simulation for a set number of generations (150).

## Running the Game

1. **Clone the repository**:

```bash
git clone https://github.com/kr3287/neat-dino-game.git
cd chrome-dino-NEAT
```

2. **Run the Game**:

```bash
python main.py
```

The `dino.py` script will start the simulation, and you'll see the dinosaurs evolving over time to avoid obstacles and survive longer.

## NEAT Configuration

The NEAT algorithm is configured using the `config-feedforward.txt` file. You can adjust parameters like population size, mutation rates, and fitness thresholds to tweak the evolution process.

## Example Output

After running the simulation, you should see dinosaurs attempting to avoid cacti and birds, jumping or ducking as they evolve. Over time, the best dinosaurs should survive longer as their neural networks improve.

## Original Game Files

The original game files (assets and basic game logic) were taken from the [Chrome Dinosaur Game by Max Rohowsky](https://github.com/MaxRohowsky/chrome-dinosaur). The NEAT-related functionality (AI, evolution, and decision-making) was implemented separately.

## Contributions

If you’d like to contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
