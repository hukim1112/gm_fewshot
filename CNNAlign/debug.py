from test_codes import data, train, model
import json, os
import argparse

def test_data(config):
    splits = ['train']
    data.synthesize_image_pair(config, splits)

def test_train(config):
    train.overfit(config, ['train'])
    #train.result_test(config, ['train'])

def test_model(config):
    model.output(config, ['train'])

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description=__doc__)
    argparser.add_argument(
        '-c', '--config',
        metavar='C',
        default='None',
        help='The Configuration file')
    args = argparser.parse_args()
    config = args.config
    with open(config) as fp:
        config = json.load(fp)
    #test_model(config)
    test_train(config)
    #test_data(config)
