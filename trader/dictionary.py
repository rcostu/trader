"""
This class reads params from a YAML file and creates an object that
contains attributes named as the params in the file, accessible through
getters:

  object.parameter

in addition to classical dictionary access method

  object[parameter]

The structure of attributes is built recursively if they contain a dictionary.

  object.attr1.attr2.attr3

"""

from os import getcwd
from pathlib import Path
from pandas import DataFrame

from utils.my_dict import MyDict
from display import Display
from yaml import safe_load, YAMLError


class Dictionary(MyDict):

    def __init__(self, default_params_filename='params.yaml', **kwargs):
        """
        Read the parameters from a default filename
        :return:
        """
        super().__init__(**kwargs)
        params = {}
        cwd = Path(getcwd())
        params_path: str = str(cwd.joinpath(default_params_filename))

        with open(params_path, 'r') as stream:
            try:
                params = safe_load(stream)
            except YAMLError as exc:
                print(exc)

        self.add_dict(self, params)

        # Check that I've states and actions to start playing with.
        if not self._action or not self._state:
            raise AssertionError('No states or actions defined in config file.')

        # Build a dictionary with a sequential number associated to each action
        setattr(self, '_action_id', MyDict())
        for tup in zip(self._action, range(len(self._action))):
            self._action_id[tup[0]] = tup[1]

        # Build the reverse dictionary for the actions dictionary
        setattr(self, '_action_name', MyDict())
        for tup in zip(range(len(self._action)), self._action):
            self._action_name[tup[0]] = tup[1]

        # Specific attributes to store number of actions and states.
        setattr(self, '_num_actions', len(self._action))

        # Build a list of lists with the names of all possible states.
        setattr(self, '_states_list', list())
        for state in self._state.keys():
            if state[0] == '_':
                self._states_list.append(self._state[state]._names)

        # Compute the total number of states as the multiplication of the
        # number of substates in eachs posible state-stack
        setattr(self, '_num_states', int)
        self._num_states = 1
        for state in self._state.keys():
            self._num_states = self._num_states * len(self._state[state]._names)

        # Create a display property to centralize all reporting activity into
        # a single function. That way I can store it all in a single dataframe
        # for later analysis.
        setattr(self, 'display', Display)
        self.display = Display(self)

        # Create a DataFrame within the configuration to store all the values
        # that are relevant to later perform data analysis.
        # The YAML file contains the column names in a parameter called
        # table_headers.
        setattr(self, 'results', DataFrame)
        self.results = DataFrame(columns=self._table_headers)

    @property
    def save_model(self):
        return self._save_model

    @property
    def state(self):
        return self._state

    @property
    def states_list(self):
        return self._states_list
