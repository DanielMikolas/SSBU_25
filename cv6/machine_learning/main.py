import warnings

# Suppress specific FutureWarnings from scikit-learn
warnings.filterwarnings("ignore", category=FutureWarning)

from sklearn.linear_model import LogisticRegression
from data.data_handling_refactored import DatasetRefactored
from experiment.experiment import Experiment
from plotting.experiment_plotter import ExperimentPlotter
from utils.logger import Logger

from sklearn.neighbors import KNeighborsClassifier  # <- pridanie noveho modelu


def initialize_models_and_params():
    """
    Initializes models and their hyperparameter grids.

    Returns:
    - models: dict, dictionary of model instances.
    - param_grids: dict, dictionary of hyperparameter grids.
    """
    models = {
        "Logistic Regression": LogisticRegression(solver='liblinear'),

        "K-Nearest Neighbors": KNeighborsClassifier()   #  - Nový model pridaný do zoznamu
    }
    param_grids = {
        "Logistic Regression": {
            "C": [0.1, 1, 10],
            "max_iter": [10000]
        },
        "K-Nearest Neighbors": {  #  - Definované parametre pre Grid Search
            "n_neighbors": [3, 5, 7],
            "weights": ["uniform", "distance"],
            "metric": ["euclidean", "manhattan"]
        }
    }
    return models, param_grids


def run_experiment(dataset, models, param_grids, logger):
    """
    Runs the experiment with the given dataset, models, and hyperparameter grids.

    Parameters:
    - dataset: Dataset instance, the dataset to use.
    - models: dict, dictionary of model instances.
    - param_grids: dict, dictionary of hyperparameter grids.
    - logger: Logger instance, for logging messages.

    Returns:
    - experiment: Experiment instance, the experiment object.
    - results: DataFrame, the results of the experiment.
    """
    logger.info("Starting the experiment...")
    experiment = Experiment(models, param_grids, logger=logger)
    results = experiment.run(dataset.data, dataset.target)
    logger.info("Experiment completed successfully.")
    return experiment, results


def plot_results(experiment, results, logger):
    """
    Plots the results of the experiment.

    Parameters:
    - experiment: Experiment instance, the experiment object.
    - results: DataFrame, the results of the experiment.
    - logger: Logger instance, for logging messages.
    """
    logger.info("Generating plots for the experiment results...")
    plotter = ExperimentPlotter(n_replications=experiment.n_replications)
    plotter.plot_metric_density(results)

    plotter.plot_evaluation_metric_over_replications(
        experiment.results.groupby('model')['accuracy'].apply(list).to_dict(),
        'Accuracy per Replication and Average Accuracy', 'Accuracy')

    plotter.plot_evaluation_metric_over_replications(
        experiment.results.groupby('model')['precision'].apply(list).to_dict(),
        'Precision per Replication and Average Precision', 'Precision')

    plotter.plot_confusion_matrices(experiment.mean_conf_matrices)
    plotter.print_best_parameters(results)
    logger.info("Plots generated successfully.")


def main():
    """
    Main function to execute the model training and evaluation pipeline.

    Initializes the dataset, defines models and their parameter grids,
    and invokes the replication of model training and evaluation.
    """
    logger = Logger(log_file="outputs/application.log")
    logger.info("Application started.")

    dataset = DatasetRefactored()
    models, param_grids = initialize_models_and_params()

    experiment, results = run_experiment(dataset, models, param_grids, logger)

    plot_results(experiment, results, logger)

    logger.info("Application finished successfully.")


if __name__ == "__main__":
    main()
