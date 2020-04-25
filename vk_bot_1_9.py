import vk_api

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/vk_stat/<int:group_id>')
def vk_stat(group_id):
    login, password = LOGIN, PASSWORD
    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()
    activities = {'likes': 0, 'comments': 0, 'subscribed': 0}
    ages = {'12-18': 0, '18-21': 0, '21-24': 0,
            '24-27': 0, '27-30': 0, '30-35': 0,
            '35-45': 0, '45-100': 0}
    cities = set()
    response = vk.stats.get(group_id=group_id, fields="reach")
    if response:
        for item in response[:10]:
            print(item)
            if 'activity' in item:
                for act in item['activity']:
                    activities[act] += item['activity'][act]
                if 'age' in item['reach']:
                    for age in item['reach']['age']:
                        ages[age['value']] += age['count']
                for place in item['reach']['cities']:
                    cities.add(place['name'])
    print(activities, ages, *cities)
    return render_template('stats.html', activities=activities,
                           ages=ages, cities=cities, title='Vk Statistics')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
