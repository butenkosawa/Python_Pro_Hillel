import time


class TimerException(Exception):
    pass


class TimerContext:
    def __init__(self, time_out: float):
        self.time_out = time_out

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = time.perf_counter() - self.start
        if exc_type is None and elapsed > self.time_out:
            raise TimerException(f'Code execution time exceeded {self.time_out} seconds')


if __name__ == '__main__':
    try:
        with TimerContext(1):
            time.sleep(2)
    except TimerException as err:
        print(f'A `TimerException` occurred in `with` block:\n{err}')
    else:
        print("Hello")
