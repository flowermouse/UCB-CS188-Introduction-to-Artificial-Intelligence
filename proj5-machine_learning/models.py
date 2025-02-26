import nn

class PerceptronModel(object):
    def __init__(self, dimensions):
        """
        Initialize a new Perceptron instance.

        A perceptron classifies data points as either belonging to a particular
        class (+1) or not (-1). `dimensions` is the dimensionality of the data.
        For example, dimensions=2 would mean that the perceptron must classify
        2D points.
        """
        self.w = nn.Parameter(1, dimensions)

    def get_weights(self):
        """
        Return a Parameter instance with the current weights of the perceptron.
        """
        return self.w

    def run(self, x):
        """
        Calculates the score assigned by the perceptron to a data point x.

        Inputs:
            x: a node with shape (1 x dimensions)
        Returns: a node containing a single number (the score)
        """
        "*** YOUR CODE HERE ***"
        return nn.DotProduct(self.w, x)

    def get_prediction(self, x):
        """
        Calculates the predicted class for a single data point `x`.

        Returns: 1 or -1
        """
        "*** YOUR CODE HERE ***"
        if nn.as_scalar(self.run(x)) >= 0:
            return 1
        else:
            return -1

    def train(self, dataset):
        """
        Train the perceptron until convergence.
        """
        "*** YOUR CODE HERE ***"
        numbers = len(dataset.y)
        while True:
            correct = True
            for _ in range(numbers):
                for x, y in dataset.iterate_once(1):
                    if self.get_prediction(x) != nn.as_scalar(y):
                        self.w.update(x, nn.as_scalar(y))
                        correct = False
            if correct:
                break
        

class RegressionModel(object):
    """
    A neural network model for approximating a function that maps from real
    numbers to real numbers. The network should be sufficiently large to be able
    to approximate sin(x) on the interval [-2pi, 2pi] to reasonable precision.
    """
    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        self.w1 = nn.Parameter(1, 20)
        self.w2 = nn.Parameter(20, 100)
        self.w3 = nn.Parameter(100, 50)
        self.w4 = nn.Parameter(50, 1)

        self.b1 = nn.Parameter(1, 20)
        self.b2 = nn.Parameter(1, 100)
        self.b3 = nn.Parameter(1, 50)
        self.b4 = nn.Parameter(1, 1)

    def run(self, x):
        """
        Runs the model for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
        Returns:
            A node with shape (batch_size x 1) containing predicted y-values
        """
        "*** YOUR CODE HERE ***"
        print(x)
        layer1 = nn.ReLU(nn.AddBias(nn.Linear(x, self.w1), self.b1))
        layer2 = nn.ReLU(nn.AddBias(nn.Linear(layer1, self.w2), self.b2))
        layer3 = nn.ReLU(nn.AddBias(nn.Linear(layer2, self.w3), self.b3))
        layer4 = nn.AddBias(nn.Linear(layer3, self.w4), self.b4)
        return layer4

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
            y: a node with shape (batch_size x 1), containing the true y-values
                to be used for training
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        predicted = self.run(x)
        return nn.SquareLoss(predicted, y)

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        batch_size = len(dataset.y)
        # notice: using loss function, the update method is to substract gradient times alpha,
        # so the learning rate should be set to negative
        alpha = -0.05
        for x, y in dataset.iterate_forever(batch_size):
            loss = self.get_loss(x, y)
            grad_w1, grad_b1, grad_w2, grad_b2, grad_w3, grad_b3, grad_w4, grad_b4 \
                = nn.gradients(loss, [self.w1, self.b1, self.w2, self.b2, self.w3, self.b3, self.w4, self.b4])
            self.w1.update(grad_w1, alpha)
            self.w2.update(grad_w2, alpha)
            self.b1.update(grad_b1, alpha)
            self.b2.update(grad_b2, alpha)
            self.w3.update(grad_w3, alpha)
            self.b3.update(grad_b3, alpha)
            self.w4.update(grad_w4, alpha)
            self.b4.update(grad_b4, alpha)
            loss = nn.as_scalar(loss)
            if loss < 0.0010:
                break

class DigitClassificationModel(object):
    """
    A model for handwritten digit classification using the MNIST dataset.

    Each handwritten digit is a 28x28 pixel grayscale image, which is flattened
    into a 784-dimensional vector for the purposes of this model. Each entry in
    the vector is a floating point number between 0 and 1.

    The goal is to sort each digit into one of 10 classes (number 0 through 9).

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        self.w1 = nn.Parameter(784, 256)
        self.w2 = nn.Parameter(256, 64)
        self.w3 = nn.Parameter(64, 10)

        self.b1 = nn.Parameter(1, 256)
        self.b2 = nn.Parameter(1, 64)
        self.b3 = nn.Parameter(1, 10)

    def run(self, x):
        """
        Runs the model for a batch of examples.

        Your model should predict a node with shape (batch_size x 10),
        containing scores. Higher scores correspond to greater probability of
        the image belonging to a particular class.

        Inputs:
            x: a node with shape (batch_size x 784)
        Output:
            A node with shape (batch_size x 10) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"
        layer1 = nn.ReLU(nn.AddBias(nn.Linear(x, self.w1), self.b1))
        layer2 = nn.ReLU(nn.AddBias(nn.Linear(layer1, self.w2), self.b2))
        layer3 = nn.AddBias(nn.Linear(layer2, self.w3), self.b3)
        return layer3

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 10). Each row is a one-hot vector encoding the correct
        digit class (0-9).

        Inputs:
            x: a node with shape (batch_size x 784)
            y: a node with shape (batch_size x 10)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        predicted = self.run(x)
        return nn.SoftmaxLoss(predicted, y)

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        batch_size = 200
        # notice: using loss function, the update method is to substract gradient times alpha,
        # so the learning rate should be set to negative
        alpha = -0.1
        for x, y in dataset.iterate_forever(batch_size):
            loss = self.get_loss(x, y)
            grad_w1, grad_b1, grad_w2, grad_b2, grad_w3, grad_b3 \
                = nn.gradients(loss, [self.w1, self.b1, self.w2, self.b2, self.w3, self.b3])
            self.w1.update(grad_w1, alpha)
            self.b1.update(grad_b1, alpha)
            self.w2.update(grad_w2, alpha)
            self.b2.update(grad_b2, alpha)
            self.w3.update(grad_w3, alpha)
            self.b3.update(grad_b3, alpha)
            if dataset.get_validation_accuracy() > 0.975:
                break


class LanguageIDModel(object):
    """
    A model for language identification at a single-word granularity.

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Our dataset contains words from five different languages, and the
        # combined alphabets of the five languages contain a total of 47 unique
        # characters.
        # You can refer to self.num_chars or len(self.languages) in your code
        self.num_chars = 47
        self.languages = ["English", "Spanish", "Finnish", "Dutch", "Polish"]

        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        self.iw1 = nn.Parameter(self.num_chars, 4*self.num_chars)
        self.iw2 = nn.Parameter(4*self.num_chars, 8*self.num_chars)

        # self.ib1 = nn.Parameter(1, 8*self.num_chars)
        # self.ib2 = nn.Parameter(1, len(self.languages))

        self.rw1 = nn.Parameter(8*self.num_chars, 8*self.num_chars)
        self.rw2 = nn.Parameter(8*self.num_chars, 8*self.num_chars)

        # self.rb1 = nn.Parameter(1, 8*self.num_chars)
        # self.rb2 = nn.Parameter(1, len(self.languages))

        self.ow = nn.Parameter(8*self.num_chars, len(self.languages))
        self.ob = nn.Parameter(1, len(self.languages))

    def run(self, xs):
        """
        Runs the model for a batch of examples.

        Although words have different lengths, our data processing guarantees
        that within a single batch, all words will be of the same length (L).

        Here `xs` will be a list of length L. Each element of `xs` will be a
        node with shape (batch_size x self.num_chars), where every row in the
        array is a one-hot vector encoding of a character. For example, if we
        have a batch of 8 three-letter words where the last word is "cat", then
        xs[1] will be a node that contains a 1 at position (7, 0). Here the
        index 7 reflects the fact that "cat" is the last word in the batch, and
        the index 0 reflects the fact that the letter "a" is the inital (0th)
        letter of our combined alphabet for this task.

        Your model should use a Recurrent Neural Network to summarize the list
        `xs` into a single node of shape (batch_size x hidden_size), for your
        choice of hidden_size. It should then calculate a node of shape
        (batch_size x 5) containing scores, where higher scores correspond to
        greater probability of the word originating from a particular language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
        Returns:
            A node with shape (batch_size x 5) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"
        # f_initial
        h = nn.ReLU(nn.Linear(nn.ReLU(nn.Linear(xs[0], self.iw1)), self.iw2))
        # f
        for char in xs[1:]:
            new_x = nn.ReLU(nn.Linear(nn.ReLU(nn.Linear(char, self.iw1)), self.iw2))
            h = nn.ReLU(nn.Linear(nn.ReLU(nn.Linear(h, self.rw1)), self.rw2))
            h = nn.Add(new_x, h)
        output = nn.AddBias(nn.Linear(h, self.ow), self.ob)
        return output
        
    def get_loss(self, xs, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 5). Each row is a one-hot vector encoding the correct
        language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
            y: a node with shape (batch_size x 5)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        predicted = self.run(xs)
        return nn.SoftmaxLoss(predicted, y)

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        batch_size = 100
        # notice: using loss function, the update method is to substract gradient times alpha,
        # so the learning rate should be set to negative
        alpha = -0.1
        while dataset.get_validation_accuracy() < 0.85:
            for x, y in dataset.iterate_once(batch_size):
                loss = self.get_loss(x, y)
                grad_iw1, grad_iw2, grad_rw1, grad_rw2, grad_ow, grad_ob \
                    = nn.gradients(loss, [self.iw1, self.iw2, self.rw1, self.rw2, self.ow, self.ob])
                self.iw1.update(grad_iw1, alpha)
                self.iw2.update(grad_iw2, alpha)
                self.rw1.update(grad_rw1, alpha)
                self.rw2.update(grad_rw2, alpha)
                self.ow.update(grad_ow, alpha)
                self.ob.update(grad_ob, alpha)
