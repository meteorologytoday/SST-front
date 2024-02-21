#!/bin/bash
#SBATCH -p cw3e-shared
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=40G
#SBATCH -t 01:00:00
#SBATCH -J job.8
#SBATCH -A csg102
#SBATCH -o job.8.%j.%N.out
#SBATCH -e job.8.%j.%N.err
#SBATCH --export=ALL

export SLURM_EXPORT_ENV=ALL

source /home/t2hsu/.bashrc_WRF4.3_gcc
ml load slurm
ml load openmpi

./run_sine.sh
