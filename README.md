# 100 prisoners problem

### My own verification of the 100 prisoners problem

Runs the scenario repeatedly and gives a summary.  

```bash
usage: prisoners_problem.py [-h] [-r TOTAL_RUNS] [-p TOTAL_PRISONERS] [--log LOG_FILE]

prisoners_problem.py: The 100 prisoners problem The director of a prison offers 100 death row prisoners, who are numbered from 1 to 100, a last chance. A room contains a cupboard with 100 drawers. The director randomly puts one prisoner's number in each closed drawer. The prisoners enter the room, one after another. Each prisoner may open and look into 50 drawers in any order. The drawers are closed again afterwards. If, during this search, every prisoner finds their number in one of
the drawers, all prisoners are pardoned. If even one prisoner does not find their number, all prisoners die. Before the first prisoner enters the room, the prisoners may discuss strategy — but may not communicate once the first prisoner enters to look in the drawers. What is the prisoners' best strategy? https://en.wikipedia.org/wiki/100_prisoners_problem

optional arguments:
  -h, --help            show this help message and exit
  -r TOTAL_RUNS, --runs TOTAL_RUNS
                        how many times to run the scenario
  -p TOTAL_PRISONERS, --prisoners TOTAL_PRISONERS
                        how many prisoners in the scenario
  --log LOG_FILE        output log
```