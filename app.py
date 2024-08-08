from flask import Flask, g, request, jsonify
from database import get_db
from functools import wraps

app = Flask(__name__)

api_username = 'Hussnain'
api_password = 'testpass'


def authorization_func(f):
    """
    The `authorization_func` decorator function checks if the request has valid authorization
    credentials before allowing access to the decorated function.
    
    :param f: The parameter `f` in the `authorization_func` function is a function that will be
    decorated with the authorization functionality
    :return: The `authorization_func` function is returning a decorated function that checks if the
    request has valid authorization credentials (username and password matching `api_username` and
    `api_password`). If the credentials are valid, it calls the original function `f` with the provided
    arguments and keyword arguments. If the credentials are not valid, it returns a JSON response with a
    message indicating that the authorization failed and a status code
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == api_username and auth.password == api_password:
            return f(*args,**kwargs)
        return jsonify({'message': 'Authorization Failed!'}), 403
    return decorated
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/member', methods=['GET'])
@authorization_func
def get_members():
    db = get_db()
    cur = db.execute('select * from members')
    results = cur.fetchall()
    members_list = []
    for mem in results:
        member_dict = {}
        member_dict['id'] = mem['id']
        member_dict['name'] = mem['name']
        member_dict['email'] = mem['email']
        member_dict['level'] = mem['level']
        members_list.append(member_dict)
    # username = request.authorization.username
    # password = request.authorization.password
    # if username == api_username and password == api_password:
    return jsonify({'members': members_list})
    # return jsonify({'message': 'Authorization Failed!'}), 403

    # return 'This returns all the members.'


@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    db = get_db()
    cur = db.execute('select * from members where id = ?', [member_id])
    member_data = cur.fetchone()

    return jsonify({'member': dict(member_data)})


@app.route('/member', methods=['POST'])
def add_member():
    json_data = request.get_json()
    name = json_data['name']
    email = json_data['email']
    level = json_data['level']
    db = get_db()
    db.execute('insert into members (name,email,level) values (?,?,?)', [
               name, email, level])
    db.commit()
    fetch_member = db.execute('select * from members where name = ?', [name])
    new_member = fetch_member.fetchone()
    member_dict = dict(new_member)
    return jsonify({'member': member_dict})


@app.route('/member/<int:member_id>', methods=['PUT', 'PATCH'])
def edit_member(member_id):
    json_data = request.get_json()
    name = json_data['name']
    email = json_data['email']
    level = json_data['level']
    db = get_db()
    db.execute('update members set name = ? , email = ?, level = ? where id = ?', [
               name, email, level, member_id])
    db.commit()
    fetch_member = db.execute(
        'select * from members where id = ?', [member_id])
    new_member = fetch_member.fetchone()
    member_dict = dict(new_member)
    return jsonify({'member': member_dict})


@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    db = get_db()
    row = db.execute('SELECT * FROM members WHERE id = ?',
                     [member_id]).fetchone()

    db.execute('DELETE FROM members WHERE id = ?', [member_id])
    db.commit()
    return jsonify(dict(row))


if __name__ == '__main__':
    app.run(debug=True)
