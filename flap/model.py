import torch
import torch.nn as nn
import torch.nn.functional as F

# class QNetwork(nn.Module):
#     """Actor (Policy) Model."""
#
#     def __init__(self, state_size, action_size, seed, fc1_units=64, fc2_units=64):
#         """Initialize parameters and build model.
#         Params
#         ======
#             state_size (int): Dimension of each state
#             action_size (int): Dimension of each action
#             seed (int): Random seed
#             fc1_units (int): Number of nodes in first hidden layer
#             fc2_units (int): Number of nodes in second hidden layer
#         """
#         super(QNetwork, self).__init__()
#         self.seed = torch.manual_seed(seed)
#         self.fc1 = nn.Linear(state_size, fc1_units)
#         self.fc2 = nn.Linear(fc1_units, fc2_units)
#         self.fc3 = nn.Linear(fc2_units, action_size)
#
#     def forward(self, state):
#         """Build a network that maps state -> action values."""
#         x = F.relu(self.fc1(state))
#         x = F.relu(self.fc2(x))
#         return self.fc3(x)

class QNetwork(nn.Module):
    def __init__(self, action_size ):
        super( QNetwork , self ).__init__()

        self.conv1 = nn.Conv2d( 1 , 16 , 3)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(16, 8, 3)
        self.conv3 = nn.Conv2d(8, 8, 3)

        self.fc1 = nn.Linear( 288 , 32 )
        self.fc2 = nn.Linear( 32, action_size )

    def forward(self, state):
        x = self.pool(F.relu(self.conv1( state )))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.pool(F.relu(self.conv3(x)))


        x = x.view(-1, 288 )
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return x
