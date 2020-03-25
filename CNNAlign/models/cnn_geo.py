from .modules import Feature_Extractor, Correlation_network, Spatial_transformer_regressor
import tensorflow as tf


class CNN_geo(tf.keras.Model):
    def __init__(self, backbone_name):
        super(CNN_geo, self).__init__()
        self.feature_extractor = Feature_Extractor(backbone_name)
        self.correlation_network = Correlation_network()
        self.geo_parameter_regressor = Spatial_transformer_regressor(18)

    def call(self, image_A, image_B):
        feature_A = self.feature_extractor(image_A)
        feature_B = self.feature_extractor(image_B)
        feature_A = self.feature_extractor.channelwise_l2_normalize(feature_A)
        feature_B = self.feature_extractor.channelwise_l2_normalize(feature_B)
        corr_scores = self.correlation_network(feature_A, feature_B)
        geo_parameters = self.geo_parameter_regressor(corr_scores)
        return geo_parameters