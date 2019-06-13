# Produce nogoods

To produce nogoods use __produce_nogoods.py__. To run it needs some files(encoding, etc), an instance and an amount of nogoods to extract.

Sample call:

```
python produce_nogoods.py --files encodings/basic_encoding.lp encodings/assumption-solver.py --instance test-instances/blocks-11.lp --nogoods-limit 10
```

Additionally, pddl instances can be used instead of regular asp instances with the --pddl-instance option(if the instance has a .pddl extension the --instance options treats the instance as pddl). The program will try to find the domain file in the same folder of the instance or in the parent folder. A domain can also be manually given with the --pddl-domain option.

Sample call:

```
python produce_nogoods.py --files encodings/basic_encoding.lp encodings/assumption-solver.py --pddl-instance path/to/pddl/instance.pddl --nogoods-limit 10
```

For more options such as maximum extraction time use --help

The nogoods will be saved into a file called __conv_ng.lp__

## Validating nogoods

To validate nogoods use the option --validate-files. The value of the option must be a file(s) that can be used to validate them. E.g __validation-encoding/state_prover.lp__ when using basic_encoding.lp as the encoding.

# Consuming nogoods

There are 2 options to consume nogoods. One is to consume the nogoods directly after producing them. Just use the --consume and --scaling-list or --scaling-exp options along with the calls given above. 

The second option is to use the __consume_nogoods.py__ program. A file containing the output nogoods from a __produce_nogoods.py__ call have to be given as input with the --nogoods option.

Sample call:

```
python consume_nogoods.py --files encodings/basic.lp encodings/assumption-solver.py test-instances/blocks-11.lp --nogoods conv_ng.lp 
```

Pddl instances are supported aswell when using the option --pddl-instance to pass them.

## Scaling

The nogoods are consumed based on a set scaling given with the --scaling-list or --scaling-exp option. 

The --scaling-list option is very straightforward. The value should just be a list of integers separated by a comma that indicate how many nogoods should be used in the run. For example: a scaling list of 2,4,8,16,32 will run 5 runs with each run having the amount of nogoods specified in the list.

The input has 3 values separated by a comma. The first value is the starting amount of nogoods. The second value is the increase factor. The third value is how many iterations to perform.

For example, a scaling of 8,2,5 will start by using 8 nogoods. The noogods used will be doubled after every iteration and there will be a total of 5 iterations. So, there will be 5 clingo calls where 8, 16, 32, 64 and 128 nogoods are consumed. Consuming nogoods will always run a baseline call with 0 nogoods added.

