# format_data

import numpy as np

def search_data(sequence_length, num_of_depend, label_start_idx,
                num_for_predict, units, points_per_hour):
    '''
    Parameters
    ----------
    sequence_length: int, length of all history data
    num_of_depend: int,
    label_start_idx: int, the first index of predicting target
    num_for_predict: int, the number of points will be predicted for each sample
    units: int, week: 7 * 24, day: 24, recent(hour): 1
    points_per_hour: int, number of points per hour, depends on data
    Returns
    ----------
    list[(start_idx, end_idx)]
    '''

    if points_per_hour < 0:
        raise ValueError("points_per_hour should be greater than 0!")

    if label_start_idx + num_for_predict > sequence_length:
        return None

    x_idx = []
    for i in range(1, num_of_depend + 1):
        start_idx = label_start_idx - points_per_hour * units * i
        end_idx = start_idx + num_for_predict
        if start_idx >= 0:
            x_idx.append((start_idx, end_idx))
        else:
            return None

    if len(x_idx) != num_of_depend:
        return None

    return x_idx[::-1]

def get_sample_indices(data_sequence, num_of_weeks, num_of_days, num_of_hours,
                       label_start_idx, num_for_predict, points_per_hour=12, with_target=True):
    '''
    Parameters
    ----------
    data_sequence: np.ndarray
                   shape is (sequence_length, num_of_vertices, num_of_features)
    num_of_weeks, num_of_days, num_of_hours: int
    label_start_idx: int, the first index of predicting target, ??值?始的那??
    num_for_predict: int,
                     the number of points will be predicted for each sample
    points_per_hour: int, default 12, number of points per hour
    Returns
    ----------
    week_sample: np.ndarray
                 shape is (num_of_weeks * points_per_hour,
                           num_of_vertices, num_of_features)
    day_sample: np.ndarray
                 shape is (num_of_days * points_per_hour,
                           num_of_vertices, num_of_features)
    hour_sample: np.ndarray
                 shape is (num_of_hours * points_per_hour,
                           num_of_vertices, num_of_features)
    target: np.ndarray
            shape is (num_for_predict, num_of_vertices, num_of_features)
    '''
    week_sample, day_sample, hour_sample = None, None, None

    if label_start_idx + num_for_predict > data_sequence.shape[0]:
        return week_sample, day_sample, hour_sample, None

    if num_of_weeks > 0:
        week_indices = search_data(data_sequence.shape[0], num_of_weeks,
                                   label_start_idx, num_for_predict,
                                   7 * 21, points_per_hour)
        if not week_indices:
            return None, None, None, None

        week_sample = np.concatenate([data_sequence[i: j]
                                      for i, j in week_indices], axis=0)

    if num_of_days > 0:
        day_indices = search_data(data_sequence.shape[0], num_of_days,
                                  label_start_idx, num_for_predict,
                                  21, points_per_hour)
        if not day_indices:
            return None, None, None, None

        day_sample = np.concatenate([data_sequence[i: j]
                                     for i, j in day_indices], axis=0)

    if num_of_hours > 0:
        hour_indices = search_data(data_sequence.shape[0], num_of_hours,
                                   label_start_idx, num_for_predict,
                                   1, points_per_hour)
        if not hour_indices:
            return None, None, None, None

        hour_sample = np.concatenate([data_sequence[i: j]
                                      for i, j in hour_indices], axis=0)
    if with_target:
        target = data_sequence[label_start_idx: label_start_idx + num_for_predict]
        return week_sample, day_sample, hour_sample, target
    else:
        return week_sample, day_sample, hour_sample


def read_and_generate_dataset(data_seq,
                              num_of_weeks, num_of_days,
                              num_of_hours, num_for_predict,
                              points_per_hour=12, save=False,save_dir_path=None):
    '''
    Parameters
    ----------
    graph_signal_matrix_filename: str, path of graph signal matrix file
    num_of_weeks, num_of_days, num_of_hours: int
    num_for_predict: int
    points_per_hour: int, default 12, depends on data

    Returns
    ----------
    feature: np.ndarray,
             shape is (num_of_samples, num_of_depend * points_per_hour,
                       num_of_vertices, num_of_features)
    target: np.ndarray,
            shape is (num_of_samples, num_of_vertices, num_for_predict)
    '''
    # data_seq = np.load(graph_signal_matrix_filename)['data']  # (sequence_length, num_of_vertices, num_of_features)

    all_samples = []
    for idx in range(data_seq.shape[0]):
        sample = get_sample_indices(data_seq, num_of_weeks, num_of_days,
                                    num_of_hours, idx, num_for_predict,
                                    points_per_hour)
        if ((sample[0] is None) and (sample[1] is None) and (sample[2] is None)):
            continue

        week_sample, day_sample, hour_sample, target = sample
        
        # target: np.ndarray, shape is (num_for_predict, num_of_vertices, num_of_features)
        
        sample = []  # [(week_sample),(day_sample),(hour_sample),target,time_sample]

        if num_of_weeks > 0:
            week_sample = np.expand_dims(week_sample, axis=0).transpose((0, 2, 3, 1))  # (1,N,F,T)
            sample.append(week_sample)

        if num_of_days > 0:
            day_sample = np.expand_dims(day_sample, axis=0).transpose((0, 2, 3, 1))  # (1,N,F,T)
            sample.append(day_sample)

        if num_of_hours > 0:
            hour_sample = np.expand_dims(hour_sample, axis=0).transpose((0, 2, 3, 1))  # (1,N,F,T)
            sample.append(hour_sample)

        # target = np.expand_dims(target, axis=0).transpose((0, 2, 3, 1))[:, :, 0, :]  # (1,N,T)
        target = np.expand_dims(target, axis=0).transpose((0, 2, 3, 1))[:, :, :2, :].sum(axis=2)  # (1,N,T)
        sample.append(target)

        time_sample = np.expand_dims(np.array([idx]), axis=0)  # (1,1)
        sample.append(time_sample)
        
        all_samples.append(
            sample)  # sampe：[(week_sample),(day_sample),(hour_sample),target,time_sample] = [(1,N,F,Tw),(1,N,F,Td),(1,N,F,Th),(1,N,2,Tpre),(1,1)]
        
#         all_samples.append(
#             sample)  # sampe：[(week_sample),(day_sample),(hour_sample),target,time_sample] = [(1,N,F,Tw),(1,N,F,Td),(1,N,F,Th),(1,N,Tpre),(1,1)]

    split_line1 = int(len(all_samples) * 0.90)
    split_line2 = int(len(all_samples) * 0.95)

    training_set = [np.concatenate(i, axis=0)
                    for i in zip(*all_samples[:split_line1])]  # [(B,N,F,Tw),(B,N,F,Td),(B,N,F,Th),(B,N,2,Tpre),(B,1)]
    validation_set = [np.concatenate(i, axis=0)
                      for i in zip(*all_samples[split_line1: split_line2])]
    testing_set = [np.concatenate(i, axis=0)
                   for i in zip(*all_samples[split_line2:])]

    train_x = np.concatenate(training_set[:-2], axis=-1)  # (B,N,F,T')
    val_x = np.concatenate(validation_set[:-2], axis=-1)
    test_x = np.concatenate(testing_set[:-2], axis=-1)

    train_target = training_set[-2]  # (B,N,T)
    val_target = validation_set[-2]
    test_target = testing_set[-2]

    train_timestamp = training_set[-1]  # (B,1)
    val_timestamp = validation_set[-1]
    test_timestamp = testing_set[-1]

    (stats, train_x_norm, val_x_norm, test_x_norm) = normalization(train_x, val_x, test_x)

    all_data = {
        'train': {
            'x': train_x_norm,
            'target': train_target,
            'timestamp': train_timestamp,
        },
        'val': {
            'x': val_x_norm,
            'target': val_target,
            'timestamp': val_timestamp,
        },
        'test': {
            'x': test_x_norm,
            'target': test_target,
            'timestamp': test_timestamp,
        },
        'stats': {
            '_mean': stats['_mean'],
            '_std': stats['_std'],
        }
    }
    print('train x:', all_data['train']['x'].shape)
    print('train target:', all_data['train']['target'].shape)
    print('train timestamp:', all_data['train']['timestamp'].shape)
    print()
    print('val x:', all_data['val']['x'].shape)
    print('val target:', all_data['val']['target'].shape)
    print('val timestamp:', all_data['val']['timestamp'].shape)
    print()
    print('test x:', all_data['test']['x'].shape)
    print('test target:', all_data['test']['target'].shape)
    print('test timestamp:', all_data['test']['timestamp'].shape)
    print()
    print('train data _mean :', stats['_mean'].shape, stats['_mean'])
    print('train data _std :', stats['_std'].shape, stats['_std'])
        
    if save:
        filename = save_dir_path + "/metro_covid_data" + '_r' + str(num_of_hours) + '_d' + str(num_of_days) + '_w' + str(num_of_weeks) + '_astcgn'
        # filename = os.path.join(dirpath, file + '_r' + str(num_of_hours) + '_d' + str(num_of_days) + '_w' + str(num_of_weeks)) + '_astcgn'
        np.savez_compressed(filename,
                            train_x=all_data['train']['x'], train_target=all_data['train']['target'],
                            train_timestamp=all_data['train']['timestamp'],
                            val_x=all_data['val']['x'], val_target=all_data['val']['target'],
                            val_timestamp=all_data['val']['timestamp'],
                            test_x=all_data['test']['x'], test_target=all_data['test']['target'],
                            test_timestamp=all_data['test']['timestamp'],
                            mean=all_data['stats']['_mean'], std=all_data['stats']['_std']
                           )
#     if save:
#         file = os.path.basename(graph_signal_matrix_filename).split('.')[0]
#         dirpath = os.path.dirname(graph_signal_matrix_filename)
#         filename = os.path.join(dirpath, file + '_r' + str(num_of_hours) + '_d' + str(num_of_days) + '_w' + str(num_of_weeks)) + '_astcgn'
#         print('save file:', filename)
#         np.savez_compressed(filename,
#                             train_x=all_data['train']['x'], train_target=all_data['train']['target'],
#                             train_timestamp=all_data['train']['timestamp'],
#                             val_x=all_data['val']['x'], val_target=all_data['val']['target'],
#                             val_timestamp=all_data['val']['timestamp'],
#                             test_x=all_data['test']['x'], test_target=all_data['test']['target'],
#                             test_timestamp=all_data['test']['timestamp'],
#                             mean=all_data['stats']['_mean'], std=all_data['stats']['_std']
#                             )
    return all_data

def normalization(train, val, test):
    '''
    Parameters
    ----------
    train, val, test: np.ndarray (B,N,F,T)
    Returns
    ----------
    stats: dict, two keys: mean and std
    train_norm, val_norm, test_norm: np.ndarray,
                                     shape is the same as original
    '''

    assert train.shape[1:] == val.shape[1:] and val.shape[1:] == test.shape[1:]  # ensure the num of nodes is the same
    mean = train.mean(axis=(0,1,3), keepdims=True)
    std = train.std(axis=(0,1,3), keepdims=True)
    std[std == 0] = 1
    print('mean.shape:',mean.shape)
    print('std.shape:',std.shape)

    def normalize(x):
        return (x - mean) / std

    train_norm = normalize(train)
    val_norm = normalize(val)
    test_norm = normalize(test)

    return {'_mean': mean, '_std': std}, train_norm, val_norm, test_norm


def read_and_generate_covid_dataset(data_seq,
                              num_of_weeks, num_of_days,
                              num_of_hours, num_for_predict,
                              points_per_hour=12, save=False,save_dir_path=None):
    '''
    Parameters
    ----------
    graph_signal_matrix_filename: str, path of graph signal matrix file
    num_of_weeks, num_of_days, num_of_hours: int
    num_for_predict: int
    points_per_hour: int, default 12, depends on data

    Returns
    ----------
    feature: np.ndarray,
             shape is (num_of_samples, num_of_depend * points_per_hour,
                       num_of_vertices, num_of_features)
    target: np.ndarray,
            shape is (num_of_samples, num_of_vertices, num_for_predict)
    '''
    # data_seq = np.load(graph_signal_matrix_filename)['data']  # (sequence_length, num_of_vertices, num_of_features)

    all_samples = []
    for idx in range(data_seq.shape[0]):
        sample = get_sample_indices(data_seq, num_of_weeks, num_of_days,
                                    num_of_hours, idx, num_for_predict,
                                    points_per_hour,  with_target=False)
        if ((sample[0] is None) and (sample[1] is None) and (sample[2] is None)):
            continue

        week_sample, day_sample, hour_sample = sample
        
        # target: np.ndarray, shape is (num_for_predict, num_of_vertices, num_of_features)
        
        sample = []  # [(week_sample),(day_sample),(hour_sample),target,time_sample]

        # if num_of_weeks > 0:
        #     week_sample = np.expand_dims(week_sample, axis=0).transpose((0, 2, 3, 1))  # (1,N,F,T)
        #     sample.append(week_sample)

        # if num_of_days > 0:
        #     day_sample = np.expand_dims(day_sample, axis=0).transpose((0, 2, 3, 1))  # (1,N,F,T)
        #     sample.append(day_sample)

        if num_of_hours > 0:
            hour_sample = np.expand_dims(hour_sample, axis=0).transpose((0, 2, 3, 1))  # (1,N,F,T)
            hour_sample = np.expand_dims(hour_sample[:,0,:,:], axis=1)
            sample.append(hour_sample)

        # target = np.expand_dims(target, axis=0).transpose((0, 2, 3, 1))[:, :, 0, :]  # (1,N,T)
        # target = np.expand_dims(target, axis=0).transpose((0, 2, 3, 1))[:, :, :2, :].sum(axis=2)  # (1,N,T)
        # sample.append(target)

        time_sample = np.expand_dims(np.array([idx]), axis=0)  # (1,1)
        sample.append(time_sample)
        
        all_samples.append(
            sample)  # sampe：[(week_sample),(day_sample),(hour_sample),target,time_sample] = [(1,N,F,Tw),(1,N,F,Td),(1,N,F,Th),(1,N,2,Tpre),(1,1)]
        

    split_line1 = int(len(all_samples) * 0.96)
    split_line2 = int(len(all_samples) * 0.98)

    training_set = [np.concatenate(i, axis=0)
                    for i in zip(*all_samples[:split_line1])]  # [(B,N,F,Tw),(B,N,F,Td),(B,N,F,Th),(B,N,2,Tpre),(B,1)]
    validation_set = [np.concatenate(i, axis=0)
                      for i in zip(*all_samples[split_line1: split_line2])]
    testing_set = [np.concatenate(i, axis=0)
                   for i in zip(*all_samples[split_line2:])]
    print(training_set[0].shape)
    # train_x = np.concatenate(training_set[:-2], axis=-1)  # (B,N,F,T')
    # val_x = np.concatenate(validation_set[:-2], axis=-1)
    # test_x = np.concatenate(testing_set[:-2], axis=-1)
    train_x = training_set[:-2]
    val_x = validation_set[:-2]
    test_x = testing_set[:-2]

    # train_target = training_set[-2]  # (B,N,T)
    # val_target = validation_set[-2]
    # test_target = testing_set[-2]

    train_timestamp = training_set[-1]  # (B,1)
    val_timestamp = validation_set[-1]
    test_timestamp = testing_set[-1]

    (stats, train_x_norm, val_x_norm, test_x_norm) = normalization(train_x, val_x, test_x)

    all_data = {
        'train': {
            'x': train_x_norm,
            # 'target': train_target,
            'timestamp': train_timestamp,
        },
        'val': {
            'x': val_x_norm,
            # 'target': val_target,
            'timestamp': val_timestamp,
        },
        'test': {
            'x': test_x_norm,
            # 'target': test_target,
            'timestamp': test_timestamp,
        },
        'stats': {
            '_mean': stats['_mean'],
            '_std': stats['_std'],
        }
    }
    print('train x:', all_data['train']['x'].shape)
    # print('train target:', all_data['train']['target'].shape)
    print('train timestamp:', all_data['train']['timestamp'].shape)
    print()
    print('val x:', all_data['val']['x'].shape)
    # print('val target:', all_data['val']['target'].shape)
    print('val timestamp:', all_data['val']['timestamp'].shape)
    print()
    print('test x:', all_data['test']['x'].shape)
    # print('test target:', all_data['test']['target'].shape)
    print('test timestamp:', all_data['test']['timestamp'].shape)
    print()
    print('train data _mean :', stats['_mean'].shape, stats['_mean'])
    print('train data _std :', stats['_std'].shape, stats['_std'])
        
    if save:
        filename = save_dir_path + "/metro_covid_data" + '_r' + str(num_of_hours) + '_d' + str(num_of_days) + '_w' + str(num_of_weeks) + '_astcgn'
        # filename = os.path.join(dirpath, file + '_r' + str(num_of_hours) + '_d' + str(num_of_days) + '_w' + str(num_of_weeks)) + '_astcgn'
        np.savez_compressed(filename,
                            train_x=all_data['train']['x'], # train_target=all_data['train']['target'],
                            train_timestamp=all_data['train']['timestamp'],
                            val_x=all_data['val']['x'], # val_target=all_data['val']['target'],
                            val_timestamp=all_data['val']['timestamp'],
                            test_x=all_data['test']['x'], # test_target=all_data['test']['target'],
                            test_timestamp=all_data['test']['timestamp'],
                            mean=all_data['stats']['_mean'], std=all_data['stats']['_std']
                           )
#     if save:
#         file = os.path.basename(graph_signal_matrix_filename).split('.')[0]
#         dirpath = os.path.dirname(graph_signal_matrix_filename)
#         filename = os.path.join(dirpath, file + '_r' + str(num_of_hours) + '_d' + str(num_of_days) + '_w' + str(num_of_weeks)) + '_astcgn'
#         print('save file:', filename)
#         np.savez_compressed(filename,
#                             train_x=all_data['train']['x'], train_target=all_data['train']['target'],
#                             train_timestamp=all_data['train']['timestamp'],
#                             val_x=all_data['val']['x'], val_target=all_data['val']['target'],
#                             val_timestamp=all_data['val']['timestamp'],
#                             test_x=all_data['test']['x'], test_target=all_data['test']['target'],
#                             test_timestamp=all_data['test']['timestamp'],
#                             mean=all_data['stats']['_mean'], std=all_data['stats']['_std']
#                             )
    return all_data