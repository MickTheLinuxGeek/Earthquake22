""" Intensity_dist_functions:  A group of helper functions to the display_intensity_dist_plot() function in
graph_functions module.

A group of functions to create each subplot of the intensity vs. distance plot.

Functions:
----------

    create_scatter_plot1()

    create_estimated1()

    create_estimated2()

    create_mean_binned()

    create_median()
"""

import logging
import numpy as np
import plotly.graph_objects as go
from plotly.graph_objects import Figure
from pandas import DataFrame

logger = logging.getLogger(__name__)


def create_scatter_plot1(dataset_df: DataFrame, intensity_dist_df: DataFrame, fig: Figure) -> Figure:
    """Function to create a scatter plot subplot of all responses with their hypo-central distance vs. cdi intensity.

    A helper function to display_intensity_dist_plot() to plot the hypo-central dist. vs. cdi intensity for each
    response to the earthquake event.

    Parameters:
    -----------
        dataset_df : A pandas dataframe
            A pandas dataframe containing all rows of class = scatterplot1
        intensity_dist_df : A pandas dataframe
            A pandas dataframe contains a row for each subplot; Used to get the subplots xlabel, ylabel, and title


    Returns:
    --------

        fig : A plotly graph_objects figure
            The corresponding subplot is added to the fig figure to build the intensity vs. distance graph.
    """

    logger.info("Entered create_scatter_plot1() function.")
    logger.debug("dataset_df parameter:\n %s", dataset_df)
    logger.debug("intensity_dist_df parameter:\n %s", intensity_dist_df)
    logger.debug("figure parameter:\n %s", fig)

    sct_plt_df = dataset_df.from_records(data=dataset_df.data)

    logger.debug("All data scatter plot dataframe:\n %s", sct_plt_df)

    x_i = list(sct_plt_df.x)
    y_i = list(sct_plt_df.y)
    ylabel = intensity_dist_df.ylabel[0]

    logger.debug("x coordinates for scatter plot:\n %s", x_i)
    logger.debug("y coordinates for scatter plot:\n %s", y_i)
    logger.debug("y axis label for scatter plot:\n %s", ylabel)

    fig.add_trace(
        go.Scatter(
            x=x_i,
            y=y_i,
            mode="markers",
            marker={"color": "rgb(148, 223, 234)", "size": 6},
            name="All Reported Data",
            customdata=x_i,
            text=y_i,
            hovertemplate="Hypocentral Dist. (km):  %{customdata}<br>" + "CDI:  %{text}",
        )
    )
    fig.update_yaxes(title_text=ylabel, range=[0, 10])
    fig.update_layout(
        yaxis={
            "tickvals": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "fixedrange": True,
        },
        title_text="Intensity Vs. Distance",
        plot_bgcolor="#FAEBD7",
        paper_bgcolor="#FFDEAD",
    )

    logger.debug("Figure structure returned:\n %s", fig)
    logger.info("Exited create_scatter_plot1() function.")

    return fig


def create_estimated1(dataset_df: DataFrame, fig: Figure) -> Figure:
    """Function to create a subplot containing estimated intensities for the reported magnitude and each distance
    compared to intensities derived from questionnaire responses.

    A helper function to display_intensity_dist_plot()
    The Intensity vs. Distance Plot shows the intensities derived from the questionnaire responses compared against
    estimates of the intensities for the reported magnitude and each distance using an Intensity Prediction Equation
    (IPE).

    Parameters:
    -----------
        dataset_df : A pandas dataframe
            A pandas dataframe containing all rows of class = estimated1

    Returns:
    --------

        fig : A plotly graph_objects figure
            The corresponding subplot is added to the fig figure to build the intensity vs. distance graph.
    """

    logger.info("Entered create_estimated1() function.")
    logger.debug("dataset_df parameter:\n %s", dataset_df)
    logger.debug("figure parameter:\n %s", fig)

    est_plt_df = dataset_df.from_records(data=dataset_df.data)

    logger.debug("Estimated1 data dataframe:\n %s", est_plt_df)

    x_i = list(est_plt_df.x)
    y_i = list(est_plt_df.y)
    name = dataset_df["legend"][0]

    logger.debug("x coordinates for scatter/line plot:\n %s", x_i)
    logger.debug("y coordinates for scatter/line plot:\n %s", y_i)
    logger.debug("Intensity Prediction Equation (IPE) used:\n %s", name)

    fig.add_trace(
        go.Scatter(
            x=x_i,
            y=y_i,
            name=name,
            mode="lines+markers",
            line={"color": "rgb(214, 86, 23)", "width": 2},
            marker={"color": "rgb(214, 86, 23)", "size": 6},
            customdata=x_i,
            text=y_i,
            hovertemplate="Hypocentral Dist. (km):  %{customdata}<br>" + "Estimated CDI:  %{text:.2f}",
        )
    )

    logger.debug("Figure structure returned:\n %s", fig)
    logger.info("Exited create_estimated1() function.")

    return fig


def create_estimated2(dataset_df: DataFrame, fig: Figure) -> Figure:
    """Function to create a subplot containing estimated intensities for the reported magnitude and each distance
    compared to intensities derived from questionnaire responses.

    A helper function to display_intensity_dist_plot()
    The Intensity vs. Distance Plot shows the intensities derived from the questionnaire responses compared against
    estimates of the intensities for the reported magnitude and each distance using an Intensity Prediction Equation
    (IPE).

    Parameters:
    -----------
        dataset_df : A pandas dataframe
            A pandas dataframe containing all rows of class = estimated2

    Returns:
    --------

        fig : A plotly graph_objects figure
            The corresponding subplot is added to the fig figure to build the intensity vs. distance graph.
    """

    logger.info("Entered create_estimated2() function.")
    logger.debug("dataset_df parameter:\n %s", dataset_df)
    logger.debug("figure parameter:\n %s", fig)

    est_plt_df = dataset_df.from_records(data=dataset_df.data)

    logger.debug("Estimated2 data dataframe:\n %s", est_plt_df)

    x_i = list(est_plt_df.x)
    y_i = list(est_plt_df.y)
    name = dataset_df["legend"][0]

    logger.debug("x coordinates for estimated2 plot:\n %s", x_i)
    logger.debug("y coordinates for estimated2 plot:\n %s", y_i)
    logger.debug("Intensity Prediction Equation (IPE) used:\n %s", name)

    fig.add_trace(
        go.Scatter(
            x=x_i,
            y=y_i,
            name=name,
            mode="lines+markers",
            line={"color": "orange", "width": 2},
            marker={"color": "orange", "size": 6},
            customdata=x_i,
            text=y_i,
            hovertemplate="Hypocentral Dist. (km):  %{customdata}<br>" + "Estimated CDI:  %{text:.2f}",
        )
    )

    logger.debug("Figure structure returned:\n %s", fig)
    logger.info("Exited create_estimated2() function.")

    return fig


def create_mean_binned(dataset_df: DataFrame, intensity_dist_df: DataFrame, fig: Figure) -> Figure:
    """Function to create a scatter plot subplot of the mean intensity +/- one STDEV at each distance bin.

    A helper function to display_intensity_dist_plot() to plot the mean intensity +/- one STDEV at each distance bin.

    Parameters:
    -----------
        dataset_df : A pandas dataframe
            A pandas dataframe containing all rows of class = binned
        intensity_dist_df : A pandas dataframe
            A pandas dataframe contains a row for each subplot; Used to get the subplots xlabel, ylabel, and title


    Returns:
    --------

        fig : A plotly graph_objects figure
            The corresponding subplot is added to the fig figure to build the intensity vs. distance graph.
    """

    logger.info("Entered create_mean_binned() function.")
    logger.debug("dataset_df parameter:\n %s", dataset_df)
    logger.debug("intensity_dist_df parameter:\n %s", intensity_dist_df)
    logger.debug("figure parameter:\n %s", fig)

    mean_plt_df = dataset_df.from_records(data=dataset_df.data)

    logger.debug("Mean binned dataframe:\n %s", mean_plt_df)

    x_i = mean_plt_df.x
    y_i = mean_plt_df.y
    yerr = mean_plt_df.stdev
    xlabel = intensity_dist_df.xlabel[0]
    ylabel = intensity_dist_df.ylabel[0]
    name = dataset_df["legend"][0]

    logger.debug("x coordinates for mean binned plot:\n %s", x_i)
    logger.debug("y coordinates for mean binned plot:\n %s", y_i)
    logger.debug("Standard deviation for mean binned plot:\n %s", yerr)
    logger.debug("y axis label for mean binned plot:\n %s", ylabel)
    logger.debug("x axis label for mean binned plot:\n %s", xlabel)
    logger.debug("Legend item name:\n %s", name)

    x_x = list(mean_plt_df.x)
    y_y = list(mean_plt_df.y)
    yyerr = list(mean_plt_df.stdev)

    n_k = np.empty(shape=(len(x_x), 3, 1))
    n_k[:, 0] = np.array(x_x).reshape(-1, 1)
    n_k[:, 1] = np.array(y_y).reshape(-1, 1)
    n_k[:, 2] = np.array(yyerr).reshape(-1, 1)

    logger.debug("Custom data array for hover (dist., CDI, Std. Dev.:\n %s", n_k)

    fig.add_trace(
        go.Scatter(
            x=x_i,
            y=y_i,
            name=name,
            error_y={
                "type": "data",
                "array": yerr,
                "color": "rgb(141, 145, 235)",
                "visible": True,
            },
            mode="markers",
            marker={"color": "rgb(141, 145, 235)", "size": 6},
            customdata=n_k,
            hovertemplate="Hypocentral Dist. (km):  %{customdata[0]}<br>"
            + "Mean CDI:  %{customdata[1]:.1f}<br>"
            + "Std. Dev. %{customdata[2]:.2f}",
        )
    )
    fig.update_xaxes(title_text=xlabel)
    fig.update_yaxes(title_text=ylabel)

    logger.debug("Figure structure returned:\n %s", fig)
    logger.info("Exited create_mean_binned() function.")

    return fig


def create_median(dataset_df: DataFrame, intensity_dist_df: DataFrame, fig: Figure) -> Figure:
    """Function to create a scatter plot subplot of the median intensity at each distance bin.

    A helper function to display_intensity_dist_plot() to plot the median intensity at each distance bin.

    Parameters:
    -----------
        dataset_df : A pandas dataframe
            A pandas dataframe containing all rows of class = median
        intensity_dist_df : A pandas dataframe
            A pandas dataframe contains a row for each subplot; Used to get the subplots xlabel, ylabel, and title


    Returns:
    --------

        fig : A plotly graph_objects figure
            The corresponding subplot is added to the fig figure to build the intensity vs. distance graph.
    """

    logger.info("Entered create_median() function.")
    logger.debug("dataset_df parameter:\n %s", dataset_df)
    logger.debug("intensity_dist_df parameter:\n %s", intensity_dist_df)
    logger.debug("figure parameter:\n %s", fig)

    median_plt_df = dataset_df.from_records(data=dataset_df.data)

    logger.debug("Median plot data dataframe:\n %s", median_plt_df)

    xii = median_plt_df.x  # Distance
    yii = median_plt_df.y  # CDI
    xlabel = intensity_dist_df.xlabel[0]
    name = dataset_df["legend"][0]

    logger.debug("Distance values for median plot:\n %s", xii)
    logger.debug("CDI values for median plot:\n %s", yii)
    logger.debug("x axis label for median plot:\n %s", xlabel)
    logger.debug("Legend item name:\n %s", name)

    fig.add_trace(
        go.Scatter(
            x=xii,
            y=yii,
            mode="markers",
            name=name,
            marker={"color": "rgb(254, 77, 85)", "size": 6},
            customdata=xii,
            text=yii,
            hovertemplate="Hypocentral Dist. (km):  %{customdata}<br>" + "Median CDI:  %{text}",
        )
    )
    fig.update_xaxes(title_text=xlabel, range=[0, max(xii)])

    logger.debug("Figure structure returned:\n %s", fig)
    logger.info("Exited create_median() function.")

    return fig
