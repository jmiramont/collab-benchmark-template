if __name__ == "__main__":
    import importlib
    from src.methods import *
    from mcsm_benchs.benchmark_utils import MethodTemplate as MethodTemplate
    import inspect

    from mcsm_benchs.Benchmark import Benchmark
    import numpy as np
    from mcsm_benchs.ResultsInterpreter import ResultsInterpreter
    import yaml
    import pickle
    import os
    
    print('Getting benchmarks paths...')
    paths = []
    for file in os.listdir('results'):
        print(file, file[-4::])
        if file[-4::]== '.pkl':
            print(file[:-4])
            paths.append(file[:-4])
    
    sub_folders = ['b{}'.format(i+1) for i,p in enumerate(paths)]
    for file, sub_folder in zip(paths,sub_folders):

        # Load Benchmark
        filename=os.path.join('results',file)
        try:
            benchmark = Benchmark.load_benchmark(filename=filename)
            interpreter = ResultsInterpreter(benchmark)

        except BaseException as err:
            print(f"Unexpected error {err=}, {type(err)=} loading {filename}.")

        # Get environment information from GitHub Actions (if possible):
        try:
            username = os.environ['OWNER']
            reponame = os.environ['NAME']
            print("Owner:", username, " Repo:", reponame)

        except BaseException as err:
            print(f"Unexpected error {err=}, {type(err)=} loading GitHub env.")
            username='USERNAME'
            reponame='MY-REPO'
        
        link = 'https://{}.github.io/{}/results/{}'.format(username,reponame,sub_folder)
        print(link)


        # Report shown in the repo 
        interpreter.save_report(filename='results_{}.md'.format(sub_folder),
                                path=os.path.join('results'), 
                                link=link)

        # Interactive figures shown in the repo
        interpreter.get_html_figures(df=interpreter.get_benchmark_as_data_frame(),
                                    #   varfun=cp_ci, 
                                    path=os.path.join('results',sub_folder), 
                                    bars=True, 
                                    ylabel='Perf. Fun.',
                                    )

        # .csv files for sharing results
        interpreter.get_csv_files(path=os.path.join('results',sub_folder),)

        #TODO Build table to summarize the results.