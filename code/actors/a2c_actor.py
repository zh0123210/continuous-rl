from torch import Tensor
from torch.distributions import Distribution
from torch.optim import Optimizer
from memory.memorytrajectory import BatchTraj
from logging import info
from actors.online_actor import OnlineActorContinuous, OnlineActorDiscrete
from gym.spaces import Box, Discrete
from models import ContinuousRandomPolicy, DiscreteRandomPolicy

# def optimize(distr: Distribution, traj: BatchTraj, critic_value: Tensor,
#              c_entropy: float, optimizer: Optimizer) -> None:
#     action = traj.actions
#     logp_action = distr.log_prob(action)
#     entropy = distr.entropy()

#     loss_critic = (- logp_action * critic_value.detach()).mean()
#     loss = loss_critic - c_entropy * entropy

#     info(f"loss_critic:{loss_critic.mean().item():3.2e}\t"
#          f"entropy:{entropy.mean().item():3.2e}")
#     optimizer.zero_grad()
#     loss.mean().backward()
#     optimizer.step()

class A2CActorContinuous(OnlineActorContinuous):
    pass
    # def _optimize_from_distr(self, distr: Distribution, traj: BatchTraj,
    #                          critic_value: Tensor) -> None:
    #     optimize(distr, traj, critic_value, self._c_entropy, self._optimizer)

class A2CActorDiscrete(OnlineActorDiscrete):
    pass
    # def _optimize_from_distr(self, distr: Distribution, traj: BatchTraj,
    #                          critic_value: Tensor) -> None:
    #     optimize(distr, traj, critic_value, self._c_entropy, self._optimizer)

# this is a dummy class
class A2CActor(object):
    @staticmethod
    def configure(**kwargs):
        action_space = kwargs['action_space']
        observation_space = kwargs['observation_space']
        assert isinstance(observation_space, Box)

        # net_dict = dict(hidden_size=kwargs['hidden_size'], nb_layers=kwargs['nb_layers'])
        nb_state_feats = observation_space.shape[-1]
        if isinstance(action_space, Box):
            nb_actions = action_space.shape[-1]
            policy_generator = ContinuousRandomPolicy
            # policy_function = ContinuousRandomPolicy(nb_state_feats, nb_actions,
            #                                          **net_dict)
            actor_generator = A2CActorContinuous
        elif isinstance(action_space, Discrete):
            nb_actions = action_space.n
            policy_generator = DiscreteRandomPolicy
            actor_generator = A2CActorDiscrete
        policy_function = policy_generator(nb_state_feats, nb_actions, kwargs['nb_layers'], kwargs['hidden_size'])

        return actor_generator(policy_function, kwargs['lr'], kwargs['optimizer'],
                               kwargs['dt'], kwargs['c_entropy'],
                               kwargs['weight_decay'])
