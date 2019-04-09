import sys
from InvertedIndex import build_ii
from timeit import default_timer as timer

def setupBuildII():
    start = timer()
    print("----------Building Inverted Index-----------")
    inverted_index = build_ii.BuildII()
    inv_ind = inverted_index.make_inverted_index()
    print("------------------DONE----------------------")
    end = timer()
    print(f"{end - start} seconds")


if __name__ == "__main__":
    print("Building Inverted Index")
    setupBuildII()

