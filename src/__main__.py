from .model import Model
import json
import os
import time
from .model import parse_args


def main() -> None:
    mod = Model()
    begin_time = time.perf_counter()
    resulta = mod.main()
    print("===", resulta, "end")
    arg = parse_args()
    path = arg.output
    os.makedirs("data/output", exist_ok=True)
    try:
        with open(path, 'w+')as f:
            json.dump(json.loads(resulta), f, indent=4)
    except IOError as e:
        print(e)
    end_time = time.perf_counter()
    print((end_time - begin_time)/60)


if __name__ == "__main__":
    try:
        main()
    except json.decoder.JSONDecodeError:
        print("error")
    except Exception as e:
        print(e)
