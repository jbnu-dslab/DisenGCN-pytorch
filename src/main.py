# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


import os.path
import sys
import torch
import fire

from pathlib import Path
from loguru import logger
from utils import *
from models.train import MyTrainer
from models.eval import MyEvaluator
from data import DataLoader


def run_model(device, hyperpm, dataset):
    in_dim = dataset.feat.shape[1]
    out_dim = hyperpm['ncaps'] * hyperpm['nhidden']

    trainer = MyTrainer(device=device,
                        in_dim=in_dim,
                        out_dim=out_dim)

    if(hyperpm['early'] == -1):
        logger.info("Train model not using early-stopping.")
    else:
        logger.info("Train model using early-stopping.")

    model = trainer.train_model(dataset=dataset, hyperpm=hyperpm)

    evaluator = MyEvaluator(device=device)
    accuracy = evaluator.evaluate(model, dataset)

    return accuracy




def main(datadir='../datasets/',
         dataname='Cora',
         cpu=False,
         nepoch=200,
         early=-1,
         lr=0.03,
         reg=0.036,
         dropout=0.35,
         nlayer=5,
         ncaps=7,
         nhidden=16,
         routit=6,
         nbsz=20,
         tau=1.0,
         bidirect=True):
    """
    :param datadir: directory of dataset
    :param dataname: name of the dataset
    :param cpu: Insist on using CPU instead of CUDA
    :param nepoch: Max number of epochs to train
    :param early: Extra iterations before early-stopping(default : -1; not using early-stopping) //8
    :param lr: Initial learning rate
    :param reg: Weight decay (L2 loss on parameters)
    :param drouput: Dropout rate (1 - keep probability)
    :param nlayer: Number of conv layers
    :param ncaps: Maximum number of capsules per layer
    :param nhidden: Number of hidden units per capsule
    :param routit: Number of iterations when routing
    :param nbsz: Size of the sampled neighborhood
    :param tau: Softmax scaling parameter
    :param bidirect : Use graph as undirected
    """

    logger.info("The main procedure has started with the following parameters:")
    device = 'cuda' if (torch.cuda.is_available() and not cpu) else 'cpu'
    param = dict()
    param['datadir'] = datadir
    param['dataname'] = dataname
    param['device'] = device
    log_param(param)

    logger.info("Training the model has begun with the following hyperparameters:")
    hyperpm = dict()
    hyperpm['nepoch'] = nepoch
    hyperpm['lr'] = lr
    hyperpm['early'] = early
    hyperpm['reg'] = reg
    hyperpm['dropout'] = dropout
    hyperpm['nlayer'] = nlayer
    hyperpm['ncaps'] = ncaps
    hyperpm['nhidden'] = nhidden
    hyperpm['routit'] = routit
    hyperpm['nbsz'] = nbsz
    hyperpm['tau'] = tau
    hyperpm['bidirect'] = bidirect
    log_param(hyperpm)

    dataset = DataLoader(data_dir=param['datadir'],
                         data_name=param['dataname'],
                         bidirection=bidirect)

    set_rng_seed(23)
    accuracy = run_model(device=device,
                         hyperpm=hyperpm,
                         dataset=dataset)

    logger.info(f"The model has been trained. The test accuracy is {accuracy:.4}")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sys.exit(fire.Fire(main))
