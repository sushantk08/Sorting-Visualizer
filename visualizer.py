import tkinter as tk


def draw_data(data, canvas, colors):
    canvas.delete("all")
    canvas_width = 600
    canvas_height = 400
    bar_width = canvas_width / (len(data) + 5)  # Adjust bar width
    max_height = max(data)
    for i, height in enumerate(data):
        # Scale the height to make the bars taller
        x0 = i * bar_width + 20
        y0 = canvas_height - (height / max_height * 300)  # Adjust bar height scaling
        x1 = (i + 1) * bar_width + 20
        y1 = canvas_height
        canvas.create_rectangle(x0, y0, x1, y1, fill=colors[i])
    root.update_idletasks()

# Bubble sort generator with visualization
def bubble_sort_gen(data, canvas):
    for i in range(len(data) - 1):
        for j in range(len(data) - 1 - i):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
            draw_data(data, canvas, ['red' if x == j or x == j + 1 else 'lightblue' for x in range(len(data))])
            yield

# Selection sort generator with visualization
def selection_sort_gen(data, canvas):
    for i in range(len(data)):
        min_idx = i
        for j in range(i+1, len(data)):
            if data[j] < data[min_idx]:
                min_idx = j
        data[i], data[min_idx] = data[min_idx], data[i]
        draw_data(data, canvas, ['green' if x == i or x == min_idx else 'lightblue' for x in range(len(data))])
        yield

# Merge Sort generator with visualization
def merge_sort_gen(data, canvas):
    yield from merge_sort_algo_gen(data, 0, len(data) - 1, canvas)

def merge_sort_algo_gen(data, left, right, canvas):
    if left < right:
        mid = (left + right) // 2
        yield from merge_sort_algo_gen(data, left, mid, canvas)
        yield from merge_sort_algo_gen(data, mid + 1, right, canvas)
        yield from merge_gen(data, left, mid, right, canvas)

def merge_gen(data, left, mid, right, canvas):
    n1 = mid - left + 1
    n2 = right - mid
    left_arr = data[left:left + n1]
    right_arr = data[mid + 1:mid + 1 + n2]

    i, j, k = 0, 0, left
    while i < n1 and j < n2:
        if left_arr[i] <= right_arr[j]:
            data[k] = left_arr[i]
            i += 1
        else:
            data[k] = right_arr[j]
            j += 1
        k += 1
        draw_data(data, canvas, ['orange' if left <= x <= right else 'lightblue' for x in range(len(data))])
        yield

    while i < n1:
        data[k] = left_arr[i]
        i += 1
        k += 1
        draw_data(data, canvas, ['orange' if left <= x <= right else 'lightblue' for x in range(len(data))])
        yield

    while j < n2:
        data[k] = right_arr[j]
        j += 1
        k += 1
        draw_data(data, canvas, ['orange' if left <= x <= right else 'lightblue' for x in range(len(data))])
        yield


def start_sorting():
    global sort_generator
    selected_algorithm = algo_menu.get()
    if selected_algorithm == "Bubble Sort":
        sort_generator = bubble_sort_gen(data, canvas)
    elif selected_algorithm == "Selection Sort":
        sort_generator = selection_sort_gen(data, canvas)
    elif selected_algorithm == "Merge Sort":
        sort_generator = merge_sort_gen(data, canvas)


def next_step():
    try:
        next(sort_generator)
    except StopIteration:
        pass

def reset():
    global data, sort_generator
    user_input = input_entry.get()
    try:
        data = list(map(int, user_input.split(',')))  # Convert input string to a list of integers
        draw_data(data, canvas, ['lightblue' for _ in range(len(data))])
        sort_generator = None
    except ValueError:
        error_label.config(text="Invalid input! Please enter comma-separated integers.")


root = tk.Tk()
root.title("Sorting Visualizer")
root.geometry("700x500")


canvas = tk.Canvas(root, width=600, height=400, bg="white")
canvas.grid(row=0, column=0, padx=10, pady=10)


frame = tk.Frame(root)
frame.grid(row=1, column=0, padx=10, pady=10)


input_label = tk.Label(frame, text="Enter comma-separated integers:")
input_label.grid(row=0, column=0, padx=5)
input_entry = tk.Entry(frame)
input_entry.grid(row=0, column=1, padx=5)


algo_menu = tk.StringVar(root)
algo_menu.set("Bubble Sort")  # Default algorithm
dropdown = tk.OptionMenu(frame, algo_menu, "Bubble Sort", "Selection Sort", "Merge Sort")
dropdown.grid(row=0, column=2, padx=10)


start_button = tk.Button(frame, text="Start Sorting", command=start_sorting)
start_button.grid(row=0, column=3, padx=10)


next_button = tk.Button(frame, text="Next Step", command=next_step)
next_button.grid(row=0, column=4, padx=10)


reset_button = tk.Button(frame, text="Reset", command=reset)
reset_button.grid(row=0, column=5, padx=10)


error_label = tk.Label(frame, text="", fg="red")
error_label.grid(row=1, columnspan=6)


data = []
sort_generator = None


root.mainloop()
