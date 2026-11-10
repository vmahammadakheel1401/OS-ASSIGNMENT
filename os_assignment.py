"""
Page Replacement Simulator (FIFO, LRU, Optimal)
Operating Systems (1BAI304) - AAT, Problem Statement 7
"""

from collections import deque


def fifo(pages, frame_count):
    frames = []
    queue = deque()          # arrival order of pages in memory
    steps, faults = [], 0
    for page in pages:
        replaced = None
        if page in frames:
            fault = False
        else:
            fault = True
            faults += 1
            if len(frames) < frame_count:
                frames.append(page)
            else:
                replaced = queue.popleft()          # oldest page out
                frames[frames.index(replaced)] = page
            queue.append(page)
        steps.append((page, list(frames), fault, replaced))
    return steps, faults


def lru(pages, frame_count):
    frames = []
    last_used = {}           # page -> index of most recent use
    steps, faults = [], 0
    for i, page in enumerate(pages):
        replaced = None
        if page in frames:
            fault = False
        else:
            fault = True
            faults += 1
            if len(frames) < frame_count:
                frames.append(page)
            else:
                replaced = min(frames, key=lambda p: last_used[p])  # least recently used
                frames[frames.index(replaced)] = page
        last_used[page] = i
        steps.append((page, list(frames), fault, replaced))
    return steps, faults


def optimal(pages, frame_count):
    frames = []
    steps, faults = [], 0
    for i, page in enumerate(pages):
        replaced = None
        if page in frames:
            fault = False
        else:
            fault = True
            faults += 1
            if len(frames) < frame_count:
                frames.append(page)
            else:
                # choose the page whose next use is farthest in the future
                def next_use(p):
                    future = pages[i + 1:]
                    return future.index(p) if p in future else float("inf")
                replaced = max(frames, key=next_use)
                frames[frames.index(replaced)] = page
        steps.append((page, list(frames), fault, replaced))
    return steps, faults


def display(name, pages, frame_count, steps, faults):
    n = len(pages)
    hits = n - faults
    print("=" * 62)
    print(f" {name} PAGE REPLACEMENT   (frames = {frame_count})")
    print("=" * 62)
    print(f"{'Step':<5}{'Page':<6}{'Frames':<20}{'Result':<8}{'Replaced'}")
    print("-" * 62)
    for i, (page, frames, fault, replaced) in enumerate(steps, 1):
        shown = " ".join(f"{f:>2}" for f in frames) + "  " * (frame_count - len(frames))
        res = "FAULT" if fault else "HIT"
        rep = str(replaced) if replaced is not None else "-"
        print(f"{i:<5}{page:<6}{shown:<20}{res:<8}{rep}")
    print("-" * 62)
    print(f"Total page requests : {n}")
    print(f"Page faults         : {faults}")
    print(f"Page hits           : {hits}")
    print(f"Page fault rate     : {faults / n * 100:.2f}%")
    print(f"Hit ratio (efficiency): {hits / n * 100:.2f}%")
    print()


def main():
    print("PAGE REPLACEMENT ALGORITHM SIMULATOR")
    raw = input("Enter page reference string (space separated)\n"
                "[press Enter for default]: ").strip()
    if raw:
        pages = list(map(int, raw.split()))
    else:
        pages = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
    raw = input("Enter number of frames [default 3]: ").strip()
    frame_count = int(raw) if raw else 3
    print()
    print("Page reference string:", *pages)
    print("Number of frames     :", frame_count)
    print()

    results = {}
    for name, algo in (("FIFO", fifo), ("LRU", lru), ("OPTIMAL", optimal)):
        steps, faults = algo(pages, frame_count)
        display(name, pages, frame_count, steps, faults)
        results[name] = faults

    n = len(pages)
    print("=" * 62)
    print(" COMPARISON SUMMARY")
    print("=" * 62)
    print(f"{'Algorithm':<12}{'Faults':<10}{'Hits':<8}{'Fault rate':<13}{'Hit ratio'}")
    for name, f in results.items():
        print(f"{name:<12}{f:<10}{n - f:<8}{f / n * 100:<13.2f}{(n - f) / n * 100:.2f}%")
    best = min(results, key=results.get)
    print(f"\nBest performance (fewest faults): {best}")

    print("\nBelady's anomaly check (FIFO) on 1 2 3 4 1 2 5 1 2 3 4 5:")
    belady = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
    for fc in (3, 4):
        print(f"  frames = {fc} -> faults = {fifo(belady, fc)[1]}")


if __name__ == "__main__":
    main()