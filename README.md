# Find Billy
### A Python solution to the classic "Find Billy" problem in O(N) time and O(1) extra space.

## Requirements
* Python 3.6+
* PIL

## Usage
```bash
$ pip install image
$ python find_billy.py <file_path>
```

### Example
```bash
$ python find_billy.py billy.txt
* | * | * | * | * | *
> | v | * | * | > | B
⌃ | > | > | > | ⌃ | *
⌃ | < | < | < | < | *
> | > | > | > | ⌃ | *
⌃ | * | * | * | * | *
1 | 2 | 3 | 4 | 5 | 6
Billy is at (6, 5)
```

### Example Input
```txt
* * * * * *
> v * * > B
^ > > > ^ *
^ < < < < *
> > > > ^ *
^ * * * * *
```

### Example Images
#### N = 12
![12x12](/images/12x12.png)
#### N = 10
![10x10](/images/10x10.png)

### Runtime
![Runtime](/runtime.png)