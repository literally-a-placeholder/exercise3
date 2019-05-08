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

## Run ##
Clone the project and run the following command from the root folder to install all dependencies.

```python
pip install -r requirements.txt
```

Execute 'run_task.py'

Sidenotes:

- only 105 results are generated, of 107 specified keywords in keywords.txt, since the two words
'order' and 'waggons' appear each in upper and lower case, which is ignored.
- optionally run 'normalize_results' after the calculation to evaluate its effect on precision and
recall. (trying to account for keywords with naturally higher distances than others, could lead to
better results in general)
- the resulting plot from the evaluation is still not entierly correct (start of the line should be
at a precision value of 1 on the left side), due to some unresolved bugs

See overall precision/recall-plot 'plot_norm_results_overall.png' for the most recent evaluation.

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