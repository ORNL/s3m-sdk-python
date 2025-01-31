#!/bin/bash --login

export MY_JOBID=$SLURM_JOBID

mkdir -p jobs/$MY_JOBID && cd jobs/$MY_JOBID

# Capture job information and environment
echo "====================== SLURM Job Info ======================="
squeue --long -j $MY_JOBID | tee job.info
echo "============================================================="
echo

echo "-------------------- Job Status --------------------"
scontrol show job=$MY_JOBID
echo "----------------------------------------------------"
echo

echo "-------------------- Job Hosts --------------------"
scontrol show hostnames | tee job.hosts
echo "----------------------------------------------------"
echo

echo "-------------------- Job Environment --------------------"
/usr/bin/env | sort | tee job.environ
echo "---------------------------------------------------------"
echo

# Collect node/proc counts
n_nodes=$SLURM_JOB_NUM_NODES
slots_per_node=$SLURM_CPUS_ON_NODE
n_procs=$(( $slots_per_node * $n_nodes ))
export MY_JOB_NUM_NODES=$n_nodes
export MY_JOB_NUM_PROCS_PER_NODE=$slots_per_node
export MY_JOB_NUM_PROCS=$n_procs
echo "INFO: Using $MY_JOB_NUM_PROCS_PER_NODE processes-per-node on $MY_JOB_NUM_NODES nodes ($MY_JOB_NUM_PROCS total processes)"
echo

# Run a couple job steps
echo "At $(date), running hostname : "
srun -n $n_procs -N $n_nodes /bin/hostname
echo
echo "At $(date), running top in batch mode for 60 seconds : "
srun -n $n_procs -N $n_nodes /usr/bin/top -b -d 6 -n 10
echo

# Show active job steps
echo "At $(date), listing job steps : "
squeue -s -j $MY_JOBID