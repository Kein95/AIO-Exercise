#46
class Solution:
    def calculate_mean(self, X):
        X = np.array(X)
        mean_value = np.mean(X)
        return float(mean_value)

#47
class Solution:
    def calculate_median(self, X):
        X = np.array(X)
        median_value = np.median(X)
        return float(median_value)

#48
class Solution:
    def calculate_variance_std(self, data):
        data = np.array(data)
        variance = np.var(data, ddof=0)
        std_dev = np.std(data, ddof=0)
        return (round(float(variance), 2), round(float(std_dev), 2))

#49
class Solution:
    def calculate_correlation_coefficient(self, X, Y):
        X = np.array(X)
        Y = np.array(Y)
        correlation_coefficient = np.corrcoef(X, Y)[0, 1]
        return float(round(correlation_coefficient, 2))

#50
class Solution:
    def calculate_dot_product(self, v, u):
        v = np.array(v)
        u = np.array(u)
        dot_product = np.dot(v, u)
        return dot_product

#51
class Solution:
    def calculate_matrix_product(self, A, B):
        A = np.array(A)
        B = np.array(B)

        if len(A[1]) != len(B):
            return -1

        C = np.dot(A, B)
        return C

#52
import math

class Solution:
    def calculate_eigenvalues_eigenvectors(self, A):
        def get_eigenvalues(matrix):
            a, b, c, d = matrix[0][0], matrix[0][1], matrix[1][0], matrix[1][1]
            trace = a + d
            determinant = a * d - b * c
            delta = trace**2 - 4 * determinant

            if delta < 0:
                raise ValueError("Eigenvalues are complex.")

            sqrt_delta = math.sqrt(delta)
            eigenvalue1 = (trace + sqrt_delta) / 2
            eigenvalue2 = (trace - sqrt_delta) / 2

            return eigenvalue1, eigenvalue2

        def get_eigenvectors(matrix, eigenvalue):
            a, b, c, d = matrix[0][0], matrix[0][1], matrix[1][0], matrix[1][1]
            if eigenvalue == a:
                x = -b
                y = a - eigenvalue
            else:
                x = -c
                y = d - eigenvalue

            norm = math.sqrt(x**2 + y**2)
            return [x / norm, y / norm]

        eigenvalues = get_eigenvalues(A)
        eigenvectors = [get_eigenvectors(A, eigenvalue) for eigenvalue in eigenvalues]

        return {eigenvalues[0]: eigenvectors[0], eigenvalues[1]: eigenvectors[1]}

#53
import math

class Solution:
    def calculate_cosine_similarity(self, x, y):
        if len(x) != len(y):
            return -1
        # Calculate dot product
        dot_product = sum(x_i * y_i for x_i, y_i in zip(x, y))

        # Calculate magnitudes
        magnitude_x = math.sqrt(sum(x_i ** 2 for x_i in x))
        magnitude_y = math.sqrt(sum(y_i ** 2 for y_i in y))

        # Avoiding division by 0
        if magnitude_x == 0 or magnitude_y == 0:
            return 0

        # Calculate cosine similarity
        cosine_similarity = dot_product / (magnitude_x * magnitude_y)

        return cosine_similarity