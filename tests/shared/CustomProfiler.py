import cProfile
import linecache
import os
import pstats
import tracemalloc

profiler = None
profileType = 'TIME'
#profileType = 'MEMORY'


def start_profiler():
    global profileType
    if profileType == 'TIME':
        start_time_profiler()
    else:
        start_memory_profiler()



def stop_profiler():
    if profileType == 'TIME':
        stop_time_profiler()
    else:
        stop_memory_profiler()


def start_time_profiler():
    global profiler
    profiler = cProfile.Profile()
    profiler.enable()

def start_memory_profiler():
    tracemalloc.start()


def stop_time_profiler():
    global profiler
    profiler.disable()
    pstats.Stats(profiler).print_stats()


def stop_memory_profiler(key_type='lineno', limit=3):

    snapshot = tracemalloc.take_snapshot()
    snapshot = snapshot.filter_traces((
        tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
        tracemalloc.Filter(False, "<unknown>"),
    ))
    top_stats = snapshot.statistics(key_type)

    print("Top %s lines" % limit)
    for index, stat in enumerate(top_stats[:limit], 1):
        frame = stat.traceback[0]
        # replace "/path/to/module/file.py" with "module/file.py"
        filename = os.sep.join(frame.filename.split(os.sep)[-2:])
        print("#%s: %s:%s: %.1f KiB"
              % (index, filename, frame.lineno, stat.size / 1024))
        line = linecache.getline(frame.filename, frame.lineno).strip()
        if line:
            print('    %s' % line)

    other = top_stats[limit:]
    if other:
        size = sum(stat.size for stat in other)
        print("%s other: %.1f KiB" % (len(other), size / 1024))
    total = sum(stat.size for stat in top_stats)
    print("Total allocated size: %.1f KiB" % (total / 1024))