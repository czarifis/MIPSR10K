### CSE240A - Graduate Computer Architecture class - MIPSR10K Simulator

This is the final version of the Project that was developed for the CSE240A - Graduate Computer Architecture class. It contains the implementation of the MIPS R10K simulator. Specifically:

* The "test results" folder contains the output of the simulator for the class wide test suit and for some of my own tests
* The "test traces used for test results" folder contains the input files that were given to our simulator to generate the corresponding output html files
* The "FinalReport.pdf" contains the report which also contains instructions on how to run the tests
* The mips10k folder contains the source code and more benchmarks that were used to verify the proper execution of the simulator ("benchmarks" is the name of folder that contains those tests)


To view some of the output test results click on any of the following links:

* [test1](http://czarifis.github.io/MIPSR10K/test%20results/mytest.html)
* [Test Branch 1](http://czarifis.github.io/MIPSR10K/test%20results/test_b1.html)
* [Test Branch 1](http://czarifis.github.io/MIPSR10K/test%20results/test_b1.html)
* [Test Branch 2](http://czarifis.github.io/MIPSR10K/test%20results/test_b6.html)
* [Test load store 1](http://czarifis.github.io/MIPSR10K/test%20results/test_ls1.html)
* [Test load store 2](http://czarifis.github.io/MIPSR10K/test%20results/test_ls4.html)
* [Test stress 1](http://czarifis.github.io/MIPSR10K/test%20results/test_s1.html)
* [Test stress 2](http://czarifis.github.io/MIPSR10K/test%20results/test_s5.html)
* [Test stress 3](http://czarifis.github.io/MIPSR10K/test%20results/test_t1.html)
* [Test stress 4](http://czarifis.github.io/MIPSR10K/test%20results/test_t5.html)


### Testing - Evaluation

This project works on Python 2.7.8 and requires the Pandas library

To view some test trace files have a look at the benchmark folder or at the "test traces used for test results" folder. More information about the test cases are provided on the afore-mentioned report pdf file.

By executing the following:
	
    python run.py -h
    
you should be getting this message:

	usage: run.py [-h] [-in FILENAME] [-out OUTPUT] [-issue ISSUE]

	optional arguments:
	  -h, --help
	  show this help message and exit
	  -in FILENAME input file path
	  -out OUTPUT
	  output file path
	  -issue ISSUE total number of instructions that can get issued (default is 4)

If something goes wrong follow the instructions on this link to install all the dependencies on your own machine: http://blog.zarifis.info/installing-anaconda-numpy-scipy-pandas-etc/

The input to the run.py file should be a text file with the trace that is about to get executed and the output should be the name of the HTML file that contains the output of the simulator. By default MIPS R10K issues 4 instructions per cycle, however by providing the issue flag the user is free to modify this number to see what would happen in other edge cases.

A valid input might look like this:

	python run.py -in benchmarks/test_s1.txt -out test_s1
    
When the execution is done check the test_s1.html file for the output.

Thanks for visiting this page.

Enjoy :)


