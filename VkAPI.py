import requests
from datetime import datetime
import plotly
import plotly.plotly as py
import plotly.graph_objs as go


plotly.tools.set_credentials_file(username='Artyom', api_key='')


domain = "https://api.vk.com/method"
access_token = ''
user_id = 


def get_friends(user_id, fields):
    """ Returns a list of user IDs or detailed information about a user's friends """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"

    query_params = {
        'domain': domain,
        'access_token': access_token,
        'user_id': user_id,
        'fields': fields
    }

    query = "{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v=5.53".format(
        **query_params)
    response = requests.get(query)

    fr_list = []
    count_fr = response.json()['response']['count']
    for i in range(count_fr):
        fr_list.append(response.json()['response']['items'][i])

    return fr_list


print(get_friends(user_id, 'bdate'))


def age_predict(user_id):
    """
    >>> age_predict(???)
    ???
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"

    bd_list = []
    for dict in get_friends(user_id, 'bdate'):
        try:
            bd_list.append(dict['bdate'])
        except:
            pass #or 'continue'

    sum_year = 0
    pattern = '.'
    pos = 0
    count = 0
    count_year = 0
    for bd in bd_list:
        while pos != -1:
            pos = bd.find(pattern, pos)
            if pos != -1:
                count += 1
                pos += 1
                pos1 = pos
        if count == 2:
            sum_year += (int(bd[pos1:]))
            count_year += 1
        pos = 0
        count = 0
    return 2016 - round(sum_year / count_year)


print(age_predict(user_id))


def messages_get_history(user_id, offset=0, count=200):
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    assert isinstance(offset, int), "offset must be positive integer"
    assert offset >= 0, "user_id must be positive integer"
    assert count >= 0, "user_id must be positive integer"

    query2_params = {
        'domain': domain,
        'access_token': access_token,
        'user_id': user_id,
        'offset': offset,
        'count': count
    }

    query2 = "{domain}/messages.getHistory?access_token={access_token}&user_id={user_id}&offset={offset}&count={count}" \
             "&v=5.53".format(**query2_params)
    response2 = requests.get(query2)
    return response2.json()['response']['items']


messages = messages_get_history(user_id)
print(messages)


def count_dates_from_messages(messages):
    date_list = []
    c_date_list = [] #count_date
    count = 0
    for message in messages:
        date = datetime.fromtimestamp(message['date']).strftime("%Y-%m-%d")
        if date not in date_list:
            date_list.append(date)
            c_date_list.append(1)
            count += 1
        else:
            for i in range(count):
                if date_list[i] == date:
                    c_date_list[i] += 1
    return (date_list, c_date_list)


a = count_dates_from_messages(messages)
print(a)
print(a[0], a[1])

data = [go.Scatter(x=a[0],y=a[1])]
py.plot(data)
