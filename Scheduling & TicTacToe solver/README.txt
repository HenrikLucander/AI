
The files *.lp contain the base code for the programming assignments
of the 6th round of the AI course. The directory instances/ contains
some test instances for graph coloring. No instances are provided for
the other two problems. Their evaluation is based on increasing the
parameter value involved in the problem.

Once completed these files can be uploaded for grading at
MyCourses. At most 50 submissions are allowed for each assignments.

We strongly recommend to use/install Clingo (= Gringo + Clasp) for
testing purposes (https://potassco.org/clingo/).

For Windows/Mac this is probably easiest through the anaconda3 or
miniconda3 environments.  With anaconda you can run `conda install -c
potassco clingo`, after which the clingo command should be avaliable
in your anaconda prompt.

On the CS departments linux computers you can set up a clingo
environment using anaconda3 and it can be activated using the module
system as `module load anaconda3`.  Then you can create a new clingo
environment through conda with the command `conda create -n myclingo
-c potassco clingo` After this the new environment, 'myclingo' can be
started with the command `source activate myclingo` Once that is
activated you should have a clingo command in your shell. You can
leave the myclingo environment with `conda deactivate`.  The next
time you log in you only need to do `module load anaconda3` and
`source activate myclingo`.

The Clingo embedded at MyCourses is subject to resource bounds and
thus it is suboptimal for debugging. Also, there may be delays with
the evaluation and, in particular, if hundreds students start to
heavily use the embedded version.

