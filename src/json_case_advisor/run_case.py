import argparse
import json
from pathlib import Path


def leq(a, b):
    return all(x <= y for x, y in zip(a, b))


def add(a, b):
    return [x + y for x, y in zip(a, b)]


def calc_need(maximum, allocation):
    return [[maximum[i][j] - allocation[i][j] for j in range(len(maximum[0]))] for i in range(len(maximum))]


def check_state(data):
    maximum = data["max"]
    allocation = data["allocation"]
    available = data["available"]
    names = data.get("processes", [f"P{i}" for i in range(len(maximum))])
    need = calc_need(maximum, allocation)
    work = available[:]
    finish = [False] * len(maximum)
    sequence = []
    rounds = []

    while True:
        picked = None
        for i, row in enumerate(need):
            if not finish[i] and leq(row, work):
                picked = i
                break
        if picked is None:
            break
        rounds.append(
            {
                "process": names[picked],
                "need": need[picked],
                "work_before": work[:],
                "release": allocation[picked],
            }
        )
        work = add(work, allocation[picked])
        finish[picked] = True
        sequence.append(names[picked])

    blocked = [names[i] for i, done in enumerate(finish) if not done]
    return {
        "safe": all(finish),
        "sequence": sequence,
        "blocked": blocked,
        "need": need,
        "rounds": rounds,
        "diagnosis": build_diagnosis(blocked, need, work, names),
    }


def build_diagnosis(blocked, need, work, names):
    if not blocked:
        return "system is safe; no deadlock risk found in this check"
    details = []
    for name in blocked:
        index = names.index(name)
        details.append(f"{name} need={need[index]} cannot be satisfied by final work={work}")
    return "; ".join(details)


def main():
    default_path = Path(__file__).resolve().parents[2] / "data" / "example_state.json"
    parser = argparse.ArgumentParser(description="Run banker algorithm from JSON")
    parser.add_argument("--input", default=str(default_path))
    parser.add_argument("--out", default="")
    args = parser.parse_args()

    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    result = check_state(data)
    text = json.dumps(result, ensure_ascii=False, indent=2)
    print(text)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
