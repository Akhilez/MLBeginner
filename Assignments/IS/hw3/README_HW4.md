How to run:

Make sure that you have python 3.6 or higher and numpy installed.

Create the following directories and files:
```yaml
<main_directory>:
  - data:
      - MNISTnumImages5000.txt
      - MNISTnumLabels5000.txt
  - figures
  - models
```
Run the file `split_mnist_data.py` to get the split dataset.
```bash
python split_mnist_data.py
```
Your should see `.npy` files created in `data` directory.

Now you can run the file `hybrid_classifier.py` to execute the Problem 1
```bash
python hybrid_classifier.py
``` 

And you can run the file `fine_tuned_classifier.py` to execute the Problem 2
```bash
python fine_tuned_classifier.py
```
