def get_dict_result(**kwargs):
    try:
        data = kwargs['data']
        model_name = kwargs.get('model', None)
        count = kwargs.get('count', None)

        result = {'code': 0, 'data': []}

        if count is not None:
            result_temp = count.fetchall()[0]
            temp = dict(result_temp)
            result['total_count'] = temp.get('count_1', None) or temp.get('count', None)

        result_temp = data.fetchall()
        for i in result_temp:
            temp = dict(i)
            # temp.pop('_sa_instance_state')
            if model_name is None:
                result['data'].append(temp)
            else:
                result['data'].append(temp[model_name])
        return result
    except Exception:
        return {'code': 1}
