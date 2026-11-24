# Simple FIFO Page Replacement Program
# Input: page reference string and number of frames
# Output: step-by-step page replacement, total page faults, and efficiency

def fifo_page_replacement(pages, frame_count):
    frames = []
    queue = []
    page_faults = 0
    steps = []

    for page in pages:
        if page in frames:
            steps.append((page, frames.copy(), "HIT", "-"))
        else:
            page_faults += 1
            if len(frames) < frame_count:
                frames.append(page)
                queue.append(page)
                steps.append((page, frames.copy(), "FAULT", "-"))
            else:
                replaced_page = queue.pop(0)
                index = frames.index(replaced_page)
                frames[index] = page
                queue.append(page)
                steps.append((page, frames.copy(), "FAULT", replaced_page))

    return steps, page_faults


def main():
    print("FIFO Page Replacement Algorithm")
    print()

    raw_pages = input("Enter page reference string (space separated): ").strip()
    if raw_pages == "":
        pages = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2]
    else:
        pages = [int(x) for x in raw_pages.split()]

    raw_frames = input("Enter number of frames: ").strip()
    if raw_frames == "":
        frame_count = 3
    else:
        frame_count = int(raw_frames)

    steps, page_faults = fifo_page_replacement(pages, frame_count)
    total_pages = len(pages)
    page_hits = total_pages - page_faults
    hit_ratio = (page_hits / total_pages) * 100
    fault_rate = (page_faults / total_pages) * 100

    print()
    print("Page Reference String:", pages)
    print("Number of Frames:", frame_count)
    print()
    print(f"{'Step':<6}{'Page':<8}{'Frames':<20}{'Result':<10}{'Replaced'}")
    print("-" * 55)

    for i, (page, frame_state, result, replaced) in enumerate(steps, start=1):
        frame_text = " ".join(str(p) for p in frame_state)
        print(f"{i:<6}{page:<8}{frame_text:<20}{result:<10}{replaced}")

    print("-" * 55)
    print("Total Page Requests:", total_pages)
    print("Total Page Faults:", page_faults)
    print("Total Page Hits:", page_hits)
    print(f"Page Fault Rate: {fault_rate:.2f}%")
    print(f"Hit Ratio (Efficiency): {hit_ratio:.2f}%")


if __name__ == "__main__":
    main()
