from invoke import Collection

from . import plot
from . import run
from . import wasm

ns = Collection(plot, run, wasm)