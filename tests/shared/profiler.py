import cProfile
import pstats

profiler = None

def start_profiler():
    global profiler
    profiler = cProfile.Profile()
    profiler.enable()

def stop_profiler():
    global profiler
    profiler.disable()
    pstats.Stats(profiler).print_stats()