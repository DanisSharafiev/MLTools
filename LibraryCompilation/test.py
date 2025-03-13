import numpy as np
from MLTools import PolynomialRegressionModel
from sklearn.metrics import mean_squared_error

def generate_data(n_samples=100):
    np.random.seed(42)
    X = np.random.uniform(-2, 2, (n_samples, 2))
    degrees = [2, 3]
    y = 2 * (X[:, 0] ** 2) + 3 * (X[:, 1] ** 3) + np.random.normal(0, 0.1, n_samples)
    return X, y, degrees

X, y_true, degrees = generate_data()
X_list = X.tolist()
y_list = [list(y_true)] 
degrees_list = [degrees]

model = PolynomialRegressionModel()
model.set_l1(0.01)
model.set_l2(0.01) 
model.train(X_list, y_list, degrees_list, 0.00005)

y_pred = model.predict(X_list)

mse = mean_squared_error(y_true, y_pred)
print(f"Mean Squared Error: {mse:.4f}")

print("\nПримеры предсказаний:")
for i in range(5):
    print(f"X: {X[i]}, True y: {y_true[i]:.4f}, Predicted y: {y_pred[i]:.4f}")
