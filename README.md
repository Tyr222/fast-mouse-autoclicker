# 🖱️ Fast Mouse - Auto Clicker

> Auto Clicker made in Python with the help of AI.

A simple, lightweight, and functional Auto Clicker application. This project marked my transition from creating sequential automation scripts to developing a complete software with a Graphical User Interface (GUI) and concurrent execution.

## 🤝 About the Development

The construction of this project was divided into two clear stages:
* **Manual Base:** The core logic of the script was built 100% manually by me, consisting of a functional auto clicker using the `pyautogui` library with a basic *start/stop* system.
* **Scaling with AI:** To transform this simple script into a real desktop application, I used Artificial Intelligence assistance. With AI, I implemented the Graphical User Interface (Tkinter), resolved concurrency conflicts with *threads*, and added global *listeners* (Pynput) for the *hotkey* system.

## 🚀 Features

* **Precise Intervals:** Set the exact time between clicks in hours, minutes, seconds, or milliseconds.
* **Pick Location:** Click a button, minimize the screen, and capture the exact `(X, Y)` coordinate where the automated click should happen.
* **Global Hotkey:** Start and stop the clicker using a customizable key (like `F6`). The shortcut works at the operating system level, meaning it can be activated even with the app minimized or a full-screen game open.

## 🛠️ Technologies and Libraries

* **Python 3:** Main application logic.
* **Tkinter:** Graphical User Interface (GUI) construction and main loop management.
* **Pynput:** Creation of *listeners* to capture mouse and keyboard events in the background.
* **Threading (Native):** Management of multiple execution threads.
* **PyAutoGUI:** Execution of hardware commands (clicks).

## 🧠 Challenges and Learnings

The evolution of this tool served as a practical lab to understand the difference between standard *scripts* and continuous *software*. The main concepts absorbed during the implementation of the GUI and Hotkeys were:

1.  **Event-Driven Programming:** The app does not run linearly. It was necessary to understand the use of custom Virtual Events (like `<<LocationPicked>>`) to force the Tkinter interface to update data on the screen instantly after a mouse click, without freezing the `mainloop()` queue.
2.  **Concurrency (Threads):** To ensure the application interface remained responsive while waiting for keyboard shortcuts, the *listeners* had to be isolated in secondary *threads* (`daemon=True`), separating hardware control from visual execution.

## ⚙️ How to run it locally

1. Clone this repository:
   `git clone https://github.com/YOUR_USER/YOUR_REPOSITORY.git`
2. Install the required dependencies:
   `pip install pyautogui pynput`
3. Run the main file:
   `python auto_clicker.py`
