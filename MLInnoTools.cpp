// g++ -O3 -Wall -shared -std=c++17 -fPIC $(python3-config --includes) MLInnoTools.cpp -o ml_inno_tools$(python3-config --extension-suffix)

#include <type_traits>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <iostream>
#include <string>
#include <vector>

namespace py = pybind11;

class DebugHelper {
public:
    static void print_matrix(std::vector<std::vector<std::optional<float>>>& x) {
        for (int i = 0; i < x.size(); i++)
        {
            for (int j = 0; j < x[0].size(); j++)
            {
                if (x[i][j]) { 
                std::cout << std::to_string(x[i][j].value()) + " ";
            } else {
                std::cout << "N ";
            }
            }
            py::print();
        }
    }
    static void print_shape(std::vector<std::vector<std::optional<float>>>& x) {
        if (x.size() == 0){
            std::cout << "0, 0\n";
        } else {
            std::cout << std::to_string(x.size()) + " " + std::to_string(x[0].size()) << "\n";
        }
    }
    static void pin() {
        std::cout << "==== PIN ====\n";
    }
};

class Validator {
public:
    static bool isNumericValue(py::object value) {
        return py::isinstance<py::float_>(value) || py::isinstance<py::int_>(value);
    }
    static bool isNullValue(py::object value) {
        auto pd = py::module_::import("pandas");
        auto isna = pd.attr("isna");
        py::object pd_NA = pd.attr("NA");
        return py::isinstance<py::none>(value) || std::isnan(value.cast<double>())
            || isna(value).cast<bool>();
    }
};

class MLMath {
public:
    static std::vector<float> get_shape(std::vector<std::vector<std::optional<float>>>& x) {
        std::vector<float> result;
        result.push_back(x.size());
        if (x.size() != 0) {
            result.push_back(x[0].size());
        }
        return result;
    }
    static void check_shapes_for_prediction(std::vector<std::vector<std::optional<float>>>& x, 
        std::vector<std::vector<std::optional<float>>>& y) {
        if (x.size() == 0) {
            throw std::invalid_argument("Matrix is empty.");
        }
        if (x[0].size() != y.size()){
            throw std::invalid_argument("Matrices shapes for model are not compatible for prediction.");
        }
    }
    static void check_shapes_for_training(std::vector<std::vector<std::optional<float>>>& x, 
        std::vector<std::vector<std::optional<float>>>& y) {
            if (x.size() == 0) {
            throw std::invalid_argument("Matrix is empty.");
        }
        if (x.size() != y[0].size()){
            throw std::invalid_argument("Matrices shapes for model are not compatible for training.");
        }
        }
    static void check_correctness_of_matrix(std::vector<std::vector<std::optional<float>>>& x) {
        if (x.size() == 0 && x[0].size() == 0){
            throw std::invalid_argument("Matrix is empty.");
        }
        int numbersInRow = -1;
        for (int i = 0; i < x.size(); i++) {
            if (numbersInRow != -1) { // Checking that number of elements in each row is equal 
                    if (numbersInRow != x[i].size()) {
                        throw std::invalid_argument("Matrix is not full.");
                    }
                } else {
                    numbersInRow = x[i].size();
                }
            for (int j = 0; j < x[i].size(); j++)
            {
                if (x[i][j] == std::nullopt) {
                    DebugHelper::print_matrix(x);
                    throw std::invalid_argument
                    ("Values presented in matrix must not be null. Row " + std::to_string(i) + ", Column " + std::to_string(j));
                }
            }
        }
    }
    static std::vector<std::vector<std::optional<float>>> product(std::vector<std::vector<std::optional<float>>>& x, 
    std::vector<std::vector<std::optional<float>>>& y) {
        std::vector<std::vector<std::optional<float>>> result;
        MLMath::check_correctness_of_matrix(x);
        MLMath::check_correctness_of_matrix(y);
        int x_x = x[0].size();
        int x_y = x.size();
        int y_x = y[0].size();
        int y_y = y.size();
        if (x_x != y_y) {
            throw std::invalid_argument("Operation is impossible, matrices are not compatible for multiplication.");
        }
        for (int i = 0; i < x_y; i++)
        {
            std::vector<std::optional<float>> row;
            for (int j = 0; j < y_x; j++)
            {
                float sum = 0;
                for (int k = 0; k < x_x; k++)
                {
                    sum += x[i][k].value() * y[k][j].value();
                }
                row.emplace_back(sum);
            }
            result.push_back(row);
        }
        return result;
    }
    static std::vector<std::vector<std::optional<float>>> transpose(std::vector<std::vector<std::optional<float>>>& x) {
        MLMath::check_correctness_of_matrix(x);
        std::vector<std::vector<std::optional<float>>> result;
        for (int i = 0; i < x[0].size(); i++)
        {
            std::vector<std::optional<float>> row;
            for (int j = 0; j < x.size(); j++)
            {
                row.push_back(x[j][i]);
            }
            result.push_back(row);
        }
        return result;
    }
    static float sign(float num) {
        if (num > 0) {
            return 1;
        }
        if (num < 0) {
            return -1;
        }
        if (num == 0) {
            return 0;
        }
    }
};

class Parser {
public:
    static void convert_to_2D_vector(py::object obj, std::vector<std::vector<std::optional<float>>>& data) {
        if (!py::isinstance<py::list>(obj)) {
            throw std::invalid_argument("Input must be list.");
        }
        int numberOfItemsInRow = -1;
        py::list outList = obj.cast<py::list>();
        for (auto pyObj : outList) {
            if (!py::isinstance<py::list>(pyObj)) {
                throw std::invalid_argument("Every element in the inputs list must be a list.");
            }
            if (numberOfItemsInRow != -1) {
                if (py::len(pyObj) != numberOfItemsInRow) {
                    throw std::invalid_argument("Number of items in a row is different.");
                }
            } else {
                numberOfItemsInRow = py::len(pyObj);
            }
            py::list pyList = pyObj.cast<py::list>();
            if (py::len(pyList) == 0) {
                continue;
            }
            std::vector<std::optional<float>> tempRow;
            for (auto value: pyList) {
                py::object pyObjValue = py::reinterpret_borrow<py::object>(value);
                if (!Validator::isNumericValue(pyObjValue)) { // Takes only integers, floats, and empty variables
                    throw std::invalid_argument("Value presented in a list is not float either integer.");
                }
                if (Validator::isNullValue(pyObjValue)) {
                    tempRow.push_back(std::nullopt);
                } else {
                    tempRow.push_back(value.cast<float>());  
                }
            }
            data.push_back(tempRow);
        }
    }
};  

class RegressionModel{
public:
    RegressionModel(){}

    virtual void train(const py::object X, const py::object Y, float learnRate) = 0;
    
    virtual std::vector<float> predict(const py::object X) = 0;

    virtual float predict_cpp(std::vector<std::vector<std::optional<float>>>& X) = 0;

protected:
    std::vector<std::vector<std::optional<float>>> weights;
    float shift;
    bool isTrained;
};

class LinearRegressionModel : public RegressionModel {
protected:
    std::vector<std::vector<std::optional<float>>> weights;
    float shift;
    bool isTrained;
    float l1;
    float l2;
public:
    LinearRegressionModel() : RegressionModel() {
        isTrained = false;
        shift = 0.0f;
        l1 = 0.0f;
        l2 = 0.0f;
    }

    void set_l1(float num) {
        l1 = num;
    }

    void set_l2(float num) {
        l2 = num;
    }

    void train(const py::object X, const py::object Y, float learnRate) override {
        weights.clear();
        std::vector<std::vector<std::optional<float>>> data;
        std::vector<std::vector<std::optional<float>>> target;
        Parser::convert_to_2D_vector(X, data);
        Parser::convert_to_2D_vector(Y, target); 
        MLMath::check_correctness_of_matrix(data);
        MLMath::check_correctness_of_matrix(target);
        MLMath::check_shapes_for_training(data, target);
        for (int j = 0; j < data[0].size(); j++) {
            std::vector<std::optional<float>> tempRow;
            tempRow.push_back(0);
            weights.push_back(tempRow);
        }
        for (int i = 0; i < 1000; i++)
        {
            iterate_updating_weights(data, target, learnRate);
            for (int j = 0; j < weights.size(); j++)
            {
                std::cout << std::to_string(weights[j][0].value()) + " ";
            }
            std::cout << std::endl;
        }
    }

    float predict_cpp(std::vector<std::vector<std::optional<float>>>& X) override {
        MLMath::check_correctness_of_matrix(X);
        if (weights.size() == 0) {
            throw std::invalid_argument("Model is not trained.");
        } 
        MLMath::check_shapes_for_prediction(X, weights);
        std::vector<std::vector<std::optional<float>>> preResult = MLMath::product(X, weights);
        std::optional<float> result = preResult[0][0];
        float result_value = result.value() + shift;
        return result_value;
    }

    // predicts according to saved values
    std::vector<float> predict(const py::object X) override {
        std::vector<std::vector<std::optional<float>>> data;
        Parser::convert_to_2D_vector(X, data);
        std::vector<float> result;
        for (int i = 0; i < data.size(); i++)
        {
            std::vector<std::vector<std::optional<float>>> temp;
            temp.push_back(data[i]);
            result.push_back(LinearRegressionModel::predict_cpp(temp));
        }
        
        return result;
    }

private:
    void iterate_updating_weights(std::vector<std::vector<std::optional<float>>>& data, 
        std::vector<std::vector<std::optional<float>>>& target, float learn_rate) {
        float sum = 0;
        std::vector<float> delta;
        for (int i = 0; i < weights.size(); i++)
        {
            delta.push_back(0);
        }
        
        for (int i = 0; i < data.size(); i++)
        {
            std::vector<std::vector<std::optional<float>>> tempVector;
            tempVector.push_back(data[i]);
            float prediction = LinearRegressionModel::predict_cpp(tempVector);
            float error = prediction - target[0][i].value();
            sum += error;
            for (int j = 0; j < weights.size(); j++)
            {
                delta[j] += error * data[i][j].value();
            }
        }
        shift -= learn_rate * sum;
        update_weights(delta, learn_rate);
    }
    void update_weights(std::vector<float> delta, float learn_rate) {
        for (int i = 0; i < weights.size(); i++)
        {
            weights[i][0] = weights[i][0].value() - learn_rate * (delta[i] + l1 * MLMath::sign(weights[i][0].value()) + 2 * l2 * weights[i][0].value());
        }
    }
};

PYBIND11_MODULE(MLInnoTools, m) {
    py::class_<LinearRegressionModel>(m, "LinearRegressionModel")
        .def(py::init())
        .def("train", &LinearRegressionModel::train)
        .def("predict", &LinearRegressionModel::predict)
        .def("set_l1", &LinearRegressionModel::set_l1)
        .def("set_l2", &LinearRegressionModel::set_l2);
}
