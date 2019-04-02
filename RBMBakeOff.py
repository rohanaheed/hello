
# -*- coding: utf-8 -*-
"""
Created on Thu May  3 11:11:13 2018

@author: Frank
"""

from Resturents import Resturents
from RBMAlgorithm import RBMAlgorithm
from surprise import NormalPredictor
from Evaluator import Evaluator

import random
import numpy as np

def LoadResturentsData():
    ml = Resturents()
    print("Loading resturent ratings...")
    data = ml.loadResturentsLatestSmall()
    print("\nComputing resturent popularity ranks so we can measure novelty later...")
    rankings = ml.getPopularityRanks()
    return (ml, data, rankings)

np.random.seed(0)
random.seed(0)

# Load up common data set for the recommender algorithms
(ml, evaluationData, rankings) = LoadResturentsData()

# Construct an Evaluator to, you know, evaluate them
evaluator = Evaluator(evaluationData, rankings)

#RBM
RBM = RBMAlgorithm(epochs=20)
evaluator.AddAlgorithm(RBM, "RBM")

 
# Just make random recommendations
Random = NormalPredictor()
evaluator.AddAlgorithm(Random, "Random")
# Fight!
evaluator.Evaluate(True)

evaluator.SampleTopNRecs(ml)
