'''
Answers for all the sections of the tutorial
'''
import random 

import pandas as pd
import numpy as np

import filepaths
from DataDescriber import DataDescriber
from DataGenerator import DataGenerator


def main():
    nhs_ae_df = load_nhs_ae_anomymous_data()
    threshold_value = len(nhs_ae_df['Treatment'].unique().tolist())
    num_tuples_to_generate = len(nhs_ae_df)
    attribute_to_datatype = {
        'Attendance ID': 'String', 'Hospital ID': 'String', 'Time in A&E (mins)': 'Integer', 'Treatment': 'String', 
        'Gender': 'String', 'Index of Multiple Deprivation Decile': 'Integer',
        'Arrival Date': 'String', 'Arrival hour range': 'String',  'Age bracket': 'String'
    }
    attribute_to_is_categorical = {
        'Attendance ID': False, 'Hospital ID': True, 'Time in A&E (mins)': False, 
        'Treatment': True, 
        'Gender': True, 'Index of Multiple Deprivation Decile': False,
        'Arrival Date': True, 'Arrival hour range': True,  'Age bracket': True
    }
    attribute_to_is_candidate_key = {
        'Attendance ID': True
    }
    

    describer = DataDescriber(category_threshold=threshold_value)
    generator = DataGenerator()

    # random mode 
    describer.describe_dataset_in_random_mode(
        filepaths.nhs_ae_anonymous,
        attribute_to_datatype=attribute_to_datatype,
        attribute_to_is_categorical=attribute_to_is_categorical)
    describer.save_dataset_description_to_file(filepaths.nhs_ae_description_random)

    generator.generate_dataset_in_random_mode(
        num_tuples_to_generate, filepaths.nhs_ae_description_random)
    generator.save_synthetic_data(filepaths.nhs_ae_synthetic_random)

    # independent mode 
    describer.describe_dataset_in_independent_attribute_mode(
        filepaths.nhs_ae_anonymous,
        attribute_to_datatype=attribute_to_datatype,
        attribute_to_is_categorical=attribute_to_is_categorical)
    describer.save_dataset_description_to_file(filepaths.nhs_ae_description_independent)

    generator.generate_dataset_in_random_mode(
        num_tuples_to_generate, filepaths.nhs_ae_description_independent)
    generator.save_synthetic_data(filepaths.nhs_ae_synthetic_independent)

    # correlated mode
    # A parameter in Differential Privacy. It roughly means that changing a row in the input dataset will not 
    # change the probability of getting the same output more than a multiplicative difference of exp(epsilon).
    # Increase epsilon value to reduce the injected noises. Set epsilon=0 to turn off differential privacy.
    epsilon = 0.1

    # The maximum number of parents in Bayesian network, i.e., the maximum number of incoming edges.
    degree_of_bayesian_network = 2

    describer.describe_dataset_in_correlated_attribute_mode(
        dataset_file=filepaths.nhs_ae_anonymous, 
        epsilon=epsilon, 
        k=degree_of_bayesian_network,
        attribute_to_datatype=attribute_to_datatype,
        attribute_to_is_categorical=attribute_to_is_categorical,
        attribute_to_is_candidate_key=attribute_to_is_candidate_key)
    describer.save_dataset_description_to_file(
        filepaths.nhs_ae_description_correlated)
    generator.generate_dataset_in_correlated_attribute_mode(
        num_tuples_to_generate, filepaths.nhs_ae_description_correlated)
    generator.save_synthetic_data(filepaths.nhs_ae_synthetic_correlated)

    print('done.')


def load_nhs_ae_anomymous_data():
    nhs_ae_df = pd.read_csv(filepaths.nhs_ae_anonymous)
    return nhs_ae_df




if __name__ == "__main__":
    main()
