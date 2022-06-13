import torch
import torch.nn as nn

DRAW_REWARD = WIN_REWARD = 1.0
LOSS_REWARD = 0.0


class AIModel(nn.Module):
    NEURON_COUNT = 36

    def __init__(self, board_size: int):
        super().__init__()
        input_size = board_size * board_size
        output_size = input_size
        self.input_layer = nn.Linear(input_size, self.NEURON_COUNT)
        self.hidden_layer = nn.Linear(self.NEURON_COUNT, self.NEURON_COUNT)
        self.output_layer = nn.Linear(self.NEURON_COUNT, output_size)

    def forward(self, x):
        # pass through dense input and hidden layers and apply activation function
        x = self.input_layer(x)
        x = torch.relu(x)

        x = self.hidden_layer(x)
        x = torch.relu(x)

        # pass through output layer and apply activation function
        x = self.output_layer(x)
        x = torch.sigmoid(x)

        return x


class NeuralNetwork:
    LEARNING_RATE = 0.1

    def __init__(self, board_size, seed):
        # for serialization purposes
        self.board_size = board_size
        self.seed = seed

        self.policy_network = AIModel(board_size)

        self.target_network = AIModel(board_size)
        self.update_target_network()
        self.target_network.eval()

        self.optimizer = torch.optim.SGD(self.policy_network.parameters(), lr=self.LEARNING_RATE)
        self.loss = nn.MSELoss()

    def update_target_network(self):
        self.target_network.load_state_dict(self.policy_network.state_dict())

    def state_dict(self):
        return {
            "board_size": self.board_size,
            "seed": self.seed,
            "policy_network": self.policy_network.state_dict(),
            "target_network": self.target_network.state_dict(),
            "optimizer": self.optimizer.state_dict(),
            "loss": self.loss.state_dict(),
        }

    @classmethod
    def from_state_dict(cls, state_dict):
        board_size = state_dict["board_size"]
        seed = state_dict["seed"]
        ret = cls(board_size, seed)

        for key, value in state_dict.items():
            if key in ("board_size", "seed"):
                continue
            obj = getattr(ret, key)
            obj.load_state_dict(value)
            if key != "optimizer":
                obj.eval()

        return ret


class InvalidGameState(Exception):
    """
    Indicates that the game reached an invalid state as a result of NN player's move.

    This allows us to later indicate to teach NN that such move shouldn't be made.
    """


def backpropagate(nn, board, move_idx, target_value):
    nn.optimizer.zero_grad()
    output = nn.policy_network(board.tensor)

    target = output.clone().detach()
    target[move_idx] = target_value
    for x, y in board.get_invalid_moves():
        target[board.size * x + y] = LOSS_REWARD
    
    loss = nn.loss(output, target)
    loss.backward()
    nn.optimizer.step()
