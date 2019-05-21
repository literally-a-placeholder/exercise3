# Signature Verification

## Task ##
Provided are signatures of 30 writers

Enrollment: 5 genuine signatures each<br>
Verification: 45 signatures each (20 genuine, 25 forgeries)<br>
Ground truth in verification-gt.txt

The goal is to compute dissimilarity for each verification signature
with respect to the 5 genuine ones and return a list of all signatures
sorted based on their score and evaluate how good the system performs
in detecting real signatures and differentiate them from the fake ones.

Recommendations:
- DTW
- Features: x, y, vx, vy, pressure
- vx, vy: velocity in x and y with respect to Δt
- Normalize for each signature individually
- Sakoe-Chiba band can be helpful
- Evaluation: mean average-precision

## Competition ##
The results from the competition (started on 21st of May, 2019) are located in the 'results_test' directory.

Containing:
- 'results.txt': sorted list for all keywords with sorted raw euclidean distances
- 'results_norm.txt': sorted list for all users/writers with sorted normalized dissimilarity measures (to account for innate differences in distances for different lengths of signature data). This is the intended output. Only use the raw distances if problems occur with further analysis.

To get the best results use the 'results_norm.txt' for precision/recall analysis of the system.

Output format as specified in the lecture (see below under 'Expected Output').

## Run ##
Clone the project and run the following command from the root folder to install all dependencies.

```python
pip install -r requirements.txt
```

Execute 'run_task.py'

Results of the validation data is located in 'results_valid':
![valid_eval](results_valid/validation_evaluation.png?raw=true "valid_eval")

## Install new Packages ##
Make sure to install new packages using the following commands in order to make sure that the
dependencies are listed in the requirements.txt file:

```python
pip install <package> 
pip freeze > requirements.txt
```

## Data ##

In this repository you'll find all the data necessary for the Signature Verification Task.

You find the following data inside the 'signaturedata' directory:

### enrollment ###

All genuine signatures of all 30 writers (5 each) as txt files in the following format:

rows: data points for each time step<br>
columns: t , x , y , pressure , penup , azimuth , inclination

- Penup 1 if change between pen-up and pen-down
- Azimuth / inclination --> angles of the pen

### verification ###

45 signatures for each writer (e.g. 20 genuine, 25 forgeries,
exact numbers and identification unknown!)

Same txt file format as enrollment data.

### 'gt.txt' and 'users.txt'

gt.txt: ground truth of all the verification data for performance evaluation

users.txt: ids of writers (here 000 - 030)

### Expected Output

- ASCII plaintext file
- One line per user (can be sorted by dissimilarity)

```
user1, signature_ID11, dissimilarity11, signature_ID12, dissimilarity12, ...
user2, signature_ID21, dissimilarity21, signature_ID22, dissimilarity22, ...
```

Example:

```
051, 46, 6.40341144, 21, 7.62949846, 17, 9.18516724, 03, 10.47132116, […]
043, 02, 0.99152807, 22, 4.82357323, 14, 2.14435743, 42, 5.05044537, […]
[…]
```
