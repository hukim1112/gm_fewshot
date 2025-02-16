import os, json, argparse
from data_loader import load_data
from models import load_model
from utils import parser, session_config
import tensorflow as tf

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('config', metavar='config_file',
                                        help='The name of config file.')
    args = parser.parse_args()
    config = args.config
    with open(config, "r") as file:
        config = json.load(file)
    test_config = config['test']

    os.environ['CUDA_VISIBLE_DEVICES'] = config['test']['gpu_id']
    session_config.setup_gpus(True, 0.9)

    ds = load_data(['test'], config)
    test_ds = ds['test']
    model = load_model('test', config)

    test_loss = tf.metrics.Mean(name='test_loss')
    test_acc = tf.metrics.Mean(name='test_accuracy')      

    # Testing process
    print("Testing started.")
    for epoch in range(test_config['n_episode']):
        support, query = test_ds.get_next_episode()
        loss, pred, eq, acc = val_step(support, query, model)   	
        test_loss(loss)
        test_acc(acc)
    template = 'Test Loss: {}, Test Accuracy: {}'
    print(template.format(test_loss.result(), test_acc.result()*100))
    print("Testing ended.")
    return

@tf.function
def val_step(support, query, model):
    n_class, n_query = support.shape[0], query.shape[1]
    z_prototypes, z_query = model(support, query)
    dists = model.calc_euclidian_dists(z_query, z_prototypes)
    log_p_y = model.calc_probability_with_dists(dists, n_class, n_query)
    loss, pred = model.loss_func(log_p_y, n_class, n_query)
    eq, acc = model.cal_metric(log_p_y, n_class, n_query)
    return loss, pred, eq, acc

if __name__ == "__main__":
    main()
