import copy

GLOBAL_CONFIG = {"feature_a": True, "max_retries": 3}


class Configuration:
    def __init__(self, updates: dict, validator=None):
        self.updates = updates
        self.validator = validator
        self._original = None

    def __enter__(self):
        global GLOBAL_CONFIG
        self._original = copy.deepcopy(GLOBAL_CONFIG)

        temp_config = copy.deepcopy(GLOBAL_CONFIG)
        temp_config.update(self.updates)

        if self.validator and not self.validator(temp_config):
            raise ValueError("Invalid configuration update")

        GLOBAL_CONFIG.update(self.updates)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        global GLOBAL_CONFIG
        GLOBAL_CONFIG = self._original


def validate_config(config: dict) -> True | False:
    # Ensure max_retries >= 0
    return config.get("max_retries", 0) >= 0


if __name__ == '__main__':

    # ==================================================
    # Test with valid updates.
    # ==================================================
    print('\nTest with valid updates')
    print("Before validation:", GLOBAL_CONFIG)

    with Configuration({'feature_a': True, 'max_retries': 9}, validate_config):
        print("Inside `with`-blok:", GLOBAL_CONFIG)

    print("After validation:", GLOBAL_CONFIG)

    # ==================================================
    # Test with invalid updates.
    # ==================================================
    print('\nTest with invalid updates')
    print("Before validation:", GLOBAL_CONFIG)

    try:
        with Configuration({'feature_a': True, 'max_retries': -1}, validate_config):
            print("Inside `with` blok:", GLOBAL_CONFIG)
    except ValueError as err:
        print(err)

    print("After validation:", GLOBAL_CONFIG)

    # ==================================================
    # Test without validator
    # ==================================================
    print('\nTest without validator')
    print("Before validation:", GLOBAL_CONFIG)

    try:
        with Configuration({'feature_a': True, 'max_retries': -2}):
            print("Inside `with` block:", GLOBAL_CONFIG)
    except ValueError as err:
        print(err)

    print("After validation:", GLOBAL_CONFIG)
