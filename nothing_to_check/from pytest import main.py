from pytest import main

def arithmetic_arranger(exprs):
    out = []
    for e in exprs:
        e = e.split(maxsplit=1)
        max_len = len(max(e, key=len))
        out.append(
            [f"{ee:>{max_len}}" for ee in e + ["-" * max_len, eval("".join(e))]]
        )

    for row in zip(*out):
        print("   ".join(row))


arithmetic_arranger(["32 + 9", "1 - 3801", "9999 + 9999", "523 - 49"])
  