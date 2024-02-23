from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt

def polynomial_regression():
    # Prompt user to input X and y
    x_metric = input("Please input the independent variable (COST, REVENUE, or ORDERS): ").upper()
    y_metric = input("Please input the dependent variable (COST, REVENUE, or ORDERS): ").upper()

    # Check if the user has input the same metric for both X and y
    if x_metric == y_metric:
        print("Warning: The same metric has been chosen for both X and y. This may not be appropriate for regression modeling.")
    
    # Load data from DataFrame df
    X = np.array(df[x_metric]).reshape(-1, 1)
    y = np.array(df[y_metric])

    # Polynomial regression
    poly = PolynomialFeatures(degree=2)
    X_poly = poly.fit_transform(X)

    model = LinearRegression()
    model.fit(X_poly, y)

    y_pred = model.predict(X_poly)

    # Plotting
    plt.scatter(X, y, color='blue', label='Actual Data Points')
    plt.plot(X, y_pred, color='red', label='Polynomial Regression')
    plt.xlabel(x_metric)
    plt.ylabel(y_metric)

    # Set the x-axis tick labels to normal number format
    plt.ticklabel_format(style='plain', axis='x')

    # Find the index of the maximum revenue value
    max_yield_index = np.argmax(y_pred)

    # Plot a vertical line at the point of maximum yield
    plt.axvline(x=X[max_yield_index][0], color='green', linestyle='--', label='Max Yield Point')

    rounded_x = round(X[max_yield_index][0], 2)
    plt.text(rounded_x, y_pred[max_yield_index], f'({rounded_x}, {y_pred[max_yield_index]:.2f})', ha='left', va='bottom', bbox=dict(facecolor='yellow', alpha=0.8))

    # Show the plot
    plt.legend(loc='upper left', fontsize='small')
    plt.show()

# Call the function
polynomial_regression()
