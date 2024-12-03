import argparse
import six, os, torch
from run.run import RUN
import asyncio

def main(args):
    RUN(args).report_generation()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--llm', type=str, default='openai', 
                        choices=["openai","claude"], required=False)

    args = parser.parse_args()

    main(args)




    
