def get_dict_result(fetch_res):
    try:
        result_temp = fetch_res.fetchall()
        result = {'code': 0, 'data': []}
        for i in result_temp:
            temp = dict(i)
            # temp.pop('_sa_instance_state')
            result['data'].append(temp)
        return result
    except Exception:
        return {'code': 1}
