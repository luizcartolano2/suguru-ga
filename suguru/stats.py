""" Module for generating statistics and plots from solving times and cells to fill.

"""
import os
import matplotlib.pyplot as plt
import seaborn as sns


class Stats:
    """
    Class for generating statistics and plots from solving times and cells to fill.
    It creates various plots to visualize the distribution of solving times,
    the relationship between solving time and number of cells to fill, and more.

    Attributes:
        times (list): List of solving times for each puzzle.
        cells_to_fill (list): List of the number of cells to fill for each puzzle.
        solver_name (str): Name of the solver used.
        output_dir (str): Directory where plots will be saved.
    """
    def __init__(self, times, cells_to_fill, solver_name, output_dir="outputs/stats"):
        self.times = times
        self.cells_to_fill = cells_to_fill
        self.solver_name = solver_name
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def plot_all(self):
        """
        Generate all plots for the statistics.
        :return: all plots saved in the output directory.
        """
        self.__plot_histogram()
        self.__plot_boxplot()
        self.__plot_time_per_puzzle()
        self.__plot_time_per_filled_cell()
        self.__plot_total_time_vs_cells_to_fill()

    def __plot_histogram(self):
        """
        Generate a histogram of solving times with a kernel density estimate (KDE).
        :return: a histogram plot saved in the output directory.
        """
        plt.figure(figsize=(8, 5))
        sns.histplot(self.times, bins=20, kde=True)
        plt.title("Distribution of Solving Times")
        plt.xlabel("Time (seconds)")
        plt.ylabel("Number of Puzzles")
        plt.tight_layout()
        self.__save("solving_time_histogram.png")

    def __plot_boxplot(self):
        """
        Generate a boxplot of solving times to visualize the distribution and identify outliers.
        :return: a boxplot saved in the output directory.
        """
        plt.figure(figsize=(6, 4))
        sns.boxplot(x=self.times)
        plt.title("Boxplot of Solving Times")
        plt.xlabel("Time (seconds)")
        plt.tight_layout()
        self.__save("solving_time_boxplot.png")

    def __plot_time_per_puzzle(self):
        """
        Generate a line plot showing the solving time for each puzzle.
        :return: a line plot saved in the output directory.
        """
        plt.figure(figsize=(10, 5))
        plt.plot(range(1, len(self.times) + 1), self.times, marker='o')
        plt.title("Solving Time per Puzzle")
        plt.xlabel("Puzzle Index")
        plt.ylabel("Time (seconds)")
        plt.grid(True)
        plt.tight_layout()
        self.__save("solving_time_per_puzzle.png")

    def __plot_time_per_filled_cell(self):
        """
        Generate a plot showing the average solving time per filled cell for each puzzle.
        :return: a plot saved in the output directory.
        """
        time_per_cell = [t / c for t, c in zip(self.times, self.cells_to_fill) if c > 0]
        plt.figure(figsize=(8, 5))
        plt.plot(range(1, len(time_per_cell) + 1), time_per_cell, marker='x')
        plt.title("Solving Time per Filled Cell")
        plt.xlabel("Puzzle Index")
        plt.ylabel("Time per Cell (seconds)")
        plt.grid(True)
        plt.tight_layout()
        self.__save("time_per_cell.png")

    def __plot_total_time_vs_cells_to_fill(self):
        """
        Generate a scatter plot showing the relationship between total solving time and number of cells to fill.
        :return: a scatter plot saved in the output directory.
        """
        plt.figure(figsize=(8, 6))
        sns.scatterplot(x=self.cells_to_fill, y=self.times)
        sns.regplot(x=self.cells_to_fill, y=self.times, scatter=False, color='red', marker='--')
        plt.title("Solving Time vs Number of Cells to Fill")
        plt.xlabel("Number of Cells to Fill")
        plt.ylabel("Total Solving Time (seconds)")
        plt.grid(True)
        plt.tight_layout()
        self.__save("solving_time_vs_missing_cells.png")

    def __save(self, filename, display=False):
        """
        Save the current plot to the output directory or display it.
        :param filename: Name of the file to save the plot as.
        :param display: If True, display the plot instead of saving it.
        :return: a plot saved in the output directory or displayed.
        """
        if display:
            plt.show()
        else:
            plt.savefig(os.path.join(self.output_dir, f'{self.solver_name}-{filename}'))
        plt.close()
