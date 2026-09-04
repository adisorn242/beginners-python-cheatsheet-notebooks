# Beginner's Python Cheat Sheet — Notebook Course

A 13-chapter Jupyter notebook course generated from the [Python Crash Course Cheat Sheets](https://ehmatthes.github.io/pcc/) by Eric Matthes, updated for modern Python and Google Colab.

## Files

| Chapter | Notebook (.ipynb) | Local script (.py) |
|---|---|---|
| 01 | Chapter01_Python_Basics_Variables_and_Strings.ipynb | — |
| 02 | Chapter02_Lists_and_Tuples.ipynb | — |
| 03 | Chapter03_If_Statements_and_While_Loops.ipynb | — |
| 04 | Chapter04_Dictionaries.ipynb | — |
| 05 | Chapter05_Functions.ipynb | — |
| 06 | Chapter06_Classes.ipynb | — |
| 07 | Chapter07_Files_and_Exceptions.ipynb | — |
| 08 | Chapter08_Testing_Your_Code.ipynb | — |
| 09 | Chapter09_Pygame_Basics.ipynb | Chapter09_Pygame_Basics.py |
| 10 | Chapter10_Data_Visualization_Matplotlib.ipynb | — |
| 11 | Chapter11_Data_Visualization_Pygal.ipynb | — |
| 12 | Chapter12_Django_Web_Apps_Part1.ipynb | Chapter12_Django_Web_Apps_Part1.py |
| 13 | Chapter13_Django_Web_Apps_Part2_User_Accounts.ipynb | Chapter13_Django_Web_Apps_Part2_User_Accounts.py |

## Where each chapter runs

### Runs the same on Google Colab and local Jupyter — Chapters 1–8, 10, 11

These notebooks are fully self-contained. Every cell executes and produces its real output
(printed text, plots, charts) in either environment — just open the `.ipynb` and run all cells.

### Runs on both, but the full experience needs local — Chapters 9, 12, 13

The code in these notebooks runs without errors on Colab, but Colab has no display and no
`localhost`, so part of the result can't actually be *seen* there:

- **Chapter 9 (Pygame):** the notebook runs headless (no visible game window) on Colab. Run
  `Chapter09_Pygame_Basics.py` on your own computer to see a real game window.
- **Chapters 12–13 (Django):** the notebooks build a complete, working Django project and pass
  `manage.py check` on Colab, but there's no browser access to `localhost:8000` from there. Run
  `Chapter12_Django_Web_Apps_Part1.py` / `Chapter13_Django_Web_Apps_Part2_User_Accounts.py`
  locally, then `python manage.py runserver` and visit `http://localhost:8000/` to see the site.

## Running on Google Colab

1. Upload the `.ipynb` file to [Google Colab](https://colab.research.google.com/), or open it
   directly from GitHub (File > Open notebook > GitHub).
2. Run cells top to bottom. Chapters 9 and 11 install their own dependencies (`pygame`,
   `pygal`) via `!pip install` cells.

## Running locally

1. Install Python 3.10+ and Jupyter (`pip install notebook`) to run the `.ipynb` files, or just
   use `python` directly for the `.py` scripts.
2. For the `.py` scripts, install what each chapter needs first:
   - Chapter 9: `pip install pygame`
   - Chapters 12–13: `pip install django`
3. Run a script with `python <filename>.py`.

## What was modernized from the original cheat sheet

- `+`/`.format()` string building replaced with f-strings.
- `collections.OrderedDict` dropped — regular dicts keep insertion order since Python 3.7.
- Matplotlib's deprecated `plt.axes()` calls replaced with `plt.subplots()`.
- Pygal's world-map add-on wrapped in a try/except, since that package can be unreliable to
  install.
