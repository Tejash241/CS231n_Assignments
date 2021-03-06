import random
import numpy as np
from cs231n.data_utils import load_CIFAR10
from cs231n.classifiers import Softmax
from cs231n.classifiers.softmax import softmax_loss_naive, softmax_loss_vectorized
import matplotlib.pyplot as plt
import time

def get_CIFAR10_data(num_training=49000, num_validation=1000, num_test=1000):
  """
  Load the CIFAR-10 dataset from disk and perform preprocessing to prepare
  it for the linear classifier. These are the same steps as we used for the
  SVM, but condensed to a single function.  
  """
  cifar10_dir = 'cs231n/datasets/cifar-10-batches-py'
  X_train, y_train, X_test, y_test = load_CIFAR10(cifar10_dir)
  
  # subsample the data
  mask = range(num_training, num_training + num_validation)
  X_val = X_train[mask]
  y_val = y_train[mask]
  mask = range(num_training)
  X_train = X_train[mask]
  y_train = y_train[mask]
  mask = range(num_test)
  X_test = X_test[mask]
  y_test = y_test[mask]
  
  X_train = np.reshape(X_train, (X_train.shape[0], -1))
  X_val = np.reshape(X_val, (X_val.shape[0], -1))
  X_test = np.reshape(X_test, (X_test.shape[0], -1))
  
  mean_image = np.mean(X_train, axis = 0)
  X_train -= mean_image
  X_val -= mean_image
  X_test -= mean_image
  
  X_train = np.hstack([X_train, np.ones((X_train.shape[0], 1))]).T
  X_val = np.hstack([X_val, np.ones((X_val.shape[0], 1))]).T
  X_test = np.hstack([X_test, np.ones((X_test.shape[0], 1))]).T
  
  return X_train, y_train, X_val, y_val, X_test, y_test

X_train, y_train, X_val, y_val, X_test, y_test = get_CIFAR10_data()
print 'Train data shape: ', X_train.shape # prints Train data shape:  (3073, 49000)
print 'Train labels shape: ', y_train.shape # prints Train labels shape:  (49000,)
print 'Validation data shape: ', X_val.shape # prints Validation data shape:  (3073, 1000)
print 'Validation labels shape: ', y_val.shape # prints Validation labels shape:  (1000,)
print 'Test data shape: ', X_test.shape # prints Test data shape:  (3073, 1000)
print 'Test labels shape: ', y_test.shape # prints Test labels shape:  (1000,)

# Generate a random softmax weight matrix and use it to compute the loss.
W = np.random.randn(10, 3073) * 0.0001
start_timer = time.time()
loss, grad = softmax_loss_naive(W, X_train, y_train, 0.0)
print 'Naive implementation took', time.time()-start_timer
# # As a rough sanity check, our loss should be something close to -log(0.1).
# print 'loss: %f' % loss
# print 'sanity check: %f' % (-np.log(0.1))
start_timer = time.time()
loss_vectorized, grad_vectorized = softmax_loss_vectorized(W, X_train, y_train, 0.0)
print 'Vectorized implementation took', time.time()-start_timer
print 'naive and vectorized loss difference', loss-loss_vectorized
print 'gradient difference', np.linalg.norm(grad-grad_vectorized, ord='fro')

# Use the validation set to tune hyperparameters (regularization strength and
# learning rate). You should experiment with different ranges for the learning
# rates and regularization strengths; if you are careful you should be able to
# get a classification accuracy of over 0.35 on the validation set.
results = {}
best_val = -1
best_softmax = None
learning_rates = [1e-7, 5e-8, 9]
regularization_strengths = [5e6, 3e5]

for lr in learning_rates:
	for rs in regularization_strengths:
		print 'Running for learning_rate %f and lambda %f' % (lr, rs)
		softmax = Softmax()
		loss_hist = softmax.train(X_train, y_train, lr, rs, 6000, verbose=True)
		y_train_pred = softmax.predict(X_train)
		acc = np.mean(y_train_pred==y_train)
		y_val_pred = softmax.predict(X_val)
		acc_val = np.mean(y_val_pred==y_val)
		print 'Training accuracy %f and Validation accuracy %f' % (acc, acc_val)
		results[(lr, rs)] = (acc, acc_val)
		if acc_val > best_val:
			best_val = acc_val
			best_softmax = softmax
    
for lr, reg in results:
    train_accuracy, val_accuracy = results[(lr, reg)]
    print 'lr %e reg %e train accuracy: %f val accuracy: %f' % (
                lr, reg, train_accuracy, val_accuracy)
    
print 'best validation accuracy achieved during cross-validation: %f' % best_val