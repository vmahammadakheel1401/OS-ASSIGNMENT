from flask import Flask, render_template, request

from os_assignment import fifo, lru, optimal

app = Flask(__name__)

DEFAULT_PAGES = "7 0 1 2 0 3 0 4 2 3 0 3 2 1 2 0 1 7 0 1"
DEFAULT_FRAMES = 3
BELADY_PAGES = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]


def parse_pages(raw: str):
    tokens = raw.replace(",", " ").split()
    if not tokens:
        raise ValueError("Please enter at least one page number.")
    pages = []
    for token in tokens:
        if not token.lstrip("-").isdigit():
            raise ValueError(f"Invalid page value: '{token}'. Use space-separated integers.")
        pages.append(int(token))
    return pages


def build_result(name, pages, frame_count, steps, faults):
    n = len(pages)
    hits = n - faults
    rows = []
    for index, (page, frames, fault, replaced) in enumerate(steps, start=1):
        padded_frames = list(frames) + ["-"] * (frame_count - len(frames))
        rows.append(
            {
                "step": index,
                "page": page,
                "frames": padded_frames,
                "result": "FAULT" if fault else "HIT",
                "replaced": replaced if replaced is not None else "-",
            }
        )
    return {
        "name": name,
        "rows": rows,
        "total": n,
        "faults": faults,
        "hits": hits,
        "fault_rate": (faults / n * 100) if n else 0,
        "hit_ratio": (hits / n * 100) if n else 0,
    }


@app.route("/", methods=["GET", "POST"])
def index():
    pages_input = DEFAULT_PAGES
    frames_input = str(DEFAULT_FRAMES)
    error = None
    results = []
    comparison = []
    best_algorithm = None
    belady_results = []

    if request.method == "POST":
        pages_input = request.form.get("pages", "").strip()
        frames_input = request.form.get("frames", "").strip()

    try:
        pages = parse_pages(pages_input)
        if not frames_input.isdigit() or int(frames_input) < 1:
            raise ValueError("Number of frames must be a positive integer.")
        frame_count = int(frames_input)

        for name, algorithm in (("FIFO", fifo), ("LRU", lru), ("OPTIMAL", optimal)):
            steps, faults = algorithm(pages, frame_count)
            result = build_result(name, pages, frame_count, steps, faults)
            results.append(result)
            comparison.append(result)

        best_algorithm = min(comparison, key=lambda item: item["faults"])["name"]

        for frame_count_check in (3, 4):
            _, belady_faults = fifo(BELADY_PAGES, frame_count_check)
            belady_results.append({"frames": frame_count_check, "faults": belady_faults})
    except ValueError as exc:
        error = str(exc)
        results = []
        comparison = []
        best_algorithm = None
        belady_results = []

    return render_template(
        "index.html",
        pages_input=pages_input,
        frames_input=frames_input,
        error=error,
        results=results,
        comparison=comparison,
        best_algorithm=best_algorithm,
        belady_pages=BELADY_PAGES,
        belady_results=belady_results,
    )


if __name__ == "__main__":
    app.run(debug=True)
