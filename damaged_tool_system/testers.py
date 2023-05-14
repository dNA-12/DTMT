import matplotlib.pyplot as plt
import mplcursors

def on_plot_hover(sel):
    if sel.artist == scatter:
        sel.annotation.set_text(f"Point {sel.target.index}: {sel.target}")
    elif sel.artist == line:
        sel.annotation.set_text("This is a line")

def main():
    fig, ax = plt.subplots()
    data = [(2, 3), (4, 5), (6, 7), (8, 9)]

    x, y = zip(*data)
    scatter = ax.scatter(x, y, marker='o', color='b')
    line, = ax.plot(x, y, color='b', linestyle='-', alpha=0.5)

    cursor = mplcursors.cursor(hover=True)
    cursor.connect("add", on_plot_hover)

    plt.show()

if __name__ == "__main__":
    main()
