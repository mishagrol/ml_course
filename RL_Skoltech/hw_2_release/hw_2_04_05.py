#!/usr/bin/env python
# coding: utf-8



from rcognita import EndiSystem, EndiControllerBase, Simulation, AnswerTracker
from IPython.display import HTML, clear_output
import numpy as np
import scipy as sp
from scipy.optimize import minimize

hw2_answers = AnswerTracker()




class TBVILS(EndiControllerBase):
    """ Implementation of Trajectory Based Value Iteration with LS minimization

    """

    def __init__(self, system, horizon_length=10, **kwargs):
        super(TBVILS, self).__init__(system, **kwargs)
        self.ctrl_mode = 3
        self.x_buffer = self.y_buffer # renaming y to x to stick to common notation
        self.horizon_length = horizon_length
        self.gamma = 0.95

        self._initialize_weights()

        # control bounds tiled over horizon_length
        self.u_min = np.tile(self.min_bounds, self.horizon_length)
        self.u_max = np.tile(self.max_bounds, self.horizon_length)
        
        
        #my variable -- GROL 
        self.W_prev = np.ones(int(self.dim_state + self.dim_input))
    def _initialize_weights(self):
        """ initialize weights for parameter vector `W` """

        num_weights = int(self.dim_state + self.dim_input)

        self.W = np.random.rand(num_weights)
        self.w_min = np.zeros(num_weights)
        self.w_max = 1e3 * np.ones(num_weights)
    
    def _update_buffers(self, u, x):
        """ update x and u buffers on each call of compute_action

        Args:

            u : float vector
                * control (action)

            x : float vector
                * state

        """
        self.u_buffer = np.vstack([self.u_buffer, u])[-self.buffer_size:, :]
        self.x_buffer = np.vstack([self.x_buffer, x])[-self.buffer_size:, :]
        
    def compute_action(self, t, x):
        """ compute action for time step

        Args:

            t : float
                * time step - current time step
            
            x : float vector
                * state

        Returns:
            u : vector
                * new action/control

        """
        time_since_last_action = t - self.ctrl_clock

        if time_since_last_action >= self.sample_time:
            # Update controller's internal clock
            self.ctrl_clock = t

            ### YOUR SOLUTION BELOW
            # Line 6: update buffers (call method above)
            self._update_buffers(self.u_curr,self.system_state) # надо определить u, x и откуда они берутся
            # Line 7: update Q-function (call weight_update method)
            self._weight_update(self.W, self.u_buffer, self.x_buffer) 
            # Line 9: update policy function (call policy_method)
            self.u_curr = self._policy(self.system_state ,self.W)
            return self.u_curr
            ### YOUR SOLUTION ABOVE

        else:
            return self.u_curr

    def _policy(self, x, W):
        """ calculate next action for state

        Args:

            x : float vector

        Returns:
        
            u : vector
                * new action/control

        """
        # define solver options
        options = {'maxiter': 200, 'disp': False, 'ftol': 1e-7}
        bounds = sp.optimize.Bounds(self.u_min, self.u_max, keep_feasible=True)

        # tile current action across buffer size to make trajectory
        u_trajectory = np.tile(self.u_curr, self.horizon_length)
        
        """
        Minimize cost-over-trajectory with respect to actions. Returns a trajectory of actions.
        You'll need to study how this works by reading the documentation. The variable `u_trajectory` 
        serves as an initial input of actions used by `minimize` to minimize 
        the cost by updating parameters.
        """
        
        U_new = minimize(lambda U: self._cost_over_traj(U, W, x), u_trajectory,
                     method='SLSQP',
                     tol=1e-7,
                     bounds=bounds,
                     options=options).x

        # output first action of new action (trajectory)
        first_u = U_new[:self.dim_input]

        return first_u

    def _cost_over_traj(self, u, w, x):
        """ generate trajectory of steps and calculate cost over 
        the trajectory

        Description: given initial action (u) and observtion (x),
        create a trajectory of predicted steps/states,
        where the number of predictions == horizon_length. 
        Then, calculate the discounted cost of this 
        trajectory with the Q-function.

        Args:

            u : float vector
                * control/action
            
            w : float vector
                * Q-function parameters
            
            x : float vector
                * state

        Returns: 

            trajectory_q_cost : float

        """
        u_trajectory = np.reshape(u, (self.horizon_length, self.dim_input))
        x_trajectory = np.zeros([self.horizon_length, self.dim_output])
        x_trajectory[0, :] = x

        for k in range(1, self.horizon_length):
            x = x + self.step_size * self.sys_dynamics(None, x, u_trajectory[k - 1, :], self.m, self.I, self.dim_state, self.is_disturb)

            x_trajectory[k, :] = x

        ### YOUR SOLUTION BELOW
        # calculate cost of trajectory by calling the value function. `calculate_td` should be false.
        traj_q_cost = self._value_function(w, u_trajectory, x_trajectory, self.horizon_length, calculate_td=False)
        ### YOUR SOLUTION ABOVE

        return traj_q_cost

    def _weight_update(self, Winit, u_buffer, x_buffer):
        """ update weights for Q-function.

        Args:

            Winit : float vector
                * initial weights for solver to start minimizing from

            u_buffer : 2D float array
                * controls buffer

            x_buffer : 2D float array
                * state buffer

        Returns:

            W_new - updated weights

        """
        ### YOUR SOLUTION BELOW
        
        # your solution should look very similar to the policy update.
        options = {'maxiter': 200, 'disp': False, 'ftol': 1e-7}

        # вероятно что-то надо в границах менять 
        bounds = sp.optimize.Bounds(self.w_min, self.w_max, keep_feasible=True)

        
        #Approximate Q
        
        #Q_s_a = self.W.T @ self._phi(self.system_state)
        
        #Target Q
        #Q_target = self.running_cost(x,self._policy(x)) + self.W.T @ self.gamma *self._phi(self.system_state)

        #self.running_cost(x_next, u_prev) + (self.gamma * self.W_prev @ self._phi(x_next, u_next)) - (W @ self._phi(x_next, u_prev))

        # def min_q_function(W):
        #     Q_s_a = W.T * self._phi(self.system_state)
        #     Q_target = self.running_cost(self.system_state ,self._policy(self.system_state, W)) + W.T * self.gamma *self._phi(self.system_state)

        #     return (Q_target -  Q_s_a)**2


        def minimiza_td(W, u_buffer, y_buffer):
            """ Cost function of the critic
            Currently uses value-iteration
            """
            Jc = 0

            for k in range(1, self.buffer_size-1):
                y_prev = y_buffer[k - 1, :]
                y_next = y_buffer[k, :]
                u_prev = u_buffer[k - 1, :]
                u_next = u_buffer[k, :]

                # Temporal difference
                e = self.running_cost(y_prev, u_prev) + (self.gamma * self.W_prev @ self._phi(y_next, u_next)) - (W @ self._phi(y_prev, u_prev))

                Jc += (1 / 2) * e**2

            return Jc

        W_new  = minimize(lambda W: minimiza_td(W, self.u_buffer, self.x_buffer), Winit,
                     method='SLSQP',
                     tol=1e-7,
                     bounds=bounds,
                     options=options).x

        self.W = W_new
        ### YOUR SOLUTION ABOVE

    def _value_function(self, W, u_container, x_container, length, calculate_td=False):
        """ Q-function

        Args:

            W : float vector
                * Q-function parameters

            u_container : 2D float array
                * buffer or trajectory of control inputs

            x_container : 2D float array
                * buffer or trajectory of observations
            
            calculate_td : boolean
                * calculcate V(S) or temporal difference?

        Returns:
            J : float
                * cost

        """

        ### YOUR SOLUTION BELOW

        J = 0

        for k in range(1, length):
            x = x_container[k - 1, :]
            u = u_container[k - 1, :]
            x_next = x_container[k, :]
            u_next = u_container[k, :]
            
            # Temporal difference
            # based on rcognita
            # old => –Jc += (1 / 2) * e**

            if calculate_td:
                e = self.running_cost(x, u) + (self.gamma * self.W @ self._phi(x_next, u_next)) - (W @ self._phi(x, u))

            #ЧТО ТАКОЕ J?? 
                J += e

            else:
                # pass# calculate cost over trajectory (don't forget to increment J)
                cost = (self.gamma**k)*(self.running_cost(x_next, u_next))
                J += cost
        ### YOUR SOLUTION ABOVE
        return J

    def _phi(self, x, u=None):
        """ Feature vector used in approximating Q

        Args:

            x : float vector
                * state

            u : float vector
                * controls

        returns:
            chi : vector
            
        """

        ### YOUR SOLUTION BELOW
        if u is not None:
            chi = np.concatenate((x, u))
        else:
            chi = x
        ### YOUR SOLUTION ABOVE

        return chi**2



# create system
sys = EndiSystem(initial_x=7, initial_y=7)

# create agent
agent = TBVILS(sys, sample_time=0.3, t1=17)

# create sim
sim = Simulation(sys, agent)

sim.run_simulation(n_runs=2, 
                is_visualization=False, 
                close_plt_on_finish=False, 
                show_annotations=True, 
                print_summary_stats=False, 
                print_statistics_at_step=True,
                print_inline=True)


### GRADING DO NOT MODIFY
statistics, = sim.final_statistics

hw2_answers.record('problem_1-2', {'mean_rc': statistics[0],
    'mean_velocity': statistics[1], 
    'sd_rc': statistics[2],
    'sd_velocity': statistics[3],
    'sd_alpha': statistics[4],
    'l2_norm': statistics[5]})



hw2_answers.print_answers()


assignment_name = "hw_2"
first_name = "Mikhail" # Use proper capitalization
last_name = "Gasanov" # Use proper capitalization

hw2_answers.save_to_json(assignment_name, first_name, last_name)

