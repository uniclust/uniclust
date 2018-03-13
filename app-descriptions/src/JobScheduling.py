# Import
import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from matplotlib import pyplot

data_predict = pd.read_csv("sample.csv")

# Make data a np.array
data_predict = data_predict.values

# Import data
data = pd.read_csv('data.csv')

# Drop date variable
#data = data.drop(['time_submit'], 1)
data = data.drop(['time_submit_value'], 1)
#data = data.drop(['time_start'], 1)
#data = data.drop(['time_end'], 1)
#data = data.drop(['time_duration_minute'], 1)


# Dimensions of dataset
n = data.shape[0]
p = data.shape[1]

# Make data a np.array
data = data.values

###############################################################
'''''
temp_data = []

for i in range(0, len(data)):
    #time_submit_value = data[i][0]
    time_duration_h = data[i][1]
    time_limit = data[i][2]
    required_cpus = data[i][3]
    temp_data.append([time_duration_h, time_limit, required_cpus])

data = temp_data
'''
###############################################################
# We divide data into training and test data
train_start = 0
train_end = int(np.floor(0.8*n))
test_start = train_end + 1
test_end = n
data_train = data[np.arange(train_start, train_end), :]
data_test = data[np.arange(test_start, test_end), :]

# We scale data
scaler = MinMaxScaler(feature_range=(-1, 1))
scaler.fit(data_train)
data_train = scaler.transform(data_train)
data_test = scaler.transform(data_test)

# Build X and y
X_train = data_train[:, 1:]
y_train = data_train[:, 0]
X_test = data_test[:, 1:]
y_test = data_test[:, 0]

# Number of metrics in training data
n_metrics = X_train.shape[1]

# Number of Neurons in each hidden layer
#n_neurons_1 = 32
#n_neurons_2 = 16
#n_neurons_3 = 8
#n_neurons_4 = 4

# Number of Neurons in each hidden layer
n_neurons_1 = 16
n_neurons_2 = 8
n_neurons_3 = 4


# Session
net = tf.InteractiveSession()

# Placeholder
X = tf.placeholder(dtype=tf.float32, shape=[None, n_metrics])
Y = tf.placeholder(dtype=tf.float32, shape=[None])


# Initializers
sigma = 1
weight_initializer = tf.variance_scaling_initializer(mode="fan_avg", distribution="uniform", scale=sigma)
bias_initializer = tf.zeros_initializer()

# Hidden weights
#W_hidden_1 = tf.Variable(weight_initializer([n_metrics, n_neurons_1]))
#bias_hidden_1 = tf.Variable(bias_initializer([n_neurons_1]))
#W_hidden_2 = tf.Variable(weight_initializer([n_neurons_1, n_neurons_2]))
#bias_hidden_2 = tf.Variable(bias_initializer([n_neurons_2]))
#W_hidden_3 = tf.Variable(weight_initializer([n_neurons_2, n_neurons_3]))
#bias_hidden_3 = tf.Variable(bias_initializer([n_neurons_3]))
#W_hidden_4 = tf.Variable(weight_initializer([n_neurons_3, n_neurons_4]))
#bias_hidden_4 = tf.Variable(bias_initializer([n_neurons_4]))
#W_hidden_5 = tf.Variable(weight_initializer([n_neurons_4, n_neurons_5]))
#bias_hidden_5 = tf.Variable(bias_initializer([n_neurons_5]))
#W_hidden_6 = tf.Variable(weight_initializer([n_neurons_5, n_neurons_6]))
#bias_hidden_6 = tf.Variable(bias_initializer([n_neurons_6]))

# Hidden weights
W_hidden_1 = tf.Variable(weight_initializer([n_metrics, n_neurons_1]))
bias_hidden_1 = tf.Variable(bias_initializer([n_neurons_1]))
W_hidden_2 = tf.Variable(weight_initializer([n_neurons_1, n_neurons_2]))
bias_hidden_2 = tf.Variable(bias_initializer([n_neurons_2]))
W_hidden_3 = tf.Variable(weight_initializer([n_neurons_2, n_neurons_3]))
bias_hidden_3 = tf.Variable(bias_initializer([n_neurons_3]))



# Output weights
W_out = tf.Variable(weight_initializer([n_neurons_3, 1]))
bias_out = tf.Variable(bias_initializer([1]))


# Hidden layer
hidden_1 = tf.nn.relu(tf.add(tf.matmul(X, W_hidden_1), bias_hidden_1))
hidden_2 = tf.nn.relu(tf.add(tf.matmul(hidden_1, W_hidden_2), bias_hidden_2))
hidden_3 = tf.nn.relu(tf.add(tf.matmul(hidden_2, W_hidden_3), bias_hidden_3))


# Output layer (transpose!)
#out = tf.transpose(tf.add(tf.matmul(hidden_6, W_out), bias_out))

# Output layer (transpose!)
out = tf.transpose(tf.add(tf.matmul(hidden_3, W_out), bias_out))

# Cost function
mse = tf.reduce_mean(tf.squared_difference(out, Y))

# Optimizer
opt = tf.train.AdamOptimizer().minimize(mse)

# Init
net.run(tf.global_variables_initializer())

#pyplot.plot(data['time_duration_minute'])


# Setup plot
plt.ion()
fig = plt.figure()
ax1 = fig.add_subplot(111)
line1, = ax1.plot(y_test,color='red')
line2, = ax1.plot(y_test * 0.5, color='black')
plt.show()


################################################################
'''''
def plot_init (data):
    plt.ion()
    fig, ax1 = plt.subplots()


  #  ax2 = ax1.twinx()

    ax1.set_ylabel('time_duration_h', color='r')
    maximum = int(max(data [:, 0]))
    ax1.set_xlim(0, maximum)
    ax1.set_ylim(0, max(data[:,1]))

  #  ax2.set_ylabel('Accuracy (train and test (dashed))', color='b')
   # ax2.set_ylim (0, 1)

    line1 = ax1.plot([], [], '*-', color = 'red', linewidth = 2)[0]
    line2 = ax2.plot([], [], '*-', color = 'blue')[0]
   # line3 = ax2.plot([], [], '*-', color = 'blue', linestyle = 'dashed')[0]


    plt.title("Accuracy")

   # return line1, line2, line3
    return line1, line2





#data = np.array (data).reshape (3,38000)
#line1, line2, line3 = plot_init (data)
#for i in range(len(data)):
   # plot_data (line1, line2, line3, data, i)
 #  plot_data(line1, line2, data, i)



plt.show()
plt.pause(20)
'''
################################################################


# Fit neural net
batch_size = 100
mse_train = []
mse_test = []

# Run
epochs = 10
for e in range(epochs):

    # Shuffle training data
    shuffle_indices = np.random.permutation(np.arange(len(y_train)))
    X_train = X_train[shuffle_indices]
    y_train = y_train[shuffle_indices]

    # Minibatch training

    for i in range(0, len(y_train) // batch_size):
        start = i * batch_size
        batch_x = X_train[start:start + batch_size]
        batch_y = y_train[start:start + batch_size]
        # Run optimizer with batch
        net.run(opt, feed_dict={X: batch_x, Y: batch_y})



            # Show progress
        if np.mod(i,50) == 0:
            # MSE train and test
            mse_train.append(net.run(mse, feed_dict={X: X_train, Y: y_train}))
            mse_test.append(net.run(mse, feed_dict={X: X_test, Y: y_test}))
            print('MSE Train: ', mse_train[-1])
            print('MSE Test: ', mse_test[-1])
            # Prediction
            pred = net.run(out, feed_dict={X: X_test})
            line2.set_ydata(pred)
            plt.title('Epoch ' + str(e) + ', Batch ' + str(i))


            ###########################################

for i in range(0, len(data_predict) // batch_size):
    start = i * batch_size
    batch_x = data_predict[start:start + batch_size]
    pred = net.run(out, feed_dict={X: batch_x})
print(pred)
#inverse_pred = scaler.inverse_transform(data_predict)
#print(inverse_pred)

            ##########################################
plt.pause(5)


##########################################################################################
''''
#read file
data_predict = pd.read_csv("sample.csv")

# Make data a np.array
data_predict = data_predict.values


temp_data = []


for i in range(0, len(data_predict)):
   # time_duration_h = data_predict[i][1]
    time_limit = data_predict[i][2]
    required_cpus = data_predict[i][3]


    temp_data.append([time_limit, required_cpus])

data_predict = temp_data
#print(data_predict)


for i in range(0, len(data_predict) // batch_size):
    start = i * batch_size
    batch_x = data_predict[start:start + batch_size]
    pred = net.run(out, feed_dict={X: batch_x})

inverse_pred = scaler.inverse_transform(data_predict)
#print(inverse_pred)
'''''
#################################################################